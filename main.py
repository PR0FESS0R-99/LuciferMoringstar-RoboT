# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) @PR0FESS0R-99

from pyrogram import Client, __version__
from simple_configs import Config

class lucifermoringstar_robot(Client):

    def __init__(self):
        super().__init__(
            name="lucifer-bot",
            plugins=("root": "LuciferMoringstar_Robot"),
            api_hash=Config.TG_API_HASH,
            api_id=Config.TG_API_ID,
            bot_token=Config.TG_BOT_TOKEN,
            sleep_threshold=60,
            workers=50
        )

    async def start(self):
        await super().start()
        usr_bot_me = self.me
        print(
            f"🤖 Lucifermoringstar-Robot based on Pyrogram v{__version__}"
            f"(Layer {layer}) started on @{usr_bot_me.username}. "       
        )

    async def stop(self, *args):
        await super().stop()
        print("🤖 Lucifermoringstar-Robot stopped. Bye.")

lucifermoringstar_robot().run()
