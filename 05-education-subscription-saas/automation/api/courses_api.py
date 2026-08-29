class CoursesAPI:

    def __init__(self, client):
        self.client = client

    def get_courses(self):
        return self.client.get("/courses")

    def get_course(self, course_id):
        return self.client.get(
            f"/courses/{course_id}"
        )