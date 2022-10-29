from pyrogram import Client, filters
from simple_configs import Config

PR0FESS0R_99 = Client(name="LuciferMoringstar-RoboT", api_id=Config.TG_API_ID, api_hash=Config.TG_API_HASH, bot_token=Config.TG_BOT_TOKEN)

@PR0FESS0R_99.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("Hi Broh")

PR0FESS0R_99.run()
