from Rocky_autofilter_Robot import environ
# Bot information
SESSION = 'Rocky_autofilter_Robot'
USER_SESSION = 'User_Bot'
API_ID = 12345
API_HASH = '0123456789abcdef0123456789abcdef'
BOT_TOKEN = '123456:Rocky_autofilter_Robot-zyx57W2v1u123ew11'
USERBOT_STRING_SESSION = 'Rocky_autofilter_Robot'

# Bot settings
CACHE_TIME = 300
USE_CAPTION_FILTER = False
PICS = (environ.get('PICS', 'https://telegra.ph/file/7e56d907542396289fee4.jpg https://telegra.ph/file/9aa8dd372f4739fe02d85.jpg https://telegra.ph/file/adffc5ce502f5578e2806.jpg https://telegra.ph/file/6937b60bc2617597b92fd.jpg https://telegra.ph/file/09a7abaab340143f9c7e7.jpg https://telegra.ph/file/5a82c4a59bd04d415af1c.jpg https://telegra.ph/file/323986d3bd9c4c1b3cb26.jpg https://telegra.ph/file/b8a82dcb89fb296f92ca0.jpg https://telegra.ph/file/31adab039a85ed88e22b0.jpg https://telegra.ph/file/c0e0f4c3ed53ac8438f34.jpg https://telegra.ph/file/eede835fb3c37e07c9cee.jpg https://telegra.ph/file/e17d2d068f71a9867d554.jpg https://telegra.ph/file/8fb1ae7d995e8735a7c25.jpg https://telegra.ph/file/8fed19586b4aa019ec215.jpg https://telegra.ph/file/8e6c923abd6139083e1de.jpg https://telegra.ph/file/0049d801d29e83d68b001.jpg')).split()

# Admins, Channels & Users
ADMINS = [12345789, 'admin123', 987654321]
CHANNELS = [-10012345678, -100987654321, 'gd_film']
AUTH_USERS = []
AUTH_CHANNEL = None

# MongoDB information
DATABASE_URI = "mongodb://[Rocky_autofilter_Robot:Rocky_autofilter_Robot@]host1[:port1][,...hostN[:portN]][/[defaultauthdb]?retryWrites=true&w=majority"
DATABASE_NAME = 'Rocky_autofilter_Robot'
COLLECTION_NAME = 'channel_files'  # If you are using the same database, then use different collection name for each bot

# Messages
START_MSG = """<b>👋𝙷𝚎𝚕𝚕𝚘 {},

𝙼𝚈 𝙽𝙰𝙼𝙴 𝙸𝚂 [Rocky autofilter Robot](https://t.me/Rocky_autofilterBOT)  𝙸 𝙲𝙰𝙽 𝙿𝚁𝙾𝚅𝙸𝙳𝙴 𝙼𝙾𝚅𝙸𝙴𝚂 𝙸𝙽 𝙼𝚈 𝙶𝚁𝙾𝚄𝙿 𝙾𝙽𝙻𝚈,
𝙸𝚃'𝚂 𝚅𝙴𝚁𝚈 𝙴𝙰𝚂𝚈. 𝙹𝚄𝚂𝚃 𝚈𝙾𝚄 𝙲𝙰𝙽 𝚂𝙴𝙰𝚁𝙲𝙷 𝙼𝙾𝚅𝙸𝙴 𝙸𝙽 𝙶𝚁𝙾𝚄𝙿 𝙰𝙽𝙳 𝙱𝙾𝚃 𝙸 𝚆𝙴𝙻𝙻 𝙿𝚁𝙾𝚅𝙸𝙳𝙴 𝙼𝙾𝚅𝙸𝙴𝚂 𝚃𝙷𝙴𝚁𝙴... 

𝚃𝚑𝚊𝚗𝚔 𝚈𝚘𝚞 𝙵𝚘𝚛 𝚁𝚎𝚚𝚞𝚎𝚜𝚝 𝙼𝚘𝚟𝚒𝚎𝚜 𝙰𝚗𝚢 𝙿𝚛𝚘𝚋𝚕𝚎𝚖 𝙲𝚘𝚗𝚝𝚊𝚌𝚝 𝙼𝚢 𝙱𝚘𝚜𝚜 𝙰𝚗𝚍 𝚁𝚎𝚚𝚞𝚎𝚜𝚝...😝

𝙼𝚊𝚒𝚗𝚝𝚊𝚒𝚗𝚎𝚍 𝙱𝚢 𝙼𝚢 𝙱𝚘𝚜𝚜 ☛[𝑺𝒂𝒄𝒉𝒊𝒏 𝑺](https://t.me/sachin_official_admin)
"""

SHARE_BUTTON_TEXT = 'Checkout {username} for searching files'
INVITE_MSG = 'Please join @.... to use this bot'
