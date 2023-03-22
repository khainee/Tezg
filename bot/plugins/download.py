import os
import re
import json
import lk21
import requests
import wget
import urllib.parse
from lk21.extractors.bypasser import Bypass
from bs4 import BeautifulSoup
from time import sleep
from pyrogram import Client, filters
from bot.helpers.sql_helper import gDriveDB, idsDB
from bot.helpers.utils import CustomFilters, humanbytes
from bot.helpers.downloader import download_file, utube_dl, download_fb
from bot.helpers.gdrive_utils import GoogleDrive 
from bot import DOWNLOAD_DIRECTORY, LOGGER
from bot.config import Messages, BotCommands
from pyrogram.errors import FloodWait, RPCError

@Client.on_message(filters.private & filters.incoming & filters.text & (filters.command(BotCommands.Download) | filters.regex('^(ht|f)tp*')) & CustomFilters.auth_users)
def _download(client, message):
    user_id = message.from_user.id
    if not message.media:
        sent_message = message.reply_text('🕵️**Checking link...**', quote=True)
        if message.command:
            link = message.command[1]
        else:
            link = message.text
        if 'drive.google.com' in link:
            return _gd(client, message, user_id, sent_message, link)
        elif 'facebook' in link:
            return _fb(client, message, user_id, sent_message, link)
        elif 'solidfiles' in link:
            return _solidfiles(client, message, user_id, sent_message, link)
        elif 'anonfiles' in link:
            return _anonfiles(client, message, user_id, sent_message, link)
        elif 'mediafire.com' in link:
            return _mediafire(client, message, user_id, sent_message, link)
        elif 'zippyshare.com' in link:
            return _zippyshare(client, message, user_id, sent_message, link)
        elif 'pornhub.com' in link:
            return _pornhub(client, message, user_id, sent_message, link)
        elif 'youtu' in link:
            return _youtu(client, message, user_id, sent_message, link)

@Client.on_message(filters.private & filters.incoming & (filters.document | filters.audio | filters.video | filters.photo) & CustomFilters.auth_users)
async def _telegram_file(client, message):
  user_id = message.from_user.id
  sent_message = await message.reply_text('🕵️**Checking File...**', quote=True)
  if isinstance(message.document, Document):
      file = message.document
  elif isinstance(message.video, Video):
      file = message.video
  elif isinstance(message.audio, Audio):
      file = message.audio
  elif isinstance(message.photo, list):
      file = message.photo[-1]  # Use the largest available photo
      file.mime_type = "image/png"
  await sent_message.edit(Messages.DOWNLOAD_TG_FILE.format(file.file_name, humanbytes(file.file_size), file.mime_type))  LOGGER.info(f'Download:{user_id}: {file.file_id}')
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

@Client.on_message(filters.incoming & filters.private & filters.command(BotCommands.YtDl) & CustomFilters.auth_users)
def _ytdl(client, message):
  user_id = message.from_user.id
  if len(message.command) > 1:
    sent_message = message.reply_text('🕵️**Checking Link...**', quote=True)
    link = message.command[1]
    LOGGER.info(f'YTDL:{user_id}: {link}')
    sent_message.edit(Messages.DOWNLOADING.format(link))
    result, file_path = utube_dl(link)
    if result:
      sent_message.edit(Messages.DOWNLOADED_SUCCESSFULLY.format(os.path.basename(file_path), humanbytes(os.path.getsize(file_path))))
      msg = GoogleDrive(user_id).upload_file(file_path)
      sent_message.edit(msg)
      LOGGER.info(f'Deleteing: {file_path}')
      os.remove(file_path)
    else:
      sent_message.edit(Messages.DOWNLOAD_ERROR.format(file_path, link))
  else:
    message.reply_text(Messages.PROVIDE_YTDL_LINK, quote=True)

#downloader

def _gd(client, message, user_id, sent_message, link):
      sent_message.edit(Messages.CLONING.format(link))
      LOGGER.info(f'Copy:{user_id}: {link}')
      msg = GoogleDrive(user_id).clone(link)
      sent_message.edit(msg)

def _fb(client, message, user_id, sent_message, link):
      url = message.text
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
              sent_message.edit(Messages.DOWNLOADING.format(link))
              result, file_path = download_file(link, dl_path)

              if os.path.exists(file_path):
                sent_message.edit(Messages.DOWNLOADED_SUCCESSFULLY.format(os.path.basename(file_path), humanbytes(os.path.getsize(file_path))))
                msg = GoogleDrive(user_id).upload_file(file_path)
                sent_message.edit(msg)
                LOGGER.info(f'Deleteing: {file_path}')
                os.remove(file_path)  
            except:
              durl = str(contents['sd']).replace('&amp;', '&')
              link = durl.strip()
              filename = os.path.basename(link)
              dl_path = DOWNLOAD_DIRECTORY
              LOGGER.info(f'Download:{user_id}: {link}')
              sent_message.edit(Messages.DOWNLOADING.format(link))
              result, file_path = download_file(link, dl_path)

              if os.path.exists(file_path):
                sent_message.edit(Messages.DOWNLOADED_SUCCESSFULLY.format(os.path.basename(file_path), humanbytes(os.path.getsize(file_path))))
                msg = GoogleDrive(user_id).upload_file(file_path)
                sent_message.edit(msg)
                LOGGER.info(f'Deleteing: {file_path}')
                os.remove(file_path)  
        
        
      except:
        sent_message = message.reply_text('🕵️**Your Facebook Link is Private & SO i cAnNot Download**', quote=True)

