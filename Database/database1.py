import re, os, pymongo, datetime, asyncio
import motor.motor_asyncio # pylint: disable=import-error
from config import DATABASE, BOT_NAME, SPELLING_MODE
from typing import List
from pyrogram.types import InlineKeyboardButton, Message, InlineKeyboardMarkup
from imdb import IMDb

imdb = IMDb() 
myclient = pymongo.MongoClient(DATABASE)
mydb = myclient[BOT_NAME]
mycol = mydb['CONNECTION']   
aambro = mydb['USERS']
GOOGLE_NAME = InlineKeyboardMarkup
GOOGLE_LINK = InlineKeyboardButton
BTN_URL_REGEX = re.compile(
    r"(\[([^\[]+?)\]\((buttonurl|buttonalert):(?:/{0,2})(.+?)(:same)?\))"
)

SMART_OPEN = '“'
SMART_CLOSE = '”'
START_CHAR = ('\'', '"', SMART_OPEN)

async def add_filter(grp_id, text, reply_text, btn, file, alert):
    mycol = mydb[str(grp_id)]
    # mycol.create_index([('text', 'text')])

    data = {
        'text':str(text),
        'reply':str(reply_text),
        'btn':str(btn),
        'file':str(file),
        'alert':str(alert)
    }

    try:
        mycol.update_one({'text': str(text)},  {"$set": data}, upsert=True)
    except:
        print('Couldnt save, check your db')
             
   
async def find_filter(group_id, name):
    mycol = mydb[str(group_id)]
    
    query = mycol.find( {"text":name})
    # query = mycol.find( { "$text": {"$search": name}})
    try:
        for file in query:
            reply_text = file['reply']
            btn = file['btn']
            fileid = file['file']
            try:
                alert = file['alert']
            except:
                alert = None
        return reply_text, btn, alert, fileid
    except:
        return None, None, None, None

async def google_search(bot, update):
    Auto_Delete=await bot.send_message(
    chat_id = update.chat.id,
    text=SPELLING_MODE.format(update.from_user.mention),
    parse_mode="html",
    reply_markup=GOOGLE_NAME([[GOOGLE_LINK("🔍 Search Google 🔎", url="https://www.imdb.com/search/")]]),
    reply_to_message_id=update.message_id
    )
    await asyncio.sleep(60) # in seconds
    await Auto_Delete.delete()


async def get_filters(group_id):
    mycol = mydb[str(group_id)]

    texts = []
    query = mycol.find()
    try:
        for file in query:
            text = file['text']
            texts.append(text)
    except:
        pass
    return texts


async def delete_filter(message, text, group_id):
    mycol = mydb[str(group_id)]
    
    myquery = {'text':text }
    query = mycol.count_documents(myquery)
    if query == 1:
        mycol.delete_one(myquery)
        await message.reply_text(
            f"'`{text}`'  deleted. I'll not respond to that filter anymore.",
            quote=True,
            parse_mode="md"
        )
    else:
        await message.reply_text("Couldn't find that filter!", quote=True)


async def del_all(message, group_id, title):
    if str(group_id) not in mydb.list_collection_names():
        await message.edit_text(f"Nothing to remove in {title}!")
        return
        
    mycol = mydb[str(group_id)]
    try:
        mycol.drop()
        await message.edit_text(f"All filters from {title} has been removed")
    except:
        await message.edit_text(f"Couldn't remove all filters from group!")
        return


async def count_filters(group_id):
    mycol = mydb[str(group_id)]

    count = mycol.count()
    if count == 0:
        return False
    else:
        return count


async def filter_stats():
    collections = mydb.list_collection_names()

    if "CONNECTION" in collections:
        collections.remove("CONNECTION")
    if "USERS" in collections:
        collections.remove("USERS")

    totalcount = 0
    for collection in collections:
        mycol = mydb[collection]
        count = mycol.count()
        totalcount = totalcount + count

    totalcollections = len(collections)

    return totalcollections, totalcount

