import pytest
from fastapi.testclient import TestClient

from app.backend.main import app

from automation.api.auth_api import AuthAPI
from automation.api.users_api import UsersAPI
from automation.api.plans_api import PlansAPI
from automation.api.subscriptions_api import SubscriptionsAPI
from automation.api.payments_api import PaymentsAPI
from automation.api.courses_api import CoursesAPI
from automation.api.access_control_api import AccessControlAPI


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def auth_api(client):
    return AuthAPI(client)


@pytest.fixture
def users_api(client):
    return UsersAPI(client)


@pytest.fixture
def plans_api(client):
    return PlansAPI(client)


@pytest.fixture
def subscriptions_api(client):
    return SubscriptionsAPI(client)


@pytest.fixture
def payments_api(client):
    return PaymentsAPI(client)


@pytest.fixture
def courses_api(client):
    return CoursesAPI(client)


@pytest.fixture
def access_api(client):
    return AccessControlAPI(client)