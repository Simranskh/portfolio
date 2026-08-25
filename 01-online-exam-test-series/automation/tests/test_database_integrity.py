from automation.utils.db_utils import get_user_by_email


def test_registered_user_exists_in_database():
    user = get_user_by_email("test@example.com")

    assert user is not None
    assert user[2] == "test@example.com"
    assert user[4] == "free"
    assert user[5] == 1


def test_password_is_hashed():
    user = get_user_by_email("test@example.com")

    assert user is not None
    assert user[3] != "Test@123"