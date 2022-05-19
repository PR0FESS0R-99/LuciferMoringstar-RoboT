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

import asyncio 
from pyrogram import Client as lucifermoringstar_robot, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserIsBlocked, PeerIdInvalid, UserNotParticipant, MessageNotModified
from LuciferMoringstar_Robot import temp, PROTECT_FILES, FILES_NOTIFICATION, CUSTOM_FILE_CAPTION, AUTH_CHANNEL, SUPPORT, CREATOR_NAME, CREATOR_USERNAME
from LuciferMoringstar_Robot.functions import get_size, BUTTONS, get_settings, save_group_settings, is_subscribed
from LuciferMoringstar_Robot.modules import autofilter_text, connection_text, spellcheck_text, welcome_text, misc_text 
from LuciferMoringstar_Robot.translation import START_MESSAGE, HELP_MESSAGE, ABOUT_MESSAGE
from database.connections_mdb import active_connection, all_connections, delete_connection, if_active, make_active, make_inactive
from database.autofilter_mdb import get_file_details, Media
from database.chats_users_mdb import db

@lucifermoringstar_robot.on_callback_query()
async def cb_handler(client: lucifermoringstar_robot, query):
    clicked = query.from_user.id
    try:
        typed = query.message.reply_to_message.from_user.id
    except:
        typed = query.from_user.id

    if (clicked == typed):

        if query.data.startswith("nextgroup"):
            ident, index, keyword = query.data.split("_")
            try:
                data = BUTTONS[keyword]
            except KeyError:
                await query.answer("𝚃𝙷𝙸𝚂 𝙼𝚈 𝙾𝙻𝙳 𝙼𝙴𝚂𝚂𝙰𝙶𝙴 𝚂𝙾 𝙿𝙻𝙴𝙰𝚂𝙴 𝚁𝙴𝚀𝚄𝙴𝚂𝚃 𝙰𝙶𝙰𝙸𝙽 🙏",show_alert=True)
                return

            if int(index) == int(data["total"]) - 2:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("🔙", callback_data=f"backgroup_{int(index)+1}_{keyword}"),
                     InlineKeyboardButton(f"📃 {int(index)+2}/{data['total']}", callback_data="pages"),
                     InlineKeyboardButton("🗑️", callback_data="close")]
                )
            else:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("🔙", callback_data=f"backgroup_{int(index)+1}_{keyword}"),
                     InlineKeyboardButton(f"📃 {int(index)+2}/{data['total']}", callback_data="pages"),
                     InlineKeyboardButton("🗑️", callback_data="close"),
                     InlineKeyboardButton("➡", callback_data=f"nextgroup_{int(index)+1}_{keyword}")]
                )

            buttons.append(
                [InlineKeyboardButton(text="🤖 CHECK MY PM 🤖", url=f"https://telegram.dog/{temp.Bot_Username}")]
            )

            await query.edit_message_reply_markup( 
                reply_markup=InlineKeyboardMarkup(buttons)
            )
            return
        elif query.data.startswith("backgroup"):
            ident, index, keyword = query.data.split("_")
            try:
                data = BUTTONS[keyword]
            except KeyError:
                await query.answer("𝚃𝙷𝙸𝚂 𝙼𝚈 𝙾𝙻𝙳 𝙼𝙴𝚂𝚂𝙰𝙶𝙴 𝚂𝙾 𝙿𝙻𝙴𝙰𝚂𝙴 𝚁𝙴𝚀𝚄𝙴𝚂𝚃 𝙰𝙶𝙰𝙸𝙽 🙏",show_alert=True)
                return

            if int(index) == 1:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton(f"📃 {int(index)}/{data['total']}", callback_data="pages"),
                     InlineKeyboardButton("🗑️", callback_data="close"),
                     InlineKeyboardButton("➡", callback_data=f"nextgroup_{int(index)-1}_{keyword}")]
                )
            else:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton("🔙", callback_data=f"backgroup_{int(index)-1}_{keyword}"),
                     InlineKeyboardButton(f"📃 {int(index)}/{data['total']}", callback_data="pages"),
                     InlineKeyboardButton("🗑️", callback_data="close"),
                     InlineKeyboardButton("➡", callback_data=f"nextgroup_{int(index)-1}_{keyword}")]
                )
            buttons.append(
                [InlineKeyboardButton(text="🤖 CHECK MY PM 🤖", url=f"https://telegram.dog/{temp.Bot_Username}")]
            )

            await query.edit_message_reply_markup( 
                reply_markup=InlineKeyboardMarkup(buttons)
            )
            return
        elif query.data.startswith("nextbot"):
            ident, index, keyword = query.data.split("_")
            try:
                data = BUTTONS[keyword]
            except KeyError:
                await query.answer("𝚃𝙷𝙸𝚂 𝙼𝚈 𝙾𝙻𝙳 𝙼𝙴𝚂𝚂𝙰𝙶𝙴 𝚂𝙾 𝙿𝙻𝙴𝙰𝚂𝙴 𝚁𝙴𝚀𝚄𝙴𝚂𝚃 𝙰𝙶𝙰𝙸𝙽 🙏",show_alert=True)
                return

            if int(index) == int(data["total"]) - 2:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("🔙", callback_data=f"backbot_{int(index)+1}_{keyword}"),
                     InlineKeyboardButton(f"📃 {int(index)+2}/{data['total']}", callback_data="pages"),
                     InlineKeyboardButton("🗑️", callback_data="close")]
                )

            else:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("🔙", callback_data=f"backbot_{int(index)+1}_{keyword}"),
                     InlineKeyboardButton(f"📃 {int(index)+2}/{data['total']}", callback_data="pages"),
                     InlineKeyboardButton("🗑️", callback_data="close"),
                     InlineKeyboardButton("➡", callback_data=f"nextbot_{int(index)+1}_{keyword}")]
                )

            await query.edit_message_reply_markup( 
                reply_markup=InlineKeyboardMarkup(buttons)
            )
            return
        elif query.data.startswith("backbot"):
            ident, index, keyword = query.data.split("_")
            try:
                data = BUTTONS[keyword]
            except KeyError:
                await query.answer("𝚃𝙷𝙸𝚂 𝙼𝚈 𝙾𝙻𝙳 𝙼𝙴𝚂𝚂𝙰𝙶𝙴 𝚂𝙾 𝙿𝙻𝙴𝙰𝚂𝙴 𝚁𝙴𝚀𝚄𝙴𝚂𝚃 𝙰𝙶𝙰𝙸𝙽 🙏",show_alert=True)
                return

            if int(index) == 1:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton(f"📃 {int(index)}/{data['total']}", callback_data="pages"),
                     InlineKeyboardButton("🗑️", callback_data="close"),
                     InlineKeyboardButton("➡", callback_data=f"nextbot_{int(index)-1}_{keyword}")]
                )

            else:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton("🔙", callback_data=f"backbot_{int(index)-1}_{keyword}"),
                     InlineKeyboardButton(f"📃 {int(index)}/{data['total']}", callback_data="pages"),
                     InlineKeyboardButton("🗑️", callback_data="close"),
                     InlineKeyboardButton("➡", callback_data=f"nextbot_{int(index)-1}_{keyword}")]
                )
            await query.edit_message_reply_markup( 
                reply_markup=InlineKeyboardMarkup(buttons)
            )
            return
        elif query.data.startswith("settings"):
            ident, set_type, status, grp_id = query.data.split("#")
            grpid = await active_connection(str(query.from_user.id))

            if str(grp_id) != str(grpid):
                await query.message.edit("𝙸𝙰𝙼 𝙽𝙾𝚃 𝙲𝙾𝙽𝙽𝙴𝙲𝚃𝙴𝙳 𝙰𝙽𝚃 𝙶𝚁𝙾𝚄𝙿..!\n   𝚄𝚂𝙴 𝚃𝙷𝙸𝚂 𝙲𝙾𝙼𝙼𝙰𝙽𝙳 /connect 𝙰𝙽𝙳 𝙲𝙾𝙽𝙽𝙴𝙲𝚃 𝚈𝙾𝚄𝚁 𝙲𝙷𝙰𝚃")

            if status == "True":
                await save_group_settings(grpid, set_type, False)
            else:
                await save_group_settings(grpid, set_type, True)

            settings = await get_settings(grpid)

            if settings is not None:

                buttons = [[
                 InlineKeyboardButton('𝙵𝙸𝙻𝚃𝙴𝚁 𝙱𝚄𝚃𝚃𝙾𝙽', callback_data=f'settings#button#{settings["button"]}#{str(grp_id)}'),        
                 InlineKeyboardButton('𝚂𝙸𝙽𝙶𝙻𝙴' if settings["button"] else '𝙳𝙾𝚄𝙱𝙻𝙴', callback_data=f'settings#button#{settings["button"]}#{str(grp_id)}')
                 ],[
                 InlineKeyboardButton('𝚆𝙴𝙻𝙲𝙾𝙼𝙴 𝙼𝚂𝙶', callback_data=f'settings#welcome#{settings["welcome"]}#{str(grp_id)}'),
                 InlineKeyboardButton('𝙾𝙽' if settings["welcome"] else '𝙾𝙵𝙵', callback_data=f'settings#welcome#{settings["welcome"]}#{str(grp_id)}')           
                 ],[  
                 InlineKeyboardButton('𝚂𝙿𝙴𝙻𝙻 𝙲𝙷𝙴𝙲𝙺', callback_data=f'settings#spellmode#{settings["spellmode"]}#{str(grp_id)}'),
                 InlineKeyboardButton('𝙾𝙽' if settings["spellmode"] else '𝙾𝙵𝙵', callback_data=f'settings#spellmode#{settings["spellmode"]}#{str(grp_id)}')           
                 ],[
                 InlineKeyboardButton('𝙱𝙾𝚃 𝙿𝙾𝚂𝚃𝙴𝚁', callback_data=f'settings#photo#{settings["photo"]}#{str(grp_id)}'),
                 InlineKeyboardButton('𝙾𝙽' if settings["photo"] else '𝙾𝙵𝙵', callback_data=f'settings#photo#{settings["photo"]}#{str(grp_id)}')           
                 ]]

                reply_markup = InlineKeyboardMarkup(buttons)
                await query.message.edit_reply_markup(reply_markup)

        elif query.data.startswith("luciferGP"):

            if not await db.is_user_exist(query.from_user.id):
                await query.answer(url=f"https://t.me/{temp.Bot_Username}?start=subscribe")
                return
            if AUTH_CHANNEL and not await is_subscribed(client, query):
                await query.answer(url=f"https://t.me/{temp.Bot_Username}?start=subscribe")
                return

            ident, file_id = query.data.split("#")
            files_ = await get_file_details(file_id)
            settings = await get_settings(query.message.chat.id)
            if not files_:
                return await query.answer('𝙵𝙸𝙻𝙴 𝙽𝙾𝚃 𝙵𝙾𝚄𝙽𝙳...!')
            files = files_[0]
            title = files.file_name
            size = get_size(files.file_size)
            FILE_CAPTION = settings["caption"]
            caption = FILE_CAPTION.format(mention=query.from_user.mention, title=title, size=size, caption=files.caption)
            buttons = [[ InlineKeyboardButton("⚜️ 𝚂𝙷𝙰𝚁𝙴 𝙼𝙴 𝚆𝙸𝚃𝙷 𝚈𝙾𝚄𝚁 𝙵𝚁𝙸𝙴𝙽𝙳𝚂 ⚜️", url=f"https://t.me/share/url?url=Best%20AutoFilter%20Bot%20%0A%40LuciferMoringstar_Robot%0A@{temp.Bot_Username}") ]]

            await client.send_cached_media(
                chat_id=query.from_user.id,
                file_id=file_id,
                caption=caption,
                reply_markup=InlineKeyboardMarkup(buttons)
            )
            await query.answer('''𝙲𝙷𝙴𝙲𝙺 𝙿𝙼, 𝙸 𝙷𝙰𝚅𝙴 𝚂𝙴𝙽𝚃 𝙵𝙸𝙻𝙴𝚂 𝙸𝙽 𝙿𝙼\n   𝙲𝙻𝙸𝙲𝙺 𝙲𝙷𝙴𝙲𝙺 𝙿𝙼 𝙱𝚄𝚃𝚃𝙾𝙽''', show_alert=True)   

        elif query.data.startswith("luciferPM"):

            if not await db.is_user_exist(query.from_user.id):
                await query.answer(url=f"https://t.me/{temp.Bot_Username}?start=subscribe")
                return
            if AUTH_CHANNEL and not await is_subscribed(client, query):
                await query.answer(url=f"https://t.me/{temp.Bot_Username}?start=subscribe")
                return

            ident, file_id = query.data.split("#")
            files_ = await get_file_details(file_id)
            if not files_:
                return await query.answer('𝙵𝙸𝙻𝙴 𝙽𝙾𝚃 𝙵𝙾𝚄𝙽𝙳...!')
            files = files_[0]
            title = files.file_name
            size = get_size(files.file_size)
            caption = CUSTOM_FILE_CAPTION.format(mention=query.from_user.mention, title=title, size=size, caption=files.caption)
            buttons = [[ InlineKeyboardButton("⚜️ 𝚂𝙷𝙰𝚁𝙴 𝙼𝙴 𝚆𝙸𝚃𝙷 𝚈𝙾𝚄𝚁 𝙵𝚁𝙸𝙴𝙽𝙳𝚂 ⚜️", url=f"https://t.me/share/url?url=Best%20AutoFilter%20Bot%20%0A%40LuciferMoringstar_Robot%0A@{temp.Bot_Username}") ]]

            await client.send_cached_media(
                chat_id=query.from_user.id,
                file_id=file_id,
                caption=caption,
                reply_markup=InlineKeyboardMarkup(buttons)
            )


        elif query.data == "start":
            buttons = [[ InlineKeyboardButton("× 𝙰𝙳𝙳 𝙼𝙴 𝚃𝙾 𝚈𝙾𝚄𝚁 𝙶𝚁𝙾𝚄𝙿 ×", url=f"http://t.me/{temp.Bot_Username}?startgroup=true") ],
                      [ InlineKeyboardButton("𝚂𝚄𝙿𝙿𝙾𝚁𝚃 💬", url=f"t.me/{SUPPORT}"), InlineKeyboardButton("𝚄𝙿𝙳𝙰𝚃𝙴𝚂 📢", url="t.me/Mo_Tech_YT") ],
                      [ InlineKeyboardButton("ℹ️ 𝙷𝙴𝙻𝙿", callback_data="help"), InlineKeyboardButton("𝙰𝙱𝙾𝚄𝚃 🤠", callback_data="about") ]] 
            await query.message.edit(START_MESSAGE.format(mention=query.from_user.mention, name=temp.Bot_Name, username=temp.Bot_Username), reply_markup=InlineKeyboardMarkup(buttons))

        elif query.data == "help":
            buttons = [[ InlineKeyboardButton("𝙰𝚄𝚃𝙾𝙵𝙸𝙻𝚃𝙴𝚁𝚂", callback_data="autofilter"), InlineKeyboardButton("𝙲𝙾𝙽𝙽𝙴𝙲𝚃𝙸𝙾𝙽𝚂", callback_data="connection"), InlineKeyboardButton("𝙲𝙰𝙿𝚃𝙸𝙾𝙽", callback_data="filecaption")  ],
                      [ InlineKeyboardButton("𝚆𝙴𝙻𝙲𝙾𝙼𝙴", callback_data="welcome"), InlineKeyboardButton("𝚂𝙿𝙴𝙻𝙻𝙲𝙷𝙴𝙲𝙺", callback_data="spellcheck"), InlineKeyboardButton("𝙼𝙸𝚂𝙲", callback_data="misc") ],
                      [ InlineKeyboardButton("𝚂𝚃𝙰𝚃𝚄𝚂", callback_data="status"), InlineKeyboardButton("𝙷𝙾𝙼𝙴", callback_data="start") ]]                     
            await query.message.edit(HELP_MESSAGE.format(mention=query.from_user.mention, name=temp.Bot_Name, username=temp.Bot_Username), reply_markup=InlineKeyboardMarkup(buttons))

        elif query.data == "about":
            buttons = [[ InlineKeyboardButton("📦 𝚂𝙾𝚄𝚁𝙲𝙴 📦", url="https://github.com/PR0FESS0R-99/LuciferMoringstar-Robot")],
                      [ InlineKeyboardButton("𝙷𝙾𝙼𝙴", callback_data="start"), InlineKeyboardButton("𝙼𝙴𝙽𝚄", callback_data="help"), InlineKeyboardButton("𝙲𝙻𝙾𝚂𝙴", callback_data="close") ]]                     
            await query.message.edit(ABOUT_MESSAGE.format(name = CREATOR_NAME, username = CREATOR_USERNAME, py3_version = temp.PY3_VERSION, pyro_version = temp.PYRO_VERSION, version = temp.BOT_VERSION, source = "https://github.com/PR0FESS0R-99/LuciferMoringstar-Robot"), reply_markup=InlineKeyboardMarkup(buttons))

        elif query.data == "status":
            files = await Media.count_documents()
            users = await db.total_users_count()
            chats = await db.total_chat_count()
            buttons = [[ InlineKeyboardButton("⇇ 𝙱𝙰𝙲𝙺", callback_data="help"), InlineKeyboardButton("𝚁𝙴𝙵𝚁𝙴𝚂𝙷", callback_data="status"), InlineKeyboardButton("𝙲𝙻𝙾𝚂𝙴 ×", callback_data="close") ]]                     
            try:
                await query.message.edit(STATUS_MESSAGE.format(bot_name=temp.Bot_Name, users=users, files=files, chats=chats), reply_markup=InlineKeyboardMarkup(buttons))
            except MessageNotModified:
                pass

        elif query.data == "files_delete":
            await Media.collection.drop()
            await query.message.edit('𝚂𝚄𝙲𝙲𝙴𝚂𝙵𝚄𝙻𝙻𝚈 𝙳𝙴𝙻𝙴𝚃𝙴𝙳 𝙰𝙻𝙻 𝚃𝙷𝙴 𝙸𝙽𝙳𝙴𝚇𝙴𝙳 𝙵𝙸𝙻𝙴𝚂..')

        elif query.data == "autofilter":
            await query.message.edit(autofilter_text, reply_markup=InlineKeyboardMarkup( [[ InlineKeyboardButton("⇇ 𝙱𝙰𝙲𝙺 ⇇", callback_data="help") ]] ))

        elif query.data == "connection":
            await query.message.edit(connection_text, reply_markup=InlineKeyboardMarkup( [[ InlineKeyboardButton("⇇ 𝙱𝙰𝙲𝙺 ⇇", callback_data="help") ]] ))

        elif query.data == "spellcheck":
            await query.message.edit(spellcheck_text, reply_markup=InlineKeyboardMarkup( [[ InlineKeyboardButton("⇇ 𝙱𝙰𝙲𝙺 ⇇", callback_data="help") ]] ))

        elif query.data == "welcome":
            await query.message.edit(welcome_text, reply_markup=InlineKeyboardMarkup( [[ InlineKeyboardButton("⇇ 𝙱𝙰𝙲𝙺 ⇇", callback_data="help") ]] ))

        elif query.data == "misc":
            await query.message.edit(misc_text, reply_markup=InlineKeyboardMarkup( [[ InlineKeyboardButton("⇇ 𝙱𝙰𝙲𝙺 ⇇", callback_data="help") ]] ))

        elif query.data == "filecaption":
            await query.message.edit(filecaption_text, reply_markup=InlineKeyboardMarkup( [[ InlineKeyboardButton("⇇ 𝙱𝙰𝙲𝙺 ⇇", callback_data="help") ]] ))

        elif query.data == "close":
            await query.message.delete()

        elif query.data == "backcb":
            await query.answer()
            userid = query.from_user.id
            groupids = await all_connections(str(userid))
            if groupids is None:
                await query.message.edit("𝚃𝙷𝙴𝚁𝙴 𝙰𝚁𝙴 𝙽𝙾 𝙰𝙲𝚃𝙸𝚅𝙴 𝙲𝙾𝙽𝙽𝙴𝙲𝚃𝙸𝙾𝙽𝚂..! 𝙲𝙾𝙽𝙽𝙴𝙲𝚃 𝚃𝙾 𝚂𝙰𝙼𝙴 𝙶𝚁𝙾𝚄𝙿𝚂 𝙵𝙸𝚁𝚂𝚃")
            return await query.answer('Piracy Is Crime')
        elif "deletecb" in query.data:
            await query.answer()
            user_id = query.from_user.id
            group_id = query.data.split(":")[1]
            delcon = await delete_connection(str(user_id), str(group_id))
            if delcon:
                await query.message.edit("𝚂𝚄𝙲𝙲𝙴𝚂𝚂𝙵𝚄𝙻𝙻𝚈 𝙳𝙴𝙻𝙴𝚃𝙴𝙳 𝙲𝙾𝙽𝙽𝙴𝙲𝚃𝙸𝙾𝙽")
            else:
                await query.message.edit("𝚂𝙾𝙼𝙴 𝙴𝚁𝚁𝙾𝚁 𝙾𝙲𝙲𝚄𝚁𝚁𝙴𝙳..!")
            return await query.answer('Piracy Is Crime')

        elif "disconnect" in query.data:
            await query.answer()
            group_id = query.data.split(":")[1]

            hr = await client.get_chat(int(group_id))
            title = hr.title
            user_id = query.from_user.id

            mkinact = await make_inactive(str(user_id))

            if mkinact:
                await query.message.edit(f"𝙳𝙸𝚂𝙲𝙾𝙽𝙽𝙴𝙲𝚃𝙴𝙳 𝙵𝚁𝙾𝙼 **{title}**")

            else:
                await query.message.edit(" 𝚂𝙾𝙼𝙴 𝙴𝚁𝚁𝙾𝚁 𝙾𝙲𝙲𝚄𝚁𝚁𝙴𝙳..!")

        elif "connectcb" in query.data:
            await query.answer()
            group_id = query.data.split(":")[1]
            hr = await client.get_chat(int(group_id))
            title = hr.title
            user_id = query.from_user.id
            mkact = await make_active(str(user_id), str(group_id))
            if mkact:
                await query.message.edit(f"𝙲𝙾𝙽𝙽𝙴𝙲𝚃𝙴𝙳 𝚃𝙾 **{title}**")            
            else:
                await query.message.edit_text('Some error occurred!!', parse_mode="md")
            return

        elif "groupcb" in query.data:
            await query.answer()
            group_id = query.data.split(":")[1]
            act = query.data.split(":")[2]
            hr = await client.get_chat(int(group_id))
            title = hr.title
            user_id = query.from_user.id

            if act == "":
                stat = "CONNECT"
                cb = "connectcb"
            else:
                stat = "DISCONNECT"
                cb = "disconnect"

            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton(f"{stat}", callback_data=f"{cb}:{group_id}"),
                 InlineKeyboardButton("DELETE", callback_data=f"deletecb:{group_id}")],
                [InlineKeyboardButton("BACK", callback_data="backcb")]
            ])
            await query.message.edit(" 𝙶𝚁𝙾𝚄𝙿 𝙽𝙰𝙼𝙴: **{title}**\n 𝙶𝚁𝙾𝚄𝙿 𝙸𝙳: `{group_id}`", reply_markup=keyboard)        
            return

        elif query.data == "delallconfirm":
            userid = query.from_user.id
            chat_type = query.message.chat.type

            if chat_type == enums.ChatType.PRIVATE:
                grpid = await active_connection(str(userid))
                if grpid is not None:
                    grp_id = grpid
                    try:
                        chat = await client.get_chat(grpid)
                        title = chat.title
                    except:
                        await query.message.edit("𝙼𝙰𝙺𝙴 𝚂𝚄𝚁𝙴 𝙸'𝙼 𝙿𝚁𝙴𝚂𝙴𝙽𝚃 𝙸𝙽 𝚈𝙾𝚄𝚁 𝙶𝚁𝙾𝚄𝙿..!", quote=True)
                        return 
                else:
                    await query.message.edit("𝙸𝙰𝙼 𝙽𝙾𝚃 𝙲𝙾𝙽𝙽𝙴𝙲𝚃𝙴𝙳 𝚃𝙾 𝙰𝙽𝚈 𝙶𝚁𝙾𝚄𝙿..!\n 𝙲𝙷𝙴𝙲𝙺 /connections 𝙾𝚁 𝙲𝙾𝙽𝙽𝙴𝙲𝚃 𝚃𝙾 𝙰𝙽𝚈 𝙶𝚁𝙾𝚄𝙿𝚂", quote=True)

                    return

            elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
                grp_id = query.message.chat.id
                title = query.message.chat.title

            else:
                return

            st = await client.get_chat_member(grp_id, userid)
            if (st.status == enums.ChatMemberStatus.OWNER) or (str(userid) in ADMINS):
                await del_all(query.message, grp_id, title)
            else:
                await query.answer("𝚈𝙾𝚄 𝙽𝙴𝙴𝙳 𝚃𝙾 𝙱𝙴 𝙶𝚁𝙾𝚄𝙿 𝙾𝚆𝙽𝙴𝚁 𝙾𝚁 𝙰𝙽 𝙰𝙳𝙼𝙸𝙽𝚂 𝚃𝙾 𝙳𝙾 𝚃𝙷𝙰𝚃.!", show_alert=True)

        elif query.data == "delallcancel":
            userid = query.from_user.id
            chat_type = query.message.chat.type

            if chat_type == enums.ChatType.PRIVATE:
                await query.message.reply_to_message.delete()
                await query.message.delete()

            elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
                grp_id = query.message.chat.id
                st = await client.get_chat_member(grp_id, userid)
                if (st.status == enums.ChatMemberStatus.OWNER) or (str(userid) in ADMINS):
                    await query.message.delete()
                    try:
                        await query.message.reply_to_message.delete()
                    except:
                        pass
                else:
                    await query.answer(" 𝚃𝙷𝙰𝚃𝚂'𝚂 𝙽𝙾𝚃 𝙵𝙾𝚁 𝚈𝙾𝚄..!", show_alert=True)
    else:
        await query.answer("This Not Your Message", show_alert=True)
