from app.services.question_service import load_questions, select_questions


def test_question_files_have_minimum_size():
    assert len(load_questions()) >= 200


def test_select_questions_for_python():
    questions = select_questions("python", "junior", ["Python Core"], 5, "technical")
    assert len(questions) == 5
    assert all(question.question["ru"] for question in questions)

