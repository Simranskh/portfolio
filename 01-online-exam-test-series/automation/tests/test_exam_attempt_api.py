from automation.utils.db_utils import (
    get_exam_attempt_by_id,
    get_exam_attempt_result,
)


def test_start_exam_attempt(exam_attempt_api):
    response = exam_attempt_api.start(
        user_id=1,
        test_series_id=1,
    )

    assert response.status_code == 201

    data = response.json()

    assert data["message"] == "Exam attempt started successfully"
    assert "attempt_id" in data
    assert data["total_marks"] > 0

    attempt_id = data["attempt_id"]

    attempt = get_exam_attempt_by_id(attempt_id)

    assert attempt is not None
    assert attempt[0] == attempt_id
    assert attempt[1] == 1
    assert attempt[2] == 1
    assert attempt[3] == 0
    assert attempt[4] == data["total_marks"]
    assert attempt[5] == "in_progress"


def test_start_exam_attempt_invalid_user(exam_attempt_api):
    response = exam_attempt_api.start_with_payload(
        {
            "user_id": 99999,
            "test_series_id": 1,
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_start_exam_attempt_invalid_test_series(exam_attempt_api):
    response = exam_attempt_api.start_with_payload(
        {
            "user_id": 1,
            "test_series_id": 99999,
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Test series not found"


def test_submit_exam_attempt(exam_attempt_api):
    start_response = exam_attempt_api.start(
        user_id=1,
        test_series_id=1,
    )

    assert start_response.status_code == 201

    start_data = start_response.json()

    attempt_id = start_data["attempt_id"]
    total_marks = start_data["total_marks"]

    submit_response = exam_attempt_api.submit(attempt_id)

    assert submit_response.status_code == 200

    data = submit_response.json()

    assert data["message"] == "Exam submitted successfully"
    assert data["attempt_id"] == attempt_id
    assert data["score"] == 0
    assert data["total_marks"] == total_marks

    attempt = get_exam_attempt_result(attempt_id)

    assert attempt is not None
    assert attempt[0] == attempt_id
    assert attempt[1] == 1
    assert attempt[2] == 1
    assert attempt[3] == 0
    assert attempt[4] == total_marks
    assert attempt[5] == "submitted"
    assert attempt[6] is not None


def test_submit_already_submitted_attempt(exam_attempt_api):
    start_response = exam_attempt_api.start(
        user_id=1,
        test_series_id=1,
    )

    assert start_response.status_code == 201

    attempt_id = start_response.json()["attempt_id"]

    first_submit = exam_attempt_api.submit(attempt_id)

    assert first_submit.status_code == 200

    second_submit = exam_attempt_api.submit(attempt_id)

    assert second_submit.status_code == 400
    assert second_submit.json()["detail"] == "Exam attempt is not in progress"


def test_get_exam_attempt(exam_attempt_api):
    start_response = exam_attempt_api.start(
        user_id=1,
        test_series_id=1,
    )

    assert start_response.status_code == 201

    start_data = start_response.json()
    attempt_id = start_data["attempt_id"]
    total_marks = start_data["total_marks"]

    get_response = exam_attempt_api.get_by_id(attempt_id)

    assert get_response.status_code == 200

    data = get_response.json()

    assert data["attempt_id"] == attempt_id
    assert data["user_id"] == 1
    assert data["test_series_id"] == 1
    assert data["score"] == 0
    assert data["total_marks"] == total_marks
    assert data["status"] == "in_progress"

    attempt = get_exam_attempt_result(attempt_id)

    assert attempt is not None
    assert attempt[0] == attempt_id
    assert attempt[1] == 1
    assert attempt[2] == 1
    assert attempt[3] == 0
    assert attempt[4] == total_marks
    assert attempt[5] == "in_progress"