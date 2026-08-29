import sqlite3

from fastapi import APIRouter, HTTPException

from config import DB_PATH


router = APIRouter(
    prefix="/courses",
    tags=["Courses"],
)


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


@router.get("")
def list_courses():
    conn = get_connection()

    rows = conn.execute(
        """
        SELECT *
        FROM courses
        WHERE is_active = 1
        ORDER BY course_id
        """
    ).fetchall()

    conn.close()

    return [dict(row) for row in rows]


@router.get("/{course_id}")
def get_course(course_id: int):
    conn = get_connection()

    course = conn.execute(
        """
        SELECT *
        FROM courses
        WHERE course_id = ?
        """,
        (course_id,),
    ).fetchone()

    conn.close()

    if not course:
        raise HTTPException(
            status_code=404,
            detail="Course not found",
        )

    return dict(course)