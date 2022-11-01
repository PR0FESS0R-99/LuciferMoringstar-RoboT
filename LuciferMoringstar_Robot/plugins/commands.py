from pyrogram import Client, filters
from LuciferMoringstart_Robot.lucifer import lucifermoringstar_robot

@lucifermoringstar_robot.on_message(filters.command("start"))
async def start_command(bot, update):
    await update.reply("Bot Started")