async def add_connection(group_id, user_id):
    query = mycol.find_one(
        { "_id": user_id },
        { "_id": 0, "active_group": 0 }
    )
    if query is not None:
        group_ids = []
        for x in query["group_details"]:
            group_ids.append(x["group_id"])

        if group_id in group_ids:
            return False

    group_details = {
        "group_id" : group_id
    }

    data = {
        '_id': user_id,
        'group_details' : [group_details],
        'active_group' : group_id,
    }
    
    if mycol.count_documents( {"_id": user_id} ) == 0:
        try:
            mycol.insert_one(data)
            return True
        except:
            print('Some error occured!')

    else:
        try:
            mycol.update_one(
                {'_id': user_id},
                {
                    "$push": {"group_details": group_details},
                    "$set": {"active_group" : group_id}
                }
            )
            return True
        except:
            print('Some error occured!')

        
async def active_connection(user_id):

    query = mycol.find_one(
        { "_id": user_id },
        { "_id": 0, "group_details": 0 }
    )
    if query:
        group_id = query['active_group']
        if group_id != None:
            return int(group_id)
        else:
            return None
    else:
        return None

async def all_connections(user_id):
    query = mycol.find_one(
        { "_id": user_id },
        { "_id": 0, "active_group": 0 }
    )
    if query is not None:
        group_ids = []
        for x in query["group_details"]:
            group_ids.append(x["group_id"])
        return group_ids
    else:
        return None


async def if_active(user_id, group_id):
    query = mycol.find_one(
        { "_id": user_id },
        { "_id": 0, "group_details": 0 }
    )
    if query is not None:
        if query['active_group'] == group_id:
            return True
        else:
            return False
    else:
        return False


async def make_active(user_id, group_id):
    update = mycol.update_one(
        {'_id': user_id},
        {"$set": {"active_group" : group_id}}
    )
    if update.modified_count == 0:
        return False
    else:
        return True


async def make_inactive(user_id):
    update = mycol.update_one(
        {'_id': user_id},
        {"$set": {"active_group" : None}}
    )
    if update.modified_count == 0:
        return False
    else:
        return True


def remove_emoji(string):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F" 
                               u"\U0001F300-\U0001F5FF"
                               u"\U0001F680-\U0001F6FF" 
                               u"\U0001F1E0-\U0001F1FF" 
                               u"\U00002500-\U00002BEF" 
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"
                               u"\u3030"
    "]+", flags=re.UNICODE)
    
    return emoji_pattern.sub(r' ', str(string))


async def delete_connection(user_id, group_id):

    try:
        update = mycol.update_one(
            {"_id": user_id},
            {"$pull" : { "group_details" : {"group_id":group_id} } }
        )
        if update.modified_count == 0:
            return False
        else:
            query = mycol.find_one(
                { "_id": user_id },
                { "_id": 0 }
            )
            if len(query["group_details"]) >= 1:
                if query['active_group'] == group_id:
                    prvs_group_id = query["group_details"][len(query["group_details"]) - 1]["group_id"]

                    mycol.update_one(
                        {'_id': user_id},
                        {"$set": {"active_group" : prvs_group_id}}
                    )
            else:
                mycol.update_one(
                    {'_id': user_id},
                    {"$set": {"active_group" : None}}
                )                    
            return True
    except Exception as e:
        print(e)
        return False




async def add_user(id, username, name, dcid):
    data = {
        '_id': id,
        'username' : username,
        'name' : name,
        'dc_id' : dcid
    }
    try:
        aambro.update_one({'_id': id},  {"$set": data}, upsert=True)
    except:
        pass


async def all_users():
    count = aambro.count()
    return count


async def find_user(id):
    query = aambro.find( {"_id":id})

    try:
        for file in query:
            name = file['name']
            username = file['username']
            dc_id = file['dc_id']
        return name, username, dc_id
    except:
        return None, None, None

def split_quotes(text: str) -> List:
    if any(text.startswith(char) for char in START_CHAR):
        counter = 1  # ignore first char -> is some kind of quote
        while counter < len(text):
            if text[counter] == "\\":
                counter += 1
            elif text[counter] == text[0] or (text[0] == SMART_OPEN and text[counter] == SMART_CLOSE):
                break
            counter += 1
        else:
            return text.split(None, 1)

        # 1 to avoid starting quote, and counter is exclusive so avoids ending
        key = remove_escapes(text[1:counter].strip())
        # index will be in range, or `else` would have been executed and returned
        rest = text[counter + 1:].strip()
        if not key:
            key = text[0] + text[0]
        return list(filter(None, [key, rest]))
    else:
        return text.split(None, 1)

