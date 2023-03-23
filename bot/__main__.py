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

async def main():
    if os.path.isfile(".restartmsg"):
        with open(".restartmsg") as f:
            chat_id, msg_id = map(int, f)
        try:
            await bot.edit_message_text(chat_id, msg_id, "Restarted successfully!")  
        except:
            pass   
        os.remove(".restartmsg")


if __name__ == "__main__":
    if not os.path.isdir(DOWNLOAD_DIRECTORY):
        os.makedirs(DOWNLOAD_DIRECTORY)
    LOGGER.info('Starting Bot !')
    bot.loop.run_until_complete(main())
    bot.run()
    LOGGER.info('Bot Stopped !')
