import base64
import json

import requests
from flask import request, jsonify, make_response, current_app
from flask_restful import Resource

from config.shared_server_config import SHARED_SERVER_USER_PATH, SHARED_SERVER_TOKEN_PATH, \
    SHARED_SERVER_APPLICATION_OWNER
from model.user import User, UserNotFoundException
from resources.error_handler import ErrorHandler


class UsersResource(Resource):

    def get(self):
        try:
            current_app.logger.info("Received UsersResource GET Request")
            users_response = User.get_all()
            current_app.logger.debug("Python Server Response: 200 - %s", users_response)
            return make_response(jsonify(users_response), 200)
        except ValueError:
            error = "Unable to handle UsersResource GET Request"
            current_app.logger.error("Python Server Response: 500 - %s", error)
            return ErrorHandler.create_error_response(500, error)

    def post(self):
        try:
            current_app.logger.info("Received UsersResource POST Request")
            user_data = json.loads(request.data)

            payload = {
                "username": user_data["username"],
                "password": user_data["password"],
                "applicationOwner": SHARED_SERVER_APPLICATION_OWNER
            }
            headers = {'content-type': 'application/json'}
            signup_response = requests.post(SHARED_SERVER_USER_PATH, data=json.dumps(payload), headers=headers)
            current_app.logger.debug("Shared Server Signup Response: %s - %s", signup_response.status_code,
                                     signup_response.text)
            if signup_response.ok:
                user_created = User.create(user_data["username"], user_data["email"], user_data["name"], '',
                                           user_data["firebase_token"])
                current_app.logger.debug("User created with firebase_token = %s", user_data["firebase_token"])
                payload.pop("applicationOwner")
                login_response = requests.post(SHARED_SERVER_TOKEN_PATH, data=json.dumps(payload), headers=headers)
                current_app.logger.debug("Shared Server Response: %s - %s", login_response.status_code,
                                         login_response.text)
                json_response = json.loads(login_response.text)

                if login_response.ok:
                    built_response = {
                        "user": user_created["user"],
                        "token": {
                            "expiresAt": json_response["token"]["expiresAt"],
                            "token": json_response["token"]["token"]
                        }
                    }
                    current_app.logger.debug("Python Server Response: %s - %s", login_response.status_code,
                                             built_response)
                else:
                    built_response = {
                        "error": {
                            "code": json_response["code"],
                            "message": json_response["message"]
                        }
                    }
                    current_app.logger.error("Python Server Response: %s - %s", login_response.status_code,
                                             built_response)
                return make_response(jsonify(built_response), login_response.status_code)
            current_app.logger.debug("Python Server Response: %s - %s", signup_response.status_code,
                                     signup_response.text)
            return make_response(signup_response.text, signup_response.status_code)
        except ValueError:
            error = "Unable to handle UsersResource POST Request"
            current_app.logger.error("Python Server Response: 500 - %s", error)
            return ErrorHandler.create_error_response(500, error)


class FacebookLoginResource(Resource):
    def post(self):
        try:
            current_app.logger.info("Received FacebookLoginResource POST Request")
            user_data = json.loads(request.data)

            payload = {
                "username": user_data["username"],
                "password": user_data["username"],
                "applicationOwner": SHARED_SERVER_APPLICATION_OWNER
            }
            headers = {'content-type': 'application/json'}

            user = User.get_facebook_user(user_data["username"])

            if user["user"] is None:
                signup_response = requests.post(SHARED_SERVER_USER_PATH, data=json.dumps(payload), headers=headers)
                current_app.logger.debug("Shared Server Signup Response: %s - %s", signup_response.status_code,
                                         signup_response.text)

                if not signup_response.ok and signup_response.status_code != 400:
                    current_app.logger.debug("Python Server Response: %s - %s", signup_response.status_code,
                                             signup_response.text)
                    return make_response(signup_response.text, signup_response.status_code)
                else:
                    profile_pic_url = user_data["profile_pic"]
                    profile_pic_bytes = base64.b64encode(requests.get(profile_pic_url).content)
                    profile_pic_string = profile_pic_bytes.decode('utf-8')

                    user = User.create(user_data["username"], user_data["email"], user_data["name"], profile_pic_string)

            payload.pop("applicationOwner")
            login_response = requests.post(SHARED_SERVER_TOKEN_PATH, data=json.dumps(payload), headers=headers)
            current_app.logger.debug("Shared Server Response: %s - %s", login_response.status_code, login_response.text)
            json_response = json.loads(login_response.text)

            if login_response.ok:
                built_response = {
                    "user": user["user"],
                    "token": {
                        "expiresAt": json_response["token"]["expiresAt"],
                        "token": json_response["token"]["token"]
                    }
                }
                current_app.logger.debug("Python Server Response: %s - %s", login_response.status_code, built_response)
            else:
                built_response = {
                    "error": {
                        "code": json_response["code"],
                        "message": json_response["message"]
                    }
                }
                current_app.logger.error("Python Server Response: %s - %s", login_response.status_code, built_response)
            return make_response(jsonify(built_response), login_response.status_code)
        except ValueError:
            error = "Unable to handle FacebookLoginResource POST Request"
            current_app.logger.error("Python Server Response: 500 - %s", error)
            return ErrorHandler.create_error_response(500, error)


