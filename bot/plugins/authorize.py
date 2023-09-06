import json
from httplib2 import Http
from bot import LOGGER, G_DRIVE_CLIENT_ID, G_DRIVE_CLIENT_SECRET, bot
from bot.config import Messages
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from oauth2client.client import OAuth2WebServerFlow, FlowExchangeError
from bot.helpers.sql_helper import gDriveDB
from bot.helpers.gdrive_utils import GoogleDrive
from bot.config import BotCommands
from bot.helpers.utils import CustomFilters


OAUTH_SCOPE = "https://www.googleapis.com/auth/drive, https://www.googleapis.com/auth/userinfo.email"
REDIRECT_URI = "https://www.drivetalkmm.tech/gdrive-auth"

flow = OAuth2WebServerFlow(
    client_id=G_DRIVE_CLIENT_ID,
    client_secret=G_DRIVE_CLIENT_SECRET,
    scope=OAUTH_SCOPE,
    redirect_uri=REDIRECT_URI
    response_type='code',
    access_type='offline',
    prompt='consent',
)

@bot.on_message(filters.private & filters.incoming & filters.command(BotCommands.Authorize))
async def _auth(client, message):
    user_id = message.from_user.id
    creds = gDriveDB.search(user_id)
    if creds is not None:
        creds.refresh(Http())
        gDriveDB._set(user_id, creds)
        await message.reply_text(Messages.ALREADY_AUTH, quote=True)
    else:
        global flow
        try:
            flow = OAuth2WebServerFlow(
                response_type='code',
                access_type='offline',
                prompt='consent',
                client_id=G_DRIVE_CLIENT_ID,
                client_secret=G_DRIVE_CLIENT_SECRET,
                scope=OAUTH_SCOPE,
                redirect_uri=REDIRECT_URI
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


@bot.on_message(filters.private & filters.incoming & filters.command(BotCommands.Revoke) & CustomFilters.auth_users)
async def _revoke(client, message):
    user_id = message.from_user.id
    try:
        gDriveDB._clear(user_id)
        LOGGER.info(f'Revoked:{user_id}')
        sent_message = await message.reply_text(Messages.REVOKED, quote=True)
    except Exception as e:
        await sent_message.edit(f"**ERROR:** ```{e}```", quote=True)


@bot.on_message(filters.private & filters.incoming & filters.text & ~CustomFilters.auth_users)
async def _token(client, message):
    token = message.text.split()[-1]
    WORD = len(token)
    if WORD == 73 and token[1] == "/":
        creds = None
        global flow
        if flow:
            try:
                user_id = message.from_user.id
                sent_message = await message.reply_text("🕵️**Checking received code...**", quote=True)
                creds = flow.step2_exchange(message.text)
                gDriveDB._set(user_id, creds)
                LOGGER.info(f'AuthSuccess: {user_id}')
                mail = GoogleDrive(user_id).getmail
                await sent_message.edit(Messages.AUTH_SUCCESSFULLY.format(mail))
                flow = None
            except FlowExchangeError:
                await sent_message.edit(Messages.INVALID_AUTH_CODE)
            except Exception as e:
                await sent_message.edit(f"**ERROR:** ```{e}```")
        else:
            await sent_message.edit(Messages.FLOW_IS_NONE, quote=True)
