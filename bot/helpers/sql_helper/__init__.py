from pymongo import MongoClient
from bot import DATABASE_URL, LOGGER, BOT_TOKEN

if DATABASE_URL is None:
    LOGGER.warning("DATABASE_URL is not set. The application cannot function without a database.")
    exit(1)

client = MongoClient(DATABASE_URL)
db = client["DRIVE_X"]
parent_id = db["ParentID"]
gDrive = db['gDriveCreds']
bot_id = BOT_TOKEN.split(':', 1)[0]

