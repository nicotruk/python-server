
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
    def sortByImportance(stories):
      StorySorter.resetValues()

      for story in stories:
        story["importance"] = StorySorter.getImportance(story)

      return sorted(stories, key=itemgetter("importance"), reverse=True)

    @staticmethod
    def getImportance(story):

      # importancia = (
      #   0.1 * (Cantidad de publicaciones) +          // Usuario con mayor publicaciones, mejor
      #   0.2 * (cantidad de contactos/popularidad) +  // Usuarios con más contactos, mejor
      #   0.3 * (horario/historia reciente) +          // Horario más cercano al actual, mejor (hora actual - hora historia)
      #   0.4 * (cantidad de reacciones)               // Más reacciones por historia mejor
      # )

      # Get user publications (average)
      userPublications = StorySorter.getUserPublications(story["user_id"])

      # Get user's contacts
      userContacts = StorySorter.getUserContacts(story["user_id"])

      # Get difference between latest story and current time (it substracts)
      storyTime = parser.parse(story["timestamp"])
      diff = storyTime - StorySorter.getPresentTime()
      storyTimeDifference = diff.total_seconds() / 60

      # Get story reactions and comments
      reactionsAndCommentsCount = len(dict.get(story, "reactions", [])) + len(dict.get(story, "comments", []))

      return (USER_PUBLICATIONS_MULTIPLIER * userPublications
        + USER_CONTACTS_MULTIPLIER * userContacts
        + STORY_TIME_DIFFERENCE_MULTIPLIER * storyTimeDifference
        + REACTIONS_AND_COMMENTS_MULTIPLIER * reactionsAndCommentsCount)

    @staticmethod
    def getPresentTime():
      if (StorySorter.presentTime is None):
        StorySorter.presentTime = datetime.utcnow()

      return StorySorter.presentTime

    @staticmethod
    def getUserContacts(user_id):
      user = next((x for x in StorySorter.users if x["user_id"] == user_id), None)

      if (user is None):
        user = db.users.find_one({"user_id": user_id})
        StorySorter.users.append(user)

      return len(user["friends_usernames"])

    @staticmethod
    def getUserPublications(user_id):
      user = next((x for x in StorySorter.users if x["user_id"] == user_id), None)

      if (user is None):
        current_app.logger.info("Noo user")
        user = db.users.find_one({"user_id": user_id})
        user["stories_publications"] = db.stories.count({ "user_id": user_id })
        StorySorter.users.append(user)

      return user["stories_publications"]

    @staticmethod
    def resetValues():
      StorySorter.presentTime = None
      StorySorter.users = []
