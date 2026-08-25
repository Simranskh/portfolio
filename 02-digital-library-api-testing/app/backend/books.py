import sqlite3
from pathlib import Path

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel


router = APIRouter(
    prefix="/api/books",
    tags=["Books"],
)


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "library.db"


class BookCreateRequest(BaseModel):
    title: str
    author: str
    isbn: str
    category: str | None = None


@router.post("", status_code=status.HTTP_201_CREATED)
def create_book(request: BookCreateRequest):
    connection = sqlite3.connect(DB_PATH)

    existing_book = connection.execute(
        """
        SELECT id
        FROM books
        WHERE isbn = ?
        """,
        (request.isbn,),
    ).fetchone()

    if existing_book is not None:
        connection.close()

        raise HTTPException(
            status_code=409,
            detail="Book with this ISBN already exists",
        )

    cursor = connection.execute(
        """
        INSERT INTO books (
            title,
            author,
            isbn,
            category
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            request.title,
            request.author,
            request.isbn,
            request.category,
        ),
    )

    connection.commit()

    book_id = cursor.lastrowid

    connection.close()

    return {
        "message": "Book created successfully",
        "book_id": book_id,
    }
@router.get("/{book_id}")
def get_book(book_id: int):
    connection = sqlite3.connect(DB_PATH)

    book = connection.execute(
        """
        SELECT
            id,
            title,
            author,
            isbn,
            category,
            is_available
        FROM books
        WHERE id = ?
        """,
        (book_id,),
    ).fetchone()

    if book is None:
        connection.close()

        raise HTTPException(
            status_code=404,
            detail="Book not found",
        )

    connection.close()

    return {
        "book_id": book[0],
        "title": book[1],
        "author": book[2],
        "isbn": book[3],
        "category": book[4],
        "is_available": bool(book[5]),
    }
class BookUpdateRequest(BaseModel):
    title: str
    author: str
    category: str | None = None
@router.put("/{book_id}")
def update_book(book_id: int, request: BookUpdateRequest):
    connection = sqlite3.connect(DB_PATH)

    book = connection.execute(
        """
        SELECT id
        FROM books
        WHERE id = ?
        """,
        (book_id,),
    ).fetchone()

    if book is None:
        connection.close()

        raise HTTPException(
            status_code=404,
            detail="Book not found",
        )

    connection.execute(
        """
        UPDATE books
        SET title = ?,
            author = ?,
            category = ?
        WHERE id = ?
        """,
        (
            request.title,
            request.author,
            request.category,
            book_id,
        ),
    )

    connection.commit()
    connection.close()

    return {
        "message": "Book updated successfully",
        "book_id": book_id,
    }
@router.delete("/{book_id}")
def delete_book(book_id: int):
    connection = sqlite3.connect(DB_PATH)

    book = connection.execute(
        """
        SELECT id
        FROM books
        WHERE id = ?
        """,
        (book_id,),
    ).fetchone()

    if book is None:
        connection.close()

        raise HTTPException(
            status_code=404,
            detail="Book not found",
        )

    connection.execute(
        """
        DELETE FROM books
        WHERE id = ?
        """,
        (book_id,),
    )

    connection.commit()
    connection.close()

    return {
        "message": "Book deleted successfully",
        "book_id": book_id,
    }
