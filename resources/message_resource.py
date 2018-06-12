import json
import time

from firebase_admin import messaging
from flask import request, jsonify, make_response, current_app
from flask_restful import Resource

import config.firebase_config
from config.firebase_config import NOTIFICATION_TYPE_MESSAGE
from model.direct_message import DirectMessage
from model.firebase_manager import FirebaseManager
from model.user import UserNotFoundException
from resources.error_handler import ErrorHandler


class DirectMessageResource(Resource):

    def post(self):
        try:
            current_app.logger.info("Received DirectMessageResource POST Request")
            request_data = json.loads(request.data)
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
            error = "Unable to send Firebase Notification - User not found"
            current_app.logger.error("Python Server Response: 409 - %s", error)
            return ErrorHandler.create_error_response(409, error)
        except messaging.ApiCallError:
            error = "Unable to send Firebase Notification - ApiCallError"
            current_app.logger.error("Python Server Response: 409 - %s", error)
            return ErrorHandler.create_error_response(409, error)


class DirectMessagesReceivedResource(Resource):

    def get(self, to_username):
        try:
            current_app.logger.info("Received DirectMessagesReceivedResource - received requests - GET Request")
            direct_messages = DirectMessage.get_received_direct_messages(to_username)
            current_app.logger.debug("Python Server Response: 200 - %s", direct_messages)
            return make_response(jsonify(direct_messages), 200)
        except ValueError:
            error = "Unable to handle DirectMessagesReceivedResource - received requests - GET Request"
            current_app.logger.error("Python Server Response: %s - %s", 500, error)
            return ErrorHandler.create_error_response(500, error)


class UserDirectMessagesResource(Resource):

    def get(self, username):
        try:
            current_app.logger.info("Received UserDirectMessagesResource - received requests - GET Request")
            direct_messages = DirectMessage.get_user_direct_messages_sorted_by_timestamp(username)
            current_app.logger.debug("Python Server Response: 200 - %s", direct_messages)
            return make_response(jsonify(direct_messages), 200)
        except ValueError:
            error = "Unable to handle UserDirectMessagesResource - received requests - GET Request"
            current_app.logger.error("Python Server Response: %s - %s", 500, error)
            return ErrorHandler.create_error_response(500, error)


class ConversationMessagesResource(Resource):

    def get(self, username, friend_username):
        try:
            current_app.logger.info("Received ConversationMessagesResource - received requests - GET Request")
            direct_messages = DirectMessage.get_conversation_messages_sorted_by_timestamp(username, friend_username)
            current_app.logger.debug("Python Server Response: 200 - %s", direct_messages)
            return make_response(jsonify(direct_messages), 200)
        except ValueError:
            error = "Unable to handle ConversationMessagesResource - received requests - GET Request"
            current_app.logger.error("Python Server Response: %s - %s", 500, error)
            return ErrorHandler.create_error_response(500, error)
