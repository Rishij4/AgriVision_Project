import os
from pymongo import MongoClient
from gridfs import GridFS
from dotenv import load_dotenv
load_dotenv()
client=MongoClient(os.getenv("MONGODB_URI","mongodb://localhost:27017"))
db=client[os.getenv("MONGODB_DB","agrivision")]
fs=GridFS(db)
users=db["users"]
analyses=db["analyses"]
