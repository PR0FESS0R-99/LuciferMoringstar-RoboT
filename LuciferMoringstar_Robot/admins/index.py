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
 
import logging, asyncio, re
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait
from pyrogram.errors.exceptions.bad_request_400 import ChannelInvalid, ChatAdminRequired, UsernameInvalid, UsernameNotModified
from LuciferMoringstar_Robot import ADMINS, LOG_CHANNEL, temp
from database.autofilter_mdb import save_file

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
lock = asyncio.Lock()

@Client.on_callback_query(filters.regex(r'^index'))
async def index_files(bot, update):
    if update.data.startswith('index_cancel'):
        temp.CANCEL = True
        return await update.answer("𝙲𝙰𝙽𝙲𝙴𝙻𝙻𝙸𝙽𝙶 𝙸𝙽𝙳𝙴𝚇𝙸𝙽𝙶..")
    _, muhammedrk, chat, lst_msg_id, from_user = update.data.split("#")
    if muhammedrk == 'reject':
        await update.message.delete()
        await bot.send_message(chat_id = int(from_user), text = """𝚈𝙾𝚄𝚁 𝚂𝚄𝙱𝙼𝙸𝚂𝚂𝙸𝙾𝙽 𝙵𝙾𝚁 𝙸𝙽𝙳𝙴𝚇𝙸𝙽𝙶 **{}** 𝙷𝙰𝚂 𝙱𝙴𝙴𝙽 𝙳𝙴𝙲𝙻𝙸𝙴𝙽𝙴𝙳 𝙱𝚈 𝙾𝚄𝚁 𝙼𝙾𝙳𝙴𝚁𝙰𝚃𝙾𝚁𝚂""".format(chat), reply_to_message_id = int(lst_msg_id))
        return

    if lock.locked():
        return await update.answer("𝚆𝙰𝙸𝚃 𝚄𝙽𝚃𝙸𝙻 𝙿𝚁𝙴𝚅𝙸𝙾𝚄𝚂 𝙿𝚁𝙾𝙲𝙴𝚂𝚂 𝙲𝙾𝙼𝙿𝙻𝙴𝚃𝙴", show_alert=True)

    msg = update.message
    await update.answer("𝙿𝚁𝙾𝙲𝙴𝚂𝚂𝙸𝙽𝙶...⏳", show_alert=True)
    if int(from_user) not in ADMINS:
        await bot.send_message(int(from_user),
                               "𝚈𝙾𝚄𝚁 𝚂𝚄𝙱𝙼𝙸𝚂𝚂𝙸𝙾𝙽 𝙵𝙾𝚁 𝙸𝙽𝙳𝙴𝚇𝙸𝙽𝙶 {} 𝙷𝙰𝚂 𝙱𝙴𝙴𝙽 𝙰𝙲𝙲𝙴𝙿𝚃𝙴𝙳 𝙱𝚈 𝙾𝚄𝚁 𝙼𝙾𝙳𝙴𝚁𝙰𝚃𝙾𝚁𝚂 𝙰𝙽𝙳 𝚆𝙸𝙻𝙻 𝙱𝙴 𝙰𝙳𝙳𝙴𝙳 𝚂𝙾𝙾𝙽".format(chat),
                               reply_to_message_id=int(lst_msg_id))
    pr0fess0r = [[ InlineKeyboardButton('𝚂𝚃𝙾𝙿', callback_data='close') ]]
    await update.message.edit(text = "𝚂𝚃𝙰𝚁𝚃𝙸𝙽𝙶 𝙸𝙽𝙳𝙴𝚇𝙸𝙽𝙶..", reply_markup=InlineKeyboardMarkup(pr0fess0r))
    try:
        chat = int(chat)
    except:
        chat = chat
    await index_files_to_db(int(lst_msg_id), chat, msg, bot)


