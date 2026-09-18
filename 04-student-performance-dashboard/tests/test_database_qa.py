import sqlite3
from pathlib import Path

import allure
import pytest


BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "database" / "student_performance.db"
QA_SQL_PATH = BASE_DIR / "sql" / "qa_validation.sql"


def load_qa_queries():
    sql = QA_SQL_PATH.read_text(encoding="utf-8")
    queries = []

    for statement in sql.split(";"):
        statement = statement.strip()

        if not statement:
            continue

        lines = statement.splitlines()
        qa_number = None

        for line in lines:
            if "QA-DB-" in line:
                for number in range(1, 16):
                    if f"QA-DB-{number:03d}" in line:
                        qa_number = number
                        break

            if qa_number is not None:
                break

        if qa_number is None:
            continue

        sql_lines = [
            line
            for line in lines
            if not line.strip().startswith("--")
        ]

        statement = "\n".join(sql_lines).strip()

        if statement.upper().startswith(("SELECT", "WITH")):
            queries.append((qa_number, statement))

    queries.sort(key=lambda item: item[0])

    return queries


@allure.epic("Student Performance Database")
@allure.feature("Database QA")
@pytest.mark.parametrize(
    "query_number, query",
    load_qa_queries()
)
def test_database_qa_validation(query_number, query):

    with allure.step(f"Execute QA Validation #{query_number}"):

        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.execute(query)
            rows = cursor.fetchall()

    allure.attach(
        query,
        name=f"QA Validation #{query_number} SQL",
        attachment_type=allure.attachment_type.TEXT
    )

    allure.attach(
        str(rows[:10]),
        name=f"QA Validation #{query_number} Result",
        attachment_type=allure.attachment_type.TEXT
    )

    assert len(rows) == 0, (
        f"QA Validation #{query_number} failed. "
        f"{len(rows)} violation(s) found."
    )