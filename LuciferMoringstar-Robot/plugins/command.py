from pyrogram import Client, filters

@Client.on_message(filters.command("start"))
async def start_command(bot, update):
    await message.reply("Bot Started")
