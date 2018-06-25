import os.path

import firebase_admin
from firebase_admin import credentials
from flask import Flask, Blueprint
from flask_restful import Api

from config.app_config import APP_NAME
from config.app_config import APP_PREFIX
from config.mongodb import MONGO_DB_NAME
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
from resources.story_resource import SingleStoryResource
from resources.file_resource import FileResource
from resources.user_resource import FacebookLoginResource
from resources.user_resource import SingleUserResource
from resources.user_resource import UserFirebaseTokenResource
from resources.user_resource import UserFriendsResource
from resources.user_resource import UserLoginResource
from resources.user_resource import UserSearchResource
from resources.user_resource import UsersResource
from resources.user_resource import UsersCountResource
from resources.stats_resource import StatsResource
from resources.stats_resource import LastXMinStatsResource
from resources.stats_resource import Last10DaysStoriesRequestsStatsResource

app = Flask(APP_NAME)
api_bp = Blueprint('api', APP_NAME)
api = Api(api_bp, prefix=APP_PREFIX)

# connect to another MongoDB database
app.config['MONGO_DBNAME'] = MONGO_DB_NAME

configure_logger(app)

# noinspection PyTypeChecker
api.add_resource(UsersResource, '/users')
# noinspection PyTypeChecker
api.add_resource(UsersCountResource, '/users/count')
# noinspection PyTypeChecker
api.add_resource(UserLoginResource, '/users/login')
# noinspection PyTypeChecker
api.add_resource(FacebookLoginResource, '/users/fb_login')
# noinspection PyTypeChecker
api.add_resource(SingleUserResource, '/users/<user_id>')
# noinspection PyTypeChecker
api.add_resource(UserFriendsResource, '/users/friends/<user_id>')
# noinspection PyTypeChecker
api.add_resource(UserSearchResource, '/users/search/<user_id>/<query>')

# noinspection PyTypeChecker
api.add_resource(FriendshipRequestResource, '/friendship/request')
# noinspection PyTypeChecker
api.add_resource(FriendshipRequestsSentResource, '/friendship/request/sent/<from_username>')
# noinspection PyTypeChecker
api.add_resource(FriendshipRequestsReceivedResource, '/friendship/request/received/<to_username>')
# noinspection PyTypeChecker
api.add_resource(SingleFriendshipRequestResource, '/friendship/request/<from_username>/<to_username>')

# noinspection PyTypeChecker
api.add_resource(FriendshipResource, '/friendship')

# noinspection PyTypeChecker
api.add_resource(DirectMessageResource, '/direct_message')
# noinspection PyTypeChecker
api.add_resource(DirectMessagesReceivedResource, '/direct_message/received/<to_username>')
# noinspection PyTypeChecker
api.add_resource(UserDirectMessagesResource, '/direct_message/<username>')
# noinspection PyTypeChecker
api.add_resource(ConversationMessagesResource, '/direct_message/conversation/<username>/<friend_username>')

# noinspection PyTypeChecker
api.add_resource(UserFirebaseTokenResource, '/users/firebase/<user_id>')

# noinspection PyTypeChecker
api.add_resource(StoriesResource, '/stories')
# noinspection PyTypeChecker
api.add_resource(SingleStoryResource, '/stories/<story_id>')
# noinspection PyTypeChecker
api.add_resource(FileResource, '/stories/<story_id>/files')

# noinspection PyTypeChecker
api.add_resource(PingResource, '/ping')
# noinspection PyTypeChecker
api.add_resource(PingSharedServerResource, '/ping/sharedServer')

# noinspection PyTypeChecker
api.add_resource(StatsResource, '/stats')
# noinspection PyTypeChecker
api.add_resource(LastXMinStatsResource, '/stats/last/<minutes>')
# noinspection PyTypeChecker
api.add_resource(Last10DaysStoriesRequestsStatsResource, '/stats/stories')

app.register_blueprint(api_bp)

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