def _solidfiles(client, message, user_id, sent_message, link):
      url = message.text
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
        sent_message.edit(Messages.DOWNLOADING.format(link))
        result, file_path = download_file(link, dl_path)
        if os.path.exists(file_path):
          sent_message.edit(Messages.DOWNLOADED_SUCCESSFULLY.format(os.path.basename(file_path), humanbytes(os.path.getsize(file_path))))
          msg = GoogleDrive(user_id).upload_file(file_path)
          sent_message.edit(msg)
          LOGGER.info(f'Deleteing: {file_path}')
          os.remove(file_path)
      except:
        sent_message = message.reply_text('🕵️**Solidfiles link error...**', quote=True)

def _anonfiles(client, message, user_id, sent_message, link):
      url = message.text
      try:
        bypasser = lk21.Bypass()
        dl_url=bypasser.bypass_anonfiles(url)
        link = dl_url.strip()
        filename = os.path.basename(link)
        dl_path = DOWNLOAD_DIRECTORY
        LOGGER.info(f'Download:{user_id}: {link}')
        sent_message.edit(Messages.DOWNLOADING.format(link))
        result, file_path = download_file(link, dl_path)
        if os.path.exists(file_path):
          sent_message.edit(Messages.DOWNLOADED_SUCCESSFULLY.format(os.path.basename(file_path), humanbytes(os.path.getsize(file_path))))
          msg = GoogleDrive(user_id).upload_file(file_path)
          sent_message.edit(msg)
          LOGGER.info(f'Deleteing: {file_path}')
          os.remove(file_path)
      except:
        sent_message = message.reply_text('🕵️**Anonfiles link error...**', quote=True)

def _mediafire(client, message, user_id, sent_message, link):
      url = message.text
      try:
        link = re.findall(r'\bhttps?://.*mediafire\.com\S+', url)[0]
      except IndexError:
        sent_message = message.reply_text('🕵️**mediafire link error...**', quote=True)
      page = BeautifulSoup(requests.get(link).content, 'lxml')
      info = page.find('a', {'aria-label': 'Download file'})
      dl_url = info.get('href')
      link = dl_url.strip()
      filename = os.path.basename(link)
      dl_path = DOWNLOAD_DIRECTORY
      LOGGER.info(f'Download:{user_id}: {link}')
      sent_message.edit(Messages.DOWNLOADING.format(link))
      result, file_path = download_file(link, dl_path)
      if os.path.exists(file_path):
        sent_message.edit(Messages.DOWNLOADED_SUCCESSFULLY.format(os.path.basename(file_path), humanbytes(os.path.getsize(file_path))))
        msg = GoogleDrive(user_id).upload_file(file_path)
        sent_message.edit(msg)
        LOGGER.info(f'Deleteing: {file_path}')
        os.remove(file_path)
      else:
        sent_message = message.reply_text('🕵️**mediafire link error...**', quote=True)

def _zippyshare(client, message, user_id, sent_message, link):
      url = message.text
      dl_url = ''
      try:
        link = re.findall(r'\bhttps?://.*zippyshare\.com\S+', url)[0]
      except IndexError:
        sent_message = message.reply_text('🕵️**zippy link error...**', quote=True)
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
      sent_message.edit(Messages.DOWNLOADING.format(link))
      result, file_path = download_file(link, dl_path)
      if os.path.exists(file_path):
        sent_message.edit(Messages.DOWNLOADED_SUCCESSFULLY.format(os.path.basename(file_path),
                                                                  humanbytes(os.path.getsize(file_path))))
        msg = GoogleDrive(user_id).upload_file(file_path)
        sent_message.edit(msg)
        LOGGER.info(f'Deleteing: {file_path}')
        os.remove(file_path)
      else:
        sent_message = message.reply_text('🕵️** zippy link error...**', quote=True)

def _pornhub(client, message, user_id, sent_message, link):
      link = message.text
      LOGGER.info(f'YTDL:{user_id}: {link}')
      sent_message.edit(Messages.DOWNLOADING.format(link))
      result, file_path = utube_dl(link)
      if result:
        sent_message.edit(Messages.DOWNLOADED_SUCCESSFULLY.format(os.path.basename(file_path), humanbytes(os.path.getsize(file_path))))
        msg = GoogleDrive(user_id).upload_file(file_path)
        sent_message.edit(msg)
        LOGGER.info(f'Deleteing: {file_path}')
        os.remove(file_path)
      else:
        sent_message = message.reply_text('🕵️**PORNHUB ERROR**', quote=True)

def _youtu(client, message, user_id, sent_message, link):
      link = message.text
      LOGGER.info(f'YTDL:{user_id}: {link}')
      sent_message.edit(Messages.DOWNLOADING.format(link))
      result, file_path = utube_dl(link)
      if result:
        sent_message.edit(Messages.DOWNLOADED_SUCCESSFULLY.format(os.path.basename(file_path), humanbytes(os.path.getsize(file_path))))
        msg = GoogleDrive(user_id).upload_file(file_path)
        sent_message.edit(msg)
        LOGGER.info(f'Deleteing: {file_path}')
        os.remove(file_path)
      else:
        sent_message = message.reply_text('🕵️**YOUTUBE ERROR**', quote=True)
