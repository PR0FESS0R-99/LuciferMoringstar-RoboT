from urllib.parse import *
from pyrogram import Client, filters
from pyrogram.types import *
from pyrogram import *

@Client.on_message(filters.private & filters.command(["share"]))
async def sharelink(bot, update):
    # https://github.com/PR0FESS0R-99/ShareText-Bot/blob/01a849d3cdb6220509b8883e47df2e64e704ae55/main.py#L17 
    if len(update.command) != 2:
        return await update.reply("**--Use Correct Format-- :-\n  • `/share your text`**")
    text = update.text.split(" ", 1)[1]
    await update.reply(
        text=f"**Message Sharing Link Is Ready** :- https://t.me/share/url?url={quote(text)}", reply_markup=InlineKeyboardMarkup( [[ InlineKeyboardButton("📤 Share Link 📤", url=f"https://t.me/share/url?url={quote(text)}") ]] )       
    )
