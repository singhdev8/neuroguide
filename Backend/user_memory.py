from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

_client = None
_collection = None

def get_collection():
    global _client, _collection
    if _collection is None:
        _client = MongoClient(os.getenv("MONGO_URI"))
        db = _client["neuroguide"]
        _collection = db["user_data"]
    return _collection

def save_feedback(user_id, technique, liked=True):
    get_collection().update_one(
        {"user_id": user_id},
        {"$push": {
            "history": {
                "technique": technique,
                "liked": liked
            }
        }},
        upsert=True
    )

def get_user_history(user_id):
    user = get_collection().find_one({"user_id": user_id})
    if not user:
        return []
    return user.get("history", [])