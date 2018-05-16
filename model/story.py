from config.mongodb import db
from pymongo import ReturnDocument
from model.db.storyVO import StoryVO
import uuid
import pprint

class Story:

    @staticmethod
    def get_all():
        db_response = list(db.stories.find())
        response = {
            "stories": []
        }

        for story in db_response:
            response["stories"].append(Story._decode(story))

        return response

    @staticmethod
    def create(user_id, location, visibility, title, description, file_url, is_quick_story, timestamp):
        id = str(uuid.uuid4())
        new_story = StoryVO(id, user_id, location, visibility, title, description, file_url, is_quick_story, timestamp)
        encoded_story = Story._encode(new_story)
        db.stories.insert_one(encoded_story)
        response = Story._decode(encoded_story)
        return response

    @staticmethod
    def _encode(item):
        return {
            "_type": "story",
            "id": item.id,
            "user_id": item.user_id,
            "location": item.location,
            "visibility": item.visibility,
            "title": item.title,
            "description": item.description,
            "file_url": item.file_url,
            "is_quick_story": item.is_quick_story,
            "timestamp": item.timestamp
        }

    @staticmethod
    def _decode(document):
        assert document["_type"] == "story"
        story = {
            "id": document["id"],
            "user_id": document["user_id"],
            "location": document["location"],
            "visibility": document["visibility"],
            "title": document["title"],
            "description": document["description"],
            "file_url": document["file_url"],
            "is_quick_story": document["is_quick_story"],
            "timestamp": document["timestamp"]
        }
        return story
