from flask import jsonify, make_response, current_app
from flask_restful import Resource

from model.stats import StatManager
from resources.error_handler import ErrorHandler


class StatsResource(Resource):
    def get(self):
        try:
            current_app.logger.info("Received StatsResource GET Request")
            stats = StatManager.get_stats()
            current_app.logger.debug("Python Server Response: 200 - %s", stats)
            return make_response(jsonify(stats), 200)
        except ValueError:
            error = "Unable to handle StatsResource GET Request"
            current_app.logger.error("Python Server Response: 500 - %s", error)
            return ErrorHandler.create_error_response(500, error)


class LastXMinStatsResource(Resource):
    def get(self, minutes):
        try:
            current_app.logger.info("Received StatsResource GET Request")
            stats = StatManager.get_stats_from_last_min(minutes)
            current_app.logger.debug("Python Server Response: 200 - %s", stats)
            return make_response(jsonify(stats), 200)
        except ValueError:
            error = "Unable to handle StatsResource GET Request"
            current_app.logger.error("Python Server Response: 500 - %s", error)
            return ErrorHandler.create_error_response(500, error)


class Last10DaysStoriesRequestsStatsResource(Resource):
    def get(self):
        try:
            current_app.logger.info("Received StatsResource GET Request")
            stats = StatManager.get_stories_stats_from_last_10_days()
            current_app.logger.debug("Python Server Response: 200 - %s", stats)
            return make_response(jsonify(stats), 200)
        except ValueError:
            error = "Unable to handle StatsResource GET Request"
            current_app.logger.error("Python Server Response: 500 - %s", error)
            return ErrorHandler.create_error_response(500, error)


