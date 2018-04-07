import json
from flask import request, jsonify
from flask_restful import Resource
from model.user import User


class UsersResource(Resource):
    def get(self):
        return jsonify(User.getAll())

    def post(self):
        user_data = json.loads(request.data)
        return jsonify(User.create(user_data["username"], user_data["password"], user_data["email"]))


'''class SingleUserResource(Resource):
    def get(self, user_id):
        mongo_response = mongo.db.users.find_one({"user_id": user_id})
        if mongo_response is None:
            return {"error": "No user with user id : {}".format(user_id)}, 404

        users_db_response = User()
        users_db_response._decode_user(mongo_response)
        return json.dumps(users_db_response.__dict__)


class UsersCountResource(Resource):
    def get(self):
        users_count = mongo.db.users.count()
        return users_count
        '''

