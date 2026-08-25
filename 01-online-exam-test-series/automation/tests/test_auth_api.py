import uuid
import pytest
from automation.utils.db_utils import get_user_by_id

def test_valid_login(auth_api):
    response = auth_api.login(
        "test@example.com",
        "Test@123",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Login successful"
    assert data["user_id"] == 1
    assert data["name"] == "ExamPro Test User"
    assert data["role"] == "free"


@pytest.mark.parametrize(
    "test_name, payload, expected_status",
    [
        (
            "wrong_password",
            {
                "email": "test@example.com",
                "password": "WrongPassword123",
            },
            401,
        ),
        (
            "unknown_email",
            {
                "email": "doesnotexist@example.com",
                "password": "Test@123",
            },
            401,
        ),
        (
            "missing_email",
            {
                "password": "Test@123",
            },
            422,
        ),
        (
            "missing_password",
            {
                "email": "test@example.com",
            },
            422,
        ),
    ],
)
def test_login_negative_scenarios(
    auth_api,
    test_name,
    payload,
    expected_status,
):
    response = auth_api.login_with_payload(payload)

    assert response.status_code == expected_status


def test_valid_registration(auth_api):
    email = f"automation_{uuid.uuid4().hex[:8]}@example.com"

    response = auth_api.register(
        name="Automation Test User",
        email=email,
        password="Test@123",

    )

    assert response.status_code == 201

    data = response.json()

    assert data["message"] == "User registered successfully"
    assert "user_id" in data


def test_duplicate_registration(auth_api):
    response = auth_api.register(
        name="Duplicate User",
        email="test@example.com",
        password="Test@123",
        role="free",
    )

    assert response.status_code == 409

    data = response.json()

    assert data["detail"] == "Email already registered"
@pytest.mark.parametrize(
    "test_name, payload, expected_status",
    [
        (
            "invalid_email",
            {
                "name": "Invalid Email User",
                "email": "not-an-email",
                "password": "Test@123",
                "role": "free",
            },
            422,
        ),
        (
            "missing_email",
            {
                "name": "Missing Email User",
                "password": "Test@123",
                "role": "free",
            },
            422,
        ),
        (
            "missing_password",
            {
                "name": "Missing Password User",
                "email": "missingpassword@example.com",
                "role": "free",
            },
            422,
        ),
        (
            "empty_name",
            {
                "name": "",
                "email": "emptyname@example.com",
                "password": "Test@123",
                "role": "free",
            },
            422,
        ),
        (
            "weak_password",
            {
                "name": "Weak Password User",
                "email": "weakpassword@example.com",
                "password": "123",
                "role": "free",
            },
            422,
        ),
    ],
)
def test_registration_negative_scenarios(
    auth_api,
    test_name,
    payload,
    expected_status,
):
    response = auth_api.register_with_payload(payload)

    assert response.status_code == expected_status
def test_registration_cannot_set_admin_role(auth_api):
    email = f"security_{uuid.uuid4().hex[:8]}@example.com"

    response = auth_api.register_with_payload(
        {
            "name": "Security Test User",
            "email": email,
            "password": "Test@123",
            "role": "admin",
        }
    )

    assert response.status_code == 201
    data = response.json()

    assert "user_id" in data
def test_registration_cannot_set_admin_role(auth_api):
    email = f"security_{uuid.uuid4().hex[:8]}@example.com"

    response = auth_api.register_with_payload(
        {
            "name": "Security Test User",
            "email": email,
            "password": "Test@123",
            "role": "admin",
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert "user_id" in data

    user_id = data["user_id"]

    user = get_user_by_id(user_id)

    assert user is not None
    assert user[0] == user_id
    assert user[1] == "Security Test User"
    assert user[2] == email
    assert user[3] == "free"