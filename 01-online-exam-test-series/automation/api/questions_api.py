import httpx


class QuestionsAPI:
    def __init__(self, base_url):
        self.base_url = base_url

    def create(
        self,
        test_series_id,
        question_text,
        option_a,
        option_b,
        option_c,
        option_d,
        correct_answer,
        marks=1,
    ):
        return httpx.post(
            f"{self.base_url}/api/questions",
            json={
                "test_series_id": test_series_id,
                "question_text": question_text,
                "option_a": option_a,
                "option_b": option_b,
                "option_c": option_c,
                "option_d": option_d,
                "correct_answer": correct_answer,
                "marks": marks,
            },
        )

    def create_with_payload(self, payload):
        return httpx.post(
            f"{self.base_url}/api/questions",
            json=payload,
        )