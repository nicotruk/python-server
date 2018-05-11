import json
import logging
import time

from flask import request, jsonify, make_response
from flask_restful import Resource

from model.direct_message import DirectMessage
from resources.error_handler import ErrorHandler


class DirectMessageResource(Resource):

    def post(self):
        try:
            logging.info("Received DirectMessageResource POST Request")
            request_data = json.loads(request.data)
            direct_message_created = DirectMessage.create(request_data["from_user_id"],
                                                          request_data["to_user_id"],
                                                          request_data["message"],
                                                          int(round(time.time() * 1000)))
            if direct_message_created is None:
                raise ValueError('DB error')
            else:
                logging.debug("Python Server Response: 201 - %s", direct_message_created)
                return make_response(jsonify(direct_message_created), 201)
        except ValueError:
            error = "Unable to handle DirectMessageResource POST Request"
            logging.error("Python Server Response: 500 - %s", error)
            return ErrorHandler.create_error_response(500, error)


class DirectMessagesReceivedResource(Resource):

    def get(self, to_user_id):
        try:
            logging.info("Received DirectMessagesReceivedResource - received requests - GET Request")
            direct_messages = DirectMessage.get_received_direct_messages(to_user_id)
            logging.debug("Python Server Response: 200 - %s", direct_messages)
            return make_response(jsonify(direct_messages), 200)
        except ValueError:
            error = "Unable to handle DirectMessagesReceivedResource - received requests - GET Request"
            logging.error("Python Server Response: %s - %s", 500, error)
            return ErrorHandler.create_error_response(500, error)
