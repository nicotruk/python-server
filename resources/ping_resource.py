import requests
from flask import Response, current_app
from flask_restful import Resource

from config.shared_server_config import SHARED_SERVER_PING_PATH

SUCCESS_MESSAGE = 'Connected'

class PingResource(Resource):
    def get(self):
        current_app.logger.info("Received PingResource GET Request")
        current_app.logger.debug("Python Server Response: 200 - %s", SUCCESS_MESSAGE)
        return Response(SUCCESS_MESSAGE, 200)


class PingSharedServerResource(Resource):
    def get(self):
        current_app.logger.info("Received PingSharedServerResource GET Request")
        current_app.logger.info("Sending Request to Shared Server at:" + SHARED_SERVER_PING_PATH)
        response = requests.get(SHARED_SERVER_PING_PATH)
        current_app.logger.debug("Shared Server Response: %s", response.status_code)
        if response.ok:
            current_app.logger.debug("Python Server Response: 200 - %s", SUCCESS_MESSAGE)
            return Response(SUCCESS_MESSAGE, 200)
        else:
            failure_message = "Connection to Shared Server failed"
            current_app.logger.warning("Python Server Response: 404 - %s", failure_message)
            return Response(failure_message, 404)
