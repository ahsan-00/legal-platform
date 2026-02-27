import pytest

BASE_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3001"

@pytest.fixture
def api_base():
    return BASE_URL

@pytest.fixture
def frontend_url():
    return FRONTEND_URL