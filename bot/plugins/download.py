import os
import re
import json
import lk21
import requests
import wget
import urllib.parse
from urllib.parse import urlparse
from lk21.extractors.bypasser import Bypass
from bs4 import BeautifulSoup
from base64 import standard_b64encode
from time import sleep
from pyrogram import Client, filters
from bot.helpers.sql_helper import gDriveDB, idsDB
from bot.helpers.utils import CustomFilters, humanbytes
from bot.helpers.downloader import download_file, utube_dl, download_fb
from bot.helpers.gdrive_utils import GoogleDrive 
from bot import DOWNLOAD_DIRECTORY, LOGGER, bot
from bot.config import Messages, BotCommands
from pyrogram.errors import FloodWait, RPCError
from cloudscraper import create_scraper
from http.cookiejar import MozillaCookieJar

@bot.on_message(filters.private & filters.incoming & filters.text & (filters.command(BotCommands.Download) | filters.regex('^(ht|f)tp*')) & CustomFilters.auth_users)
async def _download(client, message):
    user_id = message.from_user.id
    if not message.media:
        sent_message = await message.reply_text('🕵️**Checking link...**')
        if message.command:
            url = message.command[1]
        else:
            url = message.text
        if 'drive.google.com' in url:
            return await _gd(client, message, user_id, sent_message, url)
        elif 'facebook' in url:
            return await _fb(client, message, user_id, sent_message, url)
        elif 'solidfiles' in url:
            return await _solidfiles(client, message, user_id, sent_message, url)
        elif 'anonfiles' in url:
            return await _anonfiles(client, message, user_id, sent_message, url)
        elif 'mediafire.com' in url:
            return await _mediafire(client, message, user_id, sent_message, url)
        elif 'workers.dev' in url:
            return await _indexlink(client, message, user_id, sent_message, url)
        elif 'zippyshare.com' in url:
            return await _zippyshare(client, message, user_id, sent_message, url)
        elif 'pornhub.com' in url:
            return await _pornhub(client, message, user_id, sent_message, url)
        elif 'youtu' in url:
            return await _youtu(client, message, user_id, sent_message, url)
        elif any(x in url for x in ['terabox', 'nephobox', '4funbox', 'mirrobox', 'momerybox', 'teraboxapp']):
            return await tera_box(client, message, user_id, sent_message, url)
        elif '1drv.ms' in url:
            return await one_drive(client, message, user_id, sent_message, url)
        else:
            await sent_message.edit('Link Not supported')

@bot.on_message(filters.private & filters.incoming & (filters.document | filters.audio | filters.video | filters.photo) & CustomFilters.auth_users)
async def _telegram_file(client, message):
  user_id = message.from_user.id
  sent_message = await message.reply_text('🕵️**Checking File...**')
  if message.document:
    file = message.document
  elif message.video:
    file = message.video
  elif message.audio:
    file = message.audio
  elif message.photo:
  	file = message.photo
  	file.mime_type = "images/png"
  	file.file_name = f"IMG-{user_id}-{message.id}.png"
  await sent_message.edit(Messages.DOWNLOAD_TG_FILE.format(file.file_name, humanbytes(file.file_size), file.mime_type))
  LOGGER.info(f'Download:{user_id}: {file.file_id}')
  try:
    file_path = await message.download(file_name=DOWNLOAD_DIRECTORY)
    file_name = os.path.basename(file_path)
    file_size = humanbytes(os.path.getsize(file_path))
    await sent_message.edit(Messages.DOWNLOADED_SUCCESSFULLY.format(file_name, file_size))
    msg = GoogleDrive(user_id).upload_file(file_path, file.mime_type)
    await sent_message.edit(msg)
  except RPCError:
    await sent_message.edit(Messages.WENT_WRONG)
  LOGGER.info(f'Deleteing: {file_path}')
  os.remove(file_path)

@bot.on_message(filters.incoming & filters.private & filters.command(BotCommands.YtDl) & CustomFilters.auth_users)
async def _ytdl(client, message):
  user_id = message.from_user.id
  if len(message.command) > 1:
    sent_message = await message.reply_text('🕵️**Checking Link...**')
    link = message.command[1]
    LOGGER.info(f'YTDL:{user_id}: {link}')
    await sent_message.edit(Messages.DOWNLOADING.format(link))
    result, file_path = utube_dl(link)
    if result:
      await sent_message.edit(Messages.DOWNLOADED_SUCCESSFULLY.format(os.path.basename(file_path), humanbytes(os.path.getsize(file_path))))
      msg = GoogleDrive(user_id).upload_file(file_path)
      await sent_message.edit(msg)
      LOGGER.info(f'Deleteing: {file_path}')
      os.remove(file_path)
    else:
      await sent_message.edit(Messages.DOWNLOAD_ERROR.format(file_path, link))
  else:
    await sent_message.edit(Messages.PROVIDE_YTDL_LINK)

