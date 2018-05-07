class FriendshipRequestVO:

    def __init__(self, _id, from_user_id, to_user_id, timestamp):
        self._id = _id
        self.from_user_id = from_user_id
        self.to_user_id = to_user_id
        self.timestamp = timestamp
