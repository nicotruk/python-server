class User:

    def __init__(self):
        self.user_id = ""
        self.name = ""
        self.surname = ""

    def set_user_id(self, user_id):
        self.user_id = user_id

    def set_name(self, name):
        self.name = name

    def set_surname(self, surname):
        self.surname = surname

    def encode_user(self):
        return {"_type": "user", "user_id": self.user_id, "name": self.name, "surname": self.surname}

    def decode_user(self, document):
        assert document["_type"] == "user"
        self.user_id = document["user_id"]
        self.name = document["name"]
        self.surname = document["surname"]
        return self
