import httpx


class MembersAPI:
    def __init__(self, base_url):
        self.base_url = base_url

    def create(self, name, email):
        return httpx.post(
            f"{self.base_url}/api/members",
            json={
                "name": name,
                "email": email,
            },
        )

    def create_with_payload(self, payload):
        return httpx.post(
            f"{self.base_url}/api/members",
            json=payload,
        )

    def get_by_id(self, member_id):
        return httpx.get(
            f"{self.base_url}/api/members/{member_id}",
        )