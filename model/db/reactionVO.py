from model.reaction_type import ReactionType


class ReactionVO:

    def __init__(self, user_id, history_id, reaction_type):
        self.user_id = user_id
        self.history_id = history_id
        if isinstance(reaction_type, ReactionType):
            self.reaction_type = reaction_type
