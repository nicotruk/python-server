import json
import time

from firebase_admin import messaging
from flask import request, jsonify, make_response, current_app
from flask_restful import Resource

import config.firebase_config
from config.firebase_config import NOTIFICATION_TYPE_MESSAGE
from model.direct_message import DirectMessage
from model.firebase_manager import FirebaseManager
from model.stats import StatManager
from model.user import User, UserNotFoundException
from resources.error_handler import ErrorHandler
from resources.token_validation_decorator import token_validation_required


class DirectMessageResource(Resource):

    @token_validation_required
    def post(self):
        try:
            current_app.logger.info("Received DirectMessageResource POST Request")
            StatManager.create(request.environ["PATH_INFO"] + " " + request.environ["REQUEST_METHOD"])
            request_data = json.loads(request.data)
            User.get_user_by_username(request_data["to_username"])
            direct_message_created = DirectMessage.create(request_data["from_username"],
                                                          request_data["to_username"],
                                                          request_data["message"],
                                                          int(round(time.time() * 1000)))
            if direct_message_created is None:
                raise ValueError('DB error')
            else:
                if config.firebase_config.FIREBASE_NOTIFICATIONS_ENABLED is True:
                    FirebaseManager.send_firebase_message(request_data["from_username"], request_data["to_username"],
                                                          request_data["message"], NOTIFICATION_TYPE_MESSAGE)
                current_app.logger.debug("Python Server Response: 201 - %s", direct_message_created)
                return make_response(jsonify(direct_message_created), 201)
        except ValueError:
            error = "Unable to handle DirectMessageResource POST Request"
            current_app.logger.error("Python Server Response: 500 - %s", error)
            return ErrorHandler.create_error_response(500, error)
        except UserNotFoundException:
            error = "Unable to send message - User not found"
            current_app.logger.error("Python Server Response: 403 - %s", error)
            return ErrorHandler.create_error_response(403, error)
        except messaging.ApiCallError:
            error = "Unable to send Firebase Notification - ApiCallError"
            current_app.logger.error("Python Server Response: 409 - %s", error)
            return ErrorHandler.create_error_response(409, error)


class DirectMessagesReceivedResource(Resource):

    @token_validation_required
    def get(self, to_username):
        try:
            current_app.logger.info("Received DirectMessagesReceivedResource - received requests - GET Request")
            StatManager.create(request.environ["PATH_INFO"] + " " + request.environ["REQUEST_METHOD"])
            direct_messages = DirectMessage.get_received_direct_messages(to_username)
            current_app.logger.debug("Python Server Response: 200 - %s", direct_messages)
            return make_response(jsonify(direct_messages), 200)
        except ValueError:
            error = "Unable to handle DirectMessagesReceivedResource - received requests - GET Request"
            current_app.logger.error("Python Server Response: %s - %s", 500, error)
            return ErrorHandler.create_error_response(500, error)


class UserDirectMessagesResource(Resource):

    @token_validation_required
    def get(self, username):
        try:
            current_app.logger.info("Received UserDirectMessagesResource - received requests - GET Request")
            StatManager.create(request.environ["PATH_INFO"] + " " + request.environ["REQUEST_METHOD"])
            direct_messages = DirectMessage.get_user_direct_messages_sorted_by_timestamp(username)
            current_app.logger.debug("Python Server Response: 200 - %s", direct_messages)
            return make_response(jsonify(direct_messages), 200)
        except UserNotFoundException:
            error = "Unable to find a User with the parameters given. ConversationMessagesResource POST Request"
            current_app.logger.error("Python Server Response: 403 - %s", error)
            return ErrorHandler.create_error_response(403, error)
        except ValueError:
            error = "Unable to handle UserDirectMessagesResource - received requests - GET Request"
            current_app.logger.error("Python Server Response: %s - %s", 500, error)
            return ErrorHandler.create_error_response(500, error)


class ConversationMessagesResource(Resource):

    @token_validation_required
    def get(self, username, friend_username):
        try:
            current_app.logger.info("Received ConversationMessagesResource - received requests - GET Request")
            StatManager.create(request.environ["PATH_INFO"] + " " + request.environ["REQUEST_METHOD"])
            direct_messages = DirectMessage.get_conversation_messages_sorted_by_timestamp(username, friend_username)
            current_app.logger.debug("Python Server Response: 200 - %s", direct_messages)
            return make_response(jsonify(direct_messages), 200)
        except UserNotFoundException:
            error = "Unable to find a User with the parameters given. ConversationMessagesResource POST Request"
            current_app.logger.error("Python Server Response: 403 - %s", error)
            return ErrorHandler.create_error_response(403, error)
        except ValueError:
            error = "Unable to handle ConversationMessagesResource - received requests - GET Request"
            current_app.logger.error("Python Server Response: %s - %s", 500, error)
            return ErrorHandler.create_error_response(500, error)