class SingleUserResource(Resource):
    def get(self, user_id):
        try:
            current_app.logger.info("Received SingleUserResource GET Request")
            user = User.get_user_by_id(user_id)
            current_app.logger.debug("Python Server Response: 200 - %s", user)
            return make_response(jsonify(user), 200)
        except UserNotFoundException as e:
            status_code = 403
            message = e.args[0]
            current_app.logger.error("Python Server Response: %s - %s", status_code, message)
            return ErrorHandler.create_error_response(status_code, message)

    def put(self, user_id):
        try:
            current_app.logger.info("Received SingleUserResource PUT Request")
            request_data = json.loads(request.data)

            updated_user = User.update_user(user_id, request_data["name"],
                                            request_data["email"], request_data["profile_pic"])

            current_app.logger.debug("Python Server Response: 200 - %s", updated_user)
            return make_response(jsonify(updated_user), 200)
        except UserNotFoundException as e:
            status_code = 403
            message = e.args[0]
            current_app.logger.error("Python Server Response: %s - %s", status_code, message)
            return ErrorHandler.create_error_response(status_code, message)


class UserLoginResource(Resource):
    def post(self):
        try:
            current_app.logger.info("Received UserLoginResource POST Request")
            credentials = json.loads(request.data)
            payload = {
                "username": credentials["username"],
                "password": credentials["password"]
            }
            headers = {'content-type': 'application/json'}
            response = requests.post(SHARED_SERVER_TOKEN_PATH, data=json.dumps(payload), headers=headers)
            current_app.logger.debug("Shared Server Response: %s - %s", response.status_code, response.text)
            json_response = json.loads(response.text)
            if response.ok:
                user_id_response = User.get_user_id_by_username(credentials["username"])

                built_response = {
                    "token": {
                        "expiresAt": json_response["token"]["expiresAt"],
                        "token": json_response["token"]["token"]
                    },
                    "user_id": user_id_response["user_id"]
                }
                current_app.logger.debug("Python Server Response: %s - %s", response.status_code, built_response)
            else:
                built_response = {
                    "error": {
                        "code": json_response["code"],
                        "message": json_response["message"]
                    }
                }
                current_app.logger.error("Python Server Response: %s - %s", response.status_code, built_response)
            return make_response(jsonify(built_response), response.status_code)
        except ValueError:
            error = "Unable to handle UsersResource POST Request"
            current_app.logger.error("Python Server Response: %s - %s", 500, error)
            return ErrorHandler.create_error_response(500, error)


class UserSearchResource(Resource):
    def get(self, user_id, partial_username):
        try:
            current_app.logger.info("Received UserSearchResource GET Request")
            users_response = User.get_all()
            users = users_response["users"]

            built_response = {
                "found_users": []
            }

            current_username = User.get_user_by_id(user_id)["user"]["username"]

            if users:
                for user in users:
                    if partial_username in user["username"] and user_id != user["user_id"] and current_username not in \
                            user["friends_usernames"]:
                        final_user = {
                            "username": user["username"],
                            "profile_pic": user["profile_pic"],
                            "name": user["name"]
                        }

                        built_response["found_users"].append(final_user)

            current_app.logger.debug("Python Server Response: 200 - %s", built_response)

            return make_response(jsonify(built_response), 200)
        except ValueError:
            error = "Unable to handle UserSearchResource GET Request"
            current_app.logger.error("Python Server Response: 500 - %s", error)
            return ErrorHandler.create_error_response(500, error)
        except UserNotFoundException as e:
            status_code = 403
            message = e.args[0]
            current_app.logger.error("Python Server Response: %s - %s", status_code, message)
            return ErrorHandler.create_error_response(status_code, message)


class UserFriendsResource(Resource):
    def get(self, user_id):
        try:
            current_app.logger.info("Received UserFriendsResource GET Request")
            user = User.get_user_by_id(user_id)

            friends_usernames = user["user"]["friends_usernames"]

            response = {
                "friends": []
            }

            if friends_usernames:
                for username in friends_usernames:
                    return_friend = User.get_user_by_username(username)["user"]
                    friend = {
                        "username": username,
                        "profile_pic": return_friend["profile_pic"],
                        "name": return_friend["name"]
                    }
                    response["friends"].append(friend)

            current_app.logger.debug("Python Server Response: 200 - %s", user)
            return make_response(jsonify(response), 200)
        except UserNotFoundException as e:
            status_code = 403
            message = e.args[0]
            current_app.logger.error("Python Server Response: %s - %s", status_code, message)
            return ErrorHandler.create_error_response(status_code, message)


class UserFirebaseTokenResource(Resource):
    def put(self, user_id):
        try:
            current_app.logger.info("Received UserFirebaseTokenResource PUT Request")
            request_data = json.loads(request.data)

            updated_user = User.update_user_firebase_token(user_id, request_data["firebase_token"])

            current_app.logger.debug("Python Server Response: 200 - %s", updated_user)
            return make_response(jsonify(updated_user), 200)
        except UserNotFoundException as e:
            status_code = 403
            message = e.args[0]
            current_app.logger.error("Python Server Response: %s - %s", status_code, message)
            return ErrorHandler.create_error_response(status_code, message)