@Client.on_message((filters.forwarded | (filters.regex("(https://)?(t\.me/|telegram\.me/|telegram\.dog/)(c/)?(\d+|[a-zA-Z_0-9]+)/(\d+)$")) & filters.text ) & filters.private & filters.incoming)
async def send_for_index(bot, message):
    if message.text:
        regex = re.compile("(https://)?(t\.me/|telegram\.me/|telegram\.dog/)(c/)?(\d+|[a-zA-Z_0-9]+)/(\d+)$")
        match = regex.match(message.text)
        if not match:
            return await message.reply('Invalid link')
        chat_id = match.group(4)
        last_msg_id = int(match.group(5))
        if chat_id.isnumeric():
            chat_id  = int(("-100" + chat_id))
    elif message.forward_from_chat.type == enums.ChatType.CHANNEL:
        last_msg_id = message.forward_from_message_id
        chat_id = message.forward_from_chat.username or message.forward_from_chat.id
    else:
        return
    try:
        await bot.get_chat(chat_id)
    except ChannelInvalid:
        return await message.reply('This may be a private channel / group. Make me an admin over there to index the files.')
    except (UsernameInvalid, UsernameNotModified):
        return await message.reply('Invalid Link specified.')
    except Exception as e:
        logger.exception(e)
        return await message.reply(f'Errors - {e}')
    try:
        k = await bot.get_messages(chat_id, last_msg_id)
    except:
        return await message.reply('Make Sure That Iam An Admin In The Channel, if channel is private')
    if k.empty:
        return await message.reply('This may be group and iam not a admin of the group.')

    if message.from_user.id in ADMINS:
        buttons = [[
         InlineKeyboardButton('𝚈𝙴𝚂', callback_data=f'index#accept#{chat_id}#{last_msg_id}#{message.from_user.id}'),
         InlineKeyboardButton('𝙲𝙻𝙾𝚂𝙴', callback_data='close_data')
         ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        return await message.reply(
            f'Do you Want To Index This Channel/ Group ?\n\nChat ID/ Username: <code>{chat_id}</code>\nLast Message ID: <code>{last_msg_id}</code>',
            reply_markup=reply_markup)

    if type(chat_id) is int:
        try:
            link = (await bot.create_chat_invite_link(chat_id)).invite_link
        except ChatAdminRequired:
            return await message.reply('Make sure iam an admin in the chat and have permission to invite users.')
    else:
        link = f"@{message.forward_from_chat.username}"
    buttons = [[
     InlineKeyboardButton('Accept Index', callback_data=f'index#accept#{chat_id}#{last_msg_id}#{message.from_user.id}')
     ],[
     InlineKeyboardButton('Reject Index', callback_data=f'index#reject#{chat_id}#{message.id}#{message.from_user.id}')
     ]]
    
    reply_markup = InlineKeyboardMarkup(buttons)
    await bot.send_message(LOG_CHANNEL,
                           f'#IndexRequest\n\nBy : {message.from_user.mention} (<code>{message.from_user.id}</code>)\nChat ID/ Username - <code> {chat_id}</code>\nLast Message ID - <code>{last_msg_id}</code>\nInviteLink - {link}',
                           reply_markup=reply_markup)
    await message.reply('ThankYou For the Contribution, Wait For My Moderators to verify the files.')


@Client.on_message(filters.command('setskip') & filters.user(ADMINS))
async def set_skip_number(bot, update):
    if ' ' in update.text:
        _, skip = update.text.split(" ")
        try:
            skip = int(skip)
        except:
            return await update.reply("Skip number should be an integer.")
        await update.reply(f"Successfully set SKIP number as {skip}")
        temp.CURRENT = int(skip)
    else:
        await update.reply("Give me a skip number")


async def index_files_to_db(lst_msg_id, chat, msg, bot):
    total_files = 0
    duplicate = 0
    errors = 0
    deleted = 0
    no_media = 0
    async with lock:
        try:
            total = lst_msg_id + 1
            current = temp.CURRENT
            temp.CANCEL = False
            while current < total:
                if temp.CANCEL:
                    await msg.edit("Succesfully Cancelled")
                    break
                try:
                    message = await bot.get_messages(chat_id=chat, message_ids=current, replies=0)
                except FloodWait as e:
                    await asyncio.sleep(e.x)
                    message = await bot.get_messages(chat, current, replies=0)
                except Exception as e:
                    logger.exception(e)
                try:
                    for file_type in ("document", "video", "audio"):
                        media = getattr(message, file_type, None)
                        if media is not None:
                            break
                        else:
                            continue
                    media.file_type = file_type
                    media.caption = message.caption
                    aynav, vnay = await save_file(media)
                    if aynav:
                        total_files += 1
                    elif vnay == 0:
                        duplicate += 1
                    elif vnay == 2:
                        errors += 1
                except Exception as e:
                    if "NoneType" in str(e):
                        if message.empty:
                            deleted += 1
                        elif not media:
                            no_media += 1
                        logger.warning("Skipping deleted / Non-Media messages (if this continues for long, use /setskip to set a skip number)")     
                    else:
                        logger.exception(e)
                current += 1
                if current % 20 == 0:
                    can = [[InlineKeyboardButton('𝙲𝙰𝙽𝙲𝙴𝙻', callback_data='index_cancel')]]
                    reply = InlineKeyboardMarkup(can)
                    await msg.edit_text(text=f"• 𝚃𝙾𝚃𝙰𝙻 𝙼𝙴𝚂𝚂𝙰𝙶𝙴𝚂 𝙵𝙴𝚃𝙲𝙷𝙴𝙳 : <code>{current}</code>\n• 𝚃𝙾𝚃𝙰𝙻 𝙼𝙴𝚂𝚂𝙰𝙶𝙴𝚂 𝚂𝙰𝚅𝙴𝙳 : <code>{total_files}</code>\n• 𝙳𝚄𝙿𝙻𝙸𝙲𝙰𝚃𝙴 𝙵𝙸𝙻𝙴𝚂 𝚂𝙺𝙸𝙿𝙴𝙳 : <code>{duplicate}</code>\n• 𝙳𝙴𝙻𝙴𝚃𝙴𝙳 𝙼𝙴𝚂𝚂𝙰𝙶𝙴𝚂 𝚂𝙺𝙸𝙿𝙿𝙴𝙳 : <code>{deleted}</code>\n 𝙽𝙾𝙽-𝙼𝙴𝙳𝙸𝙰 𝙼𝙴𝚂𝚂𝙰𝙶𝙴𝚂 𝚂𝙺𝙸𝙿𝙿𝙴𝙳 : <code>{no_media}</code>\n• 𝙴𝚁𝚁𝙾𝚁 𝙾𝙲𝙲𝚄𝚁𝙴𝙳 : <code>{errors}</code>", reply_markup=reply)
        except Exception as e:
            logger.exception(e)
            await msg.edit(f'Error: {e}')
        else:
            await msg.edit(f'• 𝚂𝚄𝙲𝙲𝙴𝚂𝙵𝚄𝙻𝙻𝚈 𝚂𝙰𝚅𝙴𝙳 <code>{total_files}</code> 𝚃𝙾 𝙳𝙰𝚃𝙰𝙱𝙰𝚂𝙴.!\n• 𝙳𝚄𝙿𝙻𝙸𝙲𝙰𝚃𝙴 𝙵𝙸𝙻𝙴𝚂 𝚂𝙺𝙸𝙿𝙿𝙴𝙳 : <code>{duplicate}</code>\n• 𝙳𝙴𝙻𝙴𝚃𝙴𝙳 𝙼𝙴𝚂𝚂𝙰𝙶𝙴𝚂 𝚂𝙺𝙸𝙿𝙿𝙴𝙳 : <code>{deleted}</code>\n• 𝙽𝙾𝙽-𝙼𝙴𝙳𝙸𝙰 𝙼𝙴𝚂𝚂𝙰𝙶𝙴𝚂 𝚂𝙺𝙸𝙿𝙿𝙴𝙳 : <code>{no_media}</code>\n• 𝙴𝚁𝚁𝙾𝚁𝚂 𝙾𝙲𝙲𝚄𝚁𝙴𝙳 : <code>{errors}</code>')
