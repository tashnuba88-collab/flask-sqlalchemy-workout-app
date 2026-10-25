# flask-sqlalchemy-workout-app
# Workout Tracker API

A Flask backend for a workout tracking app used by personal trainers. It stores workouts and reusable exercises, and links them through a join table that holds sets, reps, or duration for each exercise in a workout. Built with Flask, SQLAlchemy, Flask-Migrate, and Marshmallow.

## Installation

```
pipenv install
pipenv shell
cd server
export FLASK_APP=app.py
flask db init
flask db migrate -m 'create exercises, workouts, workout_exercises'
flask db upgrade head
python seed.py
```

## Running the app

From the `server/` folder:

```
flask run
```

This serves on http://127.0.0.1:5000. `python app.py` also works and serves on port 5555.

## Validations

- Table constraints: unique exercise name, non-empty name and category, workout duration greater than 0, positive reps/sets/duration, one row per workout/exercise pair.
- Model validations: non-empty exercise name and category, positive workout duration, notes limited to 500 characters, positive reps/sets/duration_seconds.
- Schema validations: field lengths and ranges, required fields, and a rule that each workout exercise has either sets and reps or a duration.

## Endpoints

| Method | Path | Description |
| --- | --- | --- |
| GET | /workouts | List all workouts |
| GET | /workouts/<id> | One workout with its exercises, including reps, sets, and duration |
| POST | /workouts | Create a workout (date, duration_minutes, notes) |
| DELETE | /workouts/<id> | Delete a workout and its workout exercises |
| GET | /exercises | List all exercises |
| GET | /exercises/<id> | One exercise with the workouts it appears in |
| POST | /exercises | Create an exercise (name, category, equipment_needed) |
| DELETE | /exercises/<id> | Delete an exercise and its workout exercises |
| POST | /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises | Add an exercise to a workout with reps, sets, or duration_seconds |

Example body for the last endpoint:

```
{"sets": 3, "reps": 10}
```
