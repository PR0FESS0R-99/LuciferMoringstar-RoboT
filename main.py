import logging
import logging.config

# Get logging configurations
logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.ERROR)

from pyrogram import Client, __version__
from pyrogram.raw.all import layer
from LuciferMoringstar_Robot.database.autofilter_db import Media
from config import API_ID, API_HASH, B_KEYS, bot_info
import pyromod.listen

class LuciferMoringstar(Client):

    def __init__(self):
        super().__init__(
            "LuciferMoringstar_Robot",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=B_KEYS,
            workers=50,
            plugins={"root": "LuciferMoringstar_Robot"},
            sleep_threshold=5,
        )

    async def start(self):
        await super().start()
        await Media.ensure_indexes()       
        me = await self.get_me()
        bot_info.BOT_USERNAME = me.username
        bot_info.BOT_NAME = me.first_name
        self.username = '@' + me.username
        print(f"{me.first_name} with for Pyrogram v{__version__} (Layer {layer}) started on {me.username}.")

    async def stop(self, *args):
        await super().stop()
        print("Bot stopped. Bye.")


app = LuciferMoringstar()
app.run()
