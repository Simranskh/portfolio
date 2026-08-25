import sqlite3
from pathlib import Path

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel


router = APIRouter(
    prefix="/api/exam-attempts",
    tags=["Exam Attempts"],
)


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "exampro.db"


class ExamAttemptCreateRequest(BaseModel):
    user_id: int
    test_series_id: int


@router.post("", status_code=status.HTTP_201_CREATED)
def start_exam_attempt(request: ExamAttemptCreateRequest):
    connection = sqlite3.connect(DB_PATH)

    user = connection.execute(
        """
        SELECT id
        FROM users
        WHERE id = ?
        """,
        (request.user_id,),
    ).fetchone()

    if user is None:
        connection.close()

        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    test_series = connection.execute(
        """
        SELECT id
        FROM test_series
        WHERE id = ?
        """,
        (request.test_series_id,),
    ).fetchone()

    if test_series is None:
        connection.close()

        raise HTTPException(
            status_code=404,
            detail="Test series not found",
        )

    total_marks = connection.execute(
        """
        SELECT COALESCE(SUM(marks), 0)
        FROM questions
        WHERE test_series_id = ?
        """,
        (request.test_series_id,),
    ).fetchone()[0]

    cursor = connection.execute(
        """
        INSERT INTO exam_attempts (
            user_id,
            test_series_id,
            total_marks
        )
        VALUES (?, ?, ?)
        """,
        (
            request.user_id,
            request.test_series_id,
            total_marks,
        ),
    )

    connection.commit()

    attempt_id = cursor.lastrowid

    connection.close()

    return {
        "message": "Exam attempt started successfully",
        "attempt_id": attempt_id,
        "total_marks": total_marks,
    }
@router.post("/{attempt_id}/submit")
def submit_exam_attempt(attempt_id: int):
    connection = sqlite3.connect(DB_PATH)

    attempt = connection.execute(
        """
        SELECT id, status, total_marks
        FROM exam_attempts
        WHERE id = ?
        """,
        (attempt_id,),
    ).fetchone()

    if attempt is None:
        connection.close()

        raise HTTPException(
            status_code=404,
            detail="Exam attempt not found",
        )

    if attempt[1] != "in_progress":
        connection.close()

        raise HTTPException(
            status_code=400,
            detail="Exam attempt is not in progress",
        )

    score = connection.execute(
        """
        SELECT COALESCE(SUM(marks_awarded), 0)
        FROM attempt_answers
        WHERE attempt_id = ?
        """,
        (attempt_id,),
    ).fetchone()[0]

    connection.execute(
        """
        UPDATE exam_attempts
        SET score = ?,
            status = 'submitted',
            submitted_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """,
        (score, attempt_id),
    )

    connection.commit()

    connection.close()

    return {
        "message": "Exam submitted successfully",
        "attempt_id": attempt_id,
        "score": score,
        "total_marks": attempt[2],
    }
@router.get("/{attempt_id}")
def get_exam_attempt(attempt_id: int):
    connection = sqlite3.connect(DB_PATH)

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

    if attempt is None:
        connection.close()

        raise HTTPException(
            status_code=404,
            detail="Exam attempt not found",
        )

    connection.close()

    return {
        "attempt_id": attempt[0],
        "user_id": attempt[1],
        "test_series_id": attempt[2],
        "score": attempt[3],
        "total_marks": attempt[4],
        "status": attempt[5],
    }