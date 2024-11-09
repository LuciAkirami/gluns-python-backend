import os
from pymongo import MongoClient
from bson.objectid import ObjectId

DATABASE_URL = os.getenv("DATABASE_URL", "mongodb://db:27017")
client = MongoClient(DATABASE_URL)
db = client["llm_database"]
collection = db["user_contexts"]

def store_user_context(data: dict):
    """Store LLM response or user context in the database."""
    try:
        collection.insert_one(data)
        print("Data stored successfully.")
    except Exception as e:
        print(f"Error storing data: {e}")

def get_user_context(user_id: str):
    """Retrieve user context from the database by user ID."""
    try:
        return collection.find_one({"user_id": user_id})
    except Exception as e:
        print(f"Error retrieving data: {e}")
        return None
