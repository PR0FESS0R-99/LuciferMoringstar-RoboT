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
async def delete_connections_cmd(bot, update):
    
    if update.chat.type == enums.ChatType.PRIVATE:
        await update.reply_text("__Run /connections to view or disconnect from groups..!__", quote=True)
        return

    elif update.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        group_id = update.chat.id
        user_id = update.from_user.id
        st = await bot.get_chat_member(update.chat.id, update.from_user.id)
        if (st.status != enums.ChatMemberStatus.ADMINISTRATOR and st.status != enums.ChatMemberStatus.OWNER and update.from_user.id not in ADMINS):
            return

        delcon = await delete_connection(str(user_id), str(group_id))
        if delcon:
            await update.reply_text("__Successfully disconnected from this chat__")
        else:
            await update.reply_text("__This chat isn't connected to me!\nDo /connect to connect.__")


@Client.on_message(filters.private & filters.command("connections"))
async def all_connections_cmd(bot, update):

    userid = update.from_user.id

    groupids = await all_connections(str(userid))
    if groupids is None:
        text = "__**There Are No Active Connections..! Connect To Some Groups First**__"
        await update.reply_text(text)
        return

    buttons = []
    for groupid in groupids:
        try:
            ttl = await bot.get_chat(int(groupid))
            title = ttl.title
            active = await if_active(str(userid), str(groupid))
            act = " - ACTIVE" if active else ""
            buttons.append( [ InlineKeyboardButton(f"{title}{act}", callback_data=f"groupcb:{groupid}:{act}") ] )            
        except:
            pass

    if buttons:
        text = "**Your Connected Group Details :**\n\n"
        await update.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons))        
    else:
        text = "__**There Are No Active Connections..! Connect To Some Groups First**__"
        await update.reply_text(text)
