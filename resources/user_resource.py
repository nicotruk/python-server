import json

import requests
from flask import request, jsonify, make_response
from flask_restful import Resource

from model.user import User, UserNotFoundException
from resources.error_handler import ErrorHandler
from config.shared_server_config import SHARED_SERVER_USER_PATH, SHARED_SERVER_TOKEN_PATH


class UsersResource(Resource):
    def get(self):
        return make_response(jsonify(User.get_all()), 200)

    def post(self):
        user_data = json.loads(request.data)
        payload = {
            "username": user_data["username"],
            "password": user_data["password"],
            "applicationOwner": "1234"
        }
        headers = {'content-type': 'application/json'}
        response = requests.post(SHARED_SERVER_USER_PATH, data=json.dumps(payload), headers=headers)
        if response.status_code is 200:
            return make_response(jsonify(User.create(user_data["username"], user_data["email"])), 200)
        return make_response(response.text, response.status_code)


class SingleUserResource(Resource):
    def get(self, user_id):
        try:
            return make_response(jsonify(User.get_user_by_id(user_id)), 200)
        except UserNotFoundException as e:
            status_code = 403
            message = e.args[0]
            return ErrorHandler.create_error_response(status_code, message)


class UserLoginResource(Resource):
    def post(self):
        credentials = json.loads(request.data)
        payload = {
            "username": credentials["username"],
            "password": credentials["password"]
        }
        headers = {'content-type': 'application/json'}
        response = requests.post(SHARED_SERVER_TOKEN_PATH, data=json.dumps(payload), headers=headers)
        json_response = json.loads(response.text)
        if response.status_code is 200:
            built_response = {
                "token": {
                    "expiresAt": json_response["token"]["expiresAt"],
                    "token": json_response["token"]["token"]
                }
            }
        else:
            built_response = {
                "error": {
                    "code": json_response["code"],
                    "message": json_response["message"]
                }
            }
        return make_response(jsonify(built_response), response.status_code)


'''
class UsersCountResource(Resource):
    def get(self):
        users_count = mongo.db.users.count()
        return users_count
        '''
