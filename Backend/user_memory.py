from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client["neuroguide"]
collection = db["user_data"]


def save_feedback(user_id, technique, liked=True):
    collection.update_one(
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
    user = collection.find_one({"user_id": user_id})

    if not user:
        return []

    return user.get("history", [])