class DirectMessageVO:

    def __init__(self, from_user_id, to_user_id, message, timestamp):
        self.from_user_id = from_user_id
        self.to_user_id = to_user_id
        self.message = message
        self.timestamp = timestamp
