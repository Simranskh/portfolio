from uuid import uuid4

from automation.utils.db_utils import get_member_by_id


def test_create_member(members_api):
    email = f"member-{uuid4().hex[:10]}@example.com"

    response = members_api.create(
        name="Rahul Sharma",
        email=email,
    )

    assert response.status_code == 201

    data = response.json()

    assert data["message"] == "Member created successfully"
    assert "member_id" in data

    member_id = data["member_id"]

    member = get_member_by_id(member_id)

    assert member is not None
    assert member[0] == member_id
    assert member[1] == "Rahul Sharma"
    assert member[2] == email
    assert member[3] == 1


def test_create_member_duplicate_email(members_api):
    email = f"duplicate-{uuid4().hex[:10]}@example.com"

    first_response = members_api.create(
        name="First Member",
        email=email,
    )

    assert first_response.status_code == 201

    second_response = members_api.create(
        name="Second Member",
        email=email,
    )

    assert second_response.status_code == 409
    assert second_response.json()["detail"] == (
        "Member with this email already exists"
    )
def test_get_member(members_api):
    email = f"get-{uuid4().hex[:10]}@example.com"

    create_response = members_api.create(
        name="GET Member",
        email=email,
    )

    assert create_response.status_code == 201

    member_id = create_response.json()["member_id"]

    response = members_api.get_by_id(member_id)

    assert response.status_code == 200

    data = response.json()

    assert data["member_id"] == member_id
    assert data["name"] == "GET Member"
    assert data["email"] == email
    assert data["is_active"] is True


def test_get_member_invalid_id(members_api):
    response = members_api.get_by_id(99999)

    assert response.status_code == 404
    assert response.json()["detail"] == "Member not found"