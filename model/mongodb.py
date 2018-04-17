import os
import pprint
from pymongo import MongoClient

#mongo_uri = "mongodb://grupo2:123@ds249269.mlab.com:49269/heroku_5d6zh6jz"
mongo_uri = os.environ['DB_PORT_27017_TCP_ADDR']+":"+os.environ['MONGO_PORT']

mongo = MongoClient(mongo_uri)
db = mongo['heroku_5d6zh6jz']