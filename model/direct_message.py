from config.mongodb import db
from model.db.direct_messageVO import DirectMessageVO


class DirectMessage:

    @staticmethod
    def create(from_user_id, to_user_id, message, timestamp):
        new_direct_message = DirectMessageVO(None, from_user_id, to_user_id, message, timestamp)
        encoded_message = DirectMessage._encode_direct_message(new_direct_message)
        db_request = db.direct_messages.insert_one(encoded_message)
        response = {
            "direct_message": {
                "_id": str(db_request.inserted_id),
                "from_user_id": encoded_message["from_user_id"],
                "to_user_id": encoded_message["to_user_id"],
                "message": encoded_message["message"],
                "timestamp": encoded_message["timestamp"]
            }
        }
        return response

    @staticmethod
    def get_received_direct_messages(to_user_id):
        direct_messages_db_response = list(db.direct_messages.find({"to_user_id": to_user_id}))
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
            "from_user_id": direct_message.from_user_id,
            "to_user_id": direct_message.to_user_id,
            "message": direct_message.message,
            "timestamp": direct_message.timestamp
        }

    @staticmethod
    def _decode_direct_message(document):
        assert document["_type"] == "direct_message"
        direct_message = {
            "_id": str(document["_id"]),
            "from_user_id": document["from_user_id"],
            "to_user_id": document["to_user_id"],
            "message": document["message"],
            "timestamp": document["timestamp"]
        }
        return direct_message
