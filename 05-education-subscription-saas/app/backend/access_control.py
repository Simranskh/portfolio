import sqlite3

from fastapi import APIRouter, HTTPException

from config import DB_PATH


router = APIRouter(
    prefix="/access",
    tags=["Access Control"],
)


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


@router.post("/grant")
def grant_course_access(
    user_id: int,
    subscription_id: int,
    course_id: int,
):
    conn = get_connection()

    subscription = conn.execute(
        """
        SELECT
            s.*,
            p.max_courses
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
            status_code=403,
            detail="Active subscription required",
        )

    course = conn.execute(
        """
        SELECT *
        FROM courses
        WHERE course_id = ?
        AND is_active = 1
        """,
        (course_id,),
    ).fetchone()

    if not course:
        conn.close()
        raise HTTPException(
            status_code=404,
            detail="Course not found",
        )

    current_count = conn.execute(
        """
        SELECT COUNT(*)
        FROM entitlements
        WHERE user_id = ?
        AND subscription_id = ?
        AND revoked_at IS NULL
        """,
        (user_id, subscription_id),
    ).fetchone()[0]

    if current_count >= subscription["max_courses"]:
        conn.close()
        raise HTTPException(
            status_code=403,
            detail="Course entitlement limit reached",
        )

    existing = conn.execute(
        """
        SELECT entitlement_id
        FROM entitlements
        WHERE user_id = ?
        AND course_id = ?
        AND subscription_id = ?
        AND revoked_at IS NULL
        """,
        (user_id, course_id, subscription_id),
    ).fetchone()

    if existing:
        conn.close()
        raise HTTPException(
            status_code=409,
            detail="Course access already granted",
        )

    cursor = conn.execute(
        """
        INSERT INTO entitlements(
            user_id,
            course_id,
            subscription_id
        )
        VALUES (?, ?, ?)
        """,
        (user_id, course_id, subscription_id),
    )

    conn.commit()

    entitlement_id = cursor.lastrowid

    conn.close()

    return {
        "entitlement_id": entitlement_id,
        "user_id": user_id,
        "course_id": course_id,
        "access": True,
    }


@router.get("/check")
def check_course_access(
    user_id: int,
    course_id: int,
):
    conn = get_connection()

    access = conn.execute(
        """
        SELECT
            e.entitlement_id,
            e.user_id,
            e.course_id,
            s.status,
            s.end_date
        FROM entitlements e
        JOIN subscriptions s
            ON e.subscription_id = s.subscription_id
        WHERE e.user_id = ?
        AND e.course_id = ?
        AND e.revoked_at IS NULL
        AND s.status = 'active'
        AND datetime(s.end_date) >= datetime('now')
        """,
        (user_id, course_id),
    ).fetchone()

    conn.close()

    return {
        "user_id": user_id,
        "course_id": course_id,
        "has_access": access is not None,
        "subscription_status": (
            access["status"] if access else None
        ),
    }