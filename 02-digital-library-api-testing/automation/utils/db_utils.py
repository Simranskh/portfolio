import sqlite3
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DB_PATH = PROJECT_ROOT / "app" / "database" / "library.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def get_book_by_id(book_id: int):
    connection = get_connection()

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

    connection.close()

    return book
def get_member_by_id(member_id: int):
    connection = get_connection()

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

    connection.close()

    return member
def get_borrow_record_by_id(borrow_id: int):
    connection = get_connection()

    record = connection.execute(
        """
        SELECT
            id,
            book_id,
            member_id,
            borrowed_at,
            returned_at,
            status
        FROM borrow_records
        WHERE id = ?
        """,
        (borrow_id,),
    ).fetchone()

    connection.close()

    return record
def get_book_availability(book_id: int):
    connection = get_connection()

    result = connection.execute(
        """
        SELECT is_available
        FROM books
        WHERE id = ?
        """,
        (book_id,),
    ).fetchone()

    connection.close()

    return result
