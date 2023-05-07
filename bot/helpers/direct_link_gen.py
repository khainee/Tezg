from cloudscraper import create_scraper
from http.cookiejar import MozillaCookieJar
from os import path
from re import search, findall
from json import loads
from requests import post
from bs4 import BeautifulSoup
from uuid import uuid4
from urllib.parse import parse_qs, urlparse
from lxml import etree
from bot.helpers.utils import is_share_link
from bot import LOGGER


async def direct_link(url):
    if 'facebook' in url:
        return await _fb(url)
    elif 'drive.google.com' in url:
        return True, url
    elif 'solidfiles' in url:
        return await _solidfiles(url)
    elif 'mediafire.com' in url:
        return await _mediafire(url)
    elif 'workers.dev' in url:
        return await _indexlink(url)
    elif any(x in url for x in ['terabox', 'nephobox', '4funbox', 'mirrobox', 'momerybox', 'teraboxapp']):
        return await tera_box(url)
    elif '1drv.ms' in url:
        return await one_drive(url)
    elif is_share_link(url):
        if 'gdtot' in url:
            return await gdtot(url)
        elif 'filepress' in url:
            return await filepress(url)
        else:
            return await sharer_scraper(url)
    else:
        return False, 'No Downloader for the link'

async def _fb(url):
    try:
        r = post("https://yt1s.io/api/ajaxSearch/facebook", data={"q": url, "vt": "facebook"}).text
        bs = BeautifulSoup(r, "html5lib")
        js = str(bs).replace('<html><head></head><body>{"status":"ok","p":"facebook","links":', '').replace('</body></html>', '').replace('},', ',')
        contents = loads(js)
        if 'hd' in contents:
            durl = str(contents['hd']).replace('&amp;', '&')
        else:
            durl = str(contents['sd']).replace('&amp;', '&')
        return True, durl
    except Exception as e:
        print(f"Error: {e}")
        return False, e

async def _solidfiles(url):
    cget = create_scraper().request
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36'
        }
        pageSource = cget('get', url, headers=headers).text
        mainOptions = str(
            search(r'viewerOptions\'\,\ (.*?)\)\;', pageSource).group(1))
        return True, loads(mainOptions)["downloadUrl"]
    except Exception as e:
        return False, e

async def _mediafire(url):
    cget = create_scraper().request
    try:
        url = cget('get', url).url
        page = cget('get', url).text
    except Exception as e:
        return False, e
    if not (final_link := findall(r"\'(https?:\/\/download\d+\.mediafire\.com\/\S+\/\S+\/\S+)\'", page)):
        return False, "ERROR: No links found in this page"
    return True, final_link[0]

async def _indexlink(url):
    return True, url

async def tera_box(url):
    if not path.isfile('terabox.txt'):
        return False, "ERROR: terabox.txt not found"
    session = create_scraper()
    try:
        res = session.request('GET', url)
        key = res.url.split('?surl=')[-1]
        jar = MozillaCookieJar('terabox.txt')
        jar.load()
        session.cookies.update(jar)
        res = session.request(
            'GET', f'https://www.terabox.com/share/list?app_id=250528&shorturl={key}&root=1')
        result = res.json()['list']
    except Exception as e:
        return False, e
    if len(result) > 1:
        return False, "ERROR: Can't download mutiple files"
    result = result[0]
    if result['isdir'] != '0':
        return False, "ERROR: Can't download folder"
    return True, result['dlink']

async def one_drive(link):
    cget = create_scraper().request
    try:
        link = cget('get', link).url
        parsed_link = urlparse(link)
        link_data = parse_qs(parsed_link.query)
    except Exception as e:
        return False, e
    if not link_data:
        return False, "ERROR: Unable to find link_data"
    folder_id = link_data.get('resid')
    if not folder_id:
        return False, 'ERROR: folder id not found'
    folder_id = folder_id[0]
    authkey = link_data.get('authkey')
    if not authkey:
        return False, 'ERROR: authkey not found'
    authkey = authkey[0]
    boundary = uuid4()
    headers = {'content-type': f'multipart/form-data;boundary={boundary}'}
    data = f'--{boundary}\r\nContent-Disposition: form-data;name=data\r\nPrefer: Migration=EnableRedirect;FailOnMigratedFiles\r\nX-HTTP-Method-Override: GET\r\nContent-Type: application/json\r\n\r\n--{boundary}--'
    try:
        resp = cget(
            'get', f'https://api.onedrive.com/v1.0/drives/{folder_id.split("!", 1)[0]}/items/{folder_id}?$select=id,@content.downloadUrl&ump=1&authKey={authkey}', headers=headers, data=data).json()
    except Exception as e:
        return False, e
    if "@content.downloadUrl" not in resp:
        return False, 'ERROR: Direct link not found'
    return True, resp['@content.downloadUrl']

