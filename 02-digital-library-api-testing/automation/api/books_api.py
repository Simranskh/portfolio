import httpx


class BooksAPI:
    def __init__(self, base_url):
        self.base_url = base_url

    def create(self, title, author, isbn, category=None):
        return httpx.post(
            f"{self.base_url}/api/books",
            json={
                "title": title,
                "author": author,
                "isbn": isbn,
                "category": category,
            },
        )

    def create_with_payload(self, payload):
        return httpx.post(
            f"{self.base_url}/api/books",
            json=payload,
        )

    def get_by_id(self, book_id):
        return httpx.get(
            f"{self.base_url}/api/books/{book_id}",
        )

    def update(self, book_id, title, author, category=None):
        return httpx.put(
            f"{self.base_url}/api/books/{book_id}",
            json={
                "title": title,
                "author": author,
                "category": category,
            },
        )

    def update_with_payload(self, book_id, payload):
        return httpx.put(
            f"{self.base_url}/api/books/{book_id}",
            json=payload,
        )
    def delete(self, book_id):
        return httpx.delete(
            f"{self.base_url}/api/books/{book_id}",
        )