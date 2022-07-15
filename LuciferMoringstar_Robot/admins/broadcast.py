import os, asyncio, aiofiles, aiofiles.os, datetime, random, string, time

async def send_broadcast(bot, update, db, send_msg, temp):    
    all_users = await db.get_all_users()
    broadcast_msg = update.reply_to_message
    while True:
        broadcast_id = ''.join([random.choice(string.ascii_letters) for i in range(3)])
        if not temp.broadcast_ids.get(broadcast_id):
            break
    out = await update.reply_text(text="**𝙱𝚁𝙾𝙰𝙳𝙲𝙰𝚂𝚃 𝙸𝙽𝙸𝚃𝙸𝙰𝚃𝙴𝙳..📣**\n   𝚈𝙾𝚄 𝚆𝙸𝙻𝙻 𝙱𝙴 𝙽𝙾𝚃𝙸𝙵𝙸𝙴𝙳 𝚆𝙸𝚃𝙷 𝙻𝙾𝙶 𝙵𝙸𝙻𝙴 𝚆𝙷𝙴𝙽 𝙰𝙻𝙻 𝚃𝙷𝙴 𝚄𝚂𝙴𝚁𝚂 𝙰𝚁𝙴 𝙽𝙾𝚃𝙸𝙵𝙸𝙴𝙳 🔔")
    start_time = time.time()
    total_users = await db.total_users_count()
    done = 0
    failed = 0
    success = 0
    temp.broadcast_ids[broadcast_id] = dict(total = total_users, current = done, failed = failed, success = success)
    async with aiofiles.open('broadcast.txt', 'w') as broadcast_log_file:
        async for user in all_users:
            sts, msg = await send_msg(user_id = int(user['id']), message = broadcast_msg)            
            if msg is not None:
                await broadcast_log_file.write(msg)
            if sts == 200:
                success += 1
            else:
                failed += 1
            if sts == 400:
                await db.delete_user(user['id'])
            done += 1
            if temp.broadcast_ids.get(broadcast_id) is None:
                break
            else:
                temp.broadcast_ids[broadcast_id].update(dict(current = done, failed = failed, success = success))
    if temp.broadcast_ids.get(broadcast_id):
        temp.broadcast_ids.pop(broadcast_id)
    completed_in = datetime.timedelta(seconds=int(time.time()-start_time))
    await asyncio.sleep(3)    
    await out.delete()
    if failed == 0:
        await update.reply_text(text=f"""**📣 𝙱𝚁𝙾𝙰𝙳𝙲𝙰𝚂𝚃 𝙲𝙾𝙼𝙿𝙻𝙴𝚃𝙴𝙳 𝙸𝙽** - `{completed_in}`\n\n𝚃𝙾𝚃𝙰𝙻 𝚄𝚂𝙴𝚁𝚂 {total_users}.\n𝚃𝙾𝚃𝙰𝙻 𝙳𝙾𝙽𝙴 {done}, {success} 𝚂𝚄𝙲𝙲𝙴𝚂𝚂 & {failed} 𝙵𝙰𝙸𝙻𝙴𝙳""", quote=True)        
    else:
        await update.reply_document(document='broadcast.txt', caption=f"""** 📣 𝙱𝚁𝙾𝙰𝙳𝙲𝙰𝚂𝚃 𝙲𝙾𝙼𝙿𝙻𝙴𝚃𝙴𝙳 𝙸𝙽**- `{completed_in}`\n\n𝚃𝙾𝚃𝙰𝙻 𝚄𝚂𝙴𝚁𝚂 {total_users}.\n𝚃𝙾𝚃𝙰𝙻 𝙳𝙾𝙽𝙴 {done}, {success} 𝚂𝚄𝙲𝙲𝙴𝚂𝚂 & {failed} 𝙵𝙰𝙸𝙻𝙴𝙳""", quote=True)
    await aiofiles.os.remove('broadcast.txt')
