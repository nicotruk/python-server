from model.mongodb import mongo
import uuid
import pprint


class UserNotFoundException(Exception):
    pass


class User:

    def __init__(self, user_id, username, password, email):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.email = email

    @staticmethod
    def getAll():
        users_db_response = list(mongo.db.users.find())
        users_response = {
            "users": []
        }

        for userDBResponse in users_db_response:
            users_response["users"].append(User._decode_user(userDBResponse))

        return users_response

    @staticmethod
    def getUserById(user_id):
        user_response = mongo.db.users.find_one({"user_id": user_id})

        if user_response is None:
            raise UserNotFoundException("There is no user with that ID!")

        pprint.pprint(user_response)
        response = {
            "user": {
                "user_id": user_response["user_id"],
                "username": user_response["username"],
                "password": user_response["password"],
                "email": user_response["email"]
            }
        }
        return response

    @staticmethod
    def create(username, password, email):
        user_id = str(uuid.uuid4())
        new_user = User(user_id, username, password, email)
        encoded_user = User._encode_user(new_user)
        mongo.db.users.insert(encoded_user)
        response = {
            "user": {
                "user_id": encoded_user["user_id"],
                "username": encoded_user["username"],
                "password": encoded_user["password"],
                "email": encoded_user["email"]
            }
        }
        return response

    @staticmethod
    def _encode_user(user):
        return {"_type": "user", "user_id": user.user_id, "username": user.username, "password": user.password, "email": user.email}

    @staticmethod
    def _decode_user(document):
        assert document["_type"] == "user"
        user = {
            "user_id": document["user_id"],
            "username": document["username"],
            "password": document["password"],
            "email": document["email"]
        }
        return user
