import json
from flask import request, jsonify, make_response
from flask_restful import Resource
from model.user import User, UserNotFoundException
from resources.error_handler import ErrorHandler
import pprint

class UsersResource(Resource):
    def get(self):
        return make_response(jsonify(User.getAll()), 200)

    def post(self):
        user_data = json.loads(request.data)
        return make_response(jsonify(User.create(user_data["username"], user_data["password"], user_data["email"])), 200)


class SingleUserResource(Resource):
    def get(self, user_id):
        try:
            return make_response(jsonify(User.getUserById(user_id)), 200)
        except UserNotFoundException as e:
            status_code = 403
            message = e.args[0]
            return ErrorHandler.create_error_response(status_code, message)

'''
class UsersCountResource(Resource):
    def get(self):
        users_count = mongo.db.users.count()
        return users_count
        '''

