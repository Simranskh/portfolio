import sqlite3
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI(
    title="Quiz Practice API",
    description="API for quiz practice and automated testing",
    version="1.0.0",
)


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR.parent / "database" / "quiz.db"


class QuizCreateRequest(BaseModel):
    title: str
    description: str
    total_marks: int


@app.get("/")
def root():
    return {
        "message": "Quiz Practice API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.post("/api/quizzes", status_code=201)
def create_quiz(request: QuizCreateRequest):
    connection = sqlite3.connect(DB_PATH)

    cursor = connection.execute(
        """
        INSERT INTO quizzes (
            title,
            description,
            total_marks
        )
        VALUES (?, ?, ?)
        """,
        (
            request.title,
            request.description,
            request.total_marks,
        ),
    )

    connection.commit()

    quiz_id = cursor.lastrowid

    connection.close()

    return {
        "message": "Quiz created successfully",
        "quiz_id": quiz_id,
        "title": request.title,
        "description": request.description,
        "total_marks": request.total_marks,
    }


@app.get("/api/quizzes")
def get_quizzes():
    connection = sqlite3.connect(DB_PATH)

    quizzes = connection.execute(
        """
        SELECT
            id,
            title,
            description,
            total_marks
        FROM quizzes
        ORDER BY id
        """
    ).fetchall()

    connection.close()

    return {
        "quizzes": [
            {
                "quiz_id": quiz[0],
                "title": quiz[1],
                "description": quiz[2],
                "total_marks": quiz[3],
            }
            for quiz in quizzes
        ]
    }


@app.get("/api/quizzes/{quiz_id}")
def get_quiz(quiz_id: int):
    connection = sqlite3.connect(DB_PATH)

    quiz = connection.execute(
        """
        SELECT
            id,
            title,
            description,
            total_marks
        FROM quizzes
        WHERE id = ?
        """,
        (quiz_id,),
    ).fetchone()

    connection.close()

    if quiz is None:
        raise HTTPException(
            status_code=404,
            detail="Quiz not found",
        )

    return {
        "quiz_id": quiz[0],
        "title": quiz[1],
        "description": quiz[2],
        "total_marks": quiz[3],
    }
class QuestionCreateRequest(BaseModel):
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_answer: str
    marks: int = 1
@app.post("/api/quizzes/{quiz_id}/questions", status_code=201)
def create_question(
    quiz_id: int,
    request: QuestionCreateRequest,
):
    connection = sqlite3.connect(DB_PATH)

    quiz = connection.execute(
        "SELECT id FROM quizzes WHERE id = ?",
        (quiz_id,),
    ).fetchone()

    if quiz is None:
        connection.close()

        raise HTTPException(
            status_code=404,
            detail="Quiz not found",
        )

    cursor = connection.execute(
        """
        INSERT INTO questions (
            quiz_id,
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
            quiz_id,
            request.question_text,
            request.option_a,
            request.option_b,
            request.option_c,
            request.option_d,
            request.correct_answer,
            request.marks,
        ),
    )

    connection.commit()

    question_id = cursor.lastrowid

    connection.close()

    return {
        "message": "Question created successfully",
        "question_id": question_id,
        "quiz_id": quiz_id,
        "question_text": request.question_text,
        "correct_answer": request.correct_answer,
        "marks": request.marks,
    }
@app.get("/api/quizzes/{quiz_id}/questions")
def get_questions(quiz_id: int):
    connection = sqlite3.connect(DB_PATH)

    quiz = connection.execute(
        "SELECT id FROM quizzes WHERE id = ?",
        (quiz_id,),
    ).fetchone()

    if quiz is None:
        connection.close()
        raise HTTPException(
            status_code=404,
            detail="Quiz not found",
        )

    questions = connection.execute(
        """
        SELECT
            id,
            question_text,
            option_a,
            option_b,
            option_c,
            option_d,
            correct_answer,
            marks
        FROM questions
        WHERE quiz_id = ?
        ORDER BY id
        """,
        (quiz_id,),
    ).fetchall()

    connection.close()

    return {
        "quiz_id": quiz_id,
        "questions": [
            {
                "question_id": question[0],
                "question_text": question[1],
                "option_a": question[2],
                "option_b": question[3],
                "option_c": question[4],
                "option_d": question[5],
                "correct_answer": question[6],
                "marks": question[7],
            }
            for question in questions
        ],
    }
class AnswerRequest(BaseModel):
    question_id: int
    answer: str


class QuizAttemptRequest(BaseModel):
    user_name: str
    answers: list[AnswerRequest]
@app.post("/api/quizzes/{quiz_id}/attempt", status_code=201)
def submit_quiz_attempt(
    quiz_id: int,
    request: QuizAttemptRequest,
):
    connection = sqlite3.connect(DB_PATH)

    quiz = connection.execute(
        """
        SELECT id, total_marks
        FROM quizzes
        WHERE id = ?
        """,
        (quiz_id,),
    ).fetchone()

    if quiz is None:
        connection.close()
        raise HTTPException(
            status_code=404,
            detail="Quiz not found",
        )

    score = 0
    total_marks = 0
    question_ids = set()

    for answer in request.answers:
        question = connection.execute(
            """
            SELECT id, correct_answer, marks
            FROM questions
            WHERE id = ? AND quiz_id = ?
            """,
            (answer.question_id, quiz_id),
        ).fetchone()

        if question is None:
            connection.close()
            raise HTTPException(
                status_code=404,
                detail=f"Question {answer.question_id} not found",
            )

        question_ids.add(answer.question_id)

        marks = question[2]
        total_marks += marks

        if answer.answer.upper() == question[1].upper():
            score += marks

    cursor = connection.execute(
        """
        INSERT INTO quiz_attempts (
            quiz_id,
            user_name,
            score,
            total_marks,
            status
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            quiz_id,
            request.user_name,
            score,
            total_marks,
            "completed",
        ),
    )

    connection.commit()

    attempt_id = cursor.lastrowid

    connection.close()

    return {
        "attempt_id": attempt_id,
        "quiz_id": quiz_id,
        "user_name": request.user_name,
        "score": score,
        "total_marks": total_marks,
        "status": "completed",
    }