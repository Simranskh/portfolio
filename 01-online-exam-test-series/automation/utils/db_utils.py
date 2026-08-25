import sqlite3
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DB_PATH = PROJECT_ROOT / "app" / "database" / "exampro.db"

def get_connection():
    return sqlite3.connect(DB_PATH)


def get_user_by_email(email: str):
    connection = get_connection()

    user = connection.execute(
        """
        SELECT id, name, email, password, role, is_active
        FROM users
        WHERE email = ?
        """,
        (email,),
    ).fetchone()

    connection.close()
    return user


def activate_user(email: str):
    connection = get_connection()

    connection.execute(
        """
        UPDATE users
        SET is_active = 1
        WHERE email = ?
        """,
        (email,),
    )

    connection.commit()
    connection.close()


def get_user_by_id(user_id: int):
    connection = get_connection()

    user = connection.execute(
        """
        SELECT id, name, email, role
        FROM users
        WHERE id = ?
        """,
        (user_id,),
    ).fetchone()

    connection.close()
    return user
def get_test_series_by_id(test_series_id: int):
    connection = get_connection()

    test_series = connection.execute(
        """
        SELECT id, title, description, is_active
        FROM test_series
        WHERE id = ?
        """,
        (test_series_id,),
    ).fetchone()

    connection.close()

    return test_series

def get_question_by_id(question_id: int):
    connection = get_connection()

    question = connection.execute(
        """
        SELECT
            id,
            test_series_id,
            question_text,
            option_a,
            option_b,
            option_c,
            option_d,
            correct_answer,
            marks
        FROM questions
        WHERE id = ?
        """,
        (question_id,),
    ).fetchone()

    connection.close()

    return question

def get_exam_attempt_by_id(attempt_id: int):
    connection = get_connection()

    attempt = connection.execute(
        """
        SELECT
            id,
            user_id,
            test_series_id,
            score,
            total_marks,
            status
        FROM exam_attempts
        WHERE id = ?
        """,
        (attempt_id,),
    ).fetchone()

    connection.close()

    return attempt

def get_attempt_answer_by_id(answer_id: int):
    connection = get_connection()

    answer = connection.execute(
        """
        SELECT
            id,
            attempt_id,
            question_id,
            selected_answer,
            is_correct,
            marks_awarded
        FROM attempt_answers
        WHERE id = ?
        """,
        (answer_id,),
    ).fetchone()

    connection.close()

    return answer
def get_exam_attempt_result(attempt_id: int):
    connection = get_connection()

    attempt = connection.execute(
        """
        SELECT
            id,
            user_id,
            test_series_id,
            score,
            total_marks,
            status,
            submitted_at
        FROM exam_attempts
        WHERE id = ?
        """,
        (attempt_id,),
    ).fetchone()

    connection.close()

    return attempt