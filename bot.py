import logging
import os
import asyncio
from pyrogram import Client, idle
from pyrogram.errors import BadMsgNotification

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Load the correct config file
if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

# Ensure necessary directories exist
for directory in [Config.DOWNLOAD_LOCATION, Config.ADMIN_LOCATION, Config.CREDENTIALS_LOCATION]:
    os.makedirs(directory, exist_ok=True)

# Define Pyrogram client
app = Client(
    "Mega_Link_Downloader_Bot",
    bot_token=Config.TG_BOT_TOKEN,
    api_id=Config.APP_ID,
    api_hash=Config.API_HASH,
    plugins=dict(root="plugins"),
)

async def start_bot():
    try:
        async with app:
            logger.info("Bot started successfully.")
            await idle()  # Keep the bot running
    except BadMsgNotification as e:
        if "[16] The msg_id is too low" in str(e):
            logger.error("Time sync issue detected! Deleting session file and restarting...")
            try:
                os.remove("Mega_Link_Downloader_Bot.session")
                logger.info("Old session file deleted. Restarting bot...")
            except FileNotFoundError:
                logger.warning("No old session file found to delete.")
            await asyncio.sleep(2)  # Small delay before retrying
            await start_bot()  # Restart bot
        else:
            logger.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    asyncio.run(start_bot())

