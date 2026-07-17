from unittest.mock import patch, Mock

from helpers import fetch_product_by_name

import requests

# SUCCESSFUL SEARCH

@patch("helpers.requests.get")
def test_fetch_product_by_name_success(mock_get):

    mock_response = Mock()

    mock_response.raise_for_status.return_value = None

    mock_response.json.return_value = {
        "products": [
            {
                "product_name": "Milk",
                "brands": "Brookside",
                "ingredients_text": "Milk",
                "code": "123456789"
            }
        ]
    }

    mock_get.return_value = mock_response

    result = fetch_product_by_name("milk")

    assert len(result) == 1

    assert result[0]["product_name"] == "Milk"
    assert result[0]["brand"] == "Brookside"
    assert result[0]["ingredients"] == "Milk"
    assert result[0]["barcode"] == "123456789"

# NO PRODUCTS FOUND

@patch("helpers.requests.get")
def test_fetch_product_by_name_not_found(mock_get):

    mock_response = Mock()

    mock_response.raise_for_status.return_value = None

    mock_response.json.return_value = {
        "products": []
    }

    mock_get.return_value = mock_response

    result = fetch_product_by_name("unknown")

    assert result == []

# REQUEST EXCEPTION

@patch("helpers.requests.get")
def test_fetch_product_by_name_request_exception(mock_get):

    mock_get.side_effect = requests.RequestException(
        "Connection Error"
    )

    result = fetch_product_by_name("milk")

    assert result == []