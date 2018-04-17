import os
from pymongo import MongoClient

mongo = MongoClient(os.environ['DB_PORT_27017_TCP_ADDR'],27017)
db = mongo.python_server