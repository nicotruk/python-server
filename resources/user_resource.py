import json
from flask import request
from flask_restful import Resource
from model.mongodb import mongo
from model.user import User


class UsersResource(Resource):
    def get(self):
        users_db_response = list(mongo.db.users.find())
        users = []

        for userDBResponse in users_db_response:
            user = User()
            users.append(user.decode_user(userDBResponse))

        return json.dumps([user.__dict__ for user in users])


class UserDetailResource(Resource):
    def get(self, user_id):
        mongo_response = mongo.db.users.find_one({"user_id": user_id})
        if mongo_response is None:
            return {"error": "No user with user id : {}".format(user_id)}, 404

        users_db_response = User()
        users_db_response.decode_user(mongo_response)
        return json.dumps(users_db_response.__dict__)


class UsersCountResource(Resource):
    def get(self):
        users_count = mongo.db.users.count()
        return users_count


class UserInsertionResource(Resource):
    def post(self):
        user_data = json.loads(request.data)
        user = User()
        user.set_user_id(user_data["user_id"])
        user.set_name(user_data["name"])
        user.set_surname(user_data["surname"])
        mongo.db.users.insert(user.encode_user())

