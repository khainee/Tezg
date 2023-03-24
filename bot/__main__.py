import os
import logging
import asyncio
from pyrogram import Client
from pyrogram.handlers import MessageHandler
from bot import bot, DOWNLOAD_DIRECTORY
from bot.config import Messages as tr
from bot.plugins import authorize, copy, delete, download, help, set_parent, utils

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
LOGGER = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

if __name__ == "__main__":
    if not os.path.isdir(DOWNLOAD_DIRECTORY):
        os.makedirs(DOWNLOAD_DIRECTORY)
        LOGGER.info('Creating f"{DOWNLOAD_DIRECTORY}"')

LOGGER.info('Starting Bot !')
bot.run_forever()
LOGGER.info('Bot Stopped !')
