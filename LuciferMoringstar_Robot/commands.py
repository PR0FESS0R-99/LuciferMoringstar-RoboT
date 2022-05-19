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

import random, asyncio
from pyrogram import Client as lucifermoringstar_robot , filters, enums
from LuciferMoringstar_Robot import temp, SUPPORT, PICS, ADMINS, CREATOR_USERNAME, CREATOR_NAME
from LuciferMoringstar_Robot.translation import START_MESSAGE, SETTINGS_MESSAGE, ADMIN_CMD_MESSAGE, ABOUT_MESSAGE
from LuciferMoringstar_Robot.functions import get_settings, save_group_settings
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.connections_mdb import active_connection
from database.chats_users_mdb import db

@lucifermoringstar_robot.on_message(filters.command(["start"]) & filters.private, group=1)
async def start(bot: lucifermoringstar_robot, update):

    if not await db.is_user_exist(update.from_user.id):
        await db.add_user(update.from_user.id)

    if len(update.command) ==2 and update.command[1] in ["subscribe"]:
        FORCES=["https://telegra.ph/file/b2acb2586995d0e107760.jpg"]
        invite_link = await bot.create_chat_invite_link(int(-1001538956907))
        button=[[
         InlineKeyboardButton("🔔 SUBSCRIBE 🔔", url=invite_link.invite_link)
         ]]
        reply_markup = InlineKeyboardMarkup(button)
        await update.reply_photo(
            photo=random.choice(FORCES),
            caption=f"""<i><b>Hello {update.from_user.mention}. \nYou Have <a href="{invite_link.invite_link}">Not Subscribed</a> To <a href="{invite_link.invite_link}">My Update Channel</a>.So you do not get the Files on Inline Mode, Bot Pm and Group</i></b>""",
            reply_markup=reply_markup
        )
        return
    if len(update.command) != 2:

        buttons = [[ InlineKeyboardButton("× 𝙰𝙳𝙳 𝙼𝙴 𝚃𝙾 𝚈𝙾𝚄𝚁 𝙶𝚁𝙾𝚄𝙿 ×", url=f"http://t.me/{temp.Bot_Username}?startgroup=true") ],
                  [ InlineKeyboardButton("𝚂𝚄𝙿𝙿𝙾𝚁𝚃 💬", url=f"t.me/{SUPPORT}"), InlineKeyboardButton("𝚄𝙿𝙳𝙰𝚃𝙴𝚂 📢", url="t.me/Mo_Tech_YT") ],
                  [ InlineKeyboardButton("ℹ️ 𝙷𝙴𝙻𝙿", callback_data="help"), InlineKeyboardButton("𝙰𝙱𝙾𝚄𝚃 🤠", callback_data="about") ]] 
        await bot.send_photo(photo=random.choice(PICS), chat_id=update.chat.id, caption=START_MESSAGE.format(mention=update.from_user.mention, name=temp.Bot_Name, username=temp.Bot_Username), reply_markup=InlineKeyboardMarkup(buttons))

@lucifermoringstar_robot.on_message(filters.command(["admin"]) & filters.private, group=2)
async def admin(bot: lucifermoringstar_robot, update):
    await bot.send_photo(photo=random.choice(PICS), chat_id=update.chat.id, caption=ADMIN_CMD_MESSAGE, reply_markup=InlineKeyboardMarkup( [[ InlineKeyboardButton("× 𝙲𝙻𝙾𝚂𝙴 ×", callback_data="close") ]] ))

