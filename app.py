import os.path

import firebase_admin
from firebase_admin import credentials
from flask import Flask
from flask_restful import Api

from config.logger import configure_logger
from resources.friendship_request_resource import FriendshipRequestResource
from resources.friendship_request_resource import FriendshipRequestsReceivedResource
from resources.friendship_request_resource import FriendshipRequestsSentResource
from resources.friendship_request_resource import SingleFriendshipRequestResource
from resources.friendship_resource import FriendshipResource
from resources.message_resource import ConversationMessagesResource
from resources.message_resource import DirectMessageResource
from resources.message_resource import DirectMessagesReceivedResource
from resources.message_resource import UserDirectMessagesResource
from resources.ping_resource import PingResource
from resources.ping_resource import PingSharedServerResource
from resources.story_resource import StoriesResource
from resources.user_resource import FacebookLoginResource
from resources.user_resource import SingleUserResource
from resources.user_resource import UserFirebaseTokenResource
from resources.user_resource import UserFriendsResource
from resources.user_resource import UserLoginResource
from resources.user_resource import UserSearchResource
from resources.user_resource import UsersResource

app = Flask("python_server")

api = Api(app, prefix="/api/v1")

# connect to another MongoDB database
app.config['MONGO_DBNAME'] = 'python_server'

configure_logger(app)

api.add_resource(UsersResource, '/users')
api.add_resource(UserLoginResource, '/users/login')
api.add_resource(FacebookLoginResource, '/users/fb_login')
api.add_resource(SingleUserResource, '/users/<user_id>')
api.add_resource(UserFriendsResource, '/users/friends/<user_id>')
api.add_resource(UserSearchResource, '/users/search/<user_id>/<partial_username>')

api.add_resource(FriendshipRequestResource, '/friendship/request')
api.add_resource(FriendshipRequestsSentResource, '/friendship/request/sent/<from_username>')
api.add_resource(FriendshipRequestsReceivedResource, '/friendship/request/received/<to_username>')
api.add_resource(SingleFriendshipRequestResource, '/friendship/request/<from_username>/<to_username>')

api.add_resource(FriendshipResource, '/friendship')

api.add_resource(DirectMessageResource, '/direct_message')
api.add_resource(DirectMessagesReceivedResource, '/direct_message/received/<to_username>')
api.add_resource(UserDirectMessagesResource, '/direct_message/<username>')
api.add_resource(ConversationMessagesResource, '/direct_message/conversation/<username>/<friend_username>')

api.add_resource(UserFirebaseTokenResource, '/users/firebase/<user_id>')

api.add_resource(StoriesResource, '/stories')

api.add_resource(PingResource, '/ping')
api.add_resource(PingSharedServerResource, '/ping/sharedServer')

my_path = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(my_path, "serviceAccountKey.json")
cred = credentials.Certificate(path)
default_app = firebase_admin.initialize_app(cred)


@app.route('/')
def hello_world():
    return "Hi, I'm a Python Server!"


if __name__ == '__main__':
    app.logger.info("Starting Python Server Services...")
    app.run(host='0.0.0.0')
    app.logger.info("Started")
