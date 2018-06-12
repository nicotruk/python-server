from firebase_admin import messaging

from model.user import User, UserNotFoundException


class FirebaseManager:

    @staticmethod
    def send_firebase_message(from_username, to_username, message, notification_type):
        try:
            token = User.get_user_by_username(to_username)["user"]["firebase_token"]
            message = messaging.Message(
                notification=messaging.Notification(
                    title=from_username,
                    body=message
                ),
                data={
                    'notification_type': notification_type
                },
                token=token
            )
            messaging.send(message)
        except UserNotFoundException:
            raise UserNotFoundException