def parser(text, keyword):
    if "buttonalert" in text:
        text = (text.replace("\n", "\\n").replace("\t", "\\t"))
    buttons = []
    note_data = ""
    prev = 0
    i = 0
    alerts = []
    for match in BTN_URL_REGEX.finditer(text):
        # Check if btnurl is escaped
        n_escapes = 0
        to_check = match.start(1) - 1
        while to_check > 0 and text[to_check] == "\\":
            n_escapes += 1
            to_check -= 1

        # if even, not escaped -> create button
        if n_escapes % 2 == 0:
            note_data += text[prev:match.start(1)]
            prev = match.end(1)
            if match.group(3) == "buttonalert":
                # create a thruple with button label, url, and newline status
                if bool(match.group(5)) and buttons:
                    buttons[-1].append(InlineKeyboardButton(
                        text=match.group(2),
                        callback_data=f"alertmessage:{i}:{keyword}"
                    ))
                else:
                    buttons.append([InlineKeyboardButton(
                        text=match.group(2),
                        callback_data=f"alertmessage:{i}:{keyword}"
                    )])
                i = i + 1
                alerts.append(match.group(4))
            else:
                if bool(match.group(5)) and buttons:
                    buttons[-1].append(InlineKeyboardButton(
                        text=match.group(2),
                        url=match.group(4).replace(" ", "")
                    ))
                else:
                    buttons.append([InlineKeyboardButton(
                        text=match.group(2),
                        url=match.group(4).replace(" ", "")
                    )])

        # if odd, escaped -> move along
        else:
            note_data += text[prev:to_check]
            prev = match.start(1) - 1
    else:
        note_data += text[prev:]

    try:
        return note_data, buttons, alerts
    except:
        return note_data, buttons, None

def remove_escapes(text: str) -> str:
    counter = 0
    res = ""
    is_escaped = False
    while counter < len(text):
        if is_escaped:
            res += text[counter]
            is_escaped = False
        elif text[counter] == "\\":
            is_escaped = True
        else:
            res += text[counter]
        counter += 1
    return res


def humanbytes(size):
    if not size:
        return ""
    power = 2**10
    n = 0
    Dic_powerN = {0: ' ', 1: 'Ki', 2: 'Mi', 3: 'Gi', 4: 'Ti'}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + 'B'


async def donlee_imdb(query, bulk=False, id=False):
    if not id:
        # https://t.me/GetTGLink/4183
        pattern = re.compile(r"^(([a-zA-Z\s])*)?\s?([1-2]\d\d\d)?", re.IGNORECASE)
        match = pattern.match(query)
        year = None
        if match:
            title = match.group(1)
            year = match.group(3)
        else:
            title = query
        movieid = imdb.search_movie(title.lower(), results=10)
        if not movieid:
            return None
        if year:
            filtered=list(filter(lambda k: str(k.get('year')) == str(year), movieid))
            if not filtered:
                filtered = movieid
        else:
            filtered = movieid
        movieid=list(filter(lambda k: k.get('kind') in ['movie', 'tv series'], filtered))
        if not movieid:
            movieid = filtered
        if bulk:
            return movieid
        movieid = movieid[0].movieID
    else:
        movieid = int(query)
    movie = imdb.get_movie(movieid)
    title = movie.get('title')
    genres = ", ".join(movie.get("genres")) if movie.get("genres") else None
    rating = str(movie.get("rating"))
    if movie.get("original air date"):
        date = movie["original air date"]
    elif movie.get("year"):
        date = movie.get("year")
    else:
        date = "N/A"
    poster = movie.get('full-size cover url')
    plot = movie.get('plot')
    if plot and len(plot) > 0:
        plot = plot[0]
    if plot and len(plot) > 800:
        plot = plot[0:800] + "..."
    return {
        'title': title,
        'year': date,
        'genres': genres,
        'poster': poster,
        'plot': plot,
        'rating': rating,
        'url':f'https://www.imdb.com/title/tt{movieid}'

    }

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


