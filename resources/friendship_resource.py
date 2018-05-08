import json
import logging
import time

from flask import request, jsonify, make_response
from flask_restful import Resource

from model.friendship_request import FriendshipRequest
from resources.error_handler import ErrorHandler


class FriendshipRequestResource(Resource):

    def post(self):
        try:
            logging.info("Received FriendshipRequestResource POST Request")
            request_data = json.loads(request.data)
            friendship_request_created = FriendshipRequest.create(request_data["from_user_id"],
                                                                  request_data["to_user_id"],
                                                                  int(round(time.time() * 1000)))
            if friendship_request_created is None:
                logging.debug("Python Server Response: 200 - %s", "Friendship request already exists")
                return make_response("Friendship request already exists", 409)
            else:
                logging.debug("Python Server Response: 201 - %s", friendship_request_created)
                return make_response(jsonify(friendship_request_created), 201)
        except ValueError:
            error = "Unable to handle FriendshipRequestResource POST Request"
            logging.error("Python Server Response: 500 - %s", error)
            return ErrorHandler.create_error_response(500, error)


class FriendshipRequestsSentResource(Resource):

    def get(self, from_user_id):
        try:
            logging.info("Received FriendshipRequestResource - sent requests - GET Request")
            friendship_requests = FriendshipRequest.get_sent_friendship_requests(from_user_id)
            logging.debug("Python Server Response: 200 - %s", friendship_requests)
            return make_response(jsonify(friendship_requests), 200)
        except ValueError:
            error = "Unable to handle FriendshipRequestResource - sent requests - GET Request"
            logging.error("Python Server Response: %s - %s", 500, error)
            return ErrorHandler.create_error_response(500, error)


class FriendshipRequestsReceivedResource(Resource):

    def get(self, to_user_id):
        try:
            logging.info("Received FriendshipRequestResource - received requests - GET Request")
            friendship_requests = FriendshipRequest.get_received_friendship_requests(to_user_id)
            logging.debug("Python Server Response: 200 - %s", friendship_requests)
            return make_response(jsonify(friendship_requests), 200)
        except ValueError:
            error = "Unable to handle FriendshipRequestResource - received requests - GET Request"
            logging.error("Python Server Response: %s - %s", 500, error)
            return ErrorHandler.create_error_response(500, error)