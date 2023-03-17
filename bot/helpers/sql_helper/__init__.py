from urllib.parse import urlparse

if DATABASE_URL is None:
    LOGGER.warning("DATABASE_URL is not set. The application cannot function without a database.")
    exit(1)

url_parts = urlparse(DATABASE_URL)

if url_parts.scheme in ['mongodb', 'mongodb+srv']:
    from pymongo import MongoClient
    from bot import DATABASE_URL, LOGGER

    client = MongoClient(DATABASE_URL)
    db = client["DRIVE_X"]
    parent_id = db["ParentID"]
    gDrive = db['gDriveCreds']
elif url_parts.scheme == 'postgresql':
    from sqlalchemy import create_engine
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker, scoped_session
    from bot import DATABASE_URL, LOGGER


    def start() -> scoped_session:
      try:
        engine = create_engine(DATABASE_URL)
        BASE.metadata.bind = engine
        BASE.metadata.create_all(engine)
        return scoped_session(sessionmaker(bind=engine, autoflush=False))
      except ValueError:
        LOGGER.error('Invalid DATABASE_URL : Exiting now.')
        exit(1)


    BASE = declarative_base()
    SESSION = start()
    else:
        LOGGER.warning("Unsupported database type in DATABASE_URL. The application cannot function without a supported database.")
        exit(1)
