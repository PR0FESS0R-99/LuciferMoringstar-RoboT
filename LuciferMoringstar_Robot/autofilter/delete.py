import logging
from pyrogram import Client as LuciferMoringstar_Robot, filters as Worker
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from LuciferMoringstar_Robot.database.autofilter_db import Media
from config import ADMINS
logger = logging.getLogger(__name__)


@LuciferMoringstar_Robot.on_message(Worker.command('delete') & Worker.user(ADMINS))
async def delete(bot, message):

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
        await msg.edit('This Is Not Supported File Format')
        return

    result = await Media.collection.delete_one({
        'file_name': media.file_name,
        'file_size': media.file_size,
        'mime_type': media.mime_type
    })
    if result.deleted_count:
        await msg.edit('File Is Successfully Deleted From Database')
    else:
        await msg.edit('File Not Found In Database')


@LuciferMoringstar_Robot.on_message(Worker.command('deleteall') & Worker.user(ADMINS))
async def delete_all_index(bot, message):
    await message.reply_text(
        text="This will delete all indexed files.\nDo you want to continue??",
        reply_markup=InlineKeyboardMarkup([[
           InlineKeyboardButton("Yes", callback_data="autofilter_delete"),
           InlineKeyboardButton("No", callback_data="close")   
           ]]
        )
    )

@LuciferMoringstar_Robot.on_callback_query(Worker.regex(r'^autofilter_delete'))
async def delete_all_index_confirm(bot, message):
    await Media.collection.drop()
    await message.message.edit('Succesfully Deleted All The Indexed Files.')


