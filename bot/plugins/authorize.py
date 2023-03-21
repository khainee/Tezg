import re
import json
from httplib2 import Http
from bot import LOGGER, G_DRIVE_CLIENT_ID, G_DRIVE_CLIENT_SECRET
from bot.config import Messages
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from oauth2client.client import OAuth2WebServerFlow, FlowExchangeError
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from bot.helpers.sql_helper import gDriveDB
from bot.config import BotCommands
from bot.helpers.utils import CustomFilters


OAUTH_SCOPE = "https://www.googleapis.com/auth/drive"
REDIRECT_URI = "https://khainee.github.io/G-Drive-Bot/gdrive-auth"

flow = None

@Client.on_message(filters.private & filters.incoming & filters.command(BotCommands.Authorize))
async def _auth(client, message):
    user_id = message.from_user.id
    global flow
    try:
      flow = OAuth2WebServerFlow(
              response_type='code',
              access_type='offline',
              prompt='consent',
              client_id=G_DRIVE_CLIENT_ID,
              client_secret=G_DRIVE_CLIENT_SECRET,
              scope=OAUTH_SCOPE,
              redirect_uri=REDIRECT_URI,
      )
      auth_url = flow.step1_get_authorize_url()
      LOGGER.info(f'AuthURL:{user_id}')
      await message.reply_text(
        text=Messages.AUTH_TEXT.format(auth_url),
        quote=True,
        reply_markup=InlineKeyboardMarkup(
                  [[InlineKeyboardButton("Authorization URL", url=auth_url)]]
              )
        )
    except Exception as e:
      await message.reply_text(f"**ERROR:** ```{e}```", quote=True)

@Client.on_message(filters.private & filters.incoming & filters.text & ~CustomFilters.auth_users)
async def _token(client, message):
  token = message.text.split()[-1]
  WORD = len(token)
  if WORD == 73 and token[1] == "/":
    global flow
    if flow:
      try:
        user = message.from_user
        user_id = message.from_user.id
        sent_message = await message.reply_text("🕵️**Checking received code...**", quote=True)
        credentials = flow.step2_exchange(message.text)
        with open(f"{user_id}.pickle", 'wb') as token:
            pickle.dump(credentials, token)
        LOGGER.info(f'AuthSuccess: {user_id}')
        full_name = user.get_full_name()
        caption_text = f"Here is your token.pickle, {full_name}\n Rename it to token.pickle for working"
        await send_document(user_id, document=f"{user_id}.pickle", caption=caption_text)

        # Delete the pickle file after sending
        os.remove(f"{user_id}.pickle")
        flow = None
      except FlowExchangeError:
        await sent_message.edit(Messages.INVALID_AUTH_CODE)
      except Exception as e:
        await sent_message.edit(f"**ERROR:** ```{e}```")
    else:
        await message.reply_text(Messages.FLOW_IS_NONE, quote=True)
