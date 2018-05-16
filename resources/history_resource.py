import json
import logging
import pprint
from os import stat

import requests
from flask import request, jsonify, make_response
from flask_restful import Resource

from config.shared_server_config import SHARED_SERVER_USER_PATH, SHARED_SERVER_TOKEN_PATH
from model.user import User, UserNotFoundException
from resources.error_handler import ErrorHandler

class Story(Resource):
    def get(self):
        try:
            logging.info("Received StoryResource GET Request")
            response = Story.get_all()
            logging.debug("Python Server Response: 200 - %s", response)
            return make_response(jsonify(response), 200)
        except ValueError:
            error = "Unable to handle StoryResource GET Request"
            logging.error("Python Server Response: 500 - %s", error)
            return ErrorHandler.create_error_response(500, error)

    def post(self):
        try:
            logging.info("Received StoryResource POST Request")
            user_data = json.loads(request.data)

            payload = {
                "username": user_data["username"],
                "password": user_data["password"],
                "applicationOwner": "1234"
            }
            headers = {'content-type': 'application/json'}
            response = requests.post(SHARED_SERVER_USER_PATH, data=json.dumps(payload), headers=headers)
            logging.debug("Shared Server Response: %s - %s", response.status_code, response.text)
            if response.status_code is 200:
                user_created = User.create(user_data["username"], user_data["email"], user_data["first_name"], user_data["last_name"])
                logging.debug("Python Server Response: 200 - %s", user_created)
                return make_response(jsonify(user_created), 200)
            logging.debug("Python Server Response: %s - %s", response.status_code, response.text)
            return make_response(response.text, response.status_code)
        except ValueError:
            error = "Unable to handle UsersResource POST Request"
            logging.error("Python Server Response: 500 - %s", error)
            return ErrorHandler.create_error_response(500, error)

