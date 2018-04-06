import json
from flask import request
from flask_restful import Resource
from cats import cats


class CatResource(Resource):
    def get(self):
        return cats

    def post(self):
        cat = json.loads(request.data)
        cats.append(cat)
        return cat
