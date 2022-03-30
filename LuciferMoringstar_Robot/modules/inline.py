import logging
from pyrogram import Client as LuciferMoringstar_Robot, filters as Worker, emoji
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultCachedDocument
from LuciferMoringstar_Robot.database._utils import get_size, is_subscribed
from LuciferMoringstar_Robot.database.autofilter_db import get_search_results
from config import CACHE_TIME, AUTH_USERS, FORCES_SUB, CUSTOM_FILE_CAPTION
logger = logging.getLogger(__name__)
cache_time = 0 if AUTH_USERS or FORCES_SUB else CACHE_TIME


@LuciferMoringstar_Robot.on_inline_query(Worker.user(AUTH_USERS) if AUTH_USERS else None)
async def answer(bot, query):

    if FORCES_SUB and not await is_subscribed(bot, query):
        await query.answer(results=[],
                           cache_time=0,
                           switch_pm_text='You Have To Subscribe My Channel To Use The Bot',
                           switch_pm_parameter="subscribe")
        return

    results = []
    if '|' in query.query:
        string, file_type = query.query.split('|', maxsplit=1)
        string = string.strip()
        file_type = file_type.strip().lower()
    else:
        string = query.query.strip()
        file_type = None

    offset = int(query.offset or 0)
    reply_markup = get_reply_markup(query=string)
    files, next_offset = await get_search_results(string,
                                                  file_type=file_type,
                                                  max_results=10,
                                                  offset=offset)
    for file in files:
        title=file.file_name
        size=get_size(file.file_size)    
        caption=CUSTOM_FILE_CAPTION.format(mention=query.from_user.mention, title=title, size=size, caption=file.caption)
        results.append(
            InlineQueryResultCachedDocument(
                title=file.file_name,
                file_id=file.file_id,
                caption=caption,
                description=f'Size: {get_size(file.file_size)}\nType: {file.file_type}',
                reply_markup=reply_markup))

    if results:
        switch_pm_text = f"{emoji.FILE_FOLDER} Results"
        if string:
            switch_pm_text += f" for {string}"

        try:
            await query.answer(results=results,
                           is_personal = True,
                           cache_time=cache_time,
                           switch_pm_text=switch_pm_text,
                           switch_pm_parameter="start",
                           next_offset=str(next_offset))
        except Exception as e:
            logging.exception(str(e))
            await query.answer(results=[], is_personal=True,
                           cache_time=cache_time,
                           switch_pm_text=str(e)[:63],
                           switch_pm_parameter="error")
    else:

        switch_pm_text = f'{emoji.CROSS_MARK} No results'
        if string:
            switch_pm_text += f' for "{string}"'

        await query.answer(results=[],
                           is_personal = True,
                           cache_time=cache_time,
                           switch_pm_text=switch_pm_text,
                           switch_pm_parameter="okay")


def get_reply_markup(query):
    buttons = [[
        InlineKeyboardButton('Support Group', url='t.me/Mo_Tech_Group'),
        InlineKeyboardButton('More Botz', url='t.me/MT_Botz')
        ],[
        InlineKeyboardButton('🔍 Search again 🔎', switch_inline_query_current_chat=query)
        ]]
    return InlineKeyboardMarkup(buttons)


