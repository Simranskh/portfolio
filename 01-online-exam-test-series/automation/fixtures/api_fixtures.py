import pytest

from automation.api.auth_api import AuthAPI
from automation.api.test_series_api import TestSeriesAPI
from automation.api.questions_api import QuestionsAPI
from automation.config import BASE_URL
from automation.api.exam_attempt_api import ExamAttemptAPI
from automation.api.attempt_answers_api import AttemptAnswersAPI

@pytest.fixture
def auth_api():
    return AuthAPI(BASE_URL)


@pytest.fixture
def test_series_api():
    return TestSeriesAPI(BASE_URL)


@pytest.fixture
def questions_api():
    return QuestionsAPI(BASE_URL)
@pytest.fixture
def exam_attempt_api():
    return ExamAttemptAPI(BASE_URL)
@pytest.fixture
def attempt_answers_api():
    return AttemptAnswersAPI(BASE_URL)