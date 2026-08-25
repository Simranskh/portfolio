import pytest

from automation.api.books_api import BooksAPI
from automation.config import BASE_URL
from automation.api.members_api import MembersAPI
from automation.api.borrow_api import BorrowAPI
@pytest.fixture
def books_api():
    return BooksAPI(BASE_URL)
@pytest.fixture
def members_api():
    return MembersAPI(BASE_URL)
@pytest.fixture
def borrow_api():
    return BorrowAPI(BASE_URL)