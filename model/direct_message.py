from config.mongodb import db
from model.db.direct_messageVO import DirectMessageVO


class DirectMessage:

    @staticmethod
    def create(from_username, to_username, message, timestamp):
        new_direct_message = DirectMessageVO(None, from_username, to_username, message, timestamp)
        encoded_message = DirectMessage._encode_direct_message(new_direct_message)
        db_request = db.direct_messages.insert_one(encoded_message)
        response = {
            "direct_message": {
                "_id": str(db_request.inserted_id),
                "from_username": encoded_message["from_username"],
                "to_username": encoded_message["to_username"],
                "message": encoded_message["message"],
                "timestamp": encoded_message["timestamp"]
            }
        }
        return response

    @staticmethod
    def get_received_direct_messages(to_username):
        direct_messages_db_response = list(db.direct_messages.find({"to_username": to_username}))
        direct_messages_response = {
            "direct_messages": []
        }
        for direct_message_db_response in direct_messages_db_response:
            direct_messages_response["direct_messages"].append(
                DirectMessage._decode_direct_message(direct_message_db_response))
        return direct_messages_response

    @staticmethod
    def _encode_direct_message(direct_message):
        return {
            "_type": "direct_message",
            "from_username": direct_message.from_username,
            "to_username": direct_message.to_username,
            "message": direct_message.message,
            "timestamp": direct_message.timestamp
        }

    @staticmethod
    def _decode_direct_message(document):
        assert document["_type"] == "direct_message"
        direct_message = {
            "_id": str(document["_id"]),
            "from_username": document["from_username"],
            "to_username": document["to_username"],
            "message": document["message"],
            "timestamp": document["timestamp"]
        }
        return direct_message
