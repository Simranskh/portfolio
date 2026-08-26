import requests

from automation.config import BASE_URL


class QuizzesAPI:

    def create(self, title, description, total_marks):
        return requests.post(
            f"{BASE_URL}/api/quizzes",
            json={
                "title": title,
                "description": description,
                "total_marks": total_marks,
            },
        )

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

    def get_all(self):
        return requests.get(
            f"{BASE_URL}/api/quizzes"
        )

    def get_by_id(self, quiz_id):
        return requests.get(
            f"{BASE_URL}/api/quizzes/{quiz_id}"
        )

    def create_question(
            self,
            quiz_id,
            question_text,
            option_a,
            option_b,
            option_c,
            option_d,
            correct_answer,
            marks=1,
    ):
        return requests.post(
            f"{BASE_URL}/api/quizzes/{quiz_id}/questions",
            json={
                "question_text": question_text,
                "option_a": option_a,
                "option_b": option_b,
                "option_c": option_c,
                "option_d": option_d,
                "correct_answer": correct_answer,
                "marks": marks,
            },
        )

    def get_questions(self, quiz_id):
        return requests.get(
            f"{BASE_URL}/api/quizzes/{quiz_id}/questions"
        )

    def submit_attempt(self, quiz_id, user_name, answers):
        return requests.post(
            f"{BASE_URL}/api/quizzes/{quiz_id}/attempt",
            json={
                "user_name": user_name,
                "answers": answers,
            },
        )

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
