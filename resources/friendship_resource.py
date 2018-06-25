import json

from flask import request, jsonify, make_response, current_app
from flask_restful import Resource

import config.firebase_config
from config.firebase_config import NOTIFICATION_TYPE_FRIENDSHIP_REQUEST_ACCEPTED
from config.firebase_config import NOTIFICATION_TYPE_FRIENDSHIP_REQUEST_ACCEPTED_MESSAGE
from model.firebase_manager import FirebaseManager
from model.friendship_request import FriendshipRequest
from model.stats import StatManager
from model.user import User, UserNotFoundException
from resources.error_handler import ErrorHandler
from resources.token_validation_decorator import token_validation_required


class FriendshipResource(Resource):

    @token_validation_required
    def post(self):
        try:
            current_app.logger.info("Received SetFriendshipResource POST Request")
            StatManager.create(request.environ["PATH_INFO"] + " " + request.environ["REQUEST_METHOD"])
            friendship_data = json.loads(request.data)

            User.add_friend(friendship_data["from_username"], friendship_data["to_username"])
            User.add_friend(friendship_data["to_username"], friendship_data["from_username"])

            deleted_friendship_request = FriendshipRequest.delete(friendship_data["from_username"],
                                                                  friendship_data["to_username"])

            if deleted_friendship_request is None:
                current_app.logger.debug("Python Server Response: 409 - %s",
                                         "No friendship request found for those parameters.")
                return make_response("No friendship request found for those parameters.", 409)
            else:
                current_app.logger.debug("Python Server Response: 201 - %s", deleted_friendship_request)
                if config.firebase_config.FIREBASE_NOTIFICATIONS_ENABLED is True:
                    try:
                        user = User.get_user_by_username(friendship_data["to_username"])["user"]
                        if user is not None:
                            FirebaseManager.send_firebase_message(user["name"],
                                                                  friendship_data["from_username"],
                                                                  NOTIFICATION_TYPE_FRIENDSHIP_REQUEST_ACCEPTED_MESSAGE,
                                                                  NOTIFICATION_TYPE_FRIENDSHIP_REQUEST_ACCEPTED)
                    except UserNotFoundException:
                        pass
                return make_response(jsonify(deleted_friendship_request), 201)

        except UserNotFoundException:
            error = "Unable to find a User with the parameters given. SetFriendshipResource POST Request"
            current_app.logger.error("Python Server Response: 403 - %s", error)
            return ErrorHandler.create_error_response(403, error)
        except ValueError:
            error = "Unable to handle SetFriendshipResource POST Request"
            current_app.logger.error("Python Server Response: 500 - %s", error)
            return ErrorHandler.create_error_response(500, error)
