import sqlite3
from pathlib import Path

from fastapi import APIRouter, status
from pydantic import BaseModel

router = APIRouter(
    prefix="/api/test-series",
    tags=["Test Series"],
)

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "exampro.db"


class TestSeriesCreateRequest(BaseModel):
    title: str
    description: str | None = None


@router.post("", status_code=status.HTTP_201_CREATED)
def create_test_series(test_series: TestSeriesCreateRequest):
    connection = sqlite3.connect(DB_PATH)

    cursor = connection.execute(
        """
        INSERT INTO test_series (title, description)
        VALUES (?, ?)
        """,
        (
            test_series.title,
            test_series.description,
        ),
    )

    connection.commit()
    test_series_id = cursor.lastrowid
    connection.close()

    return {
        "message": "Test series created successfully",
        "test_series_id": test_series_id,
    }