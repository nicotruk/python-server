from functools import wraps
import json

import requests
from flask import request, make_response, current_app

from config.shared_server_config import SHARED_SERVER_TOKEN_VALIDATION_PATH, SHARED_SERVER_TOKEN


def token_validation_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_app.logger.info("Validating the user token with the shared server")
        token_headers = {'content-type': 'application/json', 'Authorization': 'Bearer {}'.format(SHARED_SERVER_TOKEN)}
        user_token = request.headers.get('Authorization').split()[1]
        token_validation_payload = {
            "token": user_token
        }
        token_validation_response = requests.post(SHARED_SERVER_TOKEN_VALIDATION_PATH,
                                                  data=json.dumps(token_validation_payload), headers=token_headers)
        if token_validation_response.ok:
            current_app.logger.info("User token was validated successfully")
            return f(*args, **kwargs)
        current_app.logger.info("User token could not be validated")
        return make_response(token_validation_response.text, token_validation_response.status_code)
    return decorated_function
