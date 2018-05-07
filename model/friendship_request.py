from config.mongodb import db
from model.db.friendship_requestVO import FriendshipRequestVO


class FriendshipRequest:

    @staticmethod
    def get_sent_friendship_requests(from_user_id):
        friendship_requests_db_response = list(db.friendship_requests.find({"from_user_id": from_user_id}))
        friendship_requests_response = {
            "friendship_requests": []
        }
        for friendshipDBResponse in friendship_requests_db_response:
            friendship_requests_response["friendship_requests"].append(
                FriendshipRequest._decode_friendship_request(friendshipDBResponse))
        return friendship_requests_response

    @staticmethod
    def get_received_friendship_requests(to_user_id):
        friendship_requests_db_response = list(db.friendship_requests.find({"to_user_id": to_user_id}))
        friendship_requests_response = {
            "friendship_requests": []
        }
        for friendshipDBResponse in friendship_requests_db_response:
            friendship_requests_response["friendship_requests"].append(
                FriendshipRequest._decode_friendship_request(friendshipDBResponse))
        return friendship_requests_response

    @staticmethod
    def create(from_user_id, to_user_id, timestamp):
        new_request = FriendshipRequestVO(None, from_user_id, to_user_id, timestamp)
        encoded_request = FriendshipRequest._encode_friendship_request(new_request)
        db_request = db.friendship_requests.find_one(
            {'from_user_id': encoded_request["from_user_id"], 'to_user_id': encoded_request["to_user_id"]})
        if db_request is None:
            db_request = db.friendship_requests.insert_one(encoded_request)
            response = {
                "friendship_request": {
                    "_id": str(db_request.inserted_id),
                    "from_user_id": encoded_request["from_user_id"],
                    "to_user_id": encoded_request["to_user_id"],
                    "timestamp": encoded_request["timestamp"]
                }
            }
        else:
            response = None
        return response

    @staticmethod
    def _encode_friendship_request(friendship_request):
        return {
            "_type": "friendship_request",
            "from_user_id": friendship_request.from_user_id,
            "to_user_id": friendship_request.to_user_id,
            "timestamp": friendship_request.timestamp
        }

    @staticmethod
    def _decode_friendship_request(document):
        assert document["_type"] == "friendship_request"
        friendship_request = {
            "_id": str(document["_id"]),
            "from_user_id": document["from_user_id"],
            "to_user_id": document["to_user_id"],
            "timestamp": document["timestamp"]
        }
        return friendship_request
