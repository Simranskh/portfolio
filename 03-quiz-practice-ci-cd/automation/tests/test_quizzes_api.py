def test_create_quiz(quizzes_api):
    response = quizzes_api.create(
        title="Python API Testing",
        description="Practice quiz for API testing concepts",
        total_marks=5,
    )

    assert response.status_code == 201

    data = response.json()

    assert data["message"] == "Quiz created successfully"
    assert data["title"] == "Python API Testing"
    assert data["total_marks"] == 5
    assert "quiz_id" in data


def test_get_quizzes(quizzes_api):
    response = quizzes_api.get_all()

    assert response.status_code == 200

    data = response.json()

    assert "quizzes" in data
    assert isinstance(data["quizzes"], list)


def test_get_quiz_by_id(quizzes_api):
    response = quizzes_api.get_by_id(1)

    assert response.status_code == 200

    data = response.json()

    assert data["quiz_id"] == 1
    assert data["title"] == "Python API Testing"


def test_get_quiz_invalid_id(quizzes_api):
    response = quizzes_api.get_by_id(999)

    assert response.status_code == 404

    data = response.json()

    assert data["detail"] == "Quiz not found"
def test_create_question(quizzes_api):
    response = quizzes_api.create_question(
        quiz_id=1,
        question_text="Which HTTP method is used to create a resource?",
        option_a="GET",
        option_b="POST",
        option_c="DELETE",
        option_d="PATCH",
        correct_answer="B",
        marks=1,
    )

    assert response.status_code == 201

    data = response.json()

    assert data["message"] == "Question created successfully"
    assert data["quiz_id"] == 1
    assert "question_id" in data
    assert data["question_text"] == (
        "Which HTTP method is used to create a resource?"
    )
    assert data["correct_answer"] == "B"
    assert data["marks"] == 1


def test_create_question_invalid_quiz(quizzes_api):
    response = quizzes_api.create_question(
        quiz_id=999,
        question_text="Test question",
        option_a="A",
        option_b="B",
        option_c="C",
        option_d="D",
        correct_answer="A",
        marks=1,
    )

    assert response.status_code == 404

    data = response.json()

    assert data["detail"] == "Quiz not found"
def test_get_questions(quizzes_api):
    response = quizzes_api.get_questions(1)

    assert response.status_code == 200

    data = response.json()

    assert data["quiz_id"] == 1
    assert "questions" in data
    assert isinstance(data["questions"], list)
    assert len(data["questions"]) > 0


def test_get_questions_invalid_quiz(quizzes_api):
    response = quizzes_api.get_questions(999)

    assert response.status_code == 404

    data = response.json()

    assert data["detail"] == "Quiz not found"
def test_submit_quiz_attempt_correct_answer(quizzes_api):
    response = quizzes_api.submit_attempt(
        quiz_id=1,
        user_name="Test User",
        answers=[
            {
                "question_id": 1,
                "answer": "B",
            }
        ],
    )

    assert response.status_code == 201

    data = response.json()

    assert data["quiz_id"] == 1
    assert data["user_name"] == "Test User"
    assert data["score"] == 1
    assert data["status"] == "completed"
    assert "attempt_id" in data


def test_submit_quiz_attempt_wrong_answer(quizzes_api):
    response = quizzes_api.submit_attempt(
        quiz_id=1,
        user_name="Test User",
        answers=[
            {
                "question_id": 1,
                "answer": "A",
            }
        ],
    )

    assert response.status_code == 201

    data = response.json()

    assert data["score"] == 0
    assert data["status"] == "completed"


def test_submit_quiz_attempt_invalid_quiz(quizzes_api):
    response = quizzes_api.submit_attempt(
        quiz_id=999,
        user_name="Test User",
        answers=[
            {
                "question_id": 1,
                "answer": "B",
            }
        ],
    )

    assert response.status_code == 404

    data = response.json()

    assert data["detail"] == "Quiz not found"


def test_submit_quiz_attempt_invalid_question(quizzes_api):
    response = quizzes_api.submit_attempt(
        quiz_id=1,
        user_name="Test User",
        answers=[
            {
                "question_id": 999,
                "answer": "B",
            }
        ],
    )

    assert response.status_code == 404

    data = response.json()

    assert data["detail"] == "Question 999 not found"