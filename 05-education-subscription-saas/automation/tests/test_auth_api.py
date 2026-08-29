def test_valid_login(auth_api):

    response = auth_api.login(
        "aarav@example.com",
        "Password123",
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["user_id"] == 1
    assert data["role"] == "student"


def test_invalid_login(auth_api):

    response = auth_api.login(
        "aarav@example.com",
        "WrongPassword",
    )

    assert response.status_code == 401


def test_logout(auth_api):

    login = auth_api.login(
        "aarav@example.com",
        "Password123",
    )

    token = login.json()["access_token"]

    response = auth_api.logout(token)

    assert response.status_code == 200
    assert response.json()["message"] == "Logged out successfully"