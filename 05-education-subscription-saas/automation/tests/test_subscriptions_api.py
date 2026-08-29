def test_create_subscription(subscriptions_api):

    response = subscriptions_api.create(
        user_id=1,
        plan_id=2,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["user_id"] == 1
    assert data["plan_id"] == 2
    assert data["status"] == "active"


def test_duplicate_active_subscription_rejected(
    subscriptions_api,
):

    response = subscriptions_api.create(
        user_id=2,
        plan_id=2,
    )

    assert response.status_code == 200

    duplicate = subscriptions_api.create(
        user_id=2,
        plan_id=3,
    )

    assert duplicate.status_code == 409

def test_get_user_subscription(
    subscriptions_api,
):
    create = subscriptions_api.create(
        user_id=1,
        plan_id=3,
    )

    assert create.status_code == 200

    response = subscriptions_api.get_user_subscription(1)

    assert response.status_code == 200

    data = response.json()

    assert data["user_id"] == 1
    assert data["plan_id"] == 3
    assert data["status"] == "active"


def test_cancel_subscription(
    subscriptions_api,
):

    create = subscriptions_api.create(
        user_id=3,
        plan_id=1,
    )

    subscription_id = create.json()["subscription_id"]

    response = subscriptions_api.cancel(
        subscription_id
    )

    assert response.status_code == 200
    assert response.json()["status"] == "cancelled"