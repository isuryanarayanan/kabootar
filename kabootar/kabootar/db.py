import os
from pymongo import MongoClient

mongodb_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
mongodb_db = os.getenv("MONGODB_DB", "local")

client = MongoClient(mongodb_uri)
db = client[mongodb_db]
