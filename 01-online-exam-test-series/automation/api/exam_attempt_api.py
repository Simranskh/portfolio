import httpx


class ExamAttemptAPI:
    def __init__(self, base_url):
        self.base_url = base_url

    def start(self, user_id, test_series_id):
        return httpx.post(
            f"{self.base_url}/api/exam-attempts",
            json={
                "user_id": user_id,
                "test_series_id": test_series_id,
            },
        )

    def start_with_payload(self, payload):
        return httpx.post(
            f"{self.base_url}/api/exam-attempts",
            json=payload,
        )

    def submit(self, attempt_id):
        return httpx.post(
            f"{self.base_url}/api/exam-attempts/{attempt_id}/submit",
        )

    def get_by_id(self, attempt_id):
        return httpx.get(
            f"{self.base_url}/api/exam-attempts/{attempt_id}",
        )