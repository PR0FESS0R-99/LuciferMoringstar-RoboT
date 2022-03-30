import logging, os, traceback

from pyrogram.errors import UserNotParticipant, FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid
from config import FORCES_SUB

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# ~~~~ File Size ~~~~ #

def get_size(size):
    """Get size in readable format"""

    units = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB"]
    size = float(size)
    i = 0
    while size >= 1024.0 and i < len(units):
        i += 1
        size /= 1024.0
    return "%.2f %s" % (size, units[i])

# ~~~~ AutoFilter Buttons ~~~~ #

def split_list(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

# ~~~~ Forces Subs ~~~~ #

async def is_subscribed(bot, query):
    try:
        user = await bot.get_chat_member(FORCES_SUB, query.from_user.id)
    except UserNotParticipant:
        pass
    except Exception as e:
        logger.exception(e)
    else:
        if not user.status == 'kicked':
            return True

    return False

# ~~~~ Broadcast Message ~~~~ #

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

# ~~~~ Collections ~~~~ #

class lucifer_temp(object):
    ME = None # User Id
    U_NAME = None # Username
    B_NAME = None # Full Name 
    BUTTONS = {} # AutoFilter
    CURRENT=int(os.environ.get("SKIP", 2)) # Skip Files
    CANCEL = False # Cancel Index


