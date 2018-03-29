from flask import Flask
from flask_restful import Api


app = Flask(__name__)

api = Api(app, prefix="/api/v1")


@app.route('/')
def hello_world():
    return "Hi, I'm root!"


if __name__ == '__main__':
    app.run()