class AccessControlAPI:

    def __init__(self, client):
        self.client = client

    def grant(
        self,
        user_id,
        subscription_id,
        course_id,
    ):
        return self.client.post(
            "/access/grant",
            params={
                "user_id": user_id,
                "subscription_id": subscription_id,
                "course_id": course_id,
            },
        )

    def check(self, user_id, course_id):
        return self.client.get(
            "/access/check",
            params={
                "user_id": user_id,
                "course_id": course_id,
            },
        )