@lucifermoringstar_robot.on_message(filters.command(["about"]) & filters.private, group=3)
async def about(bot: lucifermoringstar_robot, update):
    buttons = [[ InlineKeyboardButton("📦 𝚂𝙾𝚄𝚁𝙲𝙴 📦", url="https://github.com/PR0FESS0R-99/LuciferMoringstar-Robot")],
               [ InlineKeyboardButton("𝙷𝙾𝙼𝙴", callback_data="start"), InlineKeyboardButton("𝙼𝙴𝙽𝚄", callback_data="help"), InlineKeyboardButton("𝙲𝙻𝙾𝚂𝙴", callback_data="close") ]]                     
    await bot.send_photo(photo=random.choice(PICS), chat_id=update.chat.id, caption=ABOUT_MESSAGE.format(name = CREATOR_NAME, username = CREATOR_USERNAME, py3_version = temp.PY3_VERSION, pyro_version = temp.PYRO_VERSION, version = temp.BOT_VERSION, source = "https://github.com/PR0FESS0R-99/LuciferMoringstar-Robot"), reply_markup=InlineKeyboardMarkup(buttons))


@lucifermoringstar_robot.on_message((filters.private | filters.group) & filters.command('settings'))
async def settings(client, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f" 𝚈𝙾𝚄𝚁 𝙰𝚁𝙴 𝙰𝙽𝙾𝙽𝚈𝙼𝙾𝚄𝚂 𝙰𝙳𝙼𝙸𝙽. /connect {message.chat.id} 𝙸𝙽 𝙿𝙼")
    chat_type = message.chat.type
    if chat_type == enums.ChatType.PRIVATE:
        grpid = await active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await message.reply_text("𝙼𝙰𝙺𝙴 𝚂𝚄𝚁𝙴 𝙸𝙰𝙼 𝙿𝚁𝙴𝚂𝙴𝙽𝚃 𝙸𝙽 𝚈𝙾𝚄𝚁 𝙶𝚁𝙾𝚄𝙿..!", quote=True)
                return
        else:
            await message.reply_text("𝙸𝙰𝙼 𝙽𝙾𝚃 𝙲𝙾𝙽𝙽𝙴𝙲𝚃𝙴𝙳 𝙰𝙽𝚃 𝙶𝚁𝙾𝚄𝙿..!", quote=True)
            return

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grp_id = message.chat.id
        title = message.chat.title

    else:
        return

    member = await client.get_chat_member(grp_id, userid)
    if (
            member.status != enums.ChatMemberStatus.ADMINISTRATOR
            and member.status != enums.ChatMemberStatus.OWNER
            and userid not in ADMINS
    ):
        return

    settings = await get_settings(grp_id)

    if settings is not None:
        buttons = [[
         InlineKeyboardButton('𝙵𝙸𝙻𝚃𝙴𝚁 𝙱𝚄𝚃𝚃𝙾𝙽', callback_data=f'settings#button#{settings["button"]}#{grp_id}'),        
         InlineKeyboardButton('𝚂𝙸𝙽𝙶𝙻𝙴' if settings["button"] else '𝙳𝙾𝚄𝙱𝙻𝙴', callback_data=f'settings#button#{settings["button"]}#{grp_id}')
         ],[
         InlineKeyboardButton('𝚆𝙴𝙻𝙲𝙾𝙼𝙴 𝙼𝚂𝙶', callback_data=f'settings#welcome#{settings["welcome"]}#{grp_id}'),
         InlineKeyboardButton('𝙾𝙽' if settings["welcome"] else '𝙾𝙵𝙵', callback_data=f'settings#welcome#{settings["welcome"]}#{grp_id}')           
         ],[  
         InlineKeyboardButton('𝚂𝙿𝙴𝙻𝙻 𝙲𝙷𝙴𝙲𝙺', callback_data=f'settings#spellmode#{settings["spellmode"]}#{grp_id}'),
         InlineKeyboardButton('𝙾𝙽' if settings["spellmode"] else '𝙾𝙵𝙵', callback_data=f'settings#spellmode#{settings["spellmode"]}#{grp_id}')           
         ],[
         InlineKeyboardButton('𝙱𝙾𝚃 𝙿𝙾𝚂𝚃𝙴𝚁', callback_data=f'settings#photo#{settings["photo"]}#{grp_id}'),
         InlineKeyboardButton('𝙾𝙽' if settings["photo"] else '𝙾𝙵𝙵', callback_data=f'settings#photo#{settings["photo"]}#{grp_id}')           
         ]]

        reply_markup = InlineKeyboardMarkup(buttons)

        await message.reply_text(
            text=SETTINGS_MESSAGE.format(title=title),
            reply_markup=reply_markup,
            disable_web_page_preview=True,
            reply_to_message_id=message.id
        )


