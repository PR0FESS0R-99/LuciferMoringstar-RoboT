import logging
import asyncio
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from Config import ADMINS
import os
from LuciferMoringstar_Robot.Utils import save_file
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
RELEASE_INFO = ["1901 | IMDB", "1902 | IMDB", "1903 | IMDB", "1904 | IMDB", "1905 | IMDB", "1906 | IMDB", "1907 | IMDB", "1908 | IMDB", "1909 | IMDB", "1910 | IMDB", "1911 | IMDB", "1912 | IMDB", "1913 | IMDB", "1914 | IMDB", "1915 | IMDB", "1916 | IMDB", "1917 | IMDB", "1918 | IMDB", "1919 | IMDB", "1920 | IMDB", "1921 | IMDB", "1922 | IMDB", "1923 | IMDB", "1924 | IMDB", "1925 | IMDB", "1926 | IMDB", "1927 | IMDB", "1928 | IMDB", "1929 | IMDB", "1930 | IMDB", "1931 | IMDB", "1932 | IMDB", "1933 | IMDB", "1934 | IMDB", "1935 | IMDB", "1936 | IMDB", "1937 | IMDB", "1938 | IMDB", "1939 | IMDB", "1940 | IMDB", "1941 | IMDB", "1942 | IMDB", "1943 | IMDB", "1944 | IMDB", "1945 | IMDB", "1946 | IMDB", "1947 | IMDB", "1948 | IMDB", "1949 | IMDB", "1950 | IMDB", "1951 | IMDB", "1952 | IMDB", "1953 | IMDB", "1954 | IMDB", "1955 | IMDB", "1956 | IMDB", "1957 | IMDB", "1958 | IMDB", "1959 | IMDB", "1960 | IMDB", "1961 | IMDB", "1962 | IMDB", "1963 | IMDB", "1964 | IMDB", "1965 | IMDB", "1966 | IMDB", "1967 | IMDB", "1968 | IMDB", "1969 | IMDB", "1970 | IMDB", "1971 | IMDB", "1972 | IMDB", "1973 | IMDB", "1974 | IMDB", "1975 | IMDB", "1976 | IMDB", "1977 | IMDB", "1978 | IMDB", "1979 | IMDB", "1980 | IMDB", "1981 | IMDB", "1982 | IMDB", "1983 | IMDB", "1984 | IMDB", "1985 | IMDB", "1986 | IMDB", "1987 | IMDB", "1988 | IMDB", "1989 | IMDB", "1990 | IMDB", "1991 | IMDB", "1992 | IMDB", "1993 | IMDB", "1994 | IMDB", "1995 | IMDB", "1996 | IMDB", "1997 | IMDB", "1998 | IMDB", "1999 | IMDB", "2000 | IMDB", "2001 | IMDB", "2002 | IMDB", "2003 | IMDB", "2004 | IMDB", "2005 | IMDB", "2006 | IMDB", "2007 | IMDB", "2008 | IMDB", "2009 | IMDB", "2010 | IMDB", "2011 | IMDB", "2012 | IMDB", "2013 | IMDB", "2014 | IMDB", "2015 | IMDB", "2016 | IMDB", "2017 | IMDB", "2018 | IMDB", "2019 | IMDB", "2020 | IMDB", "2021 | IMDB", "2022 | IMDB", "2023 | IMDB", "2024 | IMDB", "2025 | IMDB", "2026 | IMDB", "2027 | IMDB", "2028 | IMDB", "2029 | IMDB", "2030 | IMDB", ]
