from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from curriculum import LESSONS, LESSON_BY_ID

APP = Path(__file__).resolve().parents[1] / "streamlit_app.py"


def app(page="Accueil"):
    at = AppTest.from_file(str(APP), default_timeout=20).run()
    assert not at.exception
    if page != "Accueil":
        at.radio(key="nav").set_value(page).run()
    assert not at.exception
    return at


@pytest.mark.parametrize("page", ["Accueil", "Cours", "Exercices", "Quiz", "Laboratoire", "Ma progression", "À propos"])
def test_all_pages_render(page):
    assert not app(page).exception


@pytest.mark.parametrize("lesson", LESSONS, ids=lambda lesson: lesson["id"])
def test_every_lesson_can_be_read_and_marked_complete(lesson):
    at = app("Cours")
    at.selectbox(key="lesson_picker").select(lesson["id"]).run()
    assert not at.exception
    at.button(key=f"complete_{lesson['id']}").click().run()
    assert lesson["id"] in at.session_state["progress"]["completed_lessons"]


def test_home_buttons_navigate_and_select_subject():
    at = app()
    next(button for button in at.button if button.label == "Découvrir le français →").click().run()
    assert not at.exception
    assert at.radio(key="nav").value == "Cours"
    assert at.selectbox(key="subject_filter").value == "Français"
    assert at.selectbox(key="lesson_picker").value == "accords"
    next(button for button in at.button if button.label == "Passer aux exercices →").click().run()
    assert at.radio(key="nav").value == "Exercices"
    assert at.selectbox(key="lesson_picker").value == "accords"


def test_numeric_exercise_retries_keep_mastered_result():
    at = app("Exercices")
    at.text_input(key="answer_mouvement:0").input("4")
    next(button for button in at.button if button.label == "Vérifier ma réponse").click().run()
    assert at.session_state["progress"]["exercises"]["mouvement:0"]["correct"] is False
    assert at.error
    at.text_input(key="answer_mouvement:0").input("5")
    next(button for button in at.button if button.label == "Vérifier ma réponse").click().run()
    assert at.session_state["progress"]["exercises"]["mouvement:0"]["correct"] is True
    at.text_input(key="answer_mouvement:0").input("4")
    next(button for button in at.button if button.label == "Vérifier ma réponse").click().run()
    assert at.session_state["progress"]["exercises"]["mouvement:0"]["correct"] is True
    assert not at.exception


def test_blank_exercise_is_not_marked_as_practiced():
    at = app("Exercices")
    next(button for button in at.button if button.label == "Vérifier ma réponse").click().run()
    assert "mouvement:0" not in at.session_state["progress"]["exercises"]
    assert at.warning


def test_written_exercise_gets_model_feedback_without_automatic_grade():
    at = app("Exercices")
    at.selectbox(key="lesson_picker").select("lecture").run()
    at.text_area(key="answer_lecture:2").input("Le parapluie et les traces de chaussures évoquent la pluie.")
    next(button for button in at.button if button.label == "Comparer avec une proposition de correction").click().run()
    assert at.session_state["progress"]["exercises"]["lecture:2"] == {"correct": None, "practiced": True}
    assert not at.exception


def test_incomplete_quiz_does_not_award_a_score():
    at = app("Quiz")
    next(button for button in at.button if button.label == "Corriger mon quiz").click().run()
    assert at.warning
    assert not at.session_state["progress"]["quizzes"]


@pytest.mark.parametrize("lesson", LESSONS, ids=lambda lesson: lesson["id"])
def test_each_quiz_grades_and_resets(lesson):
    at = app("Quiz")
    at.selectbox(key="lesson_picker").select(lesson["id"]).run()
    for index, item in enumerate(lesson["quiz"]):
        at.radio(key=f"quiz_answer_{lesson['id']}_0_{index}").set_value(item["answer"])
    next(button for button in at.button if button.label == "Corriger mon quiz").click().run()
    assert at.session_state["progress"]["quizzes"][lesson["id"]] == {"score": 4, "total": 4}
    at.button(key=f"retry_{lesson['id']}").click().run()
    assert at.radio(key=f"quiz_answer_{lesson['id']}_1_0").value is None
    assert not at.exception


def test_lower_quiz_retry_keeps_best_score():
    at = app("Quiz")
    questions = LESSON_BY_ID["mouvement"]["quiz"]
    for index, item in enumerate(questions):
        at.radio(key=f"quiz_answer_mouvement_0_{index}").set_value(item["answer"])
    next(button for button in at.button if button.label == "Corriger mon quiz").click().run()
    at.button(key="retry_mouvement").click().run()
    for index, item in enumerate(questions):
        wrong = next(option for option in item["options"] if option != item["answer"])
        at.radio(key=f"quiz_answer_mouvement_1_{index}").set_value(wrong)
    next(button for button in at.button if button.label == "Corriger mon quiz").click().run()
    assert at.metric[0].value == "0 / 4"
    assert at.session_state["progress"]["quizzes"]["mouvement"]["score"] == 4


def test_lab_calculations_respond_to_parameters():
    at = app("Laboratoire")
    at.slider(key="speed").set_value(10.0).run()
    assert at.metric[0].value == "200 m"
    at.selectbox(key="lab_tool").select("Loi d'Ohm").run()
    assert at.metric[0].value == "6 V"
    at.slider(key="current").set_value(0.5).run()
    assert at.metric[0].value == "10 V"
    assert at.metric[1].value == "5.00 W"
    at.selectbox(key="lab_tool").select("Masse et poids").run()
    at.selectbox(key="place").select("Lune · g = 1,62 N/kg").run()
    assert at.metric[0].value == "4.86 N"
    at.selectbox(key="lab_tool").select("Énergie cinétique").run()
    assert at.metric[0].value == "9.00 J"
    at.slider(key="energy_speed").set_value(6.0).run()
    assert at.metric[0].value == "36.00 J"
    assert not at.exception


def test_progress_reset_is_explicit_and_clears_session():
    at = app("Cours")
    at.button(key="complete_mouvement").click().run()
    at.radio(key="nav").set_value("Ma progression").run()
    assert at.metric[0].value == "1 / 8"
    reset = next(button for button in at.button if button.label == "Réinitialiser ma progression")
    assert reset.disabled
    at.checkbox(key="confirm_reset").check().run()
    next(button for button in at.button if button.label == "Réinitialiser ma progression").click().run()
    assert at.metric[0].value == "0 / 8"
    assert not at.exception
