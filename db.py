from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")

client = MongoClient(MONGODB_URI) if MONGODB_URI else None
db = client["study_bot"] if client is not None else None
chats_collection = db["chats"] if db is not None else None