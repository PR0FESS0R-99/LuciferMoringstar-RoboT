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
 
import re, random
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from LuciferMoringstar_Robot import temp, PICS
from LuciferMoringstar_Robot.functions import get_size, BUTTONS, split_list, get_settings
from database.autofilter_mdb import get_filter_results

async def group_filters(client, update):
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", update.text):
        return
    if 2 < len(update.text) < 100:
        btn = []
        search = update.text
        settings = await get_settings(update.chat.id)
        MOVIE_TEXT = settings["template"]
        files = await get_filter_results(query=search)
        if not files:
            reply = search.replace(" ", '+')  
            buttons = [[ InlineKeyboardButton("🔍 𝚂𝙴𝙰𝚁𝙲𝙷 𝚃𝙾 𝙶𝙾𝙾𝙶𝙻𝙴 🔎", url=f"https://www.google.com/search?q={reply}") ],[ InlineKeyboardButton("× 𝙲𝙻𝙾𝚂𝙴 ×", callback_data="close") ]]
            await update.reply_text(text=settings["spelltext"].format(query=search, first_name=update.from_user.first_name, last_name=update.from_user.last_name, title=update.chat.title, mention=update.from_user.mention), disable_web_page_preview=True, reply_markup=InlineKeyboardMarkup(buttons))           
            await asyncio.sleep(60)
            await spell.delete()
            return

        for file in files:
            file_id = file.file_id
            filesize = f"[{get_size(file.file_size)}]"
            filename = f"{file.file_name}"
            if settings["button"]:
                btn.append(
                    [InlineKeyboardButton(text=f"{filename}", callback_data=f"luciferGP#{file_id}")]
                )
            else:
                btn.append(
                    [InlineKeyboardButton(text=f"{filesize}", callback_data=f"luciferGP#{file_id}"),
                     InlineKeyboardButton(text=f"{filename}", callback_data=f"luciferGP#{file_id}")]
                )
        if not btn:
            return

        if len(btn) > 10: 
            btns = list(split_list(btn, 10)) 
            keyword = f"{update.chat.id}-{update.id}"
            BUTTONS[keyword] = {
                "total" : len(btns),
                "buttons" : btns
            }
        else:
            buttons = btn
            buttons.extend(
                (
                    [
                        InlineKeyboardButton(
                            text="📃 Pages 1/1", callback_data="pages"
                        ),
                        InlineKeyboardButton(
                            "Close 🗑️", callback_data="close"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text="🤖 CHECK MY PM 🤖",
                            url=f"https://telegram.dog/{temp.Bot_Username}",
                        )
                    ],
                )
            )

            if settings["photo"]:
                await client.send_photo(chat_id=update.chat.id, photo=random.choice(PICS), caption=MOVIE_TEXT.format(mention=update.from_user.mention, query=search, greeting="hi"), reply_markup=InlineKeyboardMarkup(buttons))
            else:
                await client.send_message(chat_id=update.chat.id, text=MOVIE_TEXT.format(mention=update.from_user.mention, query=search, greeting="hi"), reply_markup=InlineKeyboardMarkup(buttons))


            return

        data = BUTTONS[keyword]
        buttons = data['buttons'][0].copy()



        data = BUTTONS[keyword]
        buttons = data['buttons'][0].copy()

        buttons.append(
            [InlineKeyboardButton(text=f"📃 1/{data['total']}",callback_data="pages"),
             InlineKeyboardButton("🗑️", callback_data="close"),
             InlineKeyboardButton(text="➡",callback_data=f"nextgroup_0_{keyword}")]
        )

        buttons.append(
            [InlineKeyboardButton(text="🤖 CHECK MY PM 🤖", url=f"https://telegram.dog/{temp.Bot_Username}")]
        )

        if settings["photo"]:
            await client.send_photo(chat_id=update.chat.id, photo=random.choice(PICS), caption=MOVIE_TEXT.format(mention=update.from_user.mention, query=search, greeting="hi"), reply_markup=InlineKeyboardMarkup(buttons))
        else:
            await client.send_message(chat_id=update.chat.id, text=MOVIE_TEXT.format(mention=update.from_user.mention, query=search, greeting="hi"), reply_markup=InlineKeyboardMarkup(buttons))
        
 

