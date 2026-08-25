import httpx


class BorrowAPI:
    def __init__(self, base_url):
        self.base_url = base_url

    def borrow(self, book_id, member_id):
        return httpx.post(
            f"{self.base_url}/api/borrow",
            json={
                "book_id": book_id,
                "member_id": member_id,
            },
        )

    def borrow_with_payload(self, payload):
        return httpx.post(
            f"{self.base_url}/api/borrow",
            json=payload,
        )

    def return_book(self, borrow_id):
        return httpx.post(
            f"{self.base_url}/api/borrow/{borrow_id}/return",
        )