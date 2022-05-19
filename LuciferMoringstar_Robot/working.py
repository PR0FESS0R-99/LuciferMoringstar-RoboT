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
 
from pyrogram import Client as lucifermoringstar_robot, filters
from LuciferMoringstar_Robot.modules import group_filters, pm_filters
from LuciferMoringstar_Robot import AUTH_GROUPS, AUTH_USERS, LOG_CHANNEL, temp
from LuciferMoringstar_Robot.translation import CHAT_LOGS_MESSAGE
from database.chats_users_mdb import db

@lucifermoringstar_robot.on_message(filters.text & filters.private & filters.incoming & filters.user(AUTH_USERS) if AUTH_USERS else filters.text & filters.private & filters.incoming)
async def pmbot_filters(client, update):
    if update.chat.id in temp.PMAF_OFF:
        return
    else:
        await pm_filters(client, update)

@lucifermoringstar_robot.on_message(filters.text & filters.group & filters.incoming & filters.chat(AUTH_GROUPS) if AUTH_GROUPS else filters.text & filters.group & filters.incoming)
async def groupfilters(client, update):
    invite_link = await client.create_chat_invite_link(update.chat.id)
    if not await db.get_chat(update.chat.id):
        await client.send_message(LOG_CHANNEL, CHAT_LOGS_MESSAGE.format(title=update.chat.title, id=update.chat.id, join=invite_link.invite_link))       
        await db.add_chat(update.chat.id, update.chat.title)
    await group_filters(client, update)

