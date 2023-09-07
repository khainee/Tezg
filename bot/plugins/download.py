import os
from pyrogram import Client, filters
from bot.helpers.sql_helper import gDriveDB, idsDB
from bot.helpers.utils import CustomFilters, humanbytes, is_share_link
from bot.helpers.downloader import download_file, utube_dl
from bot.helpers.direct_link_gen import direct_link
from bot.helpers.gdrive_utils import GoogleDrive
from bot import DOWNLOAD_DIRECTORY, LOGGER, bot
from bot.config import Messages, BotCommands
from pyrogram.errors import FloodWait, RPCError
from uuid import uuid4

@bot.on_message(filters.private & filters.incoming & filters.text & (filters.command(BotCommands.Download) | filters.regex('^(ht|f)tp*')) & CustomFilters.auth_users)
async def _download(client, message):
    if not message.media:
        sent_message = await message.reply_text('🕵️**Checking link...**')
        url = message.command[1] if message.command else message.text
        user_id = message.from_user.id
        if 'drive.google.com' in url:
            return await _gd(client, message, user_id, sent_message, url)
        if is_share_link(url):
            return await _share_link(client, message, user_id, sent_message, url)
        else:
            return await _dl(client, message, user_id, sent_message, url)

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
    file_path = await message.download(file_name=DOWNLOAD_DIRECTORY, progress=progress, progress_args=(sent_message, file))
    file_name = os.path.basename(file_path)
    file_size = humanbytes(os.path.getsize(file_path))
    await sent_message.edit(Messages.DOWNLOADED_SUCCESSFULLY.format(file_name, file_size))
    msg = await GoogleDrive(user_id).upload_file(file_path, sent_message, file.mime_type)
    await sent_message.edit(msg)
  except RPCError:
    await sent_message.edit(Messages.WENT_WRONG)
  LOGGER.info(f'Deleteing: {file_path}')
  os.remove(file_path)

async def progress(current, total, sent_message, file):
    progress_bar = "📥 Downloading File...\n"
    progress_bar += f"File name: {file.file_name}\n"
    progress_bar += f"File Type: {file.mime_type}\n"
    progress_bar += f"File size: {humanbytes(file.file_size)}\n"
    progress_bar += f"Progress: {current * 100 / total:.1f}%\n"
    await sent_message.edit(progress_bar)

@bot.on_message(filters.incoming & filters.private & filters.command(BotCommands.YtDl) & CustomFilters.auth_users)
async def _ytdl(client, message):
    if len(message.command) > 1:
        sent_message = await message.reply_text('🕵️**Checking Link...**')
        link = message.command[1]
        user_id = message.from_user.id
        LOGGER.info(f'YTDL:{user_id}: {link}')
        await sent_message.edit(Messages.DOWNLOADING.format(link))
        result, file_path = utube_dl(link)
        if result is True:
          await sent_message.edit(Messages.DOWNLOADED_SUCCESSFULLY.format(os.path.basename(file_path), humanbytes(os.path.getsize(file_path))))
          msg = await GoogleDrive(user_id).upload_file(file_path, sent_message)
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
        if r is True:
            link = dl_url.strip()
            dl_path = DOWNLOAD_DIRECTORY
            gid = uuid4().hex[:16]
            LOGGER.info(f'Download:{user_id}: {link}')
            await sent_message.edit(Messages.DOWNLOADING.format(link))
            result, file_path = await download_file(link, dl_path, gid, sent_message)
            if result is True and os.path.exists(file_path):
                await sent_message.edit(Messages.DOWNLOADED_SUCCESSFULLY.format(os.path.basename(file_path), humanbytes(os.path.getsize(file_path))))
                msg = await GoogleDrive(user_id).upload_file(file_path, sent_message)
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
      LOGGER.info(f'Share link Copy:{user_id}: {url}')
      result, dl_url = await direct_link(url)
      if result is True:
        return await _gd(client, message, user_id, sent_message, dl_url)
      else:
        await sent_message.edit(Messages.DOWNLOAD_ERROR.format(dl_url, url))
    except Exception as e:
        await sent_message.edit(f'🕵️**Link error...\n{e}**')
