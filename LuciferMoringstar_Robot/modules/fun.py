# MIT License

# Copyright (c) 2022 Muhammed

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Telegram Link : https://telegram.dog/Mo_Tech_Group
# Repo Link : https://github.com/PR0FESS0R-99/LuciferMoringstar-Robot
# License Link : https://github.com/PR0FESS0R-99/LuciferMoringstar-Robot/blob/LuciferMoringstar-Robot/LICENSE

from pyrogram import Client, filters
from LuciferMoringstar_Robot import emoji

@Client.on_message(filters.command(["throw", "dart"]))
async def throw_dart(bot, update):
    replyID = update.id
    if update.reply_to_message:
        replyID = update.reply_to_message.id
    await bot.send_dice(chat_id=update.chat.id, emoji=emoji.THROW_DART, disable_notification=True, reply_to_message_id=replyID)

@Client.on_message(filters.command(["goal", "shoot"]))
async def roll_dice(bot, update):
    replyID = update.id
    if update.reply_to_message:
        replyID = update.reply_to_message.id
    await bot.send_dice(chat_id=update.chat.id, emoji=emoji.GOAL_E_MOJI, disable_notification=True, reply_to_message_id=replyID)

@Client.on_message(filters.private & filters.command(["luck"]))
async def luck_cownd(bot, update):
    replyID = update.id
    if update.reply_to_message:
        replyID = update.reply_to_message.id
    await bot.send_dice(chat_id=update.chat.id, emoji=emoji.TRY_YOUR_LUCK, disable_notification=True, reply_to_message_id=replyID)