@lucifermoringstar_robot.on_message((filters.private | filters.group) & filters.command('set_temp'))
async def save_template(client, message):
    sts = await message.reply("⏳️")
    await asyncio.sleep(0.3)
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f" 𝚈𝙾𝚄𝚁 𝙰𝚁𝙴 𝙰𝙽𝙾𝙽𝚈𝙼𝙾𝚄𝚂 𝙰𝙳𝙼𝙸𝙽. /connect {message.chat.id} 𝙸𝙽 𝙿𝙼")
    chat_type = message.chat.type
    if chat_type == enums.ChatType.PRIVATE:
        grpid = await active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await message.reply_text("𝙼𝙰𝙺𝙴 𝚂𝚄𝚁𝙴 𝙸𝙰𝙼 𝙿𝚁𝙴𝚂𝙴𝙽𝚃 𝙸𝙽 𝚈𝙾𝚄𝚁 𝙶𝚁𝙾𝚄𝙿..!", quote=True)
                return
        else:
            await message.reply_text("𝙸𝙰𝙼 𝙽𝙾𝚃 𝙲𝙾𝙽𝙽𝙴𝙲𝚃𝙴𝙳 𝙰𝙽𝚃 𝙶𝚁𝙾𝚄𝙿..!", quote=True)
            return

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grp_id = message.chat.id
        title = message.chat.title

    else:
        return

    member = await client.get_chat_member(grp_id, userid)
    if (
            member.status != enums.ChatMemberStatus.ADMINISTRATOR
            and member.status != enums.ChatMemberStatus.OWNER
            and userid not in ADMINS
    ):
        return

    if len(message.command) < 2:
        return await sts.edit("𝙷𝙾𝚆 𝚃𝙾 𝚄𝚂𝙴 𝚃𝙷𝙸𝚂 𝙲𝙾𝙼𝙼𝙰𝙽𝙳..!", reply_markup=InlineKeyboardMarkup( [[ InlineKeyboardButton("𝙲𝙻𝙸𝙲𝙺 𝙷𝙴𝚁𝙴", callback_data="autofilter") ]] ))

    pr0fess0r_99 = message.text.split(" ", 1)[1]
    await save_group_settings(grp_id, 'template', pr0fess0r_99)
    await sts.edit(f"""𝚂𝚄𝙲𝙲𝙴𝚂𝚂𝙵𝚄𝙻𝙻𝚈 𝙲𝙷𝙰𝙽𝙶𝙴𝙳 𝚃𝙴𝙼𝙿𝙻𝙰𝚃𝙴 (𝙰𝚄𝚃𝙾𝙵𝙸𝙻𝚃𝙴𝚁 𝚃𝙴𝙼𝙿) 𝙵𝙾𝚁 {title} 𝚃𝙾\n\n{pr0fess0r_99}""", reply_markup=InlineKeyboardMarkup( [[ InlineKeyboardButton("× 𝙲𝙻𝙾𝚂𝙴 ×", callback_data="close") ]] ))

