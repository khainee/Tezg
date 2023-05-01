import os
from pyrogram import Client, filters
from bot.helpers.sql_helper import gDriveDB, idsDB
from bot.helpers.utils import CustomFilters, humanbytes, is_share_link
from bot.helpers.downloader import download_file, utube_dl, download_fb
from bot.helpers.direct_link_gen import direct_link
from bot.helpers.gdrive_utils import GoogleDrive
from bot import DOWNLOAD_DIRECTORY, LOGGER, bot
from bot.config import Messages, BotCommands
from pyrogram.errors import FloodWait, RPCError
from uuid import uuid4

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
            await _gd(client, message, user_id, sent_message, url)
        if is_share_link(url):
            await _share_link(url)
        else:
            await _dl(client, message, user_id, sent_message, url)

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

async def _dl(client, message, user_id, sent_message, url):
    try:
      r, dl_url = await direct_link(url)
      if r == True:
        link = dl_url.strip()
        dl_path = DOWNLOAD_DIRECTORY
        gid = uuid4().hex[:16]
        LOGGER.info(f'Download:{user_id}: {link}')
        await sent_message.edit(Messages.DOWNLOADING.format(link))
        result, file_path = await download_file(link, dl_path, gid)
        if result == True and os.path.exists(file_path):
          await sent_message.edit(Messages.DOWNLOADED_SUCCESSFULLY.format(os.path.basename(file_path), humanbytes(os.path.getsize(file_path))))
          msg = GoogleDrive(user_id).upload_file(file_path)
          await sent_message.edit(msg)
          LOGGER.info(f'Deleteing: {file_path}')
          os.remove(file_path)
        else:
          await sent_message.edit(Messages.DOWNLOAD_ERROR.format(file_path, link))
      else:
          await sent_message.edit(Messages.DOWNLOAD_ERROR.format(dl_url, None))
    except Exception as e:
        await sent_message.edit(f'🕵️**Link error...\n{e}**')

async def _share_link(client, message, user_id, sent_message, url):
    try:
      r, dl_url = await direct_link(url)
      if r == True and 'drive.google.com' in dl_url:
        return await _gd(client, message, user_id, sent_message, url)
    except Exception as e:
        await sent_message.edit(f'🕵️**Link error...\n{e}**')
