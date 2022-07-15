import logging
import logging.config

# Get logging configurations
logging.config.fileConfig('logger.file')
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("imdbpy").setLevel(logging.ERROR)

from pyrogram import Client, __version__
from pyrogram.raw.all import layer
from database.autofilter_mdb import Media
from LuciferMoringstar_Robot import API_ID, API_HASH, BOT_TOKEN, temp

class Bot(Client):

    def __init__(self):
        super().__init__(
            "LuciferMoringstar_Robot",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=50,
            plugins={"root": "LuciferMoringstar_Robot"},
            sleep_threshold=5,
        )

    async def start(self):
        await super().start()
        await Media.ensure_indexes()
        me = await self.get_me()
        temp.PYRO_VERSION = __version__
        temp.ME = me.id
        temp.Bot_Username = me.username
        temp.Bot_Name = me.first_name
        self.username = '@' + me.username
        logging.info(f"{me.first_name} with for Pyrogram v{__version__} (Layer {layer}) Started on @{me.username}")                

    async def stop(self, *args):
        await super().stop()
        logging.info("Bot stopped. Bye.")


app = Bot()
app.run()
