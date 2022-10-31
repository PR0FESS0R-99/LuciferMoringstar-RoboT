# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) @PR0FESS0R-99

from pyrogram import Client, enums, __version__
from simple_configs import Config

class lucifermoringstar_robot(Client):

    def __init__(self):
        super().__init__(
            "LuciferMoringstar-Robot",
            api_hash=Config.TG_API_HASH,
            api_id=Config.TG_API_ID,
            plugins={
                "root": "./plugins"
            },
            workers=200,
            bot_token=Config.TG_BOT_TOKEN,
            sleep_threshold=10
        )

    async def start(self):
        await super().start()
        bot_details = await self.get_me()
        print("Bot Start")
        
    async def stop(self, *args):
        await super().stop()
        print("Bot stopped. Bye.")