#downloader

async def _gd(client, message, user_id, sent_message, url):
      await sent_message.edit(Messages.CLONING.format(url))
      LOGGER.info(f'Copy:{user_id}: {url}')
      msg = GoogleDrive(user_id).clone(url)
      await sent_message.edit(msg)

async def _fb(client, message, user_id, sent_message, url):
      try:
        r  = requests.post("https://yt1s.io/api/ajaxSearch/facebook", data={"q": url, "vt": "facebook"}).text
        bs = BeautifulSoup(r, "html5lib")

        js = str(bs).replace('<html><head></head><body>{"status":"ok","p":"facebook","links":', '').replace('</body></html>', '').replace('},', ',')
        text_file = open(str(user_id) + "fb.txt", "w")
        n = text_file.write(js)
        text_file.close()
        with open(str(user_id) + "fb.txt") as f:
            contents = json.load(f)
            try:
              durl = str(contents['hd']).replace('&amp;', '&')
              link = durl.strip()
              filename = os.path.basename(link)
              dl_path = DOWNLOAD_DIRECTORY
              LOGGER.info(f'Download:{user_id}: {link}')
              await sent_message.edit(Messages.DOWNLOADING.format(link))
              result, file_path = download_file(link, dl_path)

              if os.path.exists(file_path):
                await sent_message.edit(Messages.DOWNLOADED_SUCCESSFULLY.format(os.path.basename(file_path), humanbytes(os.path.getsize(file_path))))
                msg = GoogleDrive(user_id).upload_file(file_path)
                await sent_message.edit(msg)
                LOGGER.info(f'Deleteing: {file_path}')
                os.remove(file_path)  
            except:
              durl = str(contents['sd']).replace('&amp;', '&')
              link = durl.strip()
              filename = os.path.basename(link)
              dl_path = DOWNLOAD_DIRECTORY
              LOGGER.info(f'Download:{user_id}: {link}')
              await sent_message.edit(Messages.DOWNLOADING.format(link))
              result, file_path = download_file(link, dl_path)

              if os.path.exists(file_path):
                await sent_message.edit(Messages.DOWNLOADED_SUCCESSFULLY.format(os.path.basename(file_path), humanbytes(os.path.getsize(file_path))))
                msg = GoogleDrive(user_id).upload_file(file_path)
                await sent_message.edit(msg)
                LOGGER.info(f'Deleteing: {file_path}')
                os.remove(file_path)  
        
        
      except:
        await sent_message.edit('🕵️**Your Facebook Link is Private & SO i cAnNot Download**')

async def _solidfiles(client, message, user_id, sent_message, url):
      headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36'
        }
      try:
        pageSource = requests.get(url, headers = headers).text
        mainOptions = str(re.search(r'viewerOptions\'\,\ (.*?)\)\;', pageSource).group(1))
        dl_url = json.loads(mainOptions)["downloadUrl"]
        link = dl_url.strip()
        filename = os.path.basename(link)
        dl_path = DOWNLOAD_DIRECTORY
        LOGGER.info(f'Download:{user_id}: {link}')
        await sent_message.edit(Messages.DOWNLOADING.format(link))
        result, file_path = download_file(link, dl_path)
        if os.path.exists(file_path):
          await sent_message.edit(Messages.DOWNLOADED_SUCCESSFULLY.format(os.path.basename(file_path), humanbytes(os.path.getsize(file_path))))
          msg = GoogleDrive(user_id).upload_file(file_path)
          await sent_message.edit(msg)
          LOGGER.info(f'Deleteing: {file_path}')
          os.remove(file_path)
      except:
        await sent_message.edit('🕵️**Solidfiles link error...**')

