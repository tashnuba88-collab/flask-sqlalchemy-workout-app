#!/usr/bin/env python3
from datetime import date

from app import app
from models import *

with app.app_context():
    # Clear child table first, then parents
    print('Clearing tables...')
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()
    db.session.commit()

    print('Creating exercises...')
    squat = Exercise(name='Squat', category='Strength', equipment_needed=True)
    pushup = Exercise(name='Push-up', category='Strength', equipment_needed=False)
    plank = Exercise(name='Plank', category='Core', equipment_needed=False)
    run = Exercise(name='Treadmill Run', category='Cardio', equipment_needed=True)
    db.session.add_all([squat, pushup, plank, run])
    db.session.commit()

    print('Creating workouts...')
    w1 = Workout(date=date(2026, 10, 20), duration_minutes=45, notes='Leg day')
    w2 = Workout(date=date(2026, 10, 22), duration_minutes=30, notes='Quick full body')
    w3 = Workout(date=date(2026, 10, 24), duration_minutes=60, notes=None)
    db.session.add_all([w1, w2, w3])
    db.session.commit()

    print('Linking exercises to workouts...')
    links = [
        WorkoutExercise(workout_id=w1.id, exercise_id=squat.id, sets=4, reps=8),
        WorkoutExercise(workout_id=w1.id, exercise_id=plank.id, duration_seconds=90),
        WorkoutExercise(workout_id=w2.id, exercise_id=pushup.id, sets=3, reps=15),
        WorkoutExercise(workout_id=w2.id, exercise_id=plank.id, duration_seconds=60),
        WorkoutExercise(workout_id=w3.id, exercise_id=run.id, duration_seconds=1800),
        WorkoutExercise(workout_id=w3.id, exercise_id=squat.id, sets=3, reps=10),
    ]
    db.session.add_all(links)
    db.session.commit()

    print('Done seeding.')