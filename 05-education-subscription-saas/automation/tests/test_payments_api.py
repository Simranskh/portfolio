def test_successful_payment(
    subscriptions_api,
    payments_api,
):

    subscription = subscriptions_api.create(
        user_id=4,
        plan_id=2,
    )

    assert subscription.status_code == 200

    subscription_id = subscription.json()["subscription_id"]

    payment = payments_api.create(
        user_id=4,
        subscription_id=subscription_id,
    )

    assert payment.status_code == 200

    data = payment.json()

    assert data["status"] == "success"
    assert data["amount"] == 499
    assert data["transaction_id"].startswith("TXN-")


def test_payment_history(
    subscriptions_api,
    payments_api,
):

    subscription = subscriptions_api.create(
        user_id=2,
        plan_id=3,
    )

    subscription_id = subscription.json()["subscription_id"]

    payments_api.create(
        user_id=2,
        subscription_id=subscription_id,
    )

    response = payments_api.history(2)

    assert response.status_code == 200

    payments = response.json()

    assert len(payments) >= 1