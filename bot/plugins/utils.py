import os
import asyncio
import shutil
import sys
from os import execl
from time import sleep, time
from sys import executable
from psutil import disk_usage, cpu_percent, swap_memory, cpu_count, virtual_memory, net_io_counters, boot_time
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, RPCError
from bot import SUDO_USERS, DOWNLOAD_DIRECTORY, LOGGER, bot, botStartTime
from bot.helpers.utils import get_readable_time, get_readable_file_size

@bot.on_message(filters.private & filters.incoming & filters.command(['stats']))
async def stats(client, message):
    total, used, free, disk = disk_usage('/')
    swap = swap_memory()
    memory = virtual_memory()
    stats = f'<b>Bot Uptime:</b> {get_readable_time(time() - botStartTime)}\n'\
            f'<b>OS Uptime:</b> {get_readable_time(time() - boot_time())}\n\n'\
            f'<b>Total Disk Space:</b> {get_readable_file_size(total)}\n'\
            f'<b>Used:</b> {get_readable_file_size(used)} | <b>Free:</b> {get_readable_file_size(free)}\n\n'\
            f'<b>CPU:</b> {cpu_percent(interval=0.5)}%\n'\
            f'<b>RAM:</b> {memory.percent}%\n'\
            f'<b>DISK:</b> {disk}%\n\n'\
            f'<b>Physical Cores:</b> {cpu_count(logical=False)}\n'\
            f'<b>Total Cores:</b> {cpu_count(logical=True)}\n\n'\
            f'<b>SWAP:</b> {get_readable_file_size(swap.total)} | <b>Used:</b> {swap.percent}%\n'\
            f'<b>Memory Total:</b> {get_readable_file_size(memory.total)}\n'\
            f'<b>Memory Free:</b> {get_readable_file_size(memory.available)}\n'\
            f'<b>Memory Used:</b> {get_readable_file_size(memory.used)}\n'
    await message.reply_text(stats, quote=True)


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
