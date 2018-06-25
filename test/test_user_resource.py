# Lo siguiente debe inicializarse en setup.py
import os
import sys

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')
########
from config.mongodb import db
from app import app
from mock import patch
import unittest
import json
import config.firebase_config

test_user = {
    "username": "asd",
    "password": "123",
    "email": "asd@asd.com",
    "name": "Nombre Apellido",
    "profile_pic": "",
    "firebase_token": "fdsfsdfjsdkfhsdjklhjk23h4234",
}

headers = {'content-type': 'application/json', 'Authorization': 'Bearer {}'.format("asd")}


class UsersResourceTestCase(unittest.TestCase):

    def setUp(self):
        config.firebase_config.FIREBASE_NOTIFICATIONS_ENABLED = False
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        with app.app_context():
            db.users.delete_many({})
            db.friendship_requests.delete_many({})
            db.requests_stats.delete_many({})

    # /users GET
    @patch('resources.token_validation_decorator.requests.post')
    def test_get_all_users(self, mock_post):
        mock_post.return_value.status_code = 200
        response = self.app.get("/api/v1/users", headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_count_zero_users(self):
        response = self.app.get("/api/v1/users/count", headers=headers)
        self.assertEqual(response.status_code, 200)
        count = json.loads(response.data)["count"]
        self.assertEqual(count, 0)

    @patch('resources.user_resource.requests.post')
    def test_count_all_users(self, mock_post):
        mock_post.return_value.status_code = 200
        response = {
            "token": {
                "expiresAt": "123",
                "token": "asd"
            }
        }
        mock_post.return_value.text = json.dumps(response)
        user = test_user.copy()
        self.app.post("/api/v1/users",
                      data=json.dumps(user),
                      headers=headers)
        response = self.app.get("/api/v1/users/count", headers=headers)
        self.assertEqual(response.status_code, 200)
        count = json.loads(response.data)["count"]
        self.assertEqual(count, 1)

    # /users POST
    @patch('resources.user_resource.requests.post')
    def test_post_user(self, mock_post):
        mock_post.return_value.status_code = 200
        response = {
            "token": {
                "expiresAt": "123",
                "token": "asd"
            }
        }
        mock_post.return_value.text = json.dumps(response)

        user = test_user.copy()

        response = self.app.post("/api/v1/users",
                                 data=json.dumps(user),
                                 headers=headers)

        self.assertEqual(response.status_code, 200)
        user_response = json.loads(response.data)
        user.pop('password')
        user["user_id"] = user_response["user"]["user_id"]
        self.assertEqual(user, user_response["user"])

    # /users POST
    def test_post_user_with_no_data(self):
        user = ""
        response = self.app.post("/api/v1/users",
                                 data=json.dumps(user),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 500)

    # /users POST + /users/<user_id> PUT
    @patch('resources.user_resource.requests.post')
    def test_update_user(self, mock_post):
        mock_post.return_value.status_code = 200
        response = {
            "token": {
                "expiresAt": "123",
                "token": "asd"
            }
        }
        mock_post.return_value.text = json.dumps(response)

        user = test_user.copy()

        post_response = self.app.post("/api/v1/users",
                                      data=json.dumps(user),
                                      content_type='application/json')

        user_response = json.loads(post_response.data)
        user_id = user_response["user"]["user_id"]

        changes = {
            "name": "new_name",
            "email": "new_email",
            "profile_pic": "new_profile_pic"
        }

        update_response = self.app.put("/api/v1/users/{}".format(user_id),
                                       headers=headers,
                                       data=json.dumps(changes))

        json_response = json.loads(update_response.data)

        self.assertEqual(json_response["user"]["name"], changes["name"])
        self.assertEqual(json_response["user"]["email"], changes["email"])
        self.assertEqual(json_response["user"]["profile_pic"], changes["profile_pic"])

    # /users POST + /users/firebase/<user_id> PUT
    @patch('resources.user_resource.requests.post')
    def test_update_firebase_token(self, mock_post):
        mock_post.return_value.status_code = 200
        response = {
            "token": {
                "expiresAt": "123",
                "token": "asd"
            }
        }
        mock_post.return_value.text = json.dumps(response)

        user = test_user.copy()

        post_response = self.app.post("/api/v1/users",
                                      data=json.dumps(user),
                                      content_type='application/json')

        user_response = json.loads(post_response.data)
        user_id = user_response["user"]["user_id"]

        changes = {
            "firebase_token": "newFirebaseToken"
        }

        update_response = self.app.put("/api/v1/users/firebase/{}".format(user_id),
                                       data=json.dumps(changes),
                                       content_type='application/json')

        json_response = json.loads(update_response.data)

        self.assertEqual(json_response["user"]["firebase_token"], changes["firebase_token"])

    # /users/<user_id> GET
    @patch('resources.token_validation_decorator.requests.post')
    def test_get_single_user_error_user_not_found(self, mock_post):
        mock_post.return_value.status_code = 200
        response = self.app.get("/api/v1/users/1234", headers=headers)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(json.loads(response.data)["message"], "There is no user with that ID!")

    # /users POST + /users/login POST
    @patch('resources.user_resource.requests.post')
    def test_login(self, mock_post):
        user = test_user.copy()

        self.app.post("/api/v1/users",
                      data=json.dumps(user),
                      content_type='application/json')

        response = {
            "token": {
                "expiresAt": "123",
                "token": "asd"
            }
        }
        mock_post.return_value.text = json.dumps(response)
        mock_post.return_value.status_code = 200

        user = {
            "username": "asd",
            "password": "123"
        }
        response = self.app.post("/api/v1/users/login",
                                 data=json.dumps(user),
                                 content_type='application/json')

        self.assertEqual(response.status_code, 200)

    # /users POST + /users GET
    @patch('resources.user_resource.requests.post')
    def test_integration_create_user(self, mock_post):
        mock_post.return_value.status_code = 200
        response = {
            "token": {
                "expiresAt": "123",
                "token": "asd"
            }
        }
        mock_post.return_value.text = json.dumps(response)

        user = test_user.copy()
        user["profile_pic"] = ''
        user["friends_usernames"] = []

        response = self.app.post("/api/v1/users",
                                 data=json.dumps(user),
                                 content_type='application/json')

        user_response = json.loads(response.data)
        user.pop('password')
        user["user_id"] = user_response["user"]["user_id"]

        get_response = self.app.get("/api/v1/users", headers=headers)
        self.assertIn(user, json.loads(get_response.data)["users"])

    # /users POST + /users/<user_id> GET
    @patch('resources.user_resource.requests.post')
    def test_integration_get_single_user(self, mock_post):
        mock_post.return_value.status_code = 200
        response = {
            "token": {
                "expiresAt": "123",
                "token": "asd"
            }
        }
        mock_post.return_value.text = json.dumps(response)

        user = test_user.copy()
        user["profile_pic"] = ''
        user["friends_usernames"] = []

        response = self.app.post("/api/v1/users",
                                 data=json.dumps(user),
                                 content_type='application/json')

        user_response = json.loads(response.data)
        user.pop('password')
        user["user_id"] = user_response["user"]["user_id"]

        get_response1 = self.app.get('/api/v1/users/{}'.format(user["user_id"]), headers=headers)
        self.assertEqual(user, json.loads(get_response1.data)["user"])
        get_response2 = self.app.get('/api/v1/users/info/{}'.format(user["username"]), headers=headers)
        self.assertEqual(user, json.loads(get_response2.data)["user"])
        self.assertEqual(json.loads(get_response1.data)["user"], json.loads(get_response2.data)["user"])

    # /users/search/<user_id>/<query> GET
    @patch('resources.token_validation_decorator.requests.post')
    def test_user_search_user_not_found(self, mock_post):
        mock_post.return_value.status_code = 200
        response = self.app.get("/api/v1/users/search/{}/{}".format("nonExistentUserId", "aaa"), headers=headers)
        self.assertEqual(response.status_code, 403)

    # /users POST + /users/search/<user_id>/<query> GET
    @patch('resources.user_resource.requests.post')
    def test_user_search_no_match(self, mock_post):
        mock_post.return_value.status_code = 200
        response = {
            "token": {
                "expiresAt": "123",
                "token": "asd"
            }
        }
        mock_post.return_value.text = json.dumps(response)

        user = test_user.copy()
        response = self.app.post("/api/v1/users",
                                 data=json.dumps(user),
                                 content_type='application/json')
        user = json.loads(response.data)["user"]

        user2 = test_user.copy()
        user2["username"] = "anotherName"
        self.app.post("/api/v1/users",
                      data=json.dumps(user2),
                      content_type='application/json')

        query_username = user2["username"] + "1"
        self.assertGreater(len(query_username), len(user2["username"]))
        response = self.app.get("/api/v1/users/search/{}/{}".format(user["user_id"], query_username), headers=headers)
        self.assertEqual(response.status_code, 200)
        found_users = json.loads(response.data)["found_users"]
        self.assertEqual(len(found_users), 0)

    # /users POST + /users/search/<user_id>/<query> GET
    @patch('resources.user_resource.requests.post')
    def test_user_search_one_match(self, mock_post):
        mock_post.return_value.status_code = 200
        response = {
            "token": {
                "expiresAt": "123",
                "token": "asd"
            }
        }
        mock_post.return_value.text = json.dumps(response)

        user = test_user.copy()
        response = self.app.post("/api/v1/users",
                                 data=json.dumps(user),
                                 content_type='application/json')
        user = json.loads(response.data)["user"]

        user2 = test_user.copy()
        user2["username"] = "anotherName"
        self.app.post("/api/v1/users",
                      data=json.dumps(user2),
                      content_type='application/json')
        user3 = test_user.copy()
        user3["username"] = "oneNoMatchingName"
        self.app.post("/api/v1/users",
                      data=json.dumps(user3),
                      content_type='application/json')

        query_username = user2["username"][0:-2]
        self.assertGreater(len(user2["username"]), len(query_username))
        response = self.app.get("/api/v1/users/search/{}/{}".format(user["user_id"], query_username), headers=headers)
        self.assertEqual(response.status_code, 200)
        found_users = json.loads(response.data)["found_users"]
        self.assertEqual(len(found_users), 1)
        self.assertEqual(found_users[0]["username"], user2["username"])

    # /users POST + /users/search/<user_id>/<query> GET
    @patch('resources.user_resource.requests.post')
    def test_user_search_yes_match_if_friend(self, mock_post):
        mock_post.return_value.status_code = 200

        response = {
            "token": {
                "expiresAt": "123",
                "token": "asd"
            }
        }
        mock_post.return_value.text = json.dumps(response)

        user = test_user.copy()
        response = self.app.post("/api/v1/users",
                                 data=json.dumps(user),
                                 content_type='application/json')
        user = json.loads(response.data)["user"]

        friend_username = "anotherName"
        user2 = test_user.copy()
        user2["username"] = friend_username
        self.app.post("/api/v1/users",
                      data=json.dumps(user2),
                      content_type='application/json')

        friendship_request = {
            "from_username": user["username"],
            "to_username": user2["username"]
        }
        self.app.post("/api/v1/friendship/request",
                      data=json.dumps(friendship_request),
                      headers=headers)
        self.app.post("/api/v1/friendship",
                      data=json.dumps(friendship_request),
                      headers=headers)

        response = self.app.get("/api/v1/users/search/{}/{}".format(user["user_id"], friend_username),
                                headers=headers)
        self.assertEqual(response.status_code, 200)
        found_users = json.loads(response.data)["found_users"]
        self.assertEqual(len(found_users), 1)

    # /users POST + /users/friends/<user_id> GET
    @patch('resources.token_validation_decorator.requests.post')
    def test_users_friends_user_not_found(self, mock_post):
        mock_post.return_value.status_code = 200
        response = self.app.get("/api/v1/users/friends/{}".format("sarasa_id"), headers=headers)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(json.loads(response.data)["message"], "There is no user with that username!")

    # /users/friends/<user_id> GET
    @patch('resources.user_resource.requests.post')
    def test_users_friends(self, mock_post):
        mock_post.return_value.status_code = 200
        response = {
            "token": {
                "expiresAt": "123",
                "token": "asd"
            }
        }
        mock_post.return_value.text = json.dumps(response)
        user = test_user.copy()
        response = self.app.post("/api/v1/users",
                                 data=json.dumps(user),
                                 content_type='application/json')
        username = json.loads(response.data)["user"]["username"]
        user2 = test_user.copy()
        user2["username"] = user["username"] + "1"
        self.app.post("/api/v1/users",
                      data=json.dumps(user2),
                      content_type='application/json')

        response = self.app.get("/api/v1/users/friends/{}".format(username), headers=headers)
        self.assertEqual(response.status_code, 200)
        friends = json.loads(response.data)["friends"]
        self.assertEqual(len(friends), 0)

    # /users POST + /friendship/request POST + /friendship POST + /users/friends/<user_id> GET
    @patch('resources.user_resource.requests.post')
    def test_users_friends(self, mock_post):
        mock_post.return_value.status_code = 200
        response = {
            "token": {
                "expiresAt": "123",
                "token": "asd"
            }
        }
        mock_post.return_value.text = json.dumps(response)
        user = test_user.copy()
        response = self.app.post("/api/v1/users",
                                 data=json.dumps(user),
                                 content_type='application/json')
        username = json.loads(response.data)["user"]["username"]
        user2 = test_user.copy()
        user2["username"] = user["username"] + "1"
        self.app.post("/api/v1/users",
                      data=json.dumps(user2),
                      content_type='application/json')

        friendship_request = {
            "from_username": user["username"],
            "to_username": user2["username"]
        }
        self.app.post("/api/v1/friendship/request",
                      data=json.dumps(friendship_request),
                      headers=headers)
        self.app.post("/api/v1/friendship",
                      data=json.dumps(friendship_request),
                      headers=headers)

        response = self.app.get("/api/v1/users/friends/{}".format(username), headers=headers)
        self.assertEqual(response.status_code, 200)
        friends = json.loads(response.data)["friends"]
        self.assertEqual(len(friends), 1)
        self.assertEqual(friends[0]["username"], user2["username"])

    # /users POST + /users/fb_login POST
    @patch('resources.user_resource.requests.post')
    def test_facebook_login_user_already_created(self, mock_post):
        mock_post.return_value.status_code = 200
        response = {
            "token": {
                "expiresAt": "123",
                "token": "asd"
            }
        }
        mock_post.return_value.text = json.dumps(response)

        user = test_user.copy()

        self.app.post("/api/v1/users",
                      data=json.dumps(user),
                      content_type='application/json')

        fb_login_response = self.app.post("/api/v1/users/fb_login",
                                          data=json.dumps(user),
                                          content_type='application/json')
        self.assertEqual(fb_login_response.status_code, 200)
        response_data = json.loads(fb_login_response.data)
        self.assertEqual(response["token"], response_data["token"])
        response_data["user"].pop("user_id")
        user.pop("password")
        self.assertEqual(user, response_data["user"])

    # /users POST + /users/fb_login POST
    @patch('resources.user_resource.requests.post')
    def test_facebook_login_500_on_shared_server_500_on_app_server(self, mock_post):
        mock_post.return_value.status_code = 500
        mock_post.return_value.ok = False
        mock_post.return_value.text = "Internal error"

        user = test_user.copy()

        fb_login_response = self.app.post("/api/v1/users/fb_login",
                                          data=json.dumps(user),
                                          content_type='application/json')
        self.assertEqual(fb_login_response.status_code, 500)
