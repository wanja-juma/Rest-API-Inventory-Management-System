import pytest

from app import app
from data import inventory


@pytest.fixture
def client():

    app.config["TESTING"] = True

    inventory.clear()

    inventory.extend(
        [
            {
                "id": 1,
                "barcode": "3017620422003",
                "product_name": "Nutella",
                "brand": "Ferrero",
                "ingredients": "Sugar, Palm Oil",
                "price": 7.99,
                "stock": 20
            },
            {
                "id": 2,
                "barcode": "5449000000996",
                "product_name": "Coca Cola",
                "brand": "Coca Cola",
                "ingredients": "Water, Sugar",
                "price": 2.50,
                "stock": 30
            },
            {
                "id": 3,
                "barcode": "123456789",
                "product_name": "Sprite",
                "brand": "Coca Cola",
                "ingredients": "Water, Sugar",
                "price": 3.00,
                "stock": 15
            }
        ]
    )

    with app.test_client() as client:
        yield client