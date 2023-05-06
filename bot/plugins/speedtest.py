from bot import bot
from speedtest import Speedtest
from pyrogram import filters
from bot.helpers.utils import get_readable_file_size, CustomFilters

@bot.on_message(filters.private & filters.incoming & filters.command(['speedtest']) & CustomFilters.auth_users)
async def speedtest(client, message):
    speed = await message.reply_text("Running Speed Test. Wait about some secs.")
    test = Speedtest()
    test.get_best_server()
    test.download()
    test.upload()
    test.results.share()
    result = test.results.dict()
    string_speed = f'''
╭─《 🚀 SPEEDTEST INFO 》
├ <b>Upload:</b> <code>{speed_convert(result['upload'], False)}</code>
├ <b>Download:</b>  <code>{speed_convert(result['download'], False)}</code>
├ <b>Ping:</b> <code>{result['ping']} ms</code>
├ <b>Time:</b> <code>{result['timestamp']}</code>
├ <b>Data Sent:</b> <code>{get_readable_file_size(int(result['bytes_sent']))}</code>
╰ <b>Data Received:</b> <code>{get_readable_file_size(int(result['bytes_received']))}</code>
'''
    await speed.edit(string_speed)

def speed_convert(size, byte=True):
    if not byte: size = size / 8
    power = 2 ** 10
    zero = 0
    units = {0: "B/s", 1: "KB/s", 2: "MB/s", 3: "GB/s", 4: "TB/s"}
    while size > power:
        size /= power
        zero += 1
    return f"{round(size, 2)} {units[zero]}"
