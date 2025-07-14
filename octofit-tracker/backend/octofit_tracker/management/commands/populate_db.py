from django.core.management.base import BaseCommand
from pymongo import MongoClient
from pymongo.errors import BulkWriteError
from django.conf import settings

class Command(BaseCommand):
    help = 'Populate the MongoDB database with test data'

    def handle(self, *args, **kwargs):
        client = MongoClient(settings.MONGO_CONNECTION['host'], settings.MONGO_CONNECTION['port'])
        db = client[settings.MONGO_CONNECTION['db_name']]

        try:
            # Insert test data
            db.users.insert_many([
                {"email": "user1@example.com", "name": "User One"},
                {"email": "user2@example.com", "name": "User Two"}
            ], ordered=False)
        except BulkWriteError as e:
            self.stdout.write(self.style.WARNING(f"Users: {e.details['writeErrors']}"))

        try:
            db.teams.insert_one({
                "name": "Team A",
                "members": ["user1@example.com", "user2@example.com"]
            })
        except BulkWriteError as e:
            self.stdout.write(self.style.WARNING(f"Teams: {e.details['writeErrors']}"))

        try:
            db.activity.insert_many([
                {"user": "user1@example.com", "type": "running", "duration": 30},
                {"user": "user2@example.com", "type": "cycling", "duration": 45}
            ], ordered=False)
        except BulkWriteError as e:
            self.stdout.write(self.style.WARNING(f"Activity: {e.details['writeErrors']}"))

        try:
            db.leaderboard.insert_one({
                "team": "Team A",
                "points": 150
            })
        except BulkWriteError as e:
            self.stdout.write(self.style.WARNING(f"Leaderboard: {e.details['writeErrors']}"))

        try:
            db.workouts.insert_many([
                {"name": "Workout 1", "description": "A sample workout"},
                {"name": "Workout 2", "description": "Another sample workout"}
            ], ordered=False)
        except BulkWriteError as e:
            self.stdout.write(self.style.WARNING(f"Workouts: {e.details['writeErrors']}"))

        self.stdout.write(self.style.SUCCESS('Database population completed with test data'))
