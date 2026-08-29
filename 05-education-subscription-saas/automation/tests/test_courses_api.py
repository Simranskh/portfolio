def test_list_courses(courses_api):

    response = courses_api.get_courses()

    assert response.status_code == 200

    courses = response.json()

    assert len(courses) == 6


def test_get_course(courses_api):

    response = courses_api.get_course(1)

    assert response.status_code == 200

    data = response.json()

    assert data["course_name"] == "Python Fundamentals"
    assert data["subject"] == "Programming"