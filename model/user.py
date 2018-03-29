class User:

    def __init__(self, user_id, name, surname):
        self.user_id = user_id
        self.name = name
        self.surname = surname

    def encode_user(self):
        return {"_type": "user", "user_id": self.user_id, "name": self.name, "surname": self.surname}

    @staticmethod
    def decode_user(document):
        assert document["_type"] == "user"
        user = User
        user.user_id = document["user_id"]
        user.name = document["name"]
        user.surname = document["surname"]
        return user