async def gdtot(url):
    cget = create_scraper().request
    try:
        res = cget('GET', f'https://gdbot.xyz/file/{url.split("/")[-1]}')
    except Exception as e:
        return False, e
    token_url = etree.HTML(res.content).xpath(
        "//a[contains(@class,'inline-flex items-center justify-center')]/@href")
    if not token_url:
        try:
            url = cget('GET', url).url
            p_url = urlparse(url)
            res = cget(
                "GET", f"{p_url.scheme}://{p_url.hostname}/ddl/{url.split('/')[-1]}")
        except Exception as e:
            return False, e
        if (drive_link := findall(r"myDl\('(.*?)'\)", res.text)) and "drive.google.com" in drive_link[0]:
            return drive_link[0]
        else:
            return False, 'ERROR: Drive Link not found, Try in your broswer'
    token_url = token_url[0]
    try:
        token_page = cget('GET', token_url)
    except Exception as e:
        return False, e
    path = findall('\("(.*?)"\)', token_page.text)
    if not path:
        return False, 'ERROR: Cannot bypass this'
    path = path[0]
    raw = urlparse(token_url)
    final_url = f'{raw.scheme}://{raw.hostname}{path}'
    return await sharer_scraper(final_url)

async def sharer_scraper(url):
    cget = create_scraper().request
    try:
        url = cget('GET', url).url
        raw = urlparse(url)
        header = {
            "useragent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/7.0.548.0 Safari/534.10"}
        res = cget('GET', url, headers=header)
    except Exception as e:
        return False, e 
    key = findall('"key",\s+"(.*?)"', res.text)
    if not key:
        return False, "ERROR: Key not found!"
    key = key[0]
    if not etree.HTML(res.content).xpath("//button[@id='drc']"):
        return False, "ERROR: This link don't have direct download button"
    boundary = uuid4()
    headers = {
        'Content-Type': f'multipart/form-data; boundary=----WebKitFormBoundary{boundary}',
        'x-token': raw.hostname,
        'useragent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/7.0.548.0 Safari/534.10'
    }

    data = f'------WebKitFormBoundary{boundary}\r\nContent-Disposition: form-data; name="action"\r\n\r\ndirect\r\n' \
        f'------WebKitFormBoundary{boundary}\r\nContent-Disposition: form-data; name="key"\r\n\r\n{key}\r\n' \
        f'------WebKitFormBoundary{boundary}\r\nContent-Disposition: form-data; name="action_token"\r\n\r\n\r\n' \
        f'------WebKitFormBoundary{boundary}--\r\n'
    try:
        res = cget("POST", url, cookies=res.cookies,
                   headers=headers, data=data).json()
    except Exception as e:
        return False, e
    if "url" not in res:
        return False, 'ERROR: Drive Link not found, Try in your broswer'
    if "drive.google.com" in res["url"]:
        return True, res["url"]
    try:
        res = cget('GET', res["url"])
    except Exception as e:
        return False, e
    if (drive_link := etree.HTML(res.content).xpath("//a[contains(@class,'btn')]/@href")) and "drive.google.com" in drive_link[0]:
        return True, drive_link[0]
    else:
        return False, 'ERROR: Drive Link not found, Try in your broswer'

async def filepress(url):
    cget = create_scraper().request
    try:
        url = cget('GET', url).url
        raw = urlparse(url)
        json_data = {
            'id': raw.path.split('/')[-1],
            'method': 'publicDownlaod',
        }
        api = f'{raw.scheme}://{raw.hostname}/api/file/downlaod/'
        res = cget('POST', api, headers={
                   'Referer': f'{raw.scheme}://{raw.hostname}'}, json=json_data).json()
    except Exception as e:
        return False, e 
    if 'data' not in res:
        return False, f'ERROR: {res["statusText"]}'
    return True, f'https://drive.google.com/uc?id={res["data"]}&export=download'
