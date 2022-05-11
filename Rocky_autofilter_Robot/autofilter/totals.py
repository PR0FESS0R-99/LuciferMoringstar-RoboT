import logging
from pyrogram import Client as Rocky_autofilter_Robot, filters as Worker
from Rocky_autofilter_Robot.database.autofilter_db import Media
from config import ADMINS
logger = logging.getLogger(__name__)

@Rocky_autofilter_Robot.on_message(Worker.command('total') & Worker.user(ADMINS))
async def total(bot, message):

    msg = await message.reply("Processing...⏳", quote=True)
    try:
        total = await Media.count_documents()
        await msg.edit(f'📁 Saved files: {total}')
    except Exception as e:
        logger.exception('Failed to check total files')
        await msg.edit(f'Error: {e}')