@lucifermoringstar_robot.on_message((filters.private | filters.group) & filters.command('setwelcome'))
async def setwelcome(client, message):
    sts = await message.reply("⏳️")
    await asyncio.sleep(0.3)
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f" 𝚈𝙾𝚄𝚁 𝙰𝚁𝙴 𝙰𝙽𝙾𝙽𝚈𝙼𝙾𝚄𝚂 𝙰𝙳𝙼𝙸𝙽. /connect {message.chat.id} 𝙸𝙽 𝙿𝙼")
    chat_type = message.chat.type
    if chat_type == enums.ChatType.PRIVATE:
        grpid = await active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await message.reply_text("𝙼𝙰𝙺𝙴 𝚂𝚄𝚁𝙴 𝙸𝙰𝙼 𝙿𝚁𝙴𝚂𝙴𝙽𝚃 𝙸𝙽 𝚈𝙾𝚄𝚁 𝙶𝚁𝙾𝚄𝙿..!", quote=True)
                return
        else:
            await message.reply_text("𝙸𝙰𝙼 𝙽𝙾𝚃 𝙲𝙾𝙽𝙽𝙴𝙲𝚃𝙴𝙳 𝙰𝙽𝚃 𝙶𝚁𝙾𝚄𝙿..!", quote=True)
            return

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grp_id = message.chat.id
        title = message.chat.title

    else:
        return

    member = await client.get_chat_member(grp_id, userid)
    if (
            member.status != enums.ChatMemberStatus.ADMINISTRATOR
            and member.status != enums.ChatMemberStatus.OWNER
            and userid not in ADMINS
    ):
        return

    if len(message.command) < 2:
        return await sts.edit("𝙷𝙾𝚆 𝚃𝙾 𝚄𝚂𝙴 𝚃𝙷𝙸𝚂 𝙲𝙾𝙼𝙼𝙰𝙽𝙳..!", reply_markup=InlineKeyboardMarkup( [[ InlineKeyboardButton("𝙲𝙻𝙸𝙲𝙺 𝙷𝙴𝚁𝙴", callback_data="spellcheck") ]] ))

    pr0fess0r_99 = message.text.split(" ", 1)[1]
    await save_group_settings(grp_id, 'welcometext', pr0fess0r_99)
    await sts.edit(f"""𝚂𝚄𝙲𝙲𝙴𝚂𝚂𝙵𝚄𝙻𝙻𝚈 𝙲𝙷𝙰𝙽𝙶𝙴𝙳 𝚆𝙴𝙻𝙲𝙾𝙼𝙴 𝙼𝙴𝚂𝚂𝙰𝙶𝙴 𝙵𝙾𝚁 {title} 𝚃𝙾\n\n{pr0fess0r_99}""", reply_markup=InlineKeyboardMarkup( [[ InlineKeyboardButton("× 𝙲𝙻𝙾𝚂𝙴 ×", callback_data="close") ]] ))


@lucifermoringstar_robot.on_message((filters.private | filters.group) & filters.command('setspell'))
async def setspell(client, message):
    sts = await message.reply("⏳️")
    await asyncio.sleep(0.3)
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f" 𝚈𝙾𝚄𝚁 𝙰𝚁𝙴 𝙰𝙽𝙾𝙽𝚈𝙼𝙾𝚄𝚂 𝙰𝙳𝙼𝙸𝙽. /connect {message.chat.id} 𝙸𝙽 𝙿𝙼")
    chat_type = message.chat.type
    if chat_type == enums.ChatType.PRIVATE:
        grpid = await active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await message.reply_text("𝙼𝙰𝙺𝙴 𝚂𝚄𝚁𝙴 𝙸𝙰𝙼 𝙿𝚁𝙴𝚂𝙴𝙽𝚃 𝙸𝙽 𝚈𝙾𝚄𝚁 𝙶𝚁𝙾𝚄𝙿..!", quote=True)
                return
        else:
            await message.reply_text("𝙸𝙰𝙼 𝙽𝙾𝚃 𝙲𝙾𝙽𝙽𝙴𝙲𝚃𝙴𝙳 𝙰𝙽𝚃 𝙶𝚁𝙾𝚄𝙿..!", quote=True)
            return

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grp_id = message.chat.id
        title = message.chat.title

    else:
        return

    member = await client.get_chat_member(grp_id, userid)
    if (
            member.status != enums.ChatMemberStatus.ADMINISTRATOR
            and member.status != enums.ChatMemberStatus.OWNER
            and userid not in ADMINS
    ):
        return

    if len(message.command) < 2:
        return await sts.edit("𝙷𝙾𝚆 𝚃𝙾 𝚄𝚂𝙴 𝚃𝙷𝙸𝚂 𝙲𝙾𝙼𝙼𝙰𝙽𝙳..!", reply_markup=InlineKeyboardMarkup( [[ InlineKeyboardButton("𝙲𝙻𝙸𝙲𝙺 𝙷𝙴𝚁𝙴", callback_data="welcome") ]] ))

    pr0fess0r_99 = message.text.split(" ", 1)[1]
    await save_group_settings(grp_id, 'spelltext', pr0fess0r_99)
    await sts.edit(f"""𝚂𝚄𝙲𝙲𝙴𝚂𝚂𝙵𝚄𝙻𝙻𝚈 𝙲𝙷𝙰𝙽𝙶𝙴𝙳 𝚂𝙴𝚃 𝚂𝙿𝙴𝙻𝙻 𝙲𝙷𝙴𝙲𝙺 𝙵𝙾𝚁 {title} 𝚃𝙾\n\n{pr0fess0r_99}""", reply_markup=InlineKeyboardMarkup( [[ InlineKeyboardButton("× 𝙲𝙻𝙾𝚂𝙴 ×", callback_data="close") ]] ))

