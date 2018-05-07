import os
from pymongo import MongoClient

if "MONGO_URL" in os.environ:
    mongo_uri = os.environ['MONGO_URL'] + ":" + os.environ['MONGO_PORT']
else:
    mongo_uri = "mongodb://localhost:27017"

mongo = MongoClient(mongo_uri)
db = mongo['heroku_5d6zh6jz']
