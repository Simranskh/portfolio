import sqlite3
import uuid

from fastapi import APIRouter, HTTPException

from config import DB_PATH


router = APIRouter(prefix="/auth", tags=["Authentication"])

SESSIONS = {}


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


@router.post("/login")
def login(email: str, password: str):
    conn = get_connection()

    user = conn.execute(
        """
        SELECT user_id, name, email, role, is_active
        FROM users
        WHERE email = ? AND password = ?
        """,
        (email, password),
    ).fetchone()

    conn.close()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
        )

    if not user["is_active"]:
        raise HTTPException(
            status_code=403,
            detail="User account is inactive",
        )

    token = str(uuid.uuid4())

    SESSIONS[token] = user["user_id"]

    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": user["user_id"],
        "role": user["role"],
    }


@router.post("/logout")
def logout(token: str):
    if token not in SESSIONS:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
        )

    del SESSIONS[token]

    return {
        "message": "Logged out successfully"
    }