class Database:

    def __init__(self):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE)
        self.db = self._client[BOT_NAME]
        self.col = self.db["Main"]
        self.acol = self.db["Active_Chats"]
        self.fcol = self.db["Filter_Collection"]
        self.dcol = self.db.users
        self.cache = {}
        self.acache = {}


    def new_user(self, id):
        return dict(
            id = id,
            join_date = datetime.date.today().isoformat()
        )
    async def add_user(self, id):
        user = self.new_user(id)
        await self.dcol.insert_one(user)
    async def is_user_exist(self, id):
        user = await self.dcol.find_one({'id':int(id)})
        return True if user else False
    async def total_users_count(self):
        count = await self.dcol.count_documents({})
        return count
    async def get_all_users(self):
        all_users = self.dcol.find({})
        return all_users
    async def delete_user(self, user_id):
        await self.dcol.delete_many({'id': int(user_id)})




    async def create_index(self):
        """
        Create text index if not in db
        """
        await self.fcol.create_index([("file_name", "text")])


    def new_chat(self, group_id, channel_id, channel_name):
        """
        Create a document in db if the chat is new
        """
        try:
            group_id, channel_id = int(group_id), int(channel_id)
        except:
            pass
        
        return dict(
            _id = group_id,
            chat_ids = [{
                "chat_id": channel_id,
                "chat_name": channel_name
                }],
            types = dict(
                audio=False,
                document=True,
                video=True
            ),
            configs = dict(
                accuracy=0.80,
                max_pages=5,
                max_results=50,
                max_per_page=10,
                pm_fchat=True,
                show_invite_link=True
            )
        )


    async def status(self, group_id: int):
        """
        Get the total filters, total connected
        chats and total active chats of a chat
        """
        group_id = int(group_id)
        
        total_filter = await self.tf_count(group_id)
        
        chats = await self.find_chat(group_id)
        chats = chats.get("chat_ids")
        total_chats = len(chats) if chats is not None else 0
        
        achats = await self.find_active(group_id)
        if achats not in (None, False):
            achats = achats.get("chats")
            if achats == None:
                achats = []
        else:
            achats = []
        total_achats = len(achats)
        
        return total_filter, total_chats, total_achats


    async def find_group_id(self, channel_id: int):
        """
        Find all group id which is connected to a channel 
        for add a new files to db
        """
        data = self.col.find({})
        group_list = []

        for group_id in await data.to_list(length=50): # No Need Of Even 50
            for y in group_id["chat_ids"]:
                if int(y["chat_id"]) == int(channel_id):
                    group_list.append(group_id["_id"])
                else:
                    continue
        return group_list

    # Related TO Finding Channel(s)
    async def find_chat(self, group_id: int):
        """
        A funtion to fetch a group's settings
        """
        connections = self.cache.get(str(group_id))
        
        if connections is not None:
            return connections

        connections = await self.col.find_one({'_id': group_id})
        
        if connections:
            self.cache[str(group_id)] = connections

            return connections
        else: 
            return self.new_chat(None, None, None)

        
    async def add_chat(self, group_id: int, channel_id: int, channel_name):
        """
        A funtion to add/update a chat document when a new chat is connected
        """
        new = self.new_chat(group_id, channel_id, channel_name)
        update_d = {"$push" : {"chat_ids" : {"chat_id": channel_id, "chat_name" : channel_name}}}
        prev = await self.col.find_one({'_id':group_id})
        
        if prev:
            await self.col.update_one({'_id':group_id}, update_d)
            await self.update_active(group_id, channel_id, channel_name)
            await self.refresh_cache(group_id)
            
            return True
        
        self.cache[str(group_id)] = new
        
        await self.col.insert_one(new)
        await self.add_active(group_id, channel_id, channel_name)
        await self.refresh_cache(group_id)
        
        return True

    async def del_chat(self, group_id: int, channel_id: int):
        """
        A Funtion to delete a channel and its files from db of a chat connection
        """
        group_id, channel_id = int(group_id), int(channel_id) # group_id and channel_id Didnt type casted to int for some reason
        
        prev = self.col.find_one({"_id": group_id})
        
        if prev:
            
            await self.col.update_one(
                {"_id": group_id}, 
                    {"$pull" : 
                        {"chat_ids" : 
                            {"chat_id":
                                channel_id
                            }
                        }
                    },
                False,
                True
            )

            await self.del_active(group_id, channel_id)
            await self.refresh_cache(group_id)

            return True

        return False


    async def in_db(self, group_id: int, channel_id: int):
        """
        Check whether if the given channel id is in db or not...
        """
        connections = self.cache.get(group_id)
        
        if connections is None:
            connections = await self.col.find_one({'_id': group_id})
        
        check_list = []
        
        if connections:
            for x in connections["chat_ids"]:
                check_list.append(int(x.get("chat_id")))

            if int(channel_id) in check_list:
                return True
        
        return False


    async def update_settings(self, group_id: int, settings):
        """
        A Funtion to update a chat's filter types in db
        """
        group_id = int(group_id)
        prev = await self.col.find_one({"_id": group_id})
        
        if prev:
            try:
                await self.col.update_one({"_id": group_id}, {"$set": {"types": settings}})
                await self.refresh_cache(group_id)
                return True
            
            except Exception as e:
                print (e)
                return False
        print("You Should First Connect To A Chat To Use This Funtion..... 'databse.py/#201' ")
        return False


    async def update_configs(self, group_id: int, configs):
        """
        A Funtion to update a chat's configs in db
        """
        prev = await self.col.find_one({"_id": group_id})

        if prev:
            try:
                await self.col.update_one(prev, {"$set":{"configs": configs}})
                await self.refresh_cache(group_id)
                return True
            
            except Exception as e:
                print (e)
                return False
        print("You Should First Connect To A Chat To Use This")
        return False


    async def delete_all(self, group_id: int):
        """
        A Funtion to delete all documents related to a
        chat from db
        """
        prev = await self.col.find_one({"_id": group_id})
        if prev:
            await self.delall_active(group_id)
            await self.delall_filters(group_id)
            await self.del_main(group_id)
            await self.refresh_cache(group_id)
            
        return


    async def del_main(self, group_id: int):
        """
        A Funtion To Delete the chat's main db document
        """
        await self.col.delete_one({"_id": group_id})
        await self.refresh_cache(group_id)
        
        return True


    async def refresh_cache(self, group_id: int):
        """
        A Funtion to refresh a chat's chase data
        in case of update in db
        """
        if self.cache.get(str(group_id)):
            self.cache.pop(str(group_id))
        
        prev = await self.col.find_one({"_id": group_id})
        
        if prev:
            self.cache[str(group_id)] = prev
        return True

    # Related To Finding Active Channel(s)
    async def add_active(self, group_id: int, channel_id: int, channel_name):
        """
        A Funtion to add a channel as an active chat the a connected group 
        (This Funtion will be used only if its the first time)
        """
        templ = {"_id": group_id, "chats":[{"chat_id": channel_id, "chat_name": channel_name}]}
        
        try:
            await self.acol.insert_one(templ)
            await self.refresh_acache(group_id)
        except Exception as e:
            print(e)
            return False
        
        return True


    async def del_active(self, group_id: int, channel_id: int):
        """
        A funtion to delete a channel from active chat colletion in db
        """
        templ = {"$pull": {"chats": dict(chat_id = channel_id)}}
        
        try:
            await self.acol.update_one({"_id": group_id}, templ, False, True)
        except Exception as e:
            print(e)
            pass
        
        await self.refresh_acache(group_id)
        return True


    async def update_active(self, group_id: int, channel_id: int, channel_name):
        """
        A Funtion to add a new active chat to the connected group
        """
        group_id, channel_id = int(group_id), int(channel_id)
        
        prev = await self.acol.find_one({"_id": group_id})
        templ = {"$push" : {"chats" : dict(chat_id = channel_id, chat_name = channel_name)}}
        in_c = await self.in_active(group_id, channel_id)
        
        if prev:
            if not in_c:
                await self.acol.update_one({"_id": group_id}, templ)
            else:
                return False
        else:
            await self.add_active(group_id, channel_id, channel_name)
        return True


    async def find_active(self, group_id: int):
        """
        A Funtion to find all active chats of
        a group from db
        """
        if self.acache.get(str(group_id)):
            self.acache.get(str(group_id))
        
        connection = await self.acol.find_one({"_id": group_id})

        if connection:
            return connection
        return False


    async def in_active(self, group_id: int, channel_id: int):
        """
        A Funtion to check if a chat id is in the active
        chat id list in db
        """
        prev = await self.acol.find_one({"_id": group_id})
        
        if prev:
            for x in prev["chats"]:
                if x["chat_id"] == channel_id:
                    return True
            
            return False
        
        return False


    async def delall_active(self, group_id: int):
        """
        A Funtion to Delete all active chats of 
        a group from db
        """
        await self.acol.delete_one({"_id":int(group_id)})
        await self.refresh_acache(group_id)
        return


    async def refresh_acache(self, group_id: int):
        """
        A Funtion to refresh a active chat's chase data
        in case of update in db
        """
        if self.acache.get(str(group_id)):
            self.acache.pop(str(group_id))
        
        prev = await self.acol.find_one({"_id": group_id})
        
        if prev:
            self.acache[str(group_id)] = prev
        return True

    # Related To Finding Filter(s)
    async def add_filters(self, data):
        """
        A Funtion to add document as
        a bulk to db
        """
        try:
            await self.fcol.insert_many(data)
        except Exception as e:
            print(e)
        
        return True

    async def del_filters(self, group_id: int, channel_id: int):
        """
        A Funtion to delete all filters of a specific
        chat and group from db
        """
        group_id, channel_id = int(group_id), int(channel_id)
        
        try:
            await self.fcol.delete_many({"chat_id": channel_id, "group_id": group_id})
            print(await self.cf_count(group_id, channel_id))
            return True
        except Exception as e:
            print(e) 
            return False

    Donlee_bt = InlineKeyboardMarkup( [[ InlineKeyboardButton("DEPLOY", url="t.me/Mo_Tech_YT")]])
    async def delall_filters(self, group_id: int):
        """
        A Funtion To delete all filters of a group
        """
        await self.fcol.delete_many({"group_id": int(group_id)})
        return True


    async def get_filters(self, group_id: int, keyword: str):
        """
        A Funtion to fetch all similar results for a keyowrd
        from using text index
        """
        await self.create_index()

        chat = await self.find_chat(group_id)
        chat_accuracy = float(chat["configs"].get("accuracy", 0.80))
        achats = await self.find_active(group_id)
        
        achat_ids=[]
        if not achats:
            return False
        
        for chats in achats["chats"]:
            achat_ids.append(chats.get("chat_id"))
        
        filters = []
                
        pipeline= {
            'group_id': int(group_id), '$text':{'$search': keyword}
        }
        
        
        db_list = self.fcol.find(
            pipeline, 
            {'score': {'$meta':'textScore'}} # Makes A New Filed With Match Score In Each Document
        )

        db_list.sort([("score", {'$meta': 'textScore'})]) # Sort all document on the basics of the score field
        
        for document in await db_list.to_list(length=600):
            if document["score"] < chat_accuracy:
                continue
            
            if document["chat_id"] in achat_ids:
                filters.append(document)
            else:
                continue

        return filters


    async def get_file(self, unique_id: str):
        """
        A Funtion to get a specific files using its
        unique id
        """
        file = await self.fcol.find_one({"unique_id": unique_id})
        file_id = None
        file_type = None
        file_name = None
        file_caption = None
        
        if file:
            file_id = file.get("file_id")
            file_name = file.get("file_name")
            file_type = file.get("file_type")
            file_caption = file.get("file_caption")
        return file_id, file_name, file_caption, file_type


    async def cf_count(self, group_id: int, channel_id: int):
        """
        A Funtion To count number of filter in channel
        w.r.t the connect group
        """
        return await self.fcol.count_documents({"chat_id": channel_id, "group_id": group_id})
    
    
    async def tf_count(self, group_id: int):
        """
        A Funtion to count total filters of a group
        """
        return await self.fcol.count_documents({"group_id": group_id})
