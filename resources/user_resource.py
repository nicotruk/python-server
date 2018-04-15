import json
import requests
from flask import request, jsonify, make_response
from flask_restful import Resource
from flask import Response
from model.user import User, UserNotFoundException
from model.registration_data import RegistrationData
from shared_server_config import SHARED_SERVER_URI, SHARED_SERVER_USER_PATH
from resources.error_handler import ErrorHandler


class UsersResource(Resource):
    def get(self):
        return make_response(jsonify(User.getAll()), 200)

    def post(self):
        user_data = json.loads(request.data)
        '''payload = {
            "username": user_data["username"],
            "password": user_data["password"],
            "applicationOwner": "1234"
        }'''
        #response = requests.post('{}/api/user'.format(SHARED_SERVER_URI), data=json.dumps(payload))
        #if response.status_code is 200: 
        return make_response(jsonify(User.create(user_data["username"], user_data["email"])), 200)
        #return response

class SingleUserResource(Resource):
    def get(self, user_id):
        try:
            return make_response(jsonify(User.getUserById(user_id)), 200)
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
        #response = requests.post('{}/api/token'.format(SHARED_SERVER_URI), data=json.dumps(payload))
        token = {
            "token": "ahsdfqkjwrykuqetrkjghafgdhsagfdjghqefghq"
        }
        return make_response(jsonify(token))

'''
class UsersCountResource(Resource):
    def get(self):
        users_count = mongo.db.users.count()
        return users_count
        '''

class RegistrationResource(Resource):
    def post(self):
        user_data = json.loads(request.data)
        registration_data = RegistrationData("id", "rev", user_data["password"], "application_owner",
                                             user_data["username"])
        response = requests.post(SHARED_SERVER_USER_PATH, registration_data)
        if response.status_code == 200:
            return Response('Ok', 200)
        elif response.status_code == 400:
            return Response('Ok', 400)
        elif response.status_code == 401:
            return Response('Ok', 401)
        elif response.status_code == 500:
            return make_response('', 500)
