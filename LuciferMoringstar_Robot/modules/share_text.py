from urllib.parse import *
from pyrogram import Client, filters
from pyrogram.types import *
from pyrogram import *

@Client.on_message(filters.private & filters.command(["sharetext"]))
async def sharelink(bot, update):
    # https://github.com/PR0FESS0R-99/ShareText-Bot/blob/01a849d3cdb6220509b8883e47df2e64e704ae55/main.py#L17 
    if len(update.command) != 2:
        await update.reply("**--Use Correct Format-- :-\n  • `/sharetext your text`**")
    await bot.send_photo(chat_id=update.chat.id,
        caption=f"**Message Sharing Link Is Ready** :- https://t.me/share/url?url={quote(update.text)}", reply_to_message_id=update.id, reply_markup=InlineKeyboardMarkup( [[ InlineKeyboardButton("📤 Share Link 📤", url=f"https://t.me/share/url?url={quote(update.text)}") ]] )       
    )
