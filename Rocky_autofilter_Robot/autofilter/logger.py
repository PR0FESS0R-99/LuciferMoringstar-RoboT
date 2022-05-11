import logging
from pyrogram import Client as LuciferMoringstar_Robot, filters as Worker
from config import ADMINS
logger = logging.getLogger(__name__)


@LuciferMoringstar_Robot.on_message(Worker.command('logger') & Worker.user(ADMINS))
async def log_file(bot, message):
    """Send log file"""
    try:
        await message.reply_document('TelegramBot.log')
    except Exception as e:
        await message.reply(str(e))
