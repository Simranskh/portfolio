from uuid import uuid4

from automation.utils.db_utils import get_book_by_id


def test_create_book(books_api):
    isbn = f"TEST-{uuid4().hex[:12]}"

    response = books_api.create(
        title="API Testing with Python",
        author="James Smith",
        isbn=isbn,
        category="Technology",
    )

    assert response.status_code == 201

    data = response.json()

    assert data["message"] == "Book created successfully"
    assert "book_id" in data

    book_id = data["book_id"]

    book = get_book_by_id(book_id)

    assert book is not None
    assert book[0] == book_id
    assert book[1] == "API Testing with Python"
    assert book[2] == "James Smith"
    assert book[3] == isbn
    assert book[4] == "Technology"
    assert book[5] == 1


def test_create_book_duplicate_isbn(books_api):
    isbn = f"TEST-DUP-{uuid4().hex[:10]}"

    first_response = books_api.create(
        title="Digital Library Testing",
        author="QA Engineer",
        isbn=isbn,
        category="Technology",
    )

    assert first_response.status_code == 201

    second_response = books_api.create(
        title="Another Book",
        author="Another Author",
        isbn=isbn,
        category="Technology",
    )

    assert second_response.status_code == 409
    assert second_response.json()["detail"] == (
        "Book with this ISBN already exists"
    )


def test_get_book(books_api):
    isbn = f"TEST-GET-{uuid4().hex[:10]}"

    create_response = books_api.create(
        title="GET API Testing",
        author="QA Engineer",
        isbn=isbn,
        category="Testing",
    )

    assert create_response.status_code == 201

    book_id = create_response.json()["book_id"]

    response = books_api.get_by_id(book_id)

    assert response.status_code == 200

    data = response.json()

    assert data["book_id"] == book_id
    assert data["title"] == "GET API Testing"
    assert data["author"] == "QA Engineer"
    assert data["isbn"] == isbn
    assert data["category"] == "Testing"
    assert data["is_available"] is True


def test_get_book_invalid_id(books_api):
    response = books_api.get_by_id(99999)

    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"
def test_update_book(books_api):
    isbn = f"TEST-UPDATE-{uuid4().hex[:10]}"

    create_response = books_api.create(
        title="Original Book",
        author="Original Author",
        isbn=isbn,
        category="Old Category",
    )

    assert create_response.status_code == 201

    book_id = create_response.json()["book_id"]

    update_response = books_api.update(
        book_id=book_id,
        title="Updated Book",
        author="Updated Author",
        category="New Category",
    )

    assert update_response.status_code == 200

    data = update_response.json()

    assert data["message"] == "Book updated successfully"
    assert data["book_id"] == book_id

    book = get_book_by_id(book_id)

    assert book is not None
    assert book[0] == book_id
    assert book[1] == "Updated Book"
    assert book[2] == "Updated Author"
    assert book[3] == isbn
    assert book[4] == "New Category"
    assert book[5] == 1


def test_update_book_invalid_id(books_api):
    response = books_api.update_with_payload(
        99999,
        {
            "title": "Updated Book",
            "author": "Updated Author",
            "category": "Testing",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"

def test_delete_book(books_api):
        isbn = f"TEST-DELETE-{uuid4().hex[:10]}"

        create_response = books_api.create(
            title="Book To Delete",
            author="QA Engineer",
            isbn=isbn,
            category="Testing",
        )

        assert create_response.status_code == 201

        book_id = create_response.json()["book_id"]

        delete_response = books_api.delete(book_id)

        assert delete_response.status_code == 200

        data = delete_response.json()

        assert data["message"] == "Book deleted successfully"
        assert data["book_id"] == book_id

        book = get_book_by_id(book_id)

        assert book is None

def test_delete_book_invalid_id(books_api):
        response = books_api.delete(99999)

        assert response.status_code == 404
        assert response.json()["detail"] == "Book not found"