# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) @PR0FESS0R-99

from pyrogram import Client, enums, __version__
from simple_configs import Config

lucifermoringstar_robot = Client(
  name="LuciferMoringstar-Robot",
  api_hash=Config.TG_API_HASH,
  api_id=Config.TG_API_ID,
  bot_token=Config.TG_BOT_TOKEN,
  plugins={"root": "LuciferMoringstar_Robot/plugins"},
  sleep_threshold=10,
  workers=200
)
