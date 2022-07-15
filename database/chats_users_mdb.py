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

import motor.motor_asyncio, datetime
from LuciferMoringstar_Robot import DATABASE_NAME, DATABASE_URI, SINGLE_BUTTON, REQUEST_MOVIE, SPELL_MODE, SPELL_TEXT, WELCOME_TEXT, MELCOW_NEW_USERS, MOVIE_TEXT, CUSTOM_FILE_CAPTION, SAVE_FILES, FILE_MODE    

class Database:
    
    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.dcol = self.db.users
        self.grp = self.db.groups
        
    def new_user(self, id):
        return dict(
            id = id,
            join_date = datetime.date.today().isoformat()
        )        

    def new_group(self, id, title):
        return dict(
            id = id,
            title = title,
            chat_status = dict(is_disabled=False, reason="")
        )

    async def add_user(self, id):
        user = self.new_user(id)
        await self.dcol.insert_one(user)

    async def is_user_exist(self, id):
        user = await self.dcol.find_one({'id':int(id)})
        return bool(user)

    async def total_users_count(self):
        count = await self.dcol.count_documents({})
        return count

    async def get_all_users(self):
        return self.dcol.find({})

    async def delete_user(self, user_id):
        await self.dcol.delete_many({'id': int(user_id)})

    async def add_chat(self, chat, title):
        chat = self.new_group(chat, title)
        await self.grp.insert_one(chat)
    
    async def get_chat(self, chat):
        chat = await self.grp.find_one({'id':int(chat)})
        return False if not chat else chat.get('chat_status')
            
    async def update_settings(self, id, settings):
        await self.grp.update_one({'id': int(id)}, {'$set': {'settings': settings}})
       
    async def get_settings(self, id):
        default = {
            'button': SINGLE_BUTTON,
            'photo': REQUEST_MOVIE,
            'spellmode': SPELL_MODE,
            'spelltext': SPELL_TEXT,
            'welcometext': WELCOME_TEXT,
            'welcome': MELCOW_NEW_USERS,
            'template': MOVIE_TEXT,
            'caption': CUSTOM_FILE_CAPTION,
            'savefiles': SAVE_FILES,
            'filemode': FILE_MODE
        }
        chat = await self.grp.find_one({'id':int(id)})
        if chat:
            return chat.get('settings', default)
        return default
    
    async def disable_chat(self, chat, reason="No Reason"):
        chat_status = dict(is_disabled=True, reason=reason)           
        await self.grp.update_one({'id': int(chat)}, {'$set': {'chat_status': chat_status}})

    async def re_enable_chat(self, id):
        chat_status = dict(is_disabled=False, reason="")       
        await self.grp.update_one({'id': int(id)}, {'$set': {'chat_status': chat_status}})
 
    async def total_chat_count(self):
        count = await self.grp.count_documents({})
        return count
    
    async def get_all_chats(self):
        return self.grp.find({})

db = Database(DATABASE_URI, DATABASE_NAME)
