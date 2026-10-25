from marshmallow import Schema, ValidationError, fields, validate, validates_schema


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    category = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    equipment_needed = fields.Bool(load_default=False)


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(required=True, validate=validate.Range(min=1, max=600))
    notes = fields.Str(
        load_default=None, allow_none=True, validate=validate.Length(max=500)
    )


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(dump_only=True)
    exercise_id = fields.Int(dump_only=True)
    reps = fields.Int(load_default=None, allow_none=True, validate=validate.Range(min=1))
    sets = fields.Int(load_default=None, allow_none=True, validate=validate.Range(min=1))
    duration_seconds = fields.Int(
        load_default=None, allow_none=True, validate=validate.Range(min=1)
    )

    @validates_schema
    def require_a_measure(self, data, **kwargs):
        has_sets_and_reps = data.get('sets') is not None and data.get('reps') is not None
        has_duration = data.get('duration_seconds') is not None
        if not (has_sets_and_reps or has_duration):
            raise ValidationError(
                'Provide both sets and reps, or duration_seconds.', 'measure'
            )


class WorkoutExerciseWithExerciseSchema(WorkoutExerciseSchema):
    exercise = fields.Nested(ExerciseSchema, dump_only=True)


class WorkoutExerciseWithWorkoutSchema(WorkoutExerciseSchema):
    workout = fields.Nested(WorkoutSchema, dump_only=True)


class WorkoutDetailSchema(WorkoutSchema):
    workout_exercises = fields.Nested(
        WorkoutExerciseWithExerciseSchema, many=True, dump_only=True
    )


class ExerciseDetailSchema(ExerciseSchema):
    workout_exercises = fields.Nested(
        WorkoutExerciseWithWorkoutSchema, many=True, dump_only=True
    )