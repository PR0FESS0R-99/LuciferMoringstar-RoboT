from pyrogram import filters, Client, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.connections_mdb import add_connection, all_connections, if_active, delete_connection
from LuciferMoringstar_Robot import ADMINS
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

@Client.on_message((filters.private | filters.group) & filters.command('connect'))
async def addconnection(bot, update):
    userid = update.from_user.id if update.from_user else None
    if not userid:
        return await update.reply_text(f" 𝚈𝙾𝚄𝚁 𝙰𝚁𝙴 𝙰𝙽𝙾𝙽𝚈𝙼𝙾𝚄𝚂 𝙰𝙳𝙼𝙸𝙽. /connect {update.chat.id} 𝙸𝙽 𝙿𝙼")
    chat_type = update.chat.type

    if chat_type == enums.ChatType.PRIVATE:
        try:
            cmd, group_id = update.text.split(" ", 1)
        except:
            await update.reply_text("𝙴𝙽𝚃𝙴𝚁 𝙸𝙽 𝙲𝙾𝚁𝚁𝙴𝙲𝚃 𝙵𝙾𝚁𝙼𝙰𝚃..!\n<code>/connect groupid</code>\n𝙶𝙴𝚃 𝚈𝙾𝚄𝚁 𝙶𝚁𝙾𝚄𝙿 𝙸𝙳 𝙱𝚈 𝙰𝙳𝙳𝙸𝙽𝙶 𝚃𝙷𝙸𝚂 𝙱𝙾𝚃 𝚃𝙾 𝚈𝙾𝚄𝚁 𝙶𝚁𝙾𝚄𝙿 𝙰𝙼𝙳 𝚄𝚂𝙴 <code>/id</code>""", quote=True)
            return

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        group_id = update.chat.id

    try:
        member = await bot.get_chat_member(group_id, userid)
        if (
                member.status != enums.ChatMemberStatus.ADMINISTRATOR
                and member.status != enums.ChatMemberStatus.OWNER
                and str(userid) not in ADMINS
        ):
            await update.reply_text("𝚈𝙾𝚄 𝚂𝙷𝙾𝚄𝙻𝙳 𝙱𝙴 𝙰𝙽 𝙰𝙳𝙼𝙸𝙽 𝙸𝙽 𝙶𝙸𝚅𝙴𝙽 𝙶𝚁𝙾𝚄𝙿..!", quote=True)
            return
    except Exception as e:
        logger.exception(e)
        await update.reply_text(f"{e}")
        await update.reply_text("𝙸𝙽𝚅𝙰𝙻𝙸𝙳 𝙶𝚁𝙾𝚄𝙿 𝙸𝙳..!\n\n    𝙸𝙵 𝙲𝙾𝚁𝚁𝙴𝙲𝚃 𝙼𝙰𝙺𝙴 𝚂𝚄𝚁𝙴 𝙸'𝙼 𝙿𝚁𝙴𝚂𝙴𝙽𝚃 𝙸𝙽 𝚈𝙾𝚄𝚁 𝙶𝚁𝙾𝚄𝙿...!", quote=True)
        return
    try:
        st = await bot.get_chat_member(group_id, "me")
        if st.status == enums.ChatMemberStatus.ADMINISTRATOR:
            mrkyt = await bot.get_chat(group_id)
            title = mrkyt.title

            addcon = await add_connection(str(group_id), str(userid))
            if addcon:
                await update.reply_text(text=f"𝚂𝚄𝙲𝙲𝙴𝚂𝚂𝙵𝚄𝙻𝙻𝚈 𝙲𝙾𝙽𝙽𝙴𝙲𝚃𝙴𝙳 𝚃𝙾 **{title}**\n    𝙽𝙾𝚆 𝙼𝙰𝙽𝙰𝙶𝙴 𝚈𝙾𝚄𝚁 𝙶𝚁𝙾𝚄𝙿 𝙵𝚁𝙾𝙼 𝙼𝚈 𝙿𝙼..!", quote=True)
                
                if chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
                    await bot.send_message(chat_id=userid, text=f"𝙲𝙾𝙽𝙽𝙴𝙲𝚃𝙴𝙳 𝚃𝙾 **{title}** !")
            else:
                await update.reply_text(text="𝚈𝙾𝚄'𝚁𝙴 𝙰𝙻𝚁𝙴𝙰𝙳𝚈 𝙲𝙾𝙽𝙽𝙴𝙲𝚃𝙴𝙳 𝚃𝙾 𝚃𝙷𝙸𝚂 𝙲𝙷𝙰𝚃..!", quote=True)               
        else:
            await update.reply_text(text="𝙰𝙳𝙳 𝙼𝙴 𝙰𝚂 𝙰𝙽 𝙰𝙳𝙼𝙸𝙽 𝙸𝙽 𝙶𝚁𝙾𝚄𝙿..!", quote=True)
    except Exception as e:
        logger.exception(e)
        await update.reply_text(f"{e}")
        await update.reply_text('𝚂𝙾𝙼𝙴 𝙴𝚁𝚁𝙾𝚁 𝙾𝙲𝙲𝚄𝚁𝚁𝙴𝙳..!\n   𝚃𝚁𝚈 𝙰𝙶𝙰𝙸𝙽 𝙻𝙰𝚃𝙴𝚁.', quote=True)
        return

