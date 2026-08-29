import sqlite3

from fastapi import APIRouter, HTTPException

from config import DB_PATH


router = APIRouter(prefix="/plans", tags=["Plans"])


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@router.get("")
def list_plans():
    conn = get_connection()

    rows = conn.execute(
        """
        SELECT *
        FROM plans
        WHERE is_active = 1
        ORDER BY price
        """
    ).fetchall()

    conn.close()

    return [dict(row) for row in rows]


@router.get("/{plan_id}")
def get_plan(plan_id: int):
    conn = get_connection()

    plan = conn.execute(
        """
        SELECT *
        FROM plans
        WHERE plan_id = ?
        """,
        (plan_id,),
    ).fetchone()

    conn.close()

    if not plan:
        raise HTTPException(
            status_code=404,
            detail="Plan not found",
        )

    return dict(plan)