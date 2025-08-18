"""A module that loads HTML exercises from a JSON file."""

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ErrorHint:
    """A class that represents an error hint.

    Attributes
    ----------
        afterTries (int) The number of tries after which the hint should be
            displayed
        message (str) The hint message to be displayed

    """

    after_tries: int
    message: str


@dataclass(frozen=True)
class Exercise:
    """A class that represents an HTML exercise.

    Attributes
    ----------
        title (str) The title of the exercise
        explanation (str) A detailed explanation of the topic covered by the
            exercise
        example (str) An example clarifying the topic explained in the
            explanation
        description (str) Long description of the exercise detailing the
            required task, and the expected output
        answer (str) The correct answer to the exercise to check the user's
            solution against
        errorHints (list[ErrorHint]) A list of hints for the exercise

    """

    title: str
    explanation: str
    example: str
    description: str
    answer: str
    error_hints: list[ErrorHint]


@dataclass(frozen=True)
class ExerciseGroup:
    """A dataclass that represents an exercise group.

    Attributes
    ----------
        title (str) The title of the exercise group
        description (str) Long description of the exercise group detailing what it covers
        exercises (list[Exercise]) A list of exercises in the group

    """

    title: str
    description: str
    exercises: list[Exercise]


def _load_hints(hints: list[dict[str, str | int]]) -> list[ErrorHint]:
    """Load error hints from a list of dictionaries.

    Args:
    ----
        hints (list[dict[str, str | int]]): A list of dictionaries, where each
            dictionary contains an "afterTries" key and a "message" key. The
            "afterTries" key indicates the number of tries after which the hint
            should be displayed, and the "message" key contains the hint
            message to be displayed. The afterTries must be an integer > 0,
            and the message must be a string.

    Returns:
    -------
        list[ErrorHint]: A list of ErrorHint objects

    """
    return [
        ErrorHint(
            after_tries=hint["afterTries"],
            message=hint["message"],
        )
        for hint in hints
    ]


def _load_exercise(exercise_obj: dict[str, str | list | dict]) -> Exercise:
    """Load an exercise from a dictionary.

    Args:
    ----
        exercise_obj (dict[str, str | list | dict]) : A dictionary containing
            the following keys:
            - title (str): The title of the exercise
            - explanation (str): A detailed explanation of the topic covered by
                the exercise
            - example (str): An example clarifying the topic explained in the
                explanation
            - description (str): Long description of the exercise detailing the
                required task, and the expected output
            - answer (str): The correct answer to the exercise to check the
                user's solution against
            - errorHints (list[dict[str, str | int]]): A list of dictionaries,
                where each dictionary contains an "afterTries" key and a
                "message" key. The "afterTries" key indicates the number of
                tries after which the hint should be displayed, and the
                "message" key contains the hint message to be displayed. The
                afterTries must be an integer > 0, and the message must be a
                string

    Returns:
    -------
        Exercise : An Exercise object

    """
    return Exercise(
        title=exercise_obj["title"],
        explanation=exercise_obj["explanation"],
        example=exercise_obj["example"],
        description=exercise_obj["description"],
        answer=exercise_obj["answer"],
        error_hints=_load_hints(exercise_obj["errorHints"]),
    )


def load_exercises_from_json(json_file: Path) -> list[ExerciseGroup]:
    """Load exercises from JSON file.

    Args:
    ----
        json_file (Path): The path to the JSON file containing the exercises.

    Returns:
    -------
        list[ExerciseGroup]: A list of ExerciseGroup objects

    """
    exercise_groups = []

    with json_file.open() as f:
        contents = json.load(f)

    for exercise_group in contents["exerciseGroups"]:
        exercises = [_load_exercise(exercise) for exercise in exercise_group["exercises"]]
        exercise_groups.append(
            ExerciseGroup(
                exercise_group["title"],
                exercise_group["description"],
                exercises,
            ),
        )

    return exercise_groups