@Client.on_message((filters.private | filters.group) & filters.command('disconnect'))
async def deleteconnection(client, message):
    userid = message.from_user.id if message.from_user else None

    chat_type = message.chat.type
    if not userid:
        return await message.reply(f"𝚈𝙾𝚄𝚁 𝙰𝚁𝙴 𝙰𝙽𝙾𝙽𝚈𝙼𝙾𝚄𝚂 𝙰𝙳𝙼𝙸𝙽. /connect {message.chat.id} 𝙸𝙽 𝙿𝙼")

    if chat_type == enums.ChatType.PRIVATE:
        await message.reply_text("𝚁𝚄𝙽 /connections 𝚃𝙾 𝚅𝙸𝙴𝚆 𝙾𝚁 𝙳𝙸𝚂𝙲𝙾𝙽𝙽𝙴𝙲𝚃 𝙵𝚁𝙾𝙼 𝙶𝚁𝙾𝚄𝙿..!", quote=True)

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        group_id = message.chat.id

        member = await client.get_chat_member(group_id, userid)
        if (
                member.status != enums.ChatMemberStatus.ADMINISTRATOR
                and member.status != enums.ChatMemberStatus.OWNER
                and str(userid) not in ADMINS
        ):
            return

        delcon = await delete_connection(str(userid), str(group_id))
        if delcon:
            await message.reply_text("𝚂𝚄𝙲𝙲𝙴𝚂𝚂𝙵𝚄𝙻𝙻𝚈 𝙳𝙸𝚂𝙲𝙾𝙽𝙽𝙴𝙲𝚃𝙴𝙳 𝙵𝚁𝙾𝙼 𝚃𝙷𝙸𝚂 𝙲𝙷𝙰𝚃..", quote=True)
        else:
            await message.reply_text("𝚃𝙷𝙸𝚂 𝙲𝙷𝙰𝚃 𝙸𝚂𝙽'𝚃 𝙲𝙾𝙽𝙽𝙴𝙲𝚃𝙴𝙳 𝚃𝙾 𝙼𝙴\n     𝙳𝙾 /connect 𝚃𝙾 𝙲𝙾𝙽𝙽𝙴𝙲𝚃.", quote=True)


@Client.on_message(filters.private & filters.command(["connections"]))
async def all_connections(client, message):
    userid = message.from_user.id

    groupids = await all_connections(str(userid))
    if groupids is None:
        await message.reply_text("𝚃𝙷𝙴𝚁𝙴 𝙰𝚁𝙴 𝙽𝙾 𝙰𝙲𝚃𝙸𝚅𝙴 𝙲𝙾𝙽𝙽𝙴𝙲𝚃𝙸𝙾𝙽𝚂..!\n   𝙲𝙾𝙽𝙽𝙴𝙲𝚃 𝚃𝙾 𝚂𝙰𝙼𝙴 𝙶𝙴𝙾𝚄𝙿𝚂 𝙵𝙸𝚁𝚂𝚃..!", quote=True)        
        return
    buttons = []
    for groupid in groupids:
        try:
            ttl = await client.get_chat(int(groupid))
            title = ttl.title
            active = await if_active(str(userid), str(groupid))
            act = " - 🅰︎🅲︎🆃︎🅸︎🆅︎🅴︎" if active else ""
            buttons.append([InlineKeyboardButton(f"{title}{act}", callback_data=f"groupcb:{groupid}:{act}")])           
        except:
            pass

    if buttons:
        await message.reply_text("""𝚈𝙾𝚄𝚁 𝙲𝙾𝙽𝙽𝙴𝙲𝚃𝙴𝙳 𝙶𝚁𝙾𝚄𝙿 𝙳𝙴𝚃𝙰𝙸𝙻𝙴𝚂:\n\n""", reply_markup=InlineKeyboardMarkup(buttons), quote=True)        
    else:
        await message.reply_text("""𝚃𝙷𝙴𝚁𝙴 𝙰𝚁𝙴 𝙽𝙾 𝙰𝙲𝚃𝙸𝚅𝙴 𝙲𝙾𝙽𝙽𝙴𝙲𝚃𝙸𝙾𝙽𝚂..! 𝙲𝙾𝙽𝙽𝙴𝙲𝚃 𝚃𝙾 𝚂𝙰𝙼𝙴 𝙶𝚁𝙾𝚄𝙿 𝙵𝙸𝚁𝚂𝚃""", quote=True)
        
