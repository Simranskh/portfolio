import sqlite3
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, HTTPException

from config import DB_PATH


router = APIRouter(
    prefix="/subscriptions",
    tags=["Subscriptions"],
)


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


@router.post("")
def create_subscription(
    user_id: int,
    plan_id: int,
):
    conn = get_connection()

    user = conn.execute(
        """
        SELECT user_id
        FROM users
        WHERE user_id = ? AND is_active = 1
        """,
        (user_id,),
    ).fetchone()

    if not user:
        conn.close()
        raise HTTPException(
            status_code=404,
            detail="Active user not found",
        )

    plan = conn.execute(
        """
        SELECT *
        FROM plans
        WHERE plan_id = ? AND is_active = 1
        """,
        (plan_id,),
    ).fetchone()

    if not plan:
        conn.close()
        raise HTTPException(
            status_code=404,
            detail="Active plan not found",
        )

    existing = conn.execute(
        """
        SELECT subscription_id
        FROM subscriptions
        WHERE user_id = ?
        AND status = 'active'
        AND date(end_date) >= date('now')
        """,
        (user_id,),
    ).fetchone()

    if existing:
        conn.close()
        raise HTTPException(
            status_code=409,
            detail="User already has an active subscription",
        )

    start = datetime.now(timezone.utc)
    end = start + timedelta(days=plan["duration_days"])

    cursor = conn.execute(
        """
        INSERT INTO subscriptions(
            user_id,
            plan_id,
            start_date,
            end_date,
            status
        )
        VALUES (?, ?, ?, ?, 'active')
        """,
        (
            user_id,
            plan_id,
            start.isoformat(),
            end.isoformat(),
        ),
    )

    subscription_id = cursor.lastrowid

    conn.execute(
        """
        INSERT INTO audit_logs(
            user_id,
            action,
            entity_type,
            entity_id,
            details
        )
        VALUES (?, 'CREATE', 'subscription', ?, ?)
        """,
        (
            user_id,
            subscription_id,
            f"Plan: {plan['plan_name']}",
        ),
    )

    conn.commit()
    conn.close()

    return {
        "subscription_id": subscription_id,
        "user_id": user_id,
        "plan_id": plan_id,
        "status": "active",
        "start_date": start.isoformat(),
        "end_date": end.isoformat(),
    }


@router.get("/user/{user_id}")
def get_user_subscription(user_id: int):
    conn = get_connection()

    subscription = conn.execute(
        """
        SELECT
            s.subscription_id,
            s.user_id,
            s.plan_id,
            p.plan_name,
            p.price,
            p.max_courses,
            s.start_date,
            s.end_date,
            s.status,
            s.auto_renew
        FROM subscriptions s
        JOIN plans p
            ON s.plan_id = p.plan_id
        WHERE s.user_id = ?
        ORDER BY s.subscription_id DESC
        LIMIT 1
        """,
        (user_id,),
    ).fetchone()

    conn.close()

    if not subscription:
        raise HTTPException(
            status_code=404,
            detail="Subscription not found",
        )

    return dict(subscription)


@router.post("/{subscription_id}/cancel")
def cancel_subscription(subscription_id: int):
    conn = get_connection()

    subscription = conn.execute(
        """
        SELECT *
        FROM subscriptions
        WHERE subscription_id = ?
        """,
        (subscription_id,),
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

    conn.execute(
        """
        UPDATE subscriptions
        SET status = 'cancelled',
            auto_renew = 0
        WHERE subscription_id = ?
        """,
        (subscription_id,),
    )

    conn.execute(
        """
        INSERT INTO audit_logs(
            user_id,
            action,
            entity_type,
            entity_id
        )
        VALUES (?, 'CANCEL', 'subscription', ?)
        """,
        (
            subscription["user_id"],
            subscription_id,
        ),
    )

    conn.commit()
    conn.close()

    return {
        "subscription_id": subscription_id,
        "status": "cancelled",
    }


@router.post("/expire")
def expire_subscriptions():
    conn = get_connection()

    cursor = conn.execute(
        """
        UPDATE subscriptions
        SET status = 'expired'
        WHERE status = 'active'
        AND datetime(end_date) < datetime('now')
        """
    )

    conn.commit()

    updated = cursor.rowcount

    conn.close()

    return {
        "expired_subscriptions": updated
    }