async def _anonfiles(client, message, user_id, sent_message, url):
      try:
        bypasser = lk21.Bypass()
        dl_url=bypasser.bypass_anonfiles(url)
        link = dl_url.strip()
        filename = os.path.basename(link)
        dl_path = DOWNLOAD_DIRECTORY
        LOGGER.info(f'Download:{user_id}: {link}')
        await sent_message.edit(Messages.DOWNLOADING.format(link))
        result, file_path = download_file(link, dl_path)
        if os.path.exists(file_path):
          await sent_message.edit(Messages.DOWNLOADED_SUCCESSFULLY.format(os.path.basename(file_path), humanbytes(os.path.getsize(file_path))))
          msg = GoogleDrive(user_id).upload_file(file_path)
          await sent_message.edit(msg)
          LOGGER.info(f'Deleteing: {file_path}')
          os.remove(file_path)
      except:
        await sent_message.edit('🕵️**Anonfiles link error...**')

async def _mediafire(client, message, user_id, sent_message, url):
      try:
        link = re.findall(r'\bhttps?://.*mediafire\.com\S+', url)[0]
      except IndexError:
        sent_message = message.reply_text('🕵️**mediafire link error...**')
      page = BeautifulSoup(requests.get(link).content, 'lxml')
      info = page.find('a', {'aria-label': 'Download file'})
      dl_url = info.get('href')
      link = dl_url.strip()
      filename = os.path.basename(link)
      dl_path = DOWNLOAD_DIRECTORY
      LOGGER.info(f'Download:{user_id}: {link}')
      await sent_message.edit(Messages.DOWNLOADING.format(link))
      result, file_path = download_file(link, dl_path)
      if os.path.exists(file_path):
        await sent_message.edit(Messages.DOWNLOADED_SUCCESSFULLY.format(os.path.basename(file_path), humanbytes(os.path.getsize(file_path))))
        msg = GoogleDrive(user_id).upload_file(file_path)
        await sent_message.edit(msg)
        LOGGER.info(f'Deleteing: {file_path}')
        os.remove(file_path)
      else:
        await sent_message.edit('🕵️**mediafire link error...**')

async def _indexlink(client, message, user_id, sent_message, url):
    try:
      dl_url = url
      link = dl_url.strip()
      filename = os.path.basename(link)
      dl_path = DOWNLOAD_DIRECTORY
      LOGGER.info(f'Download:{user_id}: {link}')
      await sent_message.edit(Messages.DOWNLOADING.format(link))
      result, file_path = download_file(link, dl_path)
      if result == True and os.path.exists(file_path):
          await sent_message.edit(Messages.DOWNLOADED_SUCCESSFULLY.format(os.path.basename(file_path), humanbytes(os.path.getsize(file_path))))
          msg = GoogleDrive(user_id).upload_file(file_path)
          await sent_message.edit(msg)
          LOGGER.info(f'Deleteing: {file_path}')
          os.remove(file_path)
    except Exception as e:
        await sent_message.edit(f'🕵️**Index link error...\n{e}**')
        LOGGER.error(f'Error {e}')

async def _zippyshare(client, message, user_id, sent_message, url):
      dl_url = ''
      try:
        link = re.findall(r'\bhttps?://.*zippyshare\.com\S+', url)[0]
      except IndexError:
        sent_message = message.reply_text('🕵️**zippy link error...**')
      session = requests.Session()
      base_url = re.search('http.+.com', link).group()
      response = session.get(link)
      page_soup = BeautifulSoup(response.content, "lxml")
      scripts = page_soup.find_all("script", {"type": "text/javascript"})
      for script in scripts:
        if "getElementById('dlbutton')" in script.text:
          url_raw = re.search(r'= (?P<url>\".+\" \+ (?P<math>\(.+\)) .+);',
                              script.text).group('url')
          math = re.search(r'= (?P<url>\".+\" \+ (?P<math>\(.+\)) .+);',
                           script.text).group('math')
          dl_url = url_raw.replace(math, '"' + str(eval(math)) + '"')
          break
      dl_url = base_url + eval(dl_url)
      link = dl_url.strip()
      filename = urllib.parse.unquote(dl_url.split('/')[-1])
      dl_path = DOWNLOAD_DIRECTORY
      LOGGER.info(f'Download:{user_id}: {link}')
      await sent_message.edit(Messages.DOWNLOADING.format(link))
      result, file_path = download_file(link, dl_path)
      if os.path.exists(file_path):
        await sent_message.edit(Messages.DOWNLOADED_SUCCESSFULLY.format(os.path.basename(file_path),
                                                                  humanbytes(os.path.getsize(file_path))))
        msg = GoogleDrive(user_id).upload_file(file_path)
        await sent_message.edit(msg)
        LOGGER.info(f'Deleteing: {file_path}')
        os.remove(file_path)
      else:
        await sent_message.edit('🕵️** zippy link error...**')

