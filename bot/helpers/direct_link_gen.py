from cloudscraper import create_scraper
from re import search, findall
from json import loads
import os
import uuid
from requests import post
from bs4 import BeautifulSoup
from uuid import uuid4
from urllib.parse import parse_qs, urlparse

async def direct_link(url):
    if 'facebook' in url:
        return await _fb(url)
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
    print(url)

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
