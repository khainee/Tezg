from pyrogram import Client, filters
from bot.config import BotCommands, Messages
from bot.helpers.utils import CustomFilters
from bot.helpers.gdrive_utils import GoogleDrive
from bot import LOGGER, bot 

@bot.on_message(filters.private & filters.incoming & filters.command(BotCommands.Clone) & CustomFilters.auth_users)
async def _clone(client, message):
  user_id = message.from_user.id
  if len(message.command) > 1:
    link = message.command[1]
    LOGGER.info(f'Copy:{user_id}: {link}')
    sent_message = await message.reply_text(Messages.CLONING.format(link), quote=True)
    msg = GoogleDrive(user_id).clone(link)
    await sent_message.edit(msg)
  else:
    await sent_message.edit(Messages.PROVIDE_GDRIVE_URL.format(BotCommands.Clone[0]))
