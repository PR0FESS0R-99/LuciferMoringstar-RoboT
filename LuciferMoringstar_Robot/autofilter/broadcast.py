# (c) [Muhammed] @PR0FESS0R-99
# (s) @Mo_Tech_YT , @Mo_Tech_Group, @MT_Botz
# Copyright permission under MIT License
# All rights reserved by PR0FESS0R-99

import logging
logger = logging.getLogger(__name__)

import asyncio
import aiofiles
import aiofiles.os
import datetime
import traceback
import random
import string
import time
import os
from random import choice
from config import ADMINS
from pyrogram import Client as LuciferMoringstar_Robot, filters as Worker
from LuciferMoringstar_Robot.database.broadcast_db import Database
from pyrogram.errors import UserNotParticipant, FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid

db = Database() 

broadcast_ids = {}

async def send_msg(user_id, message):
    try:
        await message.copy(chat_id=user_id)
        return 200, None
    except FloodWait as e:
        await asyncio.sleep(e.x)
        return send_msg(user_id, message)
    except InputUserDeactivated:
        return 400, f"{user_id} : deactivated\n"
    except UserIsBlocked:
        return 400, f"{user_id} : blocked the bot\n"
    except PeerIdInvalid:
        return 400, f"{user_id} : user id invalid\n"
    except Exception as e:
        return 500, f"{user_id} : {traceback.format_exc()}\n"


@LuciferMoringstar_Robot.on_message(Worker.private & Worker.command(["broadcast", "send"]) & Worker.user(ADMINS) & Worker.reply)
async def broadcast_(c, m):
    print("broadcasting......")
    all_users = await db.get_all_users()
    broadcast_msg = m.reply_to_message
    
    while True:
        broadcast_id = ''.join([random.choice(string.ascii_letters) for i in range(3)])
        if not broadcast_ids.get(broadcast_id):
            break
    
    out = await m.reply_text(
        text = f"Broadcast initiated! You will be notified with log file when all the users are notified."
    )
    start_time = time.time()
    total_users = await db.total_users_count()
    done = 0
    failed = 0
    success = 0
    
    broadcast_ids[broadcast_id] = dict(
        total = total_users,
        current = done,
        failed = failed,
        success = success
    )
    
    async with aiofiles.open('broadcast.txt', 'w') as broadcast_log_file:
        async for user in all_users:
            
            sts, msg = await send_msg(
                user_id = int(user['id']),
                message = broadcast_msg
            )
            if msg is not None:
                await broadcast_log_file.write(msg)
            
            if sts == 200:
                success += 1
            else:
                failed += 1
            
            if sts == 400:
                await db.delete_user(user['id'])
            
            done += 1
            if broadcast_ids.get(broadcast_id) is None:
                break
            else:
                broadcast_ids[broadcast_id].update(
                    dict(
                        current = done,
                        failed = failed,
                        success = success
                    )
                )
    if broadcast_ids.get(broadcast_id):
        broadcast_ids.pop(broadcast_id)
    completed_in = datetime.timedelta(seconds=int(time.time()-start_time))
    
    await asyncio.sleep(3)
    
    await out.delete()
    
    if failed == 0:
        await m.reply_text(
            text=f"""
𝖻𝗋𝗈𝖺𝖽𝖼𝖺𝗌𝗍 𝖼𝗈𝗆𝗉𝗅𝖾𝗍𝖾𝖽 𝗂𝗇 {completed_in}
𝖳𝗈𝗍𝖺𝗅 𝗎𝗌𝖾𝗋𝗌 {total_users}
𝖳𝗈𝗍𝖺𝗅 𝖽𝗈𝗇𝖾 {done}
{success} 𝗌𝗎𝖼𝖼𝖾𝗌𝗌
{failed} 𝖿𝖺𝗂𝗅𝖾𝖽.""",
            quote=True
        )
    else:
        await m.reply_document(
            document='broadcast.txt',
            caption=f"""
𝖻𝗋𝗈𝖺𝖽𝖼𝖺𝗌𝗍 𝖼𝗈𝗆𝗉𝗅𝖾𝗍𝖾𝖽 𝗂𝗇 {completed_in}
𝖳𝗈𝗍𝖺𝗅 𝗎𝗌𝖾𝗋𝗌 {total_users}
𝖳𝗈𝗍𝖺𝗅 𝖽𝗈𝗇𝖾 {done}
{success} 𝗌𝗎𝖼𝖼𝖾𝗌𝗌
{failed} 𝖿𝖺𝗂𝗅𝖾𝖽.""",
            quote=True
        )
    
    await aiofiles.os.remove('broadcast.txt')
