# MIT License

# Copyright (c) 2022 Muhammed

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Telegram Link : https://telegram.dog/Mo_Tech_Group
# Repo Link : https://github.com/PR0FESS0R-99/LuciferMoringstar-Robot
# License Link : https://github.com/PR0FESS0R-99/LuciferMoringstar-Robot/blob/LuciferMoringstar-Robot/LICENSE
 
import logging, os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from LuciferMoringstar_Robot import CHANNELS, ADMINS
from database.autofilter_mdb import Media
logger = logging.getLogger(__name__)

@Client.on_message(filters.command('total') & filters.user(ADMINS))
async def total(bot, update):
    msg = await update.reply_text("Processing...⏳", quote=True)
    try:
        total = await Media.count_documents()
        await msg.edit(f'📁 Saved files: {total}')
    except Exception as e:
        logger.exception('Failed To Check Total Files')
        await msg.edit(f'Error: {e}')

@Client.on_message(filters.command('logs') & filters.user(ADMINS))
async def log_file(bot, update):
    """Send log file"""
    try:
        await update.reply_document('LuciferMoringstarLogs.txt')
    except Exception as e:
        await update.reply(str(e))

@Client.on_message(filters.command('channel') & filters.user(ADMINS))
async def channel_info(bot, update):
           
    """Send basic information of channel"""
    if isinstance(CHANNELS, (int, str)):
        channels = [CHANNELS]
    elif isinstance(CHANNELS, list):
        channels = CHANNELS
    else:
        raise ValueError("Unexpected type of CHANNELS")

    text = '📑 **Indexed channels/groups**\n'
    for channel in channels:
        chat = await bot.get_chat(channel)
        if chat.username:
            text += '\n@' + chat.username
        else:
            text += '\n' + chat.title or chat.first_name

    text += f'\n\n**Total:** {len(CHANNELS)}'

    if len(text) < 4096:
        await update.reply(text)
    else:
        file = 'Indexed channels.txt'
        with open(file, 'w') as f:
            f.write(text)
        await update.reply_document(file)
        os.remove(file)

@Client.on_message(filters.command('delete') & filters.user(ADMINS))
async def delete(bot, message):
    """Delete file from database"""
    reply = message.reply_to_message
    if reply and reply.media:
        msg = await message.reply("Processing...⏳", quote=True)
    else:
        await message.reply('Reply To File With /delete Which You Want To Delete', quote=True)
        return

    for file_type in ("document", "video", "audio"):
        media = getattr(reply, file_type, None)
        if media is not None:
            break
    else:
        await msg.edit('This Is Not Supported File Format 😡')
        return

    result = await Media.collection.delete_one({
        'file_name': media.file_name,
        'file_size': media.file_size,
        'mime_type': media.mime_type
    })
    if result.deleted_count:
        await msg.edit('File Is Successfully Deleted From Database 😮‍💨')
    else:
        await msg.edit('File Not Found In Database 😮‍💨')


@Client.on_message(filters.private & filters.command('delete') & filters.user(ADMINS))
async def delete(bot, message):
    buttons = [[ InlineKeyboardButton(text="YES", callback_data="files_delete"), InlineKeyboardButton(text="YES", callback_data="close") ]]  
    await message.reply_text("""𝚃𝙷𝙸𝚂 𝚆𝙸𝙻𝙻 𝙳𝙴𝙻𝙴𝚃𝙴 𝙰𝙻𝙻 𝙸𝙽𝙳𝙴𝚇𝙴𝙳 𝙵𝙸𝙻𝙴𝚂\n𝙳𝙾 𝚈𝙾𝚄𝚆𝙰𝙽𝚃 𝚃𝙾 𝙲𝙾𝙽𝚃𝙸𝙽𝚄𝙴?""", reply_markup=InlineKeyboardMarkup(buttons))



