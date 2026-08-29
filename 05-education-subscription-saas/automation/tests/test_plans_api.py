def test_list_active_plans(plans_api):

    response = plans_api.get_plans()

    assert response.status_code == 200

    plans = response.json()

    assert len(plans) == 4

    names = [plan["plan_name"] for plan in plans]

    assert "Free" in names
    assert "Basic" in names
    assert "Premium" in names
    assert "Annual" in names


def test_get_plan(plans_api):

    response = plans_api.get_plan(3)

    assert response.status_code == 200

    data = response.json()

    assert data["plan_name"] == "Premium"
    assert data["price"] == 999
    assert data["max_courses"] == 10