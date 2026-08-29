class UsersAPI:

    def __init__(self, client):
        self.client = client

    def create_user(self, name, email, password):
        return self.client.post(
            "/users",
            params={
                "name": name,
                "email": email,
                "password": password,
            },
        )

    def get_user(self, user_id):
        return self.client.get(
            f"/users/{user_id}"
        )