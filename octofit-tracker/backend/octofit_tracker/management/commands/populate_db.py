from django.core.management.base import BaseCommand
from djongo import models
from django.conf import settings
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']

        # Drop collections if they exist
        for col in ['users', 'teams', 'activities', 'leaderboard', 'workouts']:
            db[col].drop()

        # Create unique index on email for users
        db.users.create_index([('email', 1)], unique=True)

        # Sample data
        users = [
            {'name': 'Spider-Man', 'email': 'spiderman@marvel.com', 'team': 'Marvel'},
            {'name': 'Iron Man', 'email': 'ironman@marvel.com', 'team': 'Marvel'},
            {'name': 'Wonder Woman', 'email': 'wonderwoman@dc.com', 'team': 'DC'},
            {'name': 'Batman', 'email': 'batman@dc.com', 'team': 'DC'},
        ]
        teams = [
            {'name': 'Marvel', 'members': ['Spider-Man', 'Iron Man']},
            {'name': 'DC', 'members': ['Wonder Woman', 'Batman']},
        ]
        activities = [
            {'user': 'Spider-Man', 'activity': 'Web Swinging', 'duration': 60},
            {'user': 'Iron Man', 'activity': 'Flight', 'duration': 45},
            {'user': 'Wonder Woman', 'activity': 'Lasso Training', 'duration': 30},
            {'user': 'Batman', 'activity': 'Martial Arts', 'duration': 50},
        ]
        leaderboard = [
            {'team': 'Marvel', 'points': 105},
            {'team': 'DC', 'points': 80},
        ]
        workouts = [
            {'user': 'Spider-Man', 'workout': 'Upper Body', 'suggestion': 'Pull-ups'},
            {'user': 'Iron Man', 'workout': 'Cardio', 'suggestion': 'Running'},
            {'user': 'Wonder Woman', 'workout': 'Strength', 'suggestion': 'Deadlifts'},
            {'user': 'Batman', 'workout': 'Endurance', 'suggestion': 'Cycling'},
        ]

        db.users.insert_many(users)
        db.teams.insert_many(teams)
        db.activities.insert_many(activities)
        db.leaderboard.insert_many(leaderboard)
        db.workouts.insert_many(workouts)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
