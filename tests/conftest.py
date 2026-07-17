import pytest

from app import app
from data import inventory


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        inventory.clear()
        yield client
        inventory.clear()