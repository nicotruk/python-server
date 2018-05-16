class DirectMessageVO:

    def __init__(self, _id, from_username, to_username, message, timestamp):
        self._id = _id
        self.from_username = from_username
        self.to_username = to_username
        self.message = message
        self.timestamp = timestamp
