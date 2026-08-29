import sqlite3
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException

from config import DB_PATH


router = APIRouter(
    prefix="/payments",
    tags=["Payments"],
)


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


@router.post("")
def create_payment(
    user_id: int,
    subscription_id: int,
    payment_method: str = "card",
):
    conn = get_connection()

    subscription = conn.execute(
        """
        SELECT
            s.*,
            p.price
        FROM subscriptions s
        JOIN plans p
            ON s.plan_id = p.plan_id
        WHERE s.subscription_id = ?
        AND s.user_id = ?
        """,
        (subscription_id, user_id),
    ).fetchone()

    if not subscription:
        conn.close()
        raise HTTPException(
            status_code=404,
            detail="Subscription not found",
        )

    if subscription["status"] != "active":
        conn.close()
        raise HTTPException(
            status_code=409,
            detail="Subscription is not active",
        )

    transaction_id = f"TXN-{uuid.uuid4().hex[:12].upper()}"

    cursor = conn.execute(
        """
        INSERT INTO payments(
            user_id,
            subscription_id,
            amount,
            payment_method,
            transaction_id,
            status,
            paid_at
        )
        VALUES (?, ?, ?, ?, ?, 'success', ?)
        """,
        (
            user_id,
            subscription_id,
            subscription["price"],
            payment_method,
            transaction_id,
            datetime.now(timezone.utc).isoformat(),
        ),
    )

    conn.commit()

    payment_id = cursor.lastrowid

    conn.close()

    return {
        "payment_id": payment_id,
        "transaction_id": transaction_id,
        "amount": subscription["price"],
        "status": "success",
    }


@router.get("/user/{user_id}")
def payment_history(user_id: int):
    conn = get_connection()

    rows = conn.execute(
        """
        SELECT *
        FROM payments
        WHERE user_id = ?
        ORDER BY payment_id DESC
        """,
        (user_id,),
    ).fetchall()

    conn.close()

    return [dict(row) for row in rows]