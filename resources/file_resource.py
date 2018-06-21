import json

import requests
from flask import request, jsonify, make_response, current_app
from flask_restful import Resource

from config.shared_server_config import SHARED_SERVER_FILE_UPLOAD_PATH, SHARED_SERVER_TOKEN_VALIDATION_PATH, SHARED_SERVER_TOKEN
from model.story import Story
from resources.error_handler import ErrorHandler


class FileResource(Resource):

    def post(self, story_id):
        try:
            current_app.logger.info("Received FileResource POST Request")
            current_app.logger.info("Validating the user token with the shared server")
            token_headers = {'content-type': 'application/json', 'Authorization': 'Bearer {}'.format(SHARED_SERVER_TOKEN)}
            user_token = request.headers.get('Authorization').split()[1]
            token_validation_payload = {
                "token": user_token
            }
            token_validation_response = requests.post(SHARED_SERVER_TOKEN_VALIDATION_PATH, data=json.dumps(token_validation_payload), headers=token_headers)
            if token_validation_response.ok:
                current_app.logger.info("User token was validated successfully")
                upload_headers = {'Authorization': 'Bearer {}'.format(user_token)}
                uploaded_file = request.files['file'].read()
                filename = request.form.get('filename')
                shared_server_upload = requests.post(SHARED_SERVER_FILE_UPLOAD_PATH, files={'file': (filename, uploaded_file)}, headers=upload_headers)
                current_app.logger.debug("Shared Server Response: %s - %s", shared_server_upload.status_code, shared_server_upload.text)
                file_data = json.loads(shared_server_upload.text)
                if shared_server_upload.ok:
                    story_updated = Story.update(
                        story_id,
                        file_data['file']['resource']
                    )
                    current_app.logger.debug("Python Server Response: %s - %s", shared_server_upload.status_code,
                                             story_updated)
                    return make_response(jsonify(story_updated), 200)
                return make_response(shared_server_upload.text, shared_server_upload.status_code)
            current_app.logger.info("User token could not be validated")
            return make_response(token_validation_response.text, token_validation_response.status_code)
        except ValueError as ex:
            error = "Unable to handle FileResource POST Request" + ex
            current_app.logger.error("Python Server Response: 500 - %s", error)
            return ErrorHandler.create_error_response(500, error)

