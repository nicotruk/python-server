from flask import Flask
from flask_restful import Api

from model.mongodb import mongo
from resources.user_resource import SingleUserResource
#from resources.user_resource import UsersCountResource
from resources.user_resource import UsersResource

app = Flask("python_server")

api = Api(app, prefix="/api/v1")

# connect to another MongoDB database
app.config['MONGO_DBNAME'] = 'python_server'
mongo.init_app(app, config_prefix='MONGO')

api.add_resource(UsersResource, '/users')
#api.add_resource(UsersCountResource, '/users/count')
api.add_resource(SingleUserResource, '/users/<user_id>')
api.add_resource(CatResource, '/cats')

@app.route('/')
def hello_world():
    return "Hi, I'm a Python Server!"


if __name__ == '__main__':
    app.run()
