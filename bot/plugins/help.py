import asyncio
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, RPCError
from bot.config import Messages
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from time import time
from bot import bot

@bot.on_message(filters.private & filters.incoming & filters.command(['start']), group=2)
async def start(client, message):
    try:
      await message.reply_text(Messages.START_MSG.format(message.from_user.mention), disable_web_page_preview=True, reply_to_message_id=message.id)
    except FloodWait as e:
      await asyncio.sleep(e.x)
    except RPCError as e:
      await message.reply_text(e, quote=True)

@bot.on_message(filters.private & filters.incoming & filters.command(['ping']), group=2)
async def ping(client, message):
    start_time = int(round(time() * 1000))
    sent_message = await message.reply_text("Starting Ping")
    end_time = int(round(time() * 1000))
    await sent_message.edit(f'{end_time - start_time} ms')


@bot.on_message(filters.private & filters.incoming & filters.command(['help']), group=2)
def _help(client, message):
    client.send_message(chat_id = message.chat.id,
        text = Messages.HELP_MSG[1],
        reply_markup = InlineKeyboardMarkup(map(1)),
        reply_to_message_id = message.id
    )

help_callback_filter = filters.create(lambda _, __, query: query.data.startswith('help+'))

@bot.on_callback_query(help_callback_filter)
def help_answer(c, callback_query):
    chat_id = callback_query.from_user.id
    message_id = callback_query.message.id
    msg = int(callback_query.data.split('+')[1])
    c.edit_message_text(chat_id = chat_id,    message_id = message_id,
        text = Messages.HELP_MSG[msg],    reply_markup = InlineKeyboardMarkup(map(msg))
    )


def map(pos):
    if(pos==1):
        button = [
            [InlineKeyboardButton(text = '-->', callback_data = "help+2")]
        ]
    elif(pos==len(Messages.HELP_MSG)-1):

        button = [
            [
             InlineKeyboardButton(text = 'Support Chat', url = "https://t.me/drivetalkchannel"),
            ],
            [InlineKeyboardButton(text = '<--', callback_data = f"help+{pos-1}")]

        ]
    else:
        button = [
            [
                InlineKeyboardButton(text = '<--', callback_data = f"help+{pos-1}"),
                InlineKeyboardButton(text = '-->', callback_data = f"help+{pos+1}")
            ],
        ]
    return button
