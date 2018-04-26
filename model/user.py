from config.mongodb import db
import uuid
import pprint


class UserNotFoundException(Exception):
    pass


class User:

    def __init__(self, user_id, username, email):
        self.user_id = user_id
        self.username = username
        self.email = email

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

        pprint.pprint(user_response)
        response = {
            "user": {
                "user_id": user_response["user_id"],
                "username": user_response["username"],
                "email": user_response["email"]
            }
        }
        return response

    @staticmethod
    def create(username, email):
        user_id = str(uuid.uuid4())
        new_user = User(user_id, username, email)
        encoded_user = User._encode_user(new_user)
        db.users.insert_one(encoded_user)
        response = {
            "user": {
                "user_id": encoded_user["user_id"],
                "username": encoded_user["username"],
                "email": encoded_user["email"]
            }
        }
        return response

    @staticmethod
    def _encode_user(user):
        return {"_type": "user", "user_id": user.user_id, "username": user.username, "email": user.email}

    @staticmethod
    def _decode_user(document):
        assert document["_type"] == "user"
        user = {
            "user_id": document["user_id"],
            "username": document["username"],
            "email": document["email"]
        }
        return user
