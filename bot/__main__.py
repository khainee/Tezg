import os
import logging
from pyrogram import Client
from bot import bot, DOWNLOAD_DIRECTORY

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
LOGGER = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


if __name__ == "__main__":
    if not os.path.isdir(DOWNLOAD_DIRECTORY):
        os.makedirs(DOWNLOAD_DIRECTORY)
    LOGGER.info('Starting Bot !')
    bot.run()
    LOGGER.info('Bot Stopped !')
