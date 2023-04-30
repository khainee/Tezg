import os
import logging
from bot import bot, DOWNLOAD_DIRECTORY
from bot.plugins import authorize, copy, delete, download, help, set_parent, utils, speedtest

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
LOGGER = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

if __name__ == "__main__":
    if not os.path.isdir(DOWNLOAD_DIRECTORY):
        os.makedirs(DOWNLOAD_DIRECTORY)
        LOGGER.info(f'Creating {DOWNLOAD_DIRECTORY}')

LOGGER.info('Starting Bot !')
bot.loop.run_forever()
LOGGER.info('Bot Stopped !')
