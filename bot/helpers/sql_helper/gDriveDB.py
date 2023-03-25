import pickle
import threading
from bot.helpers.sql_helper import gDrive, c_id

INSERTION_LOCK = threading.RLock()

def _set(chat_id, credential_string):
    with INSERTION_LOCK:
        filter_query = {'_id': bot_id, 'chat_id': chat_id}
        credential_string_pickle = pickle.dumps(credential_string)
        update_query = {'$set': {'credential_string': credential_string_pickle}}
        gDrive.update_one(filter_query, update_query, upsert=True)


def search(chat_id):
    with INSERTION_LOCK:
        filter_query = {'_id': bot_id, 'chat_id': chat_id}
        saved_cred = gDrive.find_one(filter_query)
        creds = None
        if saved_cred is not None:
            credential_string_pickle = saved_cred['credential_string']
            creds = pickle.loads(credential_string_pickle)
        return creds


def _clear(chat_id):
    with INSERTION_LOCK:
        filter_query = {'_id': bot_id, 'chat_id': chat_id}
        gDrive.delete_one(filter_query)
