import os
import logging
from bot import bot, DOWNLOAD_DIRECTORY
from bot.plugins import authorize, copy, delete, download, help, set_parent, utils, speedtest

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
LOGGER = logging.getLogger(__name__)

async def main():
    if os.path.isfile(".restartmsg"):
        with open(".restartmsg") as f:
            chat_id, msg_id = map(int, f)
    try:
        await bot.edit_message_text(chat_id=chat_id, message_id=msg_id, text='Restarted Successfully!')
    except:
        pass
#    await bot.set_bot_commands([

if __name__ == "__main__":
    if not os.path.isdir(DOWNLOAD_DIRECTORY):
        os.makedirs(DOWNLOAD_DIRECTORY)
        LOGGER.info(f'Creating {DOWNLOAD_DIRECTORY}')

LOGGER.info('Starting Bot !')
bot.loop.run_until_complete(main())
bot.loop.run_forever()
LOGGER.info('Bot Stopped !')
