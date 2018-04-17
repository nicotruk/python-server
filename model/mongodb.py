import os
from pymongo import MongoClient

mongo = MongoClient(os.environ['MONGO_URL'],27017)
db = mongo.python_server