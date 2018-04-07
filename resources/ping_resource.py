import requests
from flask_restful import Resource
from flask import Response
from shared_server_config import SHARED_SERVER_URI

SUCCESS_MESSAGE = 'Connected'


class PingResource(Resource):
    def get(self):
        return Response(SUCCESS_MESSAGE, 200)


class PingSharedServerResource(Resource):
    def get(self):
        response = requests.get(SHARED_SERVER_URI)
        if response.ok:
            return Response(SUCCESS_MESSAGE, 200)
        else:
            return None
