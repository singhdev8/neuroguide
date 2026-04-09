from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["neuroguide"]

print("TEST COLLECTION:", list(db["test"].find()))
print("USER DATA:", list(db["user_data"].find()))