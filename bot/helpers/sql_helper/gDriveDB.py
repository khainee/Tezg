import pickle
from bot.helpers.sql_helper import gDrive

def _set(chat_id, credential_string):
    filter_query = {'_id': chat_id}
    credential_string_pickle = pickle.dumps(credential_string)
    update_query = {'$set': {'credential_string': credential_string_pickle}}
    gDrive.update_one(filter_query, update_query, upsert=True)

def search(chat_id):
    saved_cred = gDrive.find_one({'_id': chat_id})
    creds = None
    if saved_cred is not None:
        credential_string_pickle = saved_cred['credential_string']
        creds = pickle.loads(credential_string_pickle)
    return creds

def _clear(chat_id):
    gDrive.delete_one({'_id': chat_id})
