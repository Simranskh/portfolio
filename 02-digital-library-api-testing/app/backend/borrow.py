import sqlite3
from pathlib import Path

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel


router = APIRouter(
    prefix="/api/borrow",
    tags=["Borrow / Return"],
)


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "library.db"


class BorrowCreateRequest(BaseModel):
    book_id: int
    member_id: int


@router.post("", status_code=status.HTTP_201_CREATED)
def borrow_book(request: BorrowCreateRequest):
    connection = sqlite3.connect(DB_PATH)

    book = connection.execute(
        """
        SELECT id, is_available
        FROM books
        WHERE id = ?
        """,
        (request.book_id,),
    ).fetchone()

    if book is None:
        connection.close()

        raise HTTPException(
            status_code=404,
            detail="Book not found",
        )

    member = connection.execute(
        """
        SELECT id, is_active
        FROM members
        WHERE id = ?
        """,
        (request.member_id,),
    ).fetchone()

    if member is None:
        connection.close()

        raise HTTPException(
            status_code=404,
            detail="Member not found",
        )

    if book[1] == 0:
        connection.close()

        raise HTTPException(
            status_code=409,
            detail="Book is already borrowed",
        )

    cursor = connection.execute(
        """
        INSERT INTO borrow_records (
            book_id,
            member_id
        )
        VALUES (?, ?)
        """,
        (
            request.book_id,
            request.member_id,
        ),
    )

    connection.execute(
        """
        UPDATE books
        SET is_available = 0
        WHERE id = ?
        """,
        (request.book_id,),
    )

    connection.commit()

    borrow_id = cursor.lastrowid

    connection.close()

    return {
        "message": "Book borrowed successfully",
        "borrow_id": borrow_id,
    }
@router.post("/{borrow_id}/return")
def return_book(borrow_id: int):
    connection = sqlite3.connect(DB_PATH)

    record = connection.execute(
        """
        SELECT
            id,
            book_id,
            status
        FROM borrow_records
        WHERE id = ?
        """,
        (borrow_id,),
    ).fetchone()

    if record is None:
        connection.close()

        raise HTTPException(
            status_code=404,
            detail="Borrow record not found",
        )

    if record[2] != "borrowed":
        connection.close()

        raise HTTPException(
            status_code=409,
            detail="Book has already been returned",
        )

    connection.execute(
        """
        UPDATE borrow_records
        SET returned_at = CURRENT_TIMESTAMP,
            status = 'returned'
        WHERE id = ?
        """,
        (borrow_id,),
    )

    connection.execute(
        """
        UPDATE books
        SET is_available = 1
        WHERE id = ?
        """,
        (record[1],),
    )

    connection.commit()

    connection.close()

    return {
        "message": "Book returned successfully",
        "borrow_id": borrow_id,
    }