class FriendshipRequestVO:

    def __init__(self, _id, from_username, to_username, timestamp):
        self._id = _id
        self.from_username = from_username
        self.to_username = to_username
        self.timestamp = timestamp
