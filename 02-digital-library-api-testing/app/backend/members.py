import sqlite3
from pathlib import Path

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel


router = APIRouter(
    prefix="/api/members",
    tags=["Members"],
)


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "library.db"


class MemberCreateRequest(BaseModel):
    name: str
    email: str


@router.post("", status_code=status.HTTP_201_CREATED)
def create_member(request: MemberCreateRequest):
    connection = sqlite3.connect(DB_PATH)

    existing_member = connection.execute(
        """
        SELECT id
        FROM members
        WHERE email = ?
        """,
        (request.email,),
    ).fetchone()

    if existing_member is not None:
        connection.close()

        raise HTTPException(
            status_code=409,
            detail="Member with this email already exists",
        )

    cursor = connection.execute(
        """
        INSERT INTO members (
            name,
            email
        )
        VALUES (?, ?)
        """,
        (
            request.name,
            request.email,
        ),
    )

    connection.commit()

    member_id = cursor.lastrowid

    connection.close()

    return {
        "message": "Member created successfully",
        "member_id": member_id,
    }
@router.get("/{member_id}")
def get_member(member_id: int):
    connection = sqlite3.connect(DB_PATH)

    member = connection.execute(
        """
        SELECT
            id,
            name,
            email,
            is_active
        FROM members
        WHERE id = ?
        """,
        (member_id,),
    ).fetchone()

    if member is None:
        connection.close()

        raise HTTPException(
            status_code=404,
            detail="Member not found",
        )

    connection.close()

    return {
        "member_id": member[0],
        "name": member[1],
        "email": member[2],
        "is_active": bool(member[3]),
    }