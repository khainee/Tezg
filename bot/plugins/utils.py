import os
import shutil
import sys
from os import execl
from time import sleep
from sys import executable
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, RPCError
from bot import SUDO_USERS, DOWNLOAD_DIRECTORY, LOGGER


@Client.on_message(filters.private & filters.incoming & filters.command(['log']) & filters.user(SUDO_USERS), group=2)
def _send_log(client, message):
  with open('log.txt', 'rb') as f:
    try:
      client.send_document(
        message.chat.id,
        document=f,
        file_name=f.name,
        reply_to_message_id=message.id
        )
      LOGGER.info(f'Log file sent to {message.from_user.id}')
    except FloodWait as e:
      sleep(e.x)
    except RPCError as e:
      message.reply_text(e, quote=True)

@Client.on_message(filters.private & filters.incoming & filters.command(['restart']) & filters.user(SUDO_USERS), group=2)
async def _restart(client, message):
    shutil.rmtree(DOWNLOAD_DIRECTORY)
    LOGGER.info('Deleted DOWNLOAD_DIRECTORY successfully.')
    sent_message = await message.reply_text('**♻️ Restarting!**', quote=True)
    LOGGER.info(f'{message.from_user.id}: Restarting...')

    # Restart the bot using execl
    os.execl(sys.executable, sys.executable, "-m", "bot")
    await sent_message.edit_text('**✅ Restarted Successfully!**')
