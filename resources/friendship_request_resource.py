import json
import time

from flask import request, jsonify, make_response, current_app
from flask_restful import Resource

from model.friendship_request import FriendshipRequest
from resources.error_handler import ErrorHandler


class FriendshipRequestResource(Resource):

    def post(self):
        try:
            current_app.logger.info("Received FriendshipRequestResource POST Request")
            request_data = json.loads(request.data)
            friendship_request_created = FriendshipRequest.create(request_data["from_username"],
                                                                  request_data["to_username"],
                                                                  int(round(time.time() * 1000)))
            if friendship_request_created is None:
                current_app.logger.debug("Python Server Response: 409 - %s", "Friendship request already exists")
                return make_response("Friendship request already exists", 201)
            else:
                current_app.logger.debug("Python Server Response: 201 - %s", friendship_request_created)
                return make_response(jsonify(friendship_request_created), 201)
        except ValueError:
            error = "Unable to handle FriendshipRequestResource POST Request"
            current_app.logger.error("Python Server Response: 500 - %s", error)
            return ErrorHandler.create_error_response(500, error)


class FriendshipRequestsSentResource(Resource):

    def get(self, from_username):
        try:
            current_app.logger.info("Received FriendshipRequestResource - sent requests - GET Request")
            friendship_requests = FriendshipRequest.get_sent_friendship_requests(from_username)
            current_app.logger.debug("Python Server Response: 200 - %s", friendship_requests)
            return make_response(jsonify(friendship_requests), 200)
        except ValueError:
            error = "Unable to handle FriendshipRequestResource - sent requests - GET Request"
            current_app.logger.error("Python Server Response: %s - %s", 500, error)
            return ErrorHandler.create_error_response(500, error)


class FriendshipRequestsReceivedResource(Resource):

    def get(self, to_username):
        try:
            current_app.logger.info("Received FriendshipRequestResource - received requests - GET Request")
            friendship_requests = FriendshipRequest.get_received_friendship_requests(to_username)
            current_app.logger.debug("Python Server Response: 200 - %s", friendship_requests)
            return make_response(jsonify(friendship_requests), 200)
        except ValueError:
            error = "Unable to handle FriendshipRequestResource - received requests - GET Request"
            current_app.logger.error("Python Server Response: %s - %s", 500, error)
            return ErrorHandler.create_error_response(500, error)

class SingleFriendshipRequestResource(Resource):

    def delete(self, from_username, to_username):
        try:
            current_app.logger.info("Received SingleFriendshipRequestResource - DELETE Request")
            deleted_friendship_request = FriendshipRequest.delete(from_username, to_username)
            if deleted_friendship_request is None:
                current_app.logger.debug("Python Server Response: 409 - %s", "No friendship request found for those parameters.")
                return make_response("No friendship request found for those parameters.", 409)
            else:
                current_app.logger.debug("Python Server Response: 201 - %s", deleted_friendship_request)
                return make_response(jsonify(deleted_friendship_request), 201)
        except ValueError:
            error = "Unable to handle SingleFriendshipRequestResource - DELETE Request"
            current_app.logger.error("Python Server Response: %s - %s", 500, error)
            return ErrorHandler.create_error_response(500, error)
        
