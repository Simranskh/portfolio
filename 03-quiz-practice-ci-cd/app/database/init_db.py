import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "quiz.db"
SCHEMA_PATH = BASE_DIR / "schema.sql"


def init_database():
    connection = sqlite3.connect(DB_PATH)

    with open(SCHEMA_PATH, "r", encoding="utf-8") as file:
        schema = file.read()

    connection.executescript(schema)
    connection.commit()

    tables = connection.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        """
    ).fetchall()

    connection.close()

    print("Quiz database initialized successfully.")
    print("Tables:", tables)


if __name__ == "__main__":
    init_database()