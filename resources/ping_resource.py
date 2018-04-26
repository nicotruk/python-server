import requests
from flask_restful import Resource
from flask import Response
from shared_server_config import SHARED_SERVER_PING_PATH
import logging

SUCCESS_MESSAGE = 'Connected'


class PingResource(Resource):
    def get(self):
        logging.info("Received PingResource GET Request")
        logging.debug("Python Server Response: 200 - %s", SUCCESS_MESSAGE)
        return Response(SUCCESS_MESSAGE, 200)


class PingSharedServerResource(Resource):
    def get(self):
        logging.info("Received PingSharedServerResource GET Request")
        logging.info("Sending Request to Shared Server at:" + SHARED_SERVER_PING_PATH)
        response = requests.get(SHARED_SERVER_PING_PATH)
        logging.debug("Shared Server Response: %s", response.status_code)
        if response.ok:
            logging.debug("Python Server Response: 200 - %s", SUCCESS_MESSAGE)
            return Response(SUCCESS_MESSAGE, 200)
        else:
            logging.info("Python Server Response: None")
            return None
