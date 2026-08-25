import httpx


class AuthAPI:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def login(self, email: str, password: str):
        return httpx.post(
            f"{self.base_url}/api/auth/login",
            json={
                "email": email,
                "password": password,
            },
        )

    def login_with_payload(self, payload: dict):
        return httpx.post(
            f"{self.base_url}/api/auth/login",
            json=payload,
        )

    def register(
        self,
        name: str,
        email: str,
        password: str,
        role: str = "free",
    ):
        return httpx.post(
            f"{self.base_url}/api/auth/register",
            json={
                "name": name,
                "email": email,
                "password": password,
                "role": role,
            },
        )

    def register_with_payload(self, payload: dict):
        return httpx.post(
            f"{self.base_url}/api/auth/register",
            json=payload,
        )