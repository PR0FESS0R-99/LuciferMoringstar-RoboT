import logging
import asyncio
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from Config import ADMINS
import os
from Rocky_autofilter_Robot.Utils import save_file
from Rocky_autofilter_Robot import imdb, add_filter, find_filter, get_filters, delete_filter, count_filters, Database, active_connection, add_user, all_users,  parser, split_quotes, IMDBCONTROL, google_search  
import pyromod.listen
logger = logging.getLogger(__name__)
lock = asyncio.Lock()


@Client.on_message(filters.command(['index', 'indexfiles']) & filters.user(ADMINS))
async def index_files(bot, message):
    """Save channel or group files"""
    if lock.locked():
        await message.reply('Wait until previous process complete.')
    else:
        while True:
            last_msg = await bot.ask(text = "Forward me last message of a channel which I should save to my database.\n\nYou can forward posts from any public channel, but for private channels bot should be an admin in the channel.\n\nMake sure to forward with quotes (Not as a copy)", chat_id = message.from_user.id)
            try:
                last_msg_id = last_msg.forward_from_message_id
                if last_msg.forward_from_chat.username:
                    chat_id = last_msg.forward_from_chat.username
                else:
                    chat_id=last_msg.forward_from_chat.id
                await bot.get_messages(chat_id, last_msg_id)
                break
            except Exception as e:
                await last_msg.reply_text(f"This Is An Invalid Message, Either the channel is private and bot is not an admin in the forwarded chat, or you forwarded message as copy.\nError caused Due to <code>{e}</code>")
                continue

        msg = await message.reply('Processing...⏳')
        total_files = 0
        async with lock:
            try:
                total=last_msg_id + 1
                current=int(os.environ.get("SKIP", 2))
                nyav=0
                while True:
                    try:
                        message = await bot.get_messages(chat_id=chat_id, message_ids=current, replies=0)
                    except FloodWait as e:
                        await asyncio.sleep(e.x)
                        message = await bot.get_messages(
                            chat_id,
                            current,
                            replies=0
                            )
                    except Exception as e:
                        print(e)
                        pass
                    try:
                        for file_type in ("document", "video", "audio"):
                            media = getattr(message, file_type, None)
                            if media is not None:
                                break
                            else:
                                continue
                        media.file_type = file_type
                        media.caption = message.caption
                        await save_file(media)
                        total_files += 1
                    except Exception as e:
                        print(e)
                        pass
                    current+=1
                    nyav+=1
                    if nyav == 20:
                        await msg.edit(f"Total messages fetched: {current}\nTotal messages saved: {total_files}")
                        nyav -= 20
                    if current == total:
                        break
                    else:
                        continue
            except Exception as e:
                logger.exception(e)
                await msg.edit(f'Error: {e}')
            else:
                await msg.edit(f'Total {total_files} Saved To DataBase!')

RATING = ["5.1 | IMDB", "6.2 | IMDB", "7.3 | IMDB", "8.4 | IMDB", "9.5 | IMDB", "10.6 | IMDB", ]
GENRES = ["fun, fact",
         "Thriller, Comedy",
         "Drama, Comedy",
         "Family, Drama",
         "Action, Adventure",
         "Film Noir",
         "Documentary"]
try:
            ia = IMDBCONTROL
            my_movie=the_query
            movies = ia.search_movie(my_movie)
            #print(f"{movies[0].movieID} {movies[0]['title']}")
            movie_url = movies[0].get_fullsizeURL()
            imdb = await donlee_imdb(the_query)
            await bot.send_photo(
                photo=movie_url,
                caption=f"""↪️ Requested: {query}
🎞️ Title: <a href={imdb['url']}>{imdb.get('title')}
🎭 Genres: {imdb.get('genres')}
📆 Year: <a href={imdb['url']}/releaseinfo>{imdb.get('year')}</a>
🌟 Rating: <a href={imdb['url']}/ratings>{imdb.get('rating')}</a> / 10
🗃️ Total Files : {(len_results)}
📑 Total Page : 1/{len_result if len_result < max_pages else max_pages}
👤 Requested By : {update.from_user.mention}
🖋 StoryLine: <code>{imdb.get('plot')} </code>"
☑️ Chat : {update.chat.title}""",
                reply_markup=reply_markup,
                chat_id=update.chat.id,
                reply_to_message_id=update.message_id,
                parse_mode="html"
            )
