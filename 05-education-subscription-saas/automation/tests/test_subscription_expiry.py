import sqlite3
from datetime import datetime, timedelta, timezone
from config import DB_PATH


def test_expired_subscription_denies_access(
    subscriptions_api,
    access_api,
):

    subscription = subscriptions_api.create(
        user_id=3,
        plan_id=2,
    )

    assert subscription.status_code == 200

    subscription_id = subscription.json()["subscription_id"]

    access_api.grant(
        user_id=3,
        subscription_id=subscription_id,
        course_id=3,
    )

    conn = sqlite3.connect(DB_PATH)

    expired_date = (
            datetime.now(timezone.utc) - timedelta(days=1)
    ).isoformat()

    conn.execute(
        """
        UPDATE subscriptions
        SET end_date = ?,
            status = 'expired'
        WHERE subscription_id = ?
        """,
        (
            expired_date,
            subscription_id,
        ),
    )

    conn.commit()
    conn.close()

    response = access_api.check(
        user_id=3,
        course_id=3,
    )

    assert response.status_code == 200
    assert response.json()["has_access"] is False