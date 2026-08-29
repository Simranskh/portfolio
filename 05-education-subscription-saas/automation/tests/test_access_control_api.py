def test_grant_course_access(
    subscriptions_api,
    access_api,
):

    subscription = subscriptions_api.create(
        user_id=1,
        plan_id=3,
    )

    assert subscription.status_code == 200

    subscription_id = subscription.json()["subscription_id"]

    response = access_api.grant(
        user_id=1,
        subscription_id=subscription_id,
        course_id=1,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["access"] is True


def test_check_course_access(
    subscriptions_api,
    access_api,
):

    subscription = subscriptions_api.create(
        user_id=2,
        plan_id=3,
    )

    subscription_id = subscription.json()["subscription_id"]

    access_api.grant(
        user_id=2,
        subscription_id=subscription_id,
        course_id=2,
    )

    response = access_api.check(
        user_id=2,
        course_id=2,
    )

    assert response.status_code == 200

    assert response.json()["has_access"] is True


def test_access_denied_without_entitlement(
    access_api,
):

    response = access_api.check(
        user_id=3,
        course_id=6,
    )

    assert response.status_code == 200

    assert response.json()["has_access"] is False