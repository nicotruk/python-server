import logging

from flask import Flask
from flask_restful import Api

from model.logging import configure_logger
from resources.ping_resource import PingResource
from resources.ping_resource import PingSharedServerResource
from resources.user_resource import SingleUserResource
from resources.user_resource import UserLoginResource
# from resources.user_resource import UsersCountResource
from resources.user_resource import UsersResource

app = Flask("python_server")

api = Api(app, prefix="/api/v1")

# connect to another MongoDB database
app.config['MONGO_DBNAME'] = 'python_server'

api.add_resource(UsersResource, '/users')
api.add_resource(UserLoginResource, '/users/login')
# api.add_resource(UsersCountResource, '/users/count')
api.add_resource(SingleUserResource, '/users/<user_id>')

api.add_resource(PingResource, '/ping')
api.add_resource(PingSharedServerResource, '/pingSharedServer')


@app.route('/')
def hello_world():
    return "Hi, I'm a Python Server!"


if __name__ == '__main__':
    configure_logger()
    logging.info("Starting Python Server Services...")
    app.run(host='0.0.0.0')
    logging.info("Started")
