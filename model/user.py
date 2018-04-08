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
        usersResponse = {
            "users": []
        }

        for userDBResponse in users_db_response:
            usersResponse["users"].append(User._decode_user(userDBResponse))

        return usersResponse

    @staticmethod
    def getUserById(user_id):
        userResponse = mongo.db.users.find_one({"user_id": user_id})

        if userResponse is None:
            raise UserNotFoundException("There is no user with that ID!")

        pprint.pprint(userResponse)
        response = {
            "user": {
                "user_id": userResponse["user_id"],
                "username": userResponse["username"],
                "password": userResponse["password"],
                "email": userResponse["email"]
            }
        }
        return response

    @staticmethod
    def create(username, password, email):
        user_id = str(uuid.uuid4())
        newUser = User(user_id, username, password, email)
        encodedUser = User._encode_user(newUser)
        mongo.db.users.insert(encodedUser)
        response = {
            "user": {
                "user_id": encodedUser["user_id"],
                "username": encodedUser["username"],
                "password": encodedUser["password"],
                "email": encodedUser["email"]
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
