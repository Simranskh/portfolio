from automation.utils.db_utils import get_test_series_by_id


def test_create_test_series(test_series_api):
    response = test_series_api.create(
        title="SSC Mathematics Mock Test 1",
        description="Quantitative aptitude practice test",
    )

    assert response.status_code == 201

    data = response.json()

    assert data["message"] == "Test series created successfully"
    assert "test_series_id" in data

    test_series_id = data["test_series_id"]

    test_series = get_test_series_by_id(test_series_id)

    assert test_series is not None
    assert test_series[0] == test_series_id
    assert test_series[1] == "SSC Mathematics Mock Test 1"
    assert test_series[2] == "Quantitative aptitude practice test"
    assert test_series[3] == 1
import pytest


@pytest.mark.parametrize(
    "payload, expected_status",
    [
        (
            {
                "description": "Test without title",
            },
            422,
        ),
        (
            {
                "title": "Test Without Description",
            },
            201,
        ),
    ],
)
def test_create_test_series_validation(
    test_series_api,
    payload,
    expected_status,
):
    response = test_series_api.create_with_payload(payload)

    assert response.status_code == expected_status