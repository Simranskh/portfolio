import uuid


def test_get_existing_user(users_api):

    response = users_api.get_user(1)

    assert response.status_code == 200

    data = response.json()

    assert data["user_id"] == 1
    assert data["email"] == "aarav@example.com"


def test_create_user(users_api):

    email = f"qa_{uuid.uuid4().hex[:8]}@example.com"

    response = users_api.create_user(
        "QA Student",
        email,
        "Password123",
    )

    assert response.status_code == 200
    assert response.json()["email"] == email


def test_duplicate_email_rejected(users_api):

    response = users_api.create_user(
        "Duplicate User",
        "aarav@example.com",
        "Password123",
    )

    assert response.status_code == 409