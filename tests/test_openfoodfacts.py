from unittest.mock import patch
import requests

from helpers import fetch_product_by_barcode


class MockSuccessResponse:

    @staticmethod
    def json():

        return {
            "status": 1,
            "product": {
                "product_name": "Sprite",
                "brands": "Coca Cola",
                "ingredients_text": "Water, Sugar"
            }
        }

    def raise_for_status(self):
        pass


class MockNotFoundResponse:

    @staticmethod
    def json():

        return {
            "status": 0
        }

    def raise_for_status(self):
        pass


@patch("helpers.requests.get")
def test_fetch_barcode_success(mock_get):

    mock_get.return_value = MockSuccessResponse()

    product = fetch_product_by_barcode(
        "5449000000996"
    )

    assert product["product_name"] == "Sprite"
    assert product["brand"] == "Coca Cola"


@patch("helpers.requests.get")
def test_fetch_barcode_not_found(mock_get):

    mock_get.return_value = MockNotFoundResponse()

    product = fetch_product_by_barcode(
        "000000000"
    )

    assert product is None


@patch("helpers.requests.get")
def test_fetch_barcode_request_exception(mock_get):

    mock_get.side_effect = requests.RequestException()

    product = fetch_product_by_barcode(
        "5449000000996"
    )

    assert product is None