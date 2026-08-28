import os

from pymongo import MongoClient
from gridfs import GridFS
from dotenv import load_dotenv


load_dotenv()


MONGODB_URI = os.getenv("MONGODB_URI")

if not MONGODB_URI:
    raise RuntimeError("MONGODB_URI is not configured")


MONGODB_DB = os.getenv(
    "MONGODB_DB",
    "agrivision"
)


client = MongoClient(MONGODB_URI)

db = client[MONGODB_DB]

fs = GridFS(db)

users = db["users"]

analyses = db["analyses"]