@lucifermoringstar_robot.on_message((filters.private | filters.group) & filters.command('setcaption'))
async def filecap(client, message):
    sts = await message.reply("⏳️")
    await asyncio.sleep(0.3)
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f" 𝚈𝙾𝚄𝚁 𝙰𝚁𝙴 𝙰𝙽𝙾𝙽𝚈𝙼𝙾𝚄𝚂 𝙰𝙳𝙼𝙸𝙽. /connect {message.chat.id} 𝙸𝙽 𝙿𝙼")
    chat_type = message.chat.type
    if chat_type == enums.ChatType.PRIVATE:
        grpid = await active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await message.reply_text("𝙼𝙰𝙺𝙴 𝚂𝚄𝚁𝙴 𝙸𝙰𝙼 𝙿𝚁𝙴𝚂𝙴𝙽𝚃 𝙸𝙽 𝚈𝙾𝚄𝚁 𝙶𝚁𝙾𝚄𝙿..!", quote=True)
                return
        else:
            await message.reply_text("𝙸𝙰𝙼 𝙽𝙾𝚃 𝙲𝙾𝙽𝙽𝙴𝙲𝚃𝙴𝙳 𝙰𝙽𝚃 𝙶𝚁𝙾𝚄𝙿..!", quote=True)
            return

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grp_id = message.chat.id
        title = message.chat.title

    else:
        return

    member = await client.get_chat_member(grp_id, userid)
    if (
            member.status != enums.ChatMemberStatus.ADMINISTRATOR
            and member.status != enums.ChatMemberStatus.OWNER
            and userid not in ADMINS
    ):
        return

    if len(message.command) < 2:
        return await sts.edit("𝙷𝙾𝚆 𝚃𝙾 𝚄𝚂𝙴 𝚃𝙷𝙸𝚂 𝙲𝙾𝙼𝙼𝙰𝙽𝙳..!", reply_markup=InlineKeyboardMarkup( [[ InlineKeyboardButton("𝙲𝙻𝙸𝙲𝙺 𝙷𝙴𝚁𝙴", callback_data="filecaption") ]] ))

    pr0fess0r_99 = message.text.split(" ", 1)[1]
    await save_group_settings(grp_id, 'caption', pr0fess0r_99)
    await sts.edit(f"""𝚂𝚄𝙲𝙲𝙴𝚂𝚂𝙵𝚄𝙻𝙻𝚈 𝙲𝙷𝙰𝙽𝙶𝙴𝙳 𝙵𝙸𝙻𝙴 𝙲𝙰𝙿𝚃𝙸𝙾𝙽 𝙵𝙾𝚁 {title} 𝚃𝙾\n\n{pr0fess0r_99}""", reply_markup=InlineKeyboardMarkup( [[ InlineKeyboardButton("× 𝙲𝙻𝙾𝚂𝙴 ×", callback_data="close") ]] ))
