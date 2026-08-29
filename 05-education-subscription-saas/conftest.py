import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from database.init_db import init_database

from automation.fixtures.api_fixtures import (
    client,
    auth_api,
    users_api,
    plans_api,
    subscriptions_api,
    payments_api,
    courses_api,
    access_api,
)


@pytest.fixture(autouse=True)
def initialize_database():
    init_database()