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

import asyncio
from pyrogram import Client as lucifermoringstar_robot, filters
from LuciferMoringstar_Robot.functions import get_settings
from pyrogram.errors import ChatWriteForbidden

@lucifermoringstar_robot.on_message(filters.group & filters.new_chat_members)
async def welcome(client, update):
    settings = await get_settings(update.chat.id)
    if settings["welcome"]:
        try:
            try:            
                welcometext = settings["welcometext"]
                new_members = update.from_user.mention
                dell = await update.reply_text(welcometext.format(first_name = update.from_user.first_name, last_name = update.from_user.last_name, username = f"@{update.from_user.username}" or None, group_name = update.chat.title, mention = new_members), disable_web_page_preview=True)
                await asyncio.sleep(1000)
                await dell.delete()
            except ChatWriteForbidden:
                pass
            except Exception as error:
                pass
        except Exception as error:       
            await update.reply_text(f"{error}")
