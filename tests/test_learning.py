import copy

import pytest

from curriculum import LESSONS, LESSON_BY_ID
from learning import check_answer, default_progress, validate_progress


def test_catalogue_has_consistent_questions_and_exercises():
    assert len(LESSON_BY_ID) == len(LESSONS) == 8
    for lesson in LESSONS:
        assert len(lesson["exercises"]) == 3
        assert len(lesson["quiz"]) == 4
        for question in lesson["quiz"]:
            assert len(set(question["options"])) == len(question["options"])
            assert question["answer"] in question["options"]
        for exercise in lesson["exercises"]:
            if exercise["kind"] == "numeric":
                assert check_answer(exercise, str(exercise["answer"])) is True
            elif exercise["kind"] == "text":
                for answer in exercise["answers"]:
                    assert check_answer(exercise, answer) is True


@pytest.mark.parametrize("answer", ["0.2", "0,2", " 0,2 ", "2e-1"])
def test_numeric_answers_accept_decimal_comma_and_scientific_notation(answer):
    assert check_answer(LESSON_BY_ID["electricite"]["exercises"][1], answer)


@pytest.mark.parametrize("answer", ["", "nan", "inf", "-inf", "0.2 A", "two", "0.21"])
def test_invalid_or_wrong_answers_are_not_accepted(answer):
    assert not check_answer(LESSON_BY_ID["electricite"]["exercises"][1], answer)


def test_text_answers_ignore_case_accents_and_extra_spacing():
    assert check_answer(LESSON_BY_ID["accords"]["exercises"][2], "  DES   PETITS CHATS. ")
    assert check_answer(LESSON_BY_ID["argumentation"]["exercises"][0], "THESE")
    assert not check_answer(LESSON_BY_ID["accords"]["exercises"][0], "verts")
    assert check_answer(LESSON_BY_ID["argumentation"]["exercises"][1], "Une proposition") is None


def test_progress_can_be_exported_and_restored():
    data = default_progress()
    data["completed_lessons"] = ["mouvement", "mouvement"]
    data["exercises"] = {"mouvement:0": {"correct": True, "practiced": True},
                         "lecture:2": {"correct": None, "practiced": True}}
    data["quizzes"] = {"electricite": {"score": 3, "total": 4}}
    restored = validate_progress(data)
    assert restored["completed_lessons"] == ["mouvement"]
    assert restored["quizzes"]["electricite"]["score"] == 3
    assert restored["exercises"]["lecture:2"]["correct"] is None


@pytest.mark.parametrize("change", [
    {"schema_version": True},
    {"completed_lessons": ["unknown"]},
    {"exercises": {"mouvement:99": {"correct": True, "practiced": True}}},
    {"exercises": {"lecture:2": {"correct": True, "practiced": True}}},
    {"exercises": {"mouvement:0": {"correct": None, "practiced": True}}},
    {"quizzes": {"mouvement": {"score": 5, "total": 4}}},
    {"quizzes": {"mouvement": {"score": True, "total": 4}}},
    {"quizzes": {"mouvement": {"score": 1, "total": 99}}},
])
def test_corrupt_progress_is_rejected(change):
    data = copy.deepcopy(default_progress())
    data.update(change)
    with pytest.raises(ValueError):
        validate_progress(data)
