import os
import asyncio
import shutil
import sys
from os import execl
from time import sleep, time
from sys import executable
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, RPCError
from bot import SUDO_USERS, DOWNLOAD_DIRECTORY, LOGGER, bot, botStartTime

@bot.on_message(filters.private & filters.incoming & filters.command(['log']) & filters.user(SUDO_USERS), group=2)
async def _send_log(client, message):
  with open('log.txt', 'rb') as f:
    try:
      await client.send_document(message.chat.id, document=f, file_name=f.name, reply_to_message_id=message.id)
      LOGGER.info(f'Log file sent to {message.from_user.id}')
    except FloodWait as e:
      await asyncio.sleep(e.x)
    except RPCError as e:
      await message.reply_text(e, quote=True)

@bot.on_message(filters.private & filters.incoming & filters.command(['restart']) & filters.user(SUDO_USERS), group=2)
async def _restart(client, message):
    shutil.rmtree(DOWNLOAD_DIRECTORY)
    LOGGER.info('Deleted DOWNLOAD_DIRECTORY successfully.')
    restart_message = await message.reply_text('**♻️ Restarting...**', quote=True)
    with open(".restartmsg", "w") as f:
        f.write(f"{restart_message.chat.id}\n{restart_message.id}\n")
    LOGGER.info(f'{message.from_user.id}: Restarting...')
    execl(executable, executable, "-m", "bot")
