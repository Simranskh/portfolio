import sqlite3
from pathlib import Path

import pytest

from automation.api.quizzes_api import QuizzesAPI


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DB_PATH = PROJECT_ROOT / "app" / "database" / "quiz.db"


@pytest.fixture(scope="session", autouse=True)
def prepare_test_data():
    connection = sqlite3.connect(DB_PATH)

    connection.execute("PRAGMA foreign_keys = ON")

    connection.execute("DELETE FROM quiz_attempts")
    connection.execute("DELETE FROM questions")
    connection.execute("DELETE FROM quizzes")

    connection.execute(
        """
        INSERT INTO quizzes (
            id,
            title,
            description,
            total_marks
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            1,
            "Python API Testing",
            "Practice quiz for API testing concepts",
            5,
        ),
    )

    connection.execute(
        """
        INSERT INTO questions (
            id,
            quiz_id,
            question_text,
            option_a,
            option_b,
            option_c,
            option_d,
            correct_answer,
            marks
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            1,
            1,
            "Which HTTP method is normally used to create a resource?",
            "GET",
            "POST",
            "DELETE",
            "PUT",
            "B",
            1,
        ),
    )

    connection.commit()
    connection.close()


@pytest.fixture
def quizzes_api():
    return QuizzesAPI()