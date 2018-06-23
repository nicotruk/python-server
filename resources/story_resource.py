import json

from flask import request, jsonify, make_response, current_app
from flask_restful import Resource

import config.firebase_config
from config.firebase_config import NOTIFICATION_TYPE_STORY
from config.firebase_config import NOTIFICATION_TYPE_STORY_MESSAGE
from model.firebase_manager import FirebaseManager
from model.story import Story
from model.user import User, UserNotFoundException
from resources.error_handler import ErrorHandler
from resources.token_validation_decorator import token_validation_required


class StoriesResource(Resource):
    @token_validation_required
    def get(self):
        try:
            userId = request.args.get('user_id')
            current_app.logger.info("Received StoriesResource GET Request for User ID: " + userId)
            response = Story.get_by_user(userId)
            current_app.logger.debug("Python Server Response: 200 - %s", response)
            return make_response(jsonify(response), 200)
        except ValueError:
            error = "Unable to handle StoriesResource GET Request"
            current_app.logger.error("Python Server Response: 500 - %s", error)
            return ErrorHandler.create_error_response(500, error)
        except UserNotFoundException as e:
            status_code = 403
            message = e.args[0]
            current_app.logger.error("Python Server Response: %s - %s", status_code, message)
            return ErrorHandler.create_error_response(status_code, message)

    @token_validation_required
    def post(self):
        try:
            current_app.logger.info("Received StoriesResource POST Request")
            story_data = json.loads(request.data)
            story_created = Story.create(
                story_data["user_id"],
                story_data["location"],
                story_data["visibility"],
                story_data["title"],
                story_data["description"],
                story_data["is_quick_story"],
                story_data["timestamp"]
            )
            current_app.logger.debug("Python Server Response: 201 - %s", story_created)
            if config.firebase_config.FIREBASE_NOTIFICATIONS_ENABLED is True:
                try:
                    user = User.get_user_by_id(story_data["user_id"])
                    if user is not None:
                        user = user["user"]
                        for friend_username in user["friends_usernames"]:
                            try:
                                FirebaseManager.send_firebase_message(user["username"],
                                                                      friend_username,
                                                                      NOTIFICATION_TYPE_STORY_MESSAGE,
                                                                      NOTIFICATION_TYPE_STORY)
                            except UserNotFoundException:
                                pass
                except UserNotFoundException:
                    pass
            return make_response(jsonify(story_created), 200)
        except ValueError:
            error = "Unable to handle StoriesResource POST Request"
            current_app.logger.error("Python Server Response: 500 - %s", error)
            return ErrorHandler.create_error_response(500, error)


class SingleStoryResource(Resource):

    @token_validation_required
    def delete(self, story_id):
        try:
            current_app.logger.info("Received SingleStoryResource - DELETE Request")
            deleted_story = Story.delete(story_id)
            if deleted_story is None:
                current_app.logger.debug("Python Server Response: 403 - %s",
                                         "No story found with that ID!.")
                return make_response("No story found with that ID!.", 403)
            else:
                current_app.logger.debug("Python Server Response: 201 - %s", deleted_story)
                return make_response(jsonify(deleted_story), 201)
        except ValueError:
            error = "Unable to handle SingleFriendshipRequestResource - DELETE Request"
            current_app.logger.error("Python Server Response: %s - %s", 500, error)
            return ErrorHandler.create_error_response(500, error)
