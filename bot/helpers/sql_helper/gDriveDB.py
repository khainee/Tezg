from bot.helpers.sql_helper import url_parts

if url_parts.scheme in ['mongodb', 'mongodb+srv']:
    import pickle
    import threading
    from bot.helpers.sql_helper import gDrive

    INSERTION_LOCK = threading.RLock()

    def _set(chat_id, credential_string):
        with INSERTION_LOCK:
            filter_query = {'_id': chat_id}
            credential_string_pickle = pickle.dumps(credential_string)
            update_query = {'$set': {'credential_string': credential_string_pickle}}
            gDrive.update_one(filter_query, update_query, upsert=True)


    def search(chat_id):
        with INSERTION_LOCK:
            saved_cred = gDrive.find_one({'_id': chat_id})
            creds = None
            if saved_cred is not None:
                credential_string_pickle = saved_cred['credential_string']
                creds = pickle.loads(credential_string_pickle)
            return creds


    def _clear(chat_id):
        with INSERTION_LOCK:
            gDrive.delete_one({'_id': chat_id})

elif url_parts.scheme == 'postgresql':
    import pickle
    import threading
    from sqlalchemy import BigInteger, Column, LargeBinary
    from bot.helpers.sql_helper import BASE, SESSION

    class gDriveCreds(BASE):
        __tablename__ = "gDrive"
        chat_id = Column(BigInteger, primary_key=True)
        credential_string = Column(LargeBinary)


        def __init__(self, chat_id):
            self.chat_id = chat_id


    gDriveCreds.__table__.create(checkfirst=True)

    INSERTION_LOCK = threading.RLock()

    def _set(chat_id, credential_string):
        with INSERTION_LOCK:
            saved_cred = SESSION.query(gDriveCreds).get(chat_id)
            if not saved_cred:
                saved_cred = gDriveCreds(chat_id)

            saved_cred.credential_string = pickle.dumps(credential_string)

            SESSION.add(saved_cred)
            SESSION.commit()


    def search(chat_id):
        with INSERTION_LOCK:
            saved_cred = SESSION.query(gDriveCreds).get(chat_id)
            creds = None
            if saved_cred is not None:
                creds = pickle.loads(saved_cred.credential_string)
            return creds


    def _clear(chat_id):
        with INSERTION_LOCK:
            saved_cred = SESSION.query(gDriveCreds).get(chat_id)
            if saved_cred:
                SESSION.delete(saved_cred)
                SESSION.commit()
