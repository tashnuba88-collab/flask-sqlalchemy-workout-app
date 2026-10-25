from flask import Flask, jsonify, request
from flask_migrate import Migrate
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from models import *
from schemas import (
    ExerciseDetailSchema,
    ExerciseSchema,
    WorkoutDetailSchema,
    WorkoutExerciseSchema,
    WorkoutSchema,
)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
workout_detail_schema = WorkoutDetailSchema()
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
exercise_detail_schema = ExerciseDetailSchema()
workout_exercise_schema = WorkoutExerciseSchema()


def error(message, status):
    return jsonify({'error': message}), status


def save(obj):
    """Add obj and commit. Returns an error response, or None on success."""
    try:
        db.session.add(obj)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return error('Database constraint violated (duplicate or invalid value).', 400)
    return None


# Workouts

@app.route('/workouts', methods=['GET'])
def get_workouts():
    workouts = Workout.query.order_by(Workout.date.desc()).all()
    return jsonify(workouts_schema.dump(workouts)), 200


@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    workout = db.session.get(Workout, id)
    if not workout:
        return error('Workout not found.', 404)
    return jsonify(workout_detail_schema.dump(workout)), 200


@app.route('/workouts', methods=['POST'])
def create_workout():
    try:
        data = workout_schema.load(request.get_json(silent=True) or {})
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400

    try:
        workout = Workout(**data)
    except ValueError as err:
        return error(str(err), 400)

    failure = save(workout)
    if failure:
        return failure
    return jsonify(workout_schema.dump(workout)), 201


@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = db.session.get(Workout, id)
    if not workout:
        return error('Workout not found.', 404)
    db.session.delete(workout)  # cascades to WorkoutExercises
    db.session.commit()
    return '', 204


# Exercises

@app.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.order_by(Exercise.name).all()
    return jsonify(exercises_schema.dump(exercises)), 200


@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
    exercise = db.session.get(Exercise, id)
    if not exercise:
        return error('Exercise not found.', 404)
    return jsonify(exercise_detail_schema.dump(exercise)), 200


@app.route('/exercises', methods=['POST'])
def create_exercise():
    try:
        data = exercise_schema.load(request.get_json(silent=True) or {})
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400

    try:
        exercise = Exercise(**data)
    except ValueError as err:
        return error(str(err), 400)

    failure = save(exercise)
    if failure:
        return failure
    return jsonify(exercise_schema.dump(exercise)), 201


@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = db.session.get(Exercise, id)
    if not exercise:
        return error('Exercise not found.', 404)
    db.session.delete(exercise)  # cascades to WorkoutExercises
    db.session.commit()
    return '', 204


# Add an exercise to a workout

@app.route(
    '/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises',
    methods=['POST'],
)
def add_exercise_to_workout(workout_id, exercise_id):
    workout = db.session.get(Workout, workout_id)
    exercise = db.session.get(Exercise, exercise_id)
    if not workout:
        return error('Workout not found.', 404)
    if not exercise:
        return error('Exercise not found.', 404)

    try:
        data = workout_exercise_schema.load(request.get_json(silent=True) or {})
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400

    try:
        link = WorkoutExercise(workout_id=workout_id, exercise_id=exercise_id, **data)
    except ValueError as err:
        return error(str(err), 400)

    failure = save(link)
    if failure:
        return error('That exercise is already in this workout.', 400)
    return jsonify(workout_exercise_schema.dump(link)), 201


if __name__ == '__main__':
    app.run(port=5555, debug=True)