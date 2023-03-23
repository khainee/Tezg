import os
import logging
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

@bot.on_message(filters.private & filters.incoming & filters.command(['start']), group=2)
def _start(client, message):
    client.send_message(chat_id = message.chat.id,
        text = tr.START_MSG.format(message.from_user.mention),
        reply_to_message_id = message.id
    )

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
    bot.loop.run_forever()
    LOGGER.info('Bot Stopped !')
