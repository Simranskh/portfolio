from automation.utils.db_utils import get_question_by_id


def test_create_question(questions_api):
    response = questions_api.create(
        test_series_id=1,
        question_text="What is 2 + 2?",
        option_a="3",
        option_b="4",
        option_c="5",
        option_d="6",
        correct_answer="B",
        marks=1,
    )

    assert response.status_code == 201

    data = response.json()

    assert data["message"] == "Question created successfully"
    assert "question_id" in data

    question_id = data["question_id"]
    question = get_question_by_id(question_id)

    assert question is not None
    assert question[0] == question_id
    assert question[1] == 1
    assert question[2] == "What is 2 + 2?"
    assert question[3] == "3"
    assert question[4] == "4"
    assert question[5] == "5"
    assert question[6] == "6"
    assert question[7] == "B"
    assert question[8] == 1


def test_create_question_invalid_test_series(questions_api):
    response = questions_api.create_with_payload(
        {
            "test_series_id": 99999,
            "question_text": "What is 2 + 2?",
            "option_a": "3",
            "option_b": "4",
            "option_c": "5",
            "option_d": "6",
            "correct_answer": "B",
            "marks": 1,
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Test series not found"


def test_create_question_missing_question_text(questions_api):
    response = questions_api.create_with_payload(
        {
            "test_series_id": 1,
            "option_a": "3",
            "option_b": "4",
            "option_c": "5",
            "option_d": "6",
            "correct_answer": "B",
            "marks": 1,
        }
    )

    assert response.status_code == 422


def test_create_question_missing_option_a(questions_api):
    response = questions_api.create_with_payload(
        {
            "test_series_id": 1,
            "question_text": "What is 2 + 2?",
            "option_b": "4",
            "option_c": "5",
            "option_d": "6",
            "correct_answer": "B",
            "marks": 1,
        }
    )

    assert response.status_code == 422


def test_create_question_missing_correct_answer(questions_api):
    response = questions_api.create_with_payload(
        {
            "test_series_id": 1,
            "question_text": "What is 2 + 2?",
            "option_a": "3",
            "option_b": "4",
            "option_c": "5",
            "option_d": "6",
            "marks": 1,
        }
    )

    assert response.status_code == 422


def test_create_question_invalid_correct_answer(questions_api):
    response = questions_api.create_with_payload(
        {
            "test_series_id": 1,
            "question_text": "What is 2 + 2?",
            "option_a": "3",
            "option_b": "4",
            "option_c": "5",
            "option_d": "6",
            "correct_answer": "E",
            "marks": 1,
        }
    )

    assert response.status_code == 422


def test_create_question_default_marks(questions_api):
    response = questions_api.create_with_payload(
        {
            "test_series_id": 1,
            "question_text": "What is 5 + 5?",
            "option_a": "8",
            "option_b": "9",
            "option_c": "10",
            "option_d": "11",
            "correct_answer": "C",
        }
    )

    assert response.status_code == 201

    data = response.json()
    assert "question_id" in data

    question = get_question_by_id(data["question_id"])

    assert question is not None
    assert question[8] == 1