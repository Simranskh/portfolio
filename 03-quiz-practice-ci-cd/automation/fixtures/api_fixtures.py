import pytest

from automation.api.quizzes_api import QuizzesAPI


@pytest.fixture
def quizzes_api():
    return QuizzesAPI()