import json

import requests
from flask import request, jsonify, make_response, current_app
from flask_restful import Resource
from flask_restful import reqparse

from config.shared_server_config import SHARED_SERVER_FILE_UPLOAD_PATH
from model.story import Story
from resources.error_handler import ErrorHandler

class StoriesResource(Resource):

    def get(self):
        try:
            userId = request.args.get('user_id')
            current_app.logger.info("Received StoriesResource GET Requestfor User ID: " + userId)

            response = Story.get_by_user(userId)
            current_app.logger.debug("Python Server Response: 200 - %s", response)

            return make_response(jsonify(response), 200)
        except ValueError:
            error = "Unable to handle StoriesResource GET Request"
            current_app.logger.error("Python Server Response: 500 - %s", error)
            return ErrorHandler.create_error_response(500, error)

    def post(self):
        try:
            current_app.logger.info("Received StoriesResource POST Request")
            story_data = json.loads(request.data)
            payload = {
                "file": story_data["uploaded_file"],
                "metadata": {
                    "name": story_data["uploaded_filename"]
                }
            }
            headers = {'content-type': 'application/json'}
            response = requests.post(SHARED_SERVER_FILE_UPLOAD_PATH, data=json.dumps(payload), headers=headers)
            file_data = json.loads(response.text)
            if response.ok:
                story_created = Story.create(
                    story_data["user_id"],
                    story_data["location"],
                    story_data["visibility"],
                    story_data["title"],
                    story_data["description"],
                    file_data["file"]["resource"],
                    story_data["is_quick_story"],
                    story_data["timestamp"]
                )
                current_app.logger.debug("Python Server Response: 201 - %s", story_created)
                current_app.logger.debug("Shared Server Response: %s - %s", response.status_code, response.text)
                return make_response(jsonify(story_created), 200)
            return make_response(response.text, response.status_code)
        except ValueError:
            error = "Unable to handle StoriesResource POST Request"
            current_app.logger.error("Python Server Response: 500 - %s", error)
            return ErrorHandler.create_error_response(500, error)

