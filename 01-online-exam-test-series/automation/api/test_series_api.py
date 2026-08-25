import httpx


class TestSeriesAPI:
    def __init__(self, base_url):
        self.base_url = base_url

    def create(self, title, description=None):
        return httpx.post(
            f"{self.base_url}/api/test-series",
            json={
                "title": title,
                "description": description,
            },
        )

    def create_with_payload(self, payload):
        return httpx.post(
            f"{self.base_url}/api/test-series",
            json=payload,
        )