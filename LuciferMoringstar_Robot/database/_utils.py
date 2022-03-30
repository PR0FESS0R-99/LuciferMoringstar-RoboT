import logging

from pyrogram.errors import UserNotParticipant

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
