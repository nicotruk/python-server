from flask import Flask
from flask_pymongo import PyMongo
from flask_restful import Api
from model.user import User

app = Flask("python_server")

api = Api(app, prefix="/api/v1")

# connect to another MongoDB database on the same host
app.config['MONGO_DBNAME'] = 'python_server'
mongo = PyMongo(app, config_prefix='MONGO')


@app.route('/')
def hello_world():
    usersCount = mongo.db.users.count()
    print "Users count : {}".format(usersCount)
    user = User("1", "nico", "truksinas")

    mongo.db.users.insert(user.encode_user())
    usersCount = mongo.db.users.count()
    print "Users count : {}".format(usersCount)
    return "Hi, I'm root!"


if __name__ == '__main__':
    app.run()