import sqlite3

from config import DB_PATH


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def fetch_all(query, params=()):
    conn = get_db_connection()

    rows = conn.execute(query, params).fetchall()

    conn.close()

    return rows


def fetch_one(query, params=()):
    conn = get_db_connection()

    row = conn.execute(query, params).fetchone()

    conn.close()

    return row