import uuid

from pymongo import ReturnDocument

from config.mongodb import db
from model.db.userVO import UserVO


class UserNotFoundException(Exception):
    pass


class User:

    @staticmethod
    def get_all():
        users_db_response = list(db.users.find())
        users_response = {
            "users": []
        }

        for userDBResponse in users_db_response:
            users_response["users"].append(User._decode_user(userDBResponse))

        return users_response

    @staticmethod
    def get_user_by_id(user_id):
        user_response = db.users.find_one({"user_id": user_id})

        if user_response is None:
            raise UserNotFoundException("There is no user with that ID!")

        response = {
            "user": User._decode_user(user_response)
        }
        return response

    @staticmethod
    def get_user_id_by_username(username):
        user_response = db.users.find_one({"username": username})

        if user_response is None:
            raise UserNotFoundException("There is no user with that username!")

        response = {
            "user_id": user_response["user_id"]
        }
        return response

    @staticmethod
    def get_user_by_username(username):
        user_response = db.users.find_one({"username": username})

        if user_response is None:
            raise UserNotFoundException("There is no user with that username!")

        response = {
            "user": User._decode_user(user_response)
        }
        return response

    @staticmethod
    def get_profile_pic(username):
        try:
            response = User.get_user_by_username(username)
            return response["user"]["profile_pic"]
        except UserNotFoundException:
            return ""

    @staticmethod
    def update_user(user_id, first_name, last_name, email, profile_pic):
        updated_fields = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "profile_pic": profile_pic
        }

        result = db.users.find_one_and_update({"user_id": user_id}, {'$set': updated_fields},
                                              return_document=ReturnDocument.AFTER)

        if result is None:
            raise UserNotFoundException("There is no user with that ID!")

        response = {
            "user": User._decode_user(result)
        }

        return response

    @staticmethod
    def create(username, email, first_name, last_name, firebase_token):
        user_id = str(uuid.uuid4())
        new_user = UserVO(user_id, username, email, first_name, last_name, '', [], firebase_token)
        encoded_user = User._encode_user(new_user)
        db.users.insert_one(encoded_user)
        response = {
            "user": {
                "user_id": encoded_user["user_id"],
                "username": encoded_user["username"],
                "email": encoded_user["email"],
                "first_name": encoded_user["first_name"],
                "last_name": encoded_user["last_name"],
                "firebase_token": encoded_user["firebase_token"]
            }
        }
        return response

    @staticmethod
    def add_friend(username, friend_username):
        try:
            user_response = User.get_user_by_username(username)
            friends_usernames = user_response["user"]["friends_usernames"]
            friends_usernames.append(friend_username)
            updated_fields = {
                "friends_usernames": friends_usernames
            }

            result = db.users.find_one_and_update({"username": username}, {'$set': updated_fields},
                                                  return_document=ReturnDocument.AFTER)

            if result is None:
                raise UserNotFoundException("Couldn't update Friends Usernames list.")

            response = {
                "user": User._decode_user(result)
            }

            return response
        except UserNotFoundException:
            raise UserNotFoundException

    @staticmethod
    def _encode_user(user):
        return {
            "_type": "user",
            "user_id": user.user_id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "profile_pic": user.profile_pic,
            "friends_usernames": user.friends_usernames,
            "firebase_token": user.firebase_token
        }

    @staticmethod
    def _decode_user(document):
        assert document["_type"] == "user"
        user = {
            "user_id": document["user_id"],
            "username": document["username"],
            "email": document["email"],
            "first_name": document["first_name"],
            "last_name": document["last_name"],
            "profile_pic": document["profile_pic"],
            "friends_usernames": document["friends_usernames"],
            "firebase_token": document["firebase_token"]
        }
        return user



