from pymongo import MongoClient
from bot import DATABASE_URL, LOGGER, G_DRIVE_CLIENT_ID

if DATABASE_URL is None:
    LOGGER.warning("DATABASE_URL is not set. The application cannot function without a database.")
    exit(1)

client = MongoClient(DATABASE_URL)
db = client["DRIVE_X"]
parent_id = db["ParentID"]
gDrive = db['gDriveCreds']
c_id = G_DRIVE_CLIENT_ID.split('-', 1)[0]

