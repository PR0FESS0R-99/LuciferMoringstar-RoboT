# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) @PR0FESS0R-99

from pyrogram.raw.all import layer
from pyrogram import Client, __version__
from simple_configs import Config

Lucifermoringstar_Robot = Client(
  name="lucifer-bot",
  api_hash=Config.TG_API_HASH,
  api_id=Config.TG_API_ID,
  bot_token=Config.TG_BOT_TOKEN
)

print(f"""
🤖 Lucifermoringstar-Robot based on Pyrogram v{__version__}
(Layer {layer}) started on @{usr_bot_me.username}    
""")

Lucifermoringstar_Robot.run()
