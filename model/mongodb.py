import os
from pymongo import MongoClient

mongo_uri = "mongodb://grupo2:123@ds249269.mlab.com:49269/heroku_5d6zh6jz"

mongo = MongoClient(mongo_uri)
db = mongo['heroku_5d6zh6jz']