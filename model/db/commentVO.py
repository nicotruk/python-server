class CommentVO:

    def __init__(self, user_id, history_id, message, timestamp):
        self.user_id = user_id
        self.history_id = history_id
        self.message = message
        self.timestamp = timestamp
