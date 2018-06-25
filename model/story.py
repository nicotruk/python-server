import uuid

from pymongo import ReturnDocument

from config.mongodb import db
from model.db.storyVO import StoryVO
from model.user import UserNotFoundException
from .storySorter import StorySorter


class StoryNotFoundException(Exception):
    pass


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
    def get_by_user(user_id):

        # Get all public stories
        public_stories = list(db.stories.find({"visibility": "public"}))

        # Get all private stories
        private_stories = list(db.stories.find({"visibility": "private"}))

        # Filter out private stories, keeping only
        # 1) Private stories of the user
        # 2) Private stories of the user's friends
        user = db.users.find_one({"user_id": user_id})

        if user is None:
            raise UserNotFoundException("User not found")
        else:
            user_friends_ids = list()

            for friends_username in user["friends_usernames"]:
                friend = db.users.find_one({"username": friends_username})
                user_friends_ids.append(friend["user_id"])

            valid_user_ids = user_friends_ids + [user_id]
            visible_private_stories = list()

            for privateStory in private_stories:
                if privateStory["user_id"] in valid_user_ids:
                    visible_private_stories.append(privateStory)

            # Merge all stories
            result = public_stories + visible_private_stories

            # Sort by importance
            sorted_result = StorySorter.sort_by_importance(result)

            response = {
                "stories": []
            }

            for story in sorted_result:
                response["stories"].append(Story._decode(story))

            return response

    @staticmethod
    def get_from_user(username, user_id):

        storiesUser = db.users.find_one({ "username": username })
        currentUser = db.users.find_one({ "user_id": user_id })

        if storiesUser is None or currentUser is None:
            raise UserNotFoundException("User not found")


        if currentUser["username"] in storiesUser["friends_usernames"] or storiesUser["username"] == currentUser["username"]:
            stories = list(db.stories.find({ "user_id": storiesUser["user_id"] }))
        else:
            stories = list(db.stories.find({ "user_id": storiesUser["user_id"], "visibility": "public" }))

        response = {
            "stories": []
        }

        for story in stories:
            response["stories"].append(Story._decode(story))

        return response

    @staticmethod
    def create(user_id, location, visibility, title, description, is_quick_story, timestamp):
        story_id = str(uuid.uuid4())
        new_story = StoryVO(story_id, user_id, location, visibility, title, description, is_quick_story, timestamp, '',
                            [], [])
        encoded_story = Story._encode(new_story)
        db.stories.insert_one(encoded_story)
        response = Story._decode(encoded_story)
        return response

    @staticmethod
    def add_reaction(story_id, reaction):
        result = db.stories.find_one_and_update({"id": story_id}, {"$addToSet": {"reactions": reaction}},
                                                return_document=ReturnDocument.AFTER)
        if result is None:
            raise StoryNotFoundException("There is no story with that ID!")
        response = Story._decode(result)
        return response

    @staticmethod
    def remove_reaction(story_id, reaction):
        result = db.stories.find_one_and_update({"id": story_id}, {"$pull": {"reactions": reaction}},
                                                return_document=ReturnDocument.AFTER)
        if result is None:
            raise StoryNotFoundException("There is no story with that ID!")
        response = Story._decode(result)
        return response

    @staticmethod
    def add_comment(story_id, new_comment):
        result = db.stories.find_one_and_update({"id": story_id}, {"$addToSet": {"comments": new_comment}},
                                                return_document=ReturnDocument.AFTER)
        if result is None:
            raise StoryNotFoundException("There is no story with that ID!")
        response = Story._decode(result)
        return response

    @staticmethod
    def update_file(story_id, file_url):
        updated_fields = {"file_url": file_url}
        result = db.stories.find_one_and_update({"id": story_id}, {'$set': updated_fields},
                                                return_document=ReturnDocument.AFTER)
        if result is None:
            raise StoryNotFoundException("There is no story with that ID!")
        response = Story._decode(result)
        return response

    @staticmethod
    def delete(story_id):
        db_response = db.stories.delete_one({"id": story_id})
        if db_response.deleted_count == 1:
            response = {
                "story": {
                    "story_id": story_id
                }
            }
        else:
            response = None
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
            "reactions": item.reactions,
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
            "reactions": dict.get(document, "reactions", []),
            "comments": dict.get(document, "comments", []),
            "is_quick_story": document["is_quick_story"],
            "timestamp": document["timestamp"]
        }

        # Add user info in each story
        user = db.users.find_one({"user_id": str(story["user_id"])})
        story["username"] = user["username"]
        story["name"] = user["name"]
        story["profile_pic"] = user["profile_pic"]

        return story
