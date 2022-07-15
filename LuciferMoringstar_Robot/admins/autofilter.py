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
from database.autofilter_mdb import Media, unpack_new_file_id
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
async def deletefiles(bot, update):
    """Delete file from database"""
    reply = update.reply_to_message
    if reply and reply.media:
        msg = await update.reply_text("𝙿𝚁𝙾𝙲𝙴𝚂𝚂𝙸𝙽𝙶..⏳", quote=True)
    else:
        await update.reply_text("𝚁𝙴𝙿𝙻𝚈 𝚃𝙾 𝙵𝙸𝙻𝙴 𝚆𝙸𝚃𝙷 `/delete` 𝚆𝙷𝙸𝙲𝙷 𝚈𝙾𝚄 𝚆𝙰𝙽𝚃 𝚃𝙾 𝙳𝙴𝙻𝙴𝚃𝙴", quote=True)
        return

    for file_type in ("document", "video", "audio"):
        media = getattr(reply, file_type, None)
        if media is not None:
            break
    else:
        await msg.edit('𝚃𝙷𝙸𝚂 𝙸𝚂 𝙽𝙾𝚃 𝚂𝚄𝙿𝙿𝙾𝚁𝚃𝙴𝙳 𝙵𝙸𝙻𝙴 𝙵𝙾𝚁𝙼𝙰𝚃')
        return
    
    file_id, file_ref = unpack_new_file_id(media.file_id)

    result = await Media.collection.delete_one({
        '_id': file_id,
    })
    if result.deleted_count:
        await msg.edit("𝙵𝙸𝙻𝙴 𝙸𝚂 𝚂𝚄𝙲𝙲𝙴𝚂𝚂𝙵𝚄𝙻𝙻𝚈 𝙳𝙴𝙻𝙴𝚃𝙴𝙳 𝙵𝚁𝙾𝙼 𝙳𝙰𝚃𝙰𝙱𝙰𝚂𝙴")
    else:
        file_name = re.sub(r"(_|\-|\.|\+)", " ", str(media.file_name))
        result = await Media.collection.delete_many({
            'file_name': file_name,
            'file_size': media.file_size,
            'mime_type': media.mime_type
            })
        if result.deleted_count:
            await msg.edit("𝙵𝙸𝙻𝙴 𝙸𝚂 𝚂𝚄𝙲𝙲𝙴𝚂𝚂𝙵𝚄𝙻𝙻𝚈 𝙳𝙴𝙻𝙴𝚃𝙴𝙳 𝙵𝚁𝙾𝙼 𝙳𝙰𝚃𝙰𝙱𝙰𝚂𝙴")
        else:
            # files indexed before https://github.com/EvamariaTG/EvaMaria/commit/f3d2a1bcb155faf44178e5d7a685a1b533e714bf#diff-86b613edf1748372103e94cacff3b578b36b698ef9c16817bb98fe9ef22fb669R39 
            # have original file name.
            result = await Media.collection.delete_many({
                'file_name': media.file_name,
                'file_size': media.file_size,
                'mime_type': media.mime_type
            })
            if result.deleted_count:
                await msg.edit("𝙵𝙸𝙻𝙴 𝙸𝚂 𝚂𝚄𝙲𝙲𝙴𝚂𝚂𝙵𝚄𝙻𝙻𝚈 𝙳𝙴𝙻𝙴𝚃𝙴𝙳 𝙵𝚁𝙾𝙼 𝙳𝙰𝚃𝙰𝙱𝙰𝚂𝙴")
            else:
                await msg.edit("𝙵𝙸𝙻𝙴 𝙽𝙾𝚃 𝙵𝙾𝚄𝙽𝚃 𝙸𝙽 𝙳𝙰𝚃𝙰𝙱𝙰𝚂𝙴")


@Client.on_message(filters.private & filters.command('delall') & filters.user(ADMINS))
async def deleteall(bot, update):
    buttons = [[ InlineKeyboardButton(text="𝚈𝙴𝚂", callback_data="files_delete"), InlineKeyboardButton(text="𝙽𝙾", callback_data="close") ]]  
    await update.reply_text("""𝚃𝙷𝙸𝚂 𝚆𝙸𝙻𝙻 𝙳𝙴𝙻𝙴𝚃𝙴 𝙰𝙻𝙻 𝙸𝙽𝙳𝙴𝚇𝙴𝙳 𝙵𝙸𝙻𝙴𝚂\n𝙳𝙾 𝚈𝙾𝚄𝚆𝙰𝙽𝚃 𝚃𝙾 𝙲𝙾𝙽𝚃𝙸𝙽𝚄𝙴?""", reply_markup=InlineKeyboardMarkup(buttons))
