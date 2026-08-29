import sqlite3

from fastapi import APIRouter, HTTPException

from config import DB_PATH


router = APIRouter(prefix="/users", tags=["Users"])


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@router.post("")
def create_user(
    name: str,
    email: str,
    password: str,
):
    conn = get_connection()

    try:
        cursor = conn.execute(
            """
            INSERT INTO users(name, email, password)
            VALUES (?, ?, ?)
            """,
            (name, email, password),
        )

        conn.commit()

        return {
            "user_id": cursor.lastrowid,
            "name": name,
            "email": email,
        }

    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Email already registered",
        )

    finally:
        conn.close()


@router.get("/{user_id}")
def get_user(user_id: int):
    conn = get_connection()

    user = conn.execute(
        """
        SELECT user_id, name, email, role, is_active, created_at
        FROM users
        WHERE user_id = ?
        """,
        (user_id,),
    ).fetchone()

    conn.close()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return dict(user)