import json

import requests
from flask import request, jsonify, make_response, current_app
from flask_restful import Resource

from config.shared_server_config import SHARED_SERVER_FILE_UPLOAD_PATH, SHARED_SERVER_FILE_OWNERSHIP_PATH, \
    APP_SERVER_TOKEN
from model.stats import StatManager
from model.story import Story
from resources.error_handler import ErrorHandler
from resources.token_validation_decorator import token_validation_required


class FileResource(Resource):

    @token_validation_required
    def post(self, story_id):
        try:
            current_app.logger.info("Received FileResource POST Request")
            StatManager.create(request.environ["PATH_INFO"] + " " + request.environ["REQUEST_METHOD"])
            user_token = request.headers.get('Authorization').split()[1]
            upload_headers = {'Authorization': 'Bearer {}'.format(user_token)}
            uploaded_file = request.files['file'].read()
            filename = request.form.get('filename')
            shared_server_upload = requests.post(SHARED_SERVER_FILE_UPLOAD_PATH,
                                                 files={'file': (filename, uploaded_file)}, headers=upload_headers)
            current_app.logger.debug("Shared Server Response: %s - %s", shared_server_upload.status_code,
                                     shared_server_upload.text)
            file_data = json.loads(shared_server_upload.text)
            if shared_server_upload.ok:
                story_updated = Story.update_file(story_id, file_data['file']['resource'])
                current_app.logger.debug("Python Server Response: %s - %s", shared_server_upload.status_code,
                                         story_updated)
                current_app.logger.info("Sending file ownership request to Shared Server")
                file_ownership_headers = {'content-type': 'application/json',
                                          'Authorization': 'Bearer {}'.format(APP_SERVER_TOKEN)}
                shared_server_file_ownership = requests.post(SHARED_SERVER_FILE_OWNERSHIP_PATH,
                                                             data=json.dumps(file_data['file']),
                                                             headers=file_ownership_headers)
                current_app.logger.debug("Shared Server Response: %s - %s", shared_server_file_ownership.status_code,
                                         shared_server_file_ownership.text)

                return make_response(jsonify(story_updated), 200)

            return make_response(shared_server_upload.text, shared_server_upload.status_code)
        except ValueError as ex:
            error = "Unable to handle FileResource POST Request" + ex
            current_app.logger.error("Python Server Response: 500 - %s", error)
            return ErrorHandler.create_error_response(500, error)
