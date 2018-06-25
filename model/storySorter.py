from operator import itemgetter
from datetime import datetime
from dateutil import parser
from flask import current_app
from config.mongodb import db

USER_PUBLICATIONS_MULTIPLIER = 0.1
USER_CONTACTS_MULTIPLIER = 0.2
STORY_TIME_DIFFERENCE_MULTIPLIER = 0.3
REACTIONS_AND_COMMENTS_MULTIPLIER = 0.4


class StorySorter:

    @staticmethod
    def sort_by_importance(stories):
        StorySorter.reset_values()

        for story in stories:
            story["importance"] = StorySorter.get_importance(story)

        return sorted(stories, key=itemgetter("importance"), reverse=True)

    @staticmethod
    def get_importance(story):

        # importancia = (
        #   0.1 * (Cantidad de publicaciones) +          // Usuario con mayor publicaciones, mejor
        #   0.2 * (cantidad de contactos/popularidad) +  // Usuarios con más contactos, mejor
        #   0.3 * (horario/historia reciente) +          // Horario más cercano al actual, mejor (hora actual - hora historia)
        #   0.4 * (cantidad de reacciones)               // Más reacciones por historia mejor
        # )

        # Get user publications (average)
        user_publications = StorySorter.get_user_publications(story["user_id"])

        # Get user's contacts
        user_contacts = StorySorter.get_user_contacts(story["user_id"])

        # Get difference between latest story and current time (it substracts)
        story_time = datetime.utcfromtimestamp((story["timestamp"]))
        diff = story_time - StorySorter.get_present_time()
        story_time_difference = diff.total_seconds() / 60

        # Get story reactions and comments
        reactions_and_comments_count = len(dict.get(story, "reactions", [])) + len(dict.get(story, "comments", []))

        return (USER_PUBLICATIONS_MULTIPLIER * user_publications
                + USER_CONTACTS_MULTIPLIER * user_contacts
                + STORY_TIME_DIFFERENCE_MULTIPLIER * story_time_difference
                + REACTIONS_AND_COMMENTS_MULTIPLIER * reactions_and_comments_count)

    @staticmethod
    def get_present_time():
        if StorySorter.presentTime is None:
            StorySorter.presentTime = datetime.utcnow()

        return StorySorter.presentTime

    @staticmethod
    def get_user_contacts(user_id):
        user = next((x for x in StorySorter.users if x["user_id"] == user_id), None)

        if user is None:
            user = db.users.find_one({"user_id": user_id})
            StorySorter.users.append(user)

        return len(user["friends_usernames"])

    @staticmethod
    def get_user_publications(user_id):
        user = next((x for x in StorySorter.users if x["user_id"] == user_id), None)

        if user is None:
            user = db.users.find_one({"user_id": user_id})
            user["stories_publications"] = db.stories.count({"user_id": user_id})
            StorySorter.users.append(user)

        return user["stories_publications"]

    @staticmethod
    def reset_values():
        StorySorter.presentTime = None
        StorySorter.users = []
