class StoryVO:

    def __init__(self, id, user_id, location, visibility, title, description, file_url, is_quick_story, timestamp):
        self.id = id
        self.user_id = user_id
        self.location = location
        self.visibility = visibility
        self.title = title
        self.description = description
        self.file_url = file_url
        self.is_quick_story = is_quick_story
        self.timestamp = timestamp
