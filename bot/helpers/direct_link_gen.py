from cloudscraper import create_scraper
from re import search

async def direct_link(url):
    if 'facebook' in url:
        await _fb(url)
    elif 'solidfiles' in url:
        await _solidfiles(url)
    elif 'mediafire.com' in url:
        await _mediafire(url)
    elif 'workers.dev' in url:
        await _indexlink(url)
    elif any(x in url for x in ['terabox', 'nephobox', '4funbox', 'mirrobox', 'momerybox', 'teraboxapp']):
        await tera_box(url)
    elif '1drv.ms' in url:
        await one_drive(url)

async def _fb(url):
    print(url)

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
    print(url)

async def _indexlink(url):
    print(url)

async def tera_box(url):
    print(url)

async def one_drive(url):
    print(url)
