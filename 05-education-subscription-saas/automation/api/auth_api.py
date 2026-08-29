class AuthAPI:

    def __init__(self, client):
        self.client = client

    def login(self, email, password):
        return self.client.post(
            "/auth/login",
            params={
                "email": email,
                "password": password,
            },
        )

    def logout(self, token):
        return self.client.post(
            "/auth/logout",
            params={"token": token},
        )