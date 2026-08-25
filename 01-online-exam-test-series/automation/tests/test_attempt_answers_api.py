from automation.utils.db_utils import get_attempt_answer_by_id


def test_submit_correct_answer(attempt_answers_api, exam_attempt_api):
    start_response = exam_attempt_api.start(
        user_id=1,
        test_series_id=1,
    )

    assert start_response.status_code == 201

    attempt_id = start_response.json()["attempt_id"]

    response = attempt_answers_api.submit(
        attempt_id=attempt_id,
        question_id=3,
        selected_answer="B",
    )

    assert response.status_code == 201

    data = response.json()

    assert data["message"] == "Answer submitted successfully"
    assert "answer_id" in data
    assert data["is_correct"] is True
    assert data["marks_awarded"] == 1

    answer = get_attempt_answer_by_id(data["answer_id"])

    assert answer is not None
    assert answer[0] == data["answer_id"]
    assert answer[1] == attempt_id
    assert answer[2] == 3
    assert answer[3] == "B"
    assert answer[4] == 1
    assert answer[5] == 1


def test_submit_wrong_answer(attempt_answers_api, exam_attempt_api):
    start_response = exam_attempt_api.start(
        user_id=1,
        test_series_id=1,
    )

    assert start_response.status_code == 201

    attempt_id = start_response.json()["attempt_id"]

    response = attempt_answers_api.submit(
        attempt_id=attempt_id,
        question_id=4,
        selected_answer="A",
    )

    assert response.status_code == 201

    data = response.json()

    assert data["message"] == "Answer submitted successfully"
    assert data["is_correct"] is False
    assert data["marks_awarded"] == 0

    answer = get_attempt_answer_by_id(data["answer_id"])

    assert answer is not None
    assert answer[1] == attempt_id
    assert answer[2] == 4
    assert answer[3] == "A"
    assert answer[4] == 0
    assert answer[5] == 0


def test_submit_answer_invalid_attempt(attempt_answers_api):
    response = attempt_answers_api.submit_with_payload(
        99999,
        {
            "question_id": 3,
            "selected_answer": "B",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Exam attempt not found"


def test_submit_answer_invalid_question(
    attempt_answers_api,
    exam_attempt_api,
):
    start_response = exam_attempt_api.start(
        user_id=1,
        test_series_id=1,
    )

    assert start_response.status_code == 201

    attempt_id = start_response.json()["attempt_id"]

    response = attempt_answers_api.submit_with_payload(
        attempt_id,
        {
            "question_id": 99999,
            "selected_answer": "B",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Question not found"


def test_submit_answer_invalid_option(
    attempt_answers_api,
    exam_attempt_api,
):
    start_response = exam_attempt_api.start(
        user_id=1,
        test_series_id=1,
    )

    assert start_response.status_code == 201

    attempt_id = start_response.json()["attempt_id"]

    response = attempt_answers_api.submit_with_payload(
        attempt_id,
        {
            "question_id": 3,
            "selected_answer": "E",
        },
    )

    assert response.status_code == 422