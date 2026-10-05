"""Answer validation and portable, session-local learning progress."""

import math
import re
import unicodedata

from curriculum import LESSONS, LESSON_BY_ID


def normalize(text):
    value = unicodedata.normalize("NFKD", text.strip().lower())
    value = "".join(char for char in value if not unicodedata.combining(char))
    value = value.replace("’", "'")
    return re.sub(r"\s+", " ", value).strip(" .!?\n")


def check_answer(exercise, answer):
    if exercise["kind"] == "written":
        return None
    if exercise["kind"] == "text":
        return normalize(answer) in {normalize(item) for item in exercise["answers"]}
    try:
        number = float(answer.replace(",", ".").replace(" ", "").replace("\u00a0", ""))
    except (ValueError, TypeError, AttributeError):
        return False
    return math.isfinite(number) and math.isclose(
        number, exercise["answer"], rel_tol=0, abs_tol=exercise["tolerance"]
    )


def default_progress():
    return {"schema_version": 1, "completed_lessons": [], "exercises": {}, "quizzes": {}}


def validate_progress(data):
    """Accept only the known course IDs and the small progress schema."""
    if not isinstance(data, dict) or type(data.get("schema_version")) is not int or data["schema_version"] != 1:
        raise ValueError("Ce fichier n'est pas une sauvegarde de progression compatible.")
    completed = data.get("completed_lessons", [])
    exercises = data.get("exercises", {})
    quizzes = data.get("quizzes", {})
    if not isinstance(completed, list) or not all(isinstance(item, str) and item in LESSON_BY_ID for item in completed):
        raise ValueError("La sauvegarde contient un cours inconnu.")
    if not isinstance(exercises, dict) or not isinstance(quizzes, dict):
        raise ValueError("La sauvegarde contient une progression invalide.")
    valid_exercises = {f"{lesson['id']}:{index}": exercise for lesson in LESSONS
                       for index, exercise in enumerate(lesson["exercises"])}
    clean_exercises = {}
    for key, result in exercises.items():
        if key not in valid_exercises or not isinstance(result, dict):
            raise ValueError("La sauvegarde contient un exercice inconnu.")
        correct = result.get("correct")
        practiced = result.get("practiced")
        kind = valid_exercises[key]["kind"]
        if type(practiced) is not bool or (correct is not None and type(correct) is not bool):
            raise ValueError("La sauvegarde contient un résultat invalide.")
        if (kind == "written" and correct is not None) or (kind != "written" and type(correct) is not bool):
            raise ValueError("Le résultat ne correspond pas au type d'exercice.")
        clean_exercises[key] = {"correct": correct, "practiced": practiced}
    clean_quizzes = {}
    for key, result in quizzes.items():
        if key not in LESSON_BY_ID or not isinstance(result, dict):
            raise ValueError("La sauvegarde contient un quiz inconnu.")
        score, total = result.get("score"), result.get("total")
        if type(score) is not int or type(total) is not int or total != len(LESSON_BY_ID[key]["quiz"]) or not 0 <= score <= total:
            raise ValueError("La sauvegarde contient un score invalide.")
        clean_quizzes[key] = {"score": score, "total": total}
    return {"schema_version": 1, "completed_lessons": sorted(set(completed)),
            "exercises": clean_exercises, "quizzes": clean_quizzes}
