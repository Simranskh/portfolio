from automation.utils.db_utils import (
    fetch_one,
)


def assert_zero(query):
    row = fetch_one(query)
    assert row[0] == 0


def test_no_orphan_subscriptions():

    assert_zero(
        """
        SELECT COUNT(*)
        FROM subscriptions s
        LEFT JOIN users u
            ON s.user_id = u.user_id
        WHERE u.user_id IS NULL
        """
    )


def test_no_invalid_plan_references():

    assert_zero(
        """
        SELECT COUNT(*)
        FROM subscriptions s
        LEFT JOIN plans p
            ON s.plan_id = p.plan_id
        WHERE p.plan_id IS NULL
        """
    )


def test_no_orphan_payments():

    assert_zero(
        """
        SELECT COUNT(*)
        FROM payments p
        LEFT JOIN subscriptions s
            ON p.subscription_id = s.subscription_id
        WHERE s.subscription_id IS NULL
        """
    )


def test_payment_user_matches_subscription():

    assert_zero(
        """
        SELECT COUNT(*)
        FROM payments p
        JOIN subscriptions s
            ON p.subscription_id = s.subscription_id
        WHERE p.user_id != s.user_id
        """
    )


def test_no_negative_plan_prices():

    assert_zero(
        """
        SELECT COUNT(*)
        FROM plans
        WHERE price < 0
        """
    )


def test_valid_subscription_status():

    assert_zero(
        """
        SELECT COUNT(*)
        FROM subscriptions
        WHERE status NOT IN (
            'active',
            'expired',
            'cancelled'
        )
        """
    )


def test_no_orphan_entitlements():

    assert_zero(
        """
        SELECT COUNT(*)
        FROM entitlements e
        LEFT JOIN subscriptions s
            ON e.subscription_id = s.subscription_id
        WHERE s.subscription_id IS NULL
        """
    )


def test_successful_payment_has_timestamp():

    assert_zero(
        """
        SELECT COUNT(*)
        FROM payments
        WHERE status = 'success'
        AND paid_at IS NULL
        """
    )