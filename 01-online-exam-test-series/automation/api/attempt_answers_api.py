import httpx


class AttemptAnswersAPI:
    def __init__(self, base_url):
        self.base_url = base_url

    def submit(self, attempt_id, question_id, selected_answer):
        return httpx.post(
            f"{self.base_url}/api/exam-attempts/{attempt_id}/answers",
            json={
                "question_id": question_id,
                "selected_answer": selected_answer,
            },
        )

    def submit_with_payload(self, attempt_id, payload):
        return httpx.post(
            f"{self.base_url}/api/exam-attempts/{attempt_id}/answers",
            json=payload,
        )