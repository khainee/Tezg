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

async def main():
    if os.path.isfile(".restartmsg"):
        with open(".restartmsg") as f:
            chat_id, msg_id = map(int, f)
        try:
            await bot.edit_message_text(chat_id=chat_id, message_id=msg_id, text="Restarted successfully!")  
        except Exception as e:
            await bot.send_message(chat_id='5227230295', text=f"**ERROR:** ```{e}```")
        os.remove(".restartmsg")

if __name__ == "__main__":
    if not os.path.isdir(DOWNLOAD_DIRECTORY):
        os.makedirs(DOWNLOAD_DIRECTORY)
    LOGGER.info('Starting Bot !')
    bot.run()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    LOGGER.info('Bot Stopped !')
