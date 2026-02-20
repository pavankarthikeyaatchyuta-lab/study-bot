from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")

# Create client only if URI exists (prevents startup crash on Render)
client = MongoClient(MONGODB_URI) if MONGODB_URI else None

db = client["study_bot"] if client else None
chats_collection = db["chats"] if db else None