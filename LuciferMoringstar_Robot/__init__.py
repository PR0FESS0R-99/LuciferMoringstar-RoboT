# MIT License
# Copyright (c) 2022 Muhammed
from os import environ
from config import ( is_enabled, search, AUTH_GROUPS, AUTH_USERS, ADMINS, SUPPORT_CHAT, CREATOR_USERNAME, CREATOR_NAME, AUTH_CHANNEL,
    PICS, BOT_TOKEN, API_ID, API_HASH, DATABASE_NAME, DATABASE_URI, CHANNELS, LOG_CHANNEL, FILTER_BUTTONS, GET_FILECHANNEL, FILTER_DEL_SECOND )
from .translation import SPELLMODE_MESSAGE, WELCOME_MESSAGE, REQUEST_MESSAGE, FILECAPTION_MESSAGE, START_MESSAGE

# UserAccount
API_HASH = API_HASH
API_ID = API_ID
# Creator
CREATOR_NAME = CREATOR_NAME
CREATOR_USERNAME = CREATOR_USERNAME
# About Bot
BOT_TOKEN = BOT_TOKEN
PICS = PICS.split()
START_MESSAGE = environ.get('START_MESSAGE', START_MESSAGE)
# DataBase
DATABASE_NAME = DATABASE_NAME 
DATABASE_URI = DATABASE_URI
# Channels & Admins
CHANNELS = CHANNELS
LOG_CHANNEL = int(LOG_CHANNEL)
ADMINS = [int(admin) if search.search(admin) else admin for admin in ADMINS.split()]
AUTH_GROUPS = [int(admin) for admin in AUTH_GROUPS.split()]
AUTH_USERS = (AUTH_USERS + ADMINS) if AUTH_USERS else []
AUTH_CHANNEL = int(AUTH_CHANNEL) if AUTH_CHANNEL and search.search(AUTH_CHANNEL) else None
SUPPORT = SUPPORT_CHAT
GET_FILECHANNEL = int(GET_FILECHANNEL)
# Cache Time
CACHE_TIME = int(environ.get('CACHE_TIME', 300))
" FILES "
CUSTOM_FILE_CAPTION = environ.get("CUSTOM_FILE_CAPTION", FILECAPTION_MESSAGE)
PROTECT_FILES = "False"
FILTER_DEL_SECOND = FILTER_DEL_SECOND
" IMDB FUNCTIONS "
LONG_IMDB_DESCRIPTION = is_enabled(environ.get("LONG_IMDB_DESCRIPTION", "False"), False)
MAX_LIST_ELM = environ.get("MAX_LIST_ELM", None)

COMMANDS = ["pmautofilter", "connections", "delete"]

SINGLE_BUTTON = is_enabled((environ.get('SINGLE_BUTTON', "True")), True)
REQUEST_MOVIE = is_enabled((environ.get('REQUEST_MOVIE', "True")), True)
MOVIE_TEXT = environ.get("REQUEST_MESSAGE", REQUEST_MESSAGE)
SPELL_MODE = is_enabled((environ.get('SPELL_MODE', "True")), True)
SPELL_TEXT = environ.get("SPELLMODE_MESSAGE", SPELLMODE_MESSAGE)
MELCOW_NEW_USERS = is_enabled((environ.get('MELCOW_NEW_USERS', "True")), True)
WELCOME_TEXT = environ.get("WELCOME_MESSAGE", WELCOME_MESSAGE)
SAVE_FILES = is_enabled((environ.get('PROTECT_FILES', PROTECT_FILES)), PROTECT_FILES)
FILE_MODE = is_enabled((environ.get('FILE_MODE', "True")), True)


class temp(object):
    BANNED_USERS = []
    ME = None # User Id
    Bot_Username = None # Username
    Bot_Name = "LuciferMoringstar" # Full Name 
    BUTTONS = {} # AutoFilter
    CURRENT = int(environ.get("SKIP", 2)) # Skip Files
    CANCEL = False # Cancel Index
    PYRO_VERSION = "2.0.27"
    PY3_VERSION = "3.0.13"
    BOT_VERSION = "1.0.2"
    PMAF_OFF = []
    filterBtns = int(FILTER_BUTTONS)
    broadcast_ids = {} # don't change this..!!   

class emoji(object):
    GOAL_E_MOJI = "⚽"
    TRY_YOUR_LUCK = "🎰"
    THROW_DART = "🎯"

