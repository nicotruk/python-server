import time

from config.mongodb import db
from model.db.statVO import StatVO


class StatManager:

    @staticmethod
    def get_stats():
        stats_db_response = list(db.requests_stats.find())
        stats_response = {
            "stats": []
        }

        for statDBResponse in stats_db_response:
            stats_response["stats"].append(StatManager._decode_stat(statDBResponse))

        return stats_response

    @staticmethod
    def get_stats_from_last_min(last_min):
        actual_time = int(round(time.time() * 1000))
        x_min_before_time = actual_time - (int(last_min) * 60 * 1000)
        stats_db_response = list(db.requests_stats.find({"timestamp": {"$gte": x_min_before_time}}))
        stats_response = {
            "stats": []
        }

        for statDBResponse in stats_db_response:
            stats_response["stats"].append(StatManager._decode_stat(statDBResponse))

        return stats_response

    @staticmethod
    def create(request):
        new_stat = StatVO(request, int(round(time.time() * 1000)))
        encoded_stat = StatManager._encode_stat(new_stat)
        db.requests_stats.insert_one(encoded_stat)
        response = {
            "stat": {
                "request": encoded_stat["request"],
                "timestamp": encoded_stat["timestamp"]
            }
        }
        return response

    @staticmethod
    def _encode_stat(stat):
        return {
            "_type": "stat",
            "request": stat.request,
            "timestamp": stat.timestamp
        }

    @staticmethod
    def _decode_stat(document):
        assert document["_type"] == "stat"
        stat = {
            "request": document["request"],
            "timestamp": document["timestamp"]
        }
        return stat
