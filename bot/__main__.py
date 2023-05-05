import os
import logging
from pyrogram.types import BotCommand
from bot.config import BotCommands
from bot import bot, DOWNLOAD_DIRECTORY, LOGGER
from bot.plugins import authorize, copy, delete, download, help, set_parent, utils, speedtest

async def main():
    if os.path.isfile(".restartmsg"):
        with open(".restartmsg") as f:
            chat_id, msg_id = map(int, f)
        try:
            await bot.edit_message_text(chat_id=chat_id, message_id=msg_id, text='Restarted Successfully!')
        except:
            pass
    try:
        await bot.set_bot_commands([
            BotCommand(f'{BotCommands.Start}', 'Start Command'),
            BotCommand(f'{BotCommands.Download}', 'Download support link'),
            BotCommand(f'{BotCommands.Authorize}', 'Authorizing GDrive Account'),
            BotCommand(f'{BotCommands.SetFolder}', 'Set Custom Upload Folder'),
            BotCommand(f'{BotCommands.Revoke}', 'Revoke GDrive Account'),
            BotCommand(f'{BotCommands.Clone}', 'Clone GDrive Files'),
            BotCommand(f'{BotCommands.Delete}', 'Delete GDrive Files'),
            BotCommand(f'{BotCommands.EmptyTrash}', 'Empty GDrive Trash'),
            BotCommand(f'{BotCommands.YtDl}', 'Download yt-dlp support link'),
            BotCommand(f'{BotCommands.Speed}', 'Test the speed of server'),
            BotCommand(f'{BotCommands.Stats}', 'Status of the Bot'),
            BotCommand(f'{BotCommands.Ping}', 'Ping the bot')])
    except Exception as e:
        LOGGER.error(f"Error occurred: {e}")


if __name__ == "__main__":
    if not os.path.isdir(DOWNLOAD_DIRECTORY):
        os.makedirs(DOWNLOAD_DIRECTORY)
        LOGGER.info(f'Creating {DOWNLOAD_DIRECTORY}')

LOGGER.info('Starting Bot !')
bot.loop.run_until_complete(main())
bot.loop.run_forever()
LOGGER.info('Bot Stopped !')
