import sqlite3
from pathlib import Path

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Literal


router = APIRouter(
    prefix="/api/exam-attempts",
    tags=["Attempt Answers"],
)


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "exampro.db"


class AnswerCreateRequest(BaseModel):
    question_id: int
    selected_answer: Literal["A", "B", "C", "D"]


@router.post(
    "/{attempt_id}/answers",
    status_code=status.HTTP_201_CREATED,
)
def submit_answer(
    attempt_id: int,
    answer: AnswerCreateRequest,
):
    connection = sqlite3.connect(DB_PATH)

    attempt = connection.execute(
        """
        SELECT id, status
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

    question = connection.execute(
        """
        SELECT correct_answer, marks
        FROM questions
        WHERE id = ?
        """,
        (answer.question_id,),
    ).fetchone()

    if question is None:
        connection.close()

        raise HTTPException(
            status_code=404,
            detail="Question not found",
        )

    correct_answer = question[0]
    marks = question[1]

    is_correct = int(answer.selected_answer == correct_answer)
    marks_awarded = marks if is_correct else 0

    cursor = connection.execute(
        """
        INSERT INTO attempt_answers (
            attempt_id,
            question_id,
            selected_answer,
            is_correct,
            marks_awarded
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            attempt_id,
            answer.question_id,
            answer.selected_answer,
            is_correct,
            marks_awarded,
        ),
    )

    connection.commit()

    answer_id = cursor.lastrowid

    connection.close()

    return {
        "message": "Answer submitted successfully",
        "answer_id": answer_id,
        "is_correct": bool(is_correct),
        "marks_awarded": marks_awarded,
    }