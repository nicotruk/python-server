import os
from pymongo import MongoClient

# mongo_uri = os.environ['MONGO_URL'] + ":" + os.environ['MONGO_PORT']

# Para correr el comando pytest localmente, comentar la linea anterior y descomentar la siguiente.
mongo_uri = "mongodb://localhost:27017"

mongo = MongoClient(mongo_uri)
db = mongo['heroku_5d6zh6jz']
