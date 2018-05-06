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


class UsersResource(Resource):
    def get(self):
        try:
            logging.info("Received UsersResource GET Request")
            users_response = User.get_all()
            logging.debug("Python Server Response: 200 - %s", users_response)
            return make_response(jsonify(users_response), 200)
        except ValueError:
            error = "Unable to handle UsersResource GET Request"
            logging.error("Python Server Response: 500 - %s", error)
            return ErrorHandler.create_error_response(500, error)

    def post(self):
        try:
            logging.info("Received UsersResource POST Request")
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


class SingleUserResource(Resource):
    def get(self, user_id):
        try:
            logging.info("Received SingleUserResource GET Request")
            user = User.get_user_by_id(user_id)
            logging.debug("Python Server Response: 200 - %s", user)
            return make_response(jsonify(user), 200)
        except UserNotFoundException as e:
            status_code = 403
            message = e.args[0]
            logging.error("Python Server Response: %s - %s", status_code, message)
            return ErrorHandler.create_error_response(status_code, message)

    def put(self, user_id):
        try:
            logging.info("Received SingleUserResource PUT Request")
            request_data = json.loads(request.data)

            updated_user = User.update_user(user_id, request_data["first_name"], request_data["last_name"],
                request_data["email"], request_data["profile_pic"])

            logging.debug("Python Server Response: 200 - %s", updated_user)
            return make_response(jsonify(updated_user), 200)
        except UserNotFoundException as e:
            status_code = 403
            message = e.args[0]
            logging.error("Python Server Response: %s - %s", status_code, message)
            return ErrorHandler.create_error_response(status_code, message)


class UserLoginResource(Resource):
    def post(self):
        try:
            logging.info("Received UserLoginResource POST Request")
            credentials = json.loads(request.data)
            payload = {
                "username": credentials["username"],
                "password": credentials["password"]
            }
            headers = {'content-type': 'application/json'}
            response = requests.post(SHARED_SERVER_TOKEN_PATH, data=json.dumps(payload), headers=headers)
            logging.debug("Shared Server Response: %s - %s", response.status_code, response.text)
            json_response = json.loads(response.text)
            if response.status_code is 200:
                built_response = {
                    "token": {
                        "expiresAt": json_response["token"]["expiresAt"],
                        "token": json_response["token"]["token"]
                    }
                }
                logging.debug("Python Server Response: %s - %s", response.status_code, built_response)
            else:
                built_response = {
                    "error": {
                        "code": json_response["code"],
                        "message": json_response["message"]
                    }
                }
                logging.error("Python Server Response: %s - %s", response.status_code, built_response)
            return make_response(jsonify(built_response), response.status_code)
        except ValueError:
            error = "Unable to handle UsersResource POST Request"
            logging.error("Python Server Response: %s - %s", 500, error)
            return ErrorHandler.create_error_response(500, error)

