import sqlite3
from pathlib import Path
from typing import Literal
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel


router = APIRouter(
    prefix="/api/questions",
    tags=["Questions"],
)


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "exampro.db"


class QuestionCreateRequest(BaseModel):
    test_series_id: int
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_answer: Literal["A", "B", "C", "D"]
    marks: int = 1


@router.post("", status_code=status.HTTP_201_CREATED)
def create_question(question: QuestionCreateRequest):
    connection = sqlite3.connect(DB_PATH)

    test_series = connection.execute(
        """
        SELECT id
        FROM test_series
        WHERE id = ?
        """,
        (question.test_series_id,),
    ).fetchone()

    if test_series is None:
        connection.close()

        raise HTTPException(
            status_code=404,
            detail="Test series not found",
        )

    cursor = connection.execute(
        """
        INSERT INTO questions (
            test_series_id,
            question_text,
            option_a,
            option_b,
            option_c,
            option_d,
            correct_answer,
            marks
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            question.test_series_id,
            question.question_text,
            question.option_a,
            question.option_b,
            question.option_c,
            question.option_d,
            question.correct_answer,
            question.marks,
        ),
    )

    connection.commit()

    question_id = cursor.lastrowid

    connection.close()

    return {
        "message": "Question created successfully",
        "question_id": question_id,
    }