import json
import time

from firebase_admin import messaging
from flask import request, jsonify, make_response, current_app
from flask_restful import Resource

import config.firebase_config
from config.firebase_config import NOTIFICATION_TYPE_FRIENDSHIP_REQUEST
from config.firebase_config import NOTIFICATION_TYPE_FRIENDSHIP_REQUEST_MESSAGE
from model.firebase_manager import FirebaseManager
from model.friendship_request import FriendshipRequest
from model.stats import StatManager
from model.user import User, UserNotFoundException
from resources.error_handler import ErrorHandler
from resources.token_validation_decorator import token_validation_required


class FriendshipRequestResource(Resource):

    @token_validation_required
    def post(self):
        try:
            current_app.logger.info("Received FriendshipRequestResource POST Request")
            StatManager.create(request.environ["PATH_INFO"] + " " + request.environ["REQUEST_METHOD"])
            request_data = json.loads(request.data)
            friendship_request_created = FriendshipRequest.create(request_data["from_username"],
                                                                  request_data["to_username"],
                                                                  int(round(time.time() * 1000)))

            from_username = User.get_user_by_username(request_data["from_username"])
            if request_data["to_username"] in from_username["user"]["friends_usernames"]:
                current_app.logger.debug("Python Server Response: 409 - %s", "Users are already friends.")
                return make_response("Users are already friends.", 409)

            if friendship_request_created is None:
                current_app.logger.debug("Python Server Response: 409 - %s", "Friendship request already exists")
                return make_response("Friendship request already exists", 409)
            else:
                current_app.logger.debug("Python Server Response: 201 - %s", friendship_request_created)
                if config.firebase_config.FIREBASE_NOTIFICATIONS_ENABLED is True:
                    try:
                        user = User.get_user_by_username(request_data["from_username"])["user"]
                        if user is not None:
                            FirebaseManager.send_firebase_message(user["name"],
                                                                  request_data["to_username"],
                                                                  NOTIFICATION_TYPE_FRIENDSHIP_REQUEST_MESSAGE,
                                                                  NOTIFICATION_TYPE_FRIENDSHIP_REQUEST)
                    except UserNotFoundException:
                        pass
                return make_response(jsonify(friendship_request_created), 201)
        except ValueError:
            error = "Unable to handle FriendshipRequestResource POST Request"
            current_app.logger.error("Python Server Response: 500 - %s", error)
            return ErrorHandler.create_error_response(500, error)
        except messaging.ApiCallError:
            error = "Unable to send Firebase Notification - ApiCallError"
            current_app.logger.error("Python Server Response: 409 - %s", error)
            return ErrorHandler.create_error_response(500, error)
        except UserNotFoundException as e:
            status_code = 403
            message = e.args[0]
            current_app.logger.error("Python Server Response: %s - %s", status_code, message)
            return ErrorHandler.create_error_response(status_code, message)


class FriendshipRequestsSentResource(Resource):

    @token_validation_required
    def get(self, from_username):
        try:
            current_app.logger.info("Received FriendshipRequestResource - sent requests - GET Request")
            StatManager.create(request.environ["PATH_INFO"] + " " + request.environ["REQUEST_METHOD"])
            friendship_requests = FriendshipRequest.get_sent_friendship_requests(from_username)

            if friendship_requests["friendship_requests"]:
                for friendship_request in friendship_requests["friendship_requests"]:
                    user = User.get_user_by_username(friendship_request["to_username"])["user"]
                    friendship_request["profile_pic"] = user["profile_pic"]
                    friendship_request["name"] = user["name"]

            current_app.logger.debug("Python Server Response: 200 - %s", friendship_requests)
            return make_response(jsonify(friendship_requests), 200)
        except ValueError:
            error = "Unable to handle FriendshipRequestResource - sent requests - GET Request"
            current_app.logger.error("Python Server Response: %s - %s", 500, error)
            return ErrorHandler.create_error_response(500, error)
        except UserNotFoundException as e:
            status_code = 403
            message = e.args[0]
            current_app.logger.error("Python Server Response: %s - %s", status_code, message)
            return ErrorHandler.create_error_response(status_code, message)


class FriendshipRequestsReceivedResource(Resource):

    @token_validation_required
    def get(self, to_username):
        try:
            current_app.logger.info("Received FriendshipRequestResource - received requests - GET Request")
            StatManager.create(request.environ["PATH_INFO"] + " " + request.environ["REQUEST_METHOD"])
            friendship_requests = FriendshipRequest.get_received_friendship_requests(to_username)

            if friendship_requests["friendship_requests"]:
                for friendship_request in friendship_requests["friendship_requests"]:
                    user = User.get_user_by_username(friendship_request["from_username"])["user"]
                    friendship_request["profile_pic"] = user["profile_pic"]
                    friendship_request["name"] = user["name"]

            current_app.logger.debug("Python Server Response: 200 - %s", friendship_requests)
            return make_response(jsonify(friendship_requests), 200)
        except ValueError:
            error = "Unable to handle FriendshipRequestResource - received requests - GET Request"
            current_app.logger.error("Python Server Response: %s - %s", 500, error)
            return ErrorHandler.create_error_response(500, error)
        except UserNotFoundException as e:
            status_code = 403
            message = e.args[0]
            current_app.logger.error("Python Server Response: %s - %s", status_code, message)
            return ErrorHandler.create_error_response(status_code, message)


class SingleFriendshipRequestResource(Resource):

    @token_validation_required
    def delete(self, from_username, to_username):
        try:
            current_app.logger.info("Received SingleFriendshipRequestResource - DELETE Request")
            StatManager.create(request.environ["PATH_INFO"] + " " + request.environ["REQUEST_METHOD"])
            deleted_friendship_request = FriendshipRequest.delete(from_username, to_username)
            if deleted_friendship_request is None:
                current_app.logger.debug("Python Server Response: 409 - %s",
                                         "No friendship request found for those parameters.")
                return make_response("No friendship request found for those parameters.", 409)
            else:
                current_app.logger.debug("Python Server Response: 201 - %s", deleted_friendship_request)
                return make_response(jsonify(deleted_friendship_request), 201)
        except ValueError:
            error = "Unable to handle SingleFriendshipRequestResource - DELETE Request"
            current_app.logger.error("Python Server Response: %s - %s", 500, error)
            return ErrorHandler.create_error_response(500, error)
