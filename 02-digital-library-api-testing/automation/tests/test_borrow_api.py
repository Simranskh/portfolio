from uuid import uuid4

from automation.utils.db_utils import (
    get_book_availability,
    get_borrow_record_by_id,
)


def test_borrow_book(
    borrow_api,
    books_api,
    members_api,
):
    book_isbn = f"TEST-BORROW-{uuid4().hex[:10]}"
    member_email = f"borrow-{uuid4().hex[:10]}@example.com"

    # Create a fresh book
    book_response = books_api.create(
        title="Borrow Test Book",
        author="QA Engineer",
        isbn=book_isbn,
        category="Testing",
    )

    assert book_response.status_code == 201

    book_id = book_response.json()["book_id"]

    # Create a fresh member
    member_response = members_api.create(
        name="Borrow Test Member",
        email=member_email,
    )

    assert member_response.status_code == 201

    member_id = member_response.json()["member_id"]

    # Borrow the book
    response = borrow_api.borrow(
        book_id=book_id,
        member_id=member_id,
    )

    assert response.status_code == 201

    data = response.json()

    assert data["message"] == "Book borrowed successfully"
    assert "borrow_id" in data

    borrow_id = data["borrow_id"]

    # Validate borrow record
    record = get_borrow_record_by_id(borrow_id)

    assert record is not None
    assert record[0] == borrow_id
    assert record[1] == book_id
    assert record[2] == member_id
    assert record[3] is not None
    assert record[4] is None
    assert record[5] == "borrowed"

    # Validate book availability
    availability = get_book_availability(book_id)

    assert availability is not None
    assert availability[0] == 0

def test_borrow_invalid_book(
            borrow_api,
            members_api,
    ):
        member_email = f"invalid-book-{uuid4().hex[:10]}@example.com"

        member_response = members_api.create(
            name="Invalid Book Member",
            email=member_email,
        )

        assert member_response.status_code == 201

        member_id = member_response.json()["member_id"]

        response = borrow_api.borrow(
            book_id=99999,
            member_id=member_id,
        )

        assert response.status_code == 404
        assert response.json()["detail"] == "Book not found"
def test_borrow_invalid_member(
            borrow_api,
            books_api,
    ):
        book_isbn = f"TEST-INVALID-MEMBER-{uuid4().hex[:8]}"

        book_response = books_api.create(
            title="Invalid Member Book",
            author="QA Engineer",
            isbn=book_isbn,
            category="Testing",
        )

        assert book_response.status_code == 201

        book_id = book_response.json()["book_id"]

        response = borrow_api.borrow(
            book_id=book_id,
            member_id=99999,
        )

        assert response.status_code == 404
        assert response.json()["detail"] == "Member not found"

def test_borrow_already_borrowed_book(
            borrow_api,
            books_api,
            members_api,
    ):
        book_isbn = f"TEST-ALREADY-BORROWED-{uuid4().hex[:8]}"
        first_email = f"borrow1-{uuid4().hex[:8]}@example.com"
        second_email = f"borrow2-{uuid4().hex[:8]}@example.com"

        book_response = books_api.create(
            title="Already Borrowed Book",
            author="QA Engineer",
            isbn=book_isbn,
            category="Testing",
        )

        assert book_response.status_code == 201

        book_id = book_response.json()["book_id"]

        first_member_response = members_api.create(
            name="First Borrower",
            email=first_email,
        )

        assert first_member_response.status_code == 201

        first_member_id = first_member_response.json()["member_id"]

        second_member_response = members_api.create(
            name="Second Borrower",
            email=second_email,
        )

        assert second_member_response.status_code == 201

        second_member_id = second_member_response.json()["member_id"]

        first_borrow = borrow_api.borrow(
            book_id=book_id,
            member_id=first_member_id,
        )

        assert first_borrow.status_code == 201

        second_borrow = borrow_api.borrow(
            book_id=book_id,
            member_id=second_member_id,
        )

        assert second_borrow.status_code == 409
        assert second_borrow.json()["detail"] == "Book is already borrowed"
def return_book(self, borrow_id):
    return httpx.post(
        f"{self.base_url}/api/borrow/{borrow_id}/return",
    )
def test_return_book(
    borrow_api,
    books_api,
    members_api,
):
    book_isbn = f"TEST-RETURN-{uuid4().hex[:10]}"
    member_email = f"return-{uuid4().hex[:10]}@example.com"

    book_response = books_api.create(
        title="Return Test Book",
        author="QA Engineer",
        isbn=book_isbn,
        category="Testing",
    )

    assert book_response.status_code == 201

    book_id = book_response.json()["book_id"]

    member_response = members_api.create(
        name="Return Test Member",
        email=member_email,
    )

    assert member_response.status_code == 201

    member_id = member_response.json()["member_id"]

    borrow_response = borrow_api.borrow(
        book_id=book_id,
        member_id=member_id,
    )

    assert borrow_response.status_code == 201

    borrow_id = borrow_response.json()["borrow_id"]

    return_response = borrow_api.return_book(borrow_id)

    assert return_response.status_code == 200

    data = return_response.json()

    assert data["message"] == "Book returned successfully"
    assert data["borrow_id"] == borrow_id

    record = get_borrow_record_by_id(borrow_id)

    assert record is not None
    assert record[0] == borrow_id
    assert record[1] == book_id
    assert record[2] == member_id
    assert record[4] is not None
    assert record[5] == "returned"

    availability = get_book_availability(book_id)

    assert availability is not None
    assert availability[0] == 1
def test_return_invalid_borrow_id(borrow_api):
    response = borrow_api.return_book(99999)

    assert response.status_code == 404
    assert response.json()["detail"] == "Borrow record not found"


def test_return_already_returned_book(
    borrow_api,
    books_api,
    members_api,
):
    book_isbn = f"TEST-RETURN-TWICE-{uuid4().hex[:8]}"
    member_email = f"return-twice-{uuid4().hex[:8]}@example.com"

    book_response = books_api.create(
        title="Return Twice Book",
        author="QA Engineer",
        isbn=book_isbn,
        category="Testing",
    )

    assert book_response.status_code == 201

    book_id = book_response.json()["book_id"]

    member_response = members_api.create(
        name="Return Twice Member",
        email=member_email,
    )

    assert member_response.status_code == 201

    member_id = member_response.json()["member_id"]

    borrow_response = borrow_api.borrow(
        book_id=book_id,
        member_id=member_id,
    )

    assert borrow_response.status_code == 201

    borrow_id = borrow_response.json()["borrow_id"]

    first_return = borrow_api.return_book(borrow_id)

    assert first_return.status_code == 200

    second_return = borrow_api.return_book(borrow_id)

    assert second_return.status_code == 409
    assert second_return.json()["detail"] == "Book has already been returned"