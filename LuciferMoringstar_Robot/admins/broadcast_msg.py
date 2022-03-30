# (c) [Muhammed] @PR0FESS0R-99
# (s) @Mo_Tech_YT , @Mo_Tech_Group, @MT_Botz
# Copyright permission under MIT License
# All rights reserved by PR0FESS0R-99

import asyncio, aiofiles, aiofiles.os, datetime, traceback, random, string, time, os
from pyrogram import Client as lucifermoringstar_robot, filters as filter
from LuciferMoringstar_Robot.database.users_chats_db import db
from LuciferMoringstar_Robot.database._utils import send_msg
from random import choice
from config import ADMINS

class config(object):
    broadcast_ids = {} # don't change this..!!
# https://github.com/PR0FESS0R-99/Broadcast-Bot

@lucifermoringstar_robot.on_message(filter.private & filter.command(["broadcast", "send"]) & filter.user(ADMINS) & filter.reply)
async def send_broadcast(client, message):
    all_users = await db.get_all_users()
    broadcast_msg = message.reply_to_message

    while True:
        broadcast_id = ''.join([random.choice(string.ascii_letters) for i in range(3)])
        if not config.broadcast_ids.get(broadcast_id):
            break

    out = await message.reply_text(text="**Broadcast Initiated..📣**\nYou will Be Notified with log File When All The Users Are Notified 🔔")
    start_time = time.time()
    total_users = await db.total_users_count()
    done = 0
    failed = 0
    success = 0

    config.broadcast_ids[broadcast_id] = dict(
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
            if config.broadcast_ids.get(broadcast_id) is None:
                break
            else:
                config.broadcast_ids[broadcast_id].update(
                    dict(
                        current = done,
                        failed = failed,
                        success = success
                    )
                )
    if config.broadcast_ids.get(broadcast_id):
        config.broadcast_ids.pop(broadcast_id)
    completed_in = datetime.timedelta(seconds=int(time.time()-start_time))

    await asyncio.sleep(3)    
    await out.delete()

    if failed == 0:
        await message.reply_text(text=f"""**📣 Broadcast Completed in** - `{completed_in}`\n\nTotal Users {total_users}.\nTotal Done {done}, {success} Success & {failed} Failed.""", quote=True)        
    else:
        await message.reply_document(document='broadcast.txt', caption=f"""** 📣 Broadcast Completed in **- `{completed_in}`\n\nTotal Users {total_users}.\nTotal Done {done}, {success} Success & {failed} Failed.""", quote=True)

    await aiofiles.os.remove('broadcast.txt')
