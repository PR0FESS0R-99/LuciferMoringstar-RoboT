from pyrogram import Client, filters
from LuciferMoringstar-Robot.plugins.work import message

@Client.on_message(filters.command("start"))
async def start_command(bot, update):
    await update.reply("Bot Started")
    await message(update)
    
