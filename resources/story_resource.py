import json
import logging

import requests
from flask import request, jsonify, make_response
from flask_restful import Resource

from config.shared_server_config import SHARED_SERVER_USER_PATH, SHARED_SERVER_TOKEN_PATH, SHARED_SERVER_APPLICATION_OWNER
from model.story import Story
from resources.error_handler import ErrorHandler

class StoriesResource(Resource):

    def get(self):
        try:
            logging.info("Received StoriesResource GET Request")
            response = Story.get_all()
            logging.debug("Python Server Response: 200 - %s", response)
            return make_response(jsonify(response), 200)
        except ValueError:
            error = "Unable to handle StoriesResource GET Request"
            logging.error("Python Server Response: 500 - %s", error)
            return ErrorHandler.create_error_response(500, error)

    def post(self):
        try:
            logging.info("Received StoriesResource POST Request")
            story_data = json.loads(request.data)

            # TODO: generate fileURL based on info retrieved by Androd
            # and a call to the shared server to save the blob
            file_url = ''

            story_created = Story.create(
                story_data["user_id"],
                story_data["location"],
                story_data["visibility"],
                story_data["title"],
                story_data["description"],
                file_url,
                story_data["is_quick_story"],
                story_data["timestamp"]
            )
            logging.debug("Python Server Response: 201 - %s", story_created)
            return make_response(jsonify(story_created), 200)
        except ValueError:
            error = "Unable to handle StoriesResource POST Request"
            logging.error("Python Server Response: 500 - %s", error)
            return ErrorHandler.create_error_response(500, error)