async def _pornhub(client, message, user_id, sent_message, url):
      LOGGER.info(f'YTDL:{user_id}: {url}')
      await sent_message.edit(Messages.DOWNLOADING.format(url))
      result, file_path = utube_dl(url)
      if result:
        await sent_message.edit(Messages.DOWNLOADED_SUCCESSFULLY.format(os.path.basename(file_path), humanbytes(os.path.getsize(file_path))))
        msg = GoogleDrive(user_id).upload_file(file_path)
        await sent_message.edit(msg)
        LOGGER.info(f'Deleteing: {file_path}')
        os.remove(file_path)
      else:
        await sent_message.edit('🕵️**PORNHUB ERROR**')

async def _youtu(client, message, user_id, sent_message, url):
      link = url
      LOGGER.info(f'YTDL:{user_id}: {link}')
      await sent_message.edit(Messages.DOWNLOADING.format(link))
      result, file_path = utube_dl(link)
      if result:
        await sent_message.edit(Messages.DOWNLOADED_SUCCESSFULLY.format(os.path.basename(file_path), humanbytes(os.path.getsize(file_path))))
        msg = GoogleDrive(user_id).upload_file(file_path)
        await sent_message.edit(msg)
        LOGGER.info(f'Deleteing: {file_path}')
        os.remove(file_path)
      else:
        await sent_message.edit('🕵️**YOUTUBE ERROR**')

async def tera_box(client, message, user_id, sent_message, url):
    try:
      session = create_scraper()
      res = session.request('GET', url)
      key = res.url.split('?surl=')[-1]
      jar = MozillaCookieJar('terabox.txt')
      jar.load()
      session.cookies.update(jar)
      res = session.request('GET', f'https://www.terabox.com/share/list?app_id=250528&shorturl={key}&root=1')
      result = res.json()['list']
      if len(result) == 1:
          result = result[0]
          if result['isdir'] == '0':
              link = result['dlink']
              filename= result['server_filename']
              dl_path = os.path.join(f'{DOWNLOAD_DIRECTORY}/{filename}')
              LOGGER.info(f'Download:{user_id}: {link}')
              await sent_message.edit(Messages.DOWNLOADING.format(link))
              result, file_path = download_file(link, dl_path)
              if os.path.exists(file_path):
                  await sent_message.edit(Messages.DOWNLOADED_SUCCESSFULLY.format(os.path.basename(file_path), humanbytes(os.path.getsize(file_path))))
                  msg = GoogleDrive(user_id).upload_file(file_path)
                  await sent_message.edit(msg)
                  LOGGER.info(f'Deleteing: {file_path}')
                  os.remove(file_path)
          else:
              await sent_message.edit("Can't download folder")
      else:
          await sent_message.edit("Can't download mutiple files")
    except:
        await sent_message.edit('🕵️**Terabox link error...**')

async def one_drive(client, message, user_id, sent_message, url):
    try:
      link_without_query = urlparse(url)._replace(query=None).geturl()
      direct_link_encoded = str(standard_b64encode(bytes(link_without_query, "utf-8")), "utf-8")
      direct_link1 = f"https://api.onedrive.com/v1.0/shares/u!{direct_link_encoded}/root/content"
      resp = requests.head(direct_link1)
      if resp.status_code == 302:
          link = resp.next.url
          dl_path = DOWNLOAD_DIRECTORY
          LOGGER.info(f'Download:{user_id}: {link}')
          await sent_message.edit(Messages.DOWNLOADING.format(link))
          result, file_path = download_file(link, dl_path)
          if os.path.exists(file_path):
              await sent_message.edit(Messages.DOWNLOADED_SUCCESSFULLY.format(os.path.basename(file_path), humanbytes(os.path.getsize(file_path))))
              msg = GoogleDrive(user_id).upload_file(file_path)
              await sent_message.edit(msg)
              LOGGER.info(f'Deleteing: {file_path}')
              os.remove(file_path)
      else:
          await sent_message.edit('🕵️**Your Onedrive Link is Private & SO i cAnNot Download**')
    except:
        await sent_message.edit('🕵️**Onedrive link error...**')
