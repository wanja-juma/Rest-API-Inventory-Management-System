from unittest.mock import patch

import cli


class MockInventoryResponse:

    status_code = 200

    def json(self):

        return [
            {
                "id": 1,
                "product_name": "Nutella",
                "brand": "Ferrero",
                "price": 7.99,
                "stock": 20,
                "barcode": "3017620422003"
            }
        ]


@patch("cli.requests.get")
def test_view_inventory(mock_get):

    mock_get.return_value = MockInventoryResponse()

    cli.view_inventory()

    assert mock_get.called


@patch("cli.requests.post")
@patch("builtins.input")
def test_add_product(mock_input, mock_post):

    mock_input.side_effect = [
        "3017620422003",
        "7.99",
        "25"
    ]

    mock_post.return_value.status_code = 201

    cli.add_product()

    assert mock_post.called


@patch("cli.requests.patch")
@patch("builtins.input")
def test_update_product(mock_input, mock_patch):

    mock_input.side_effect = [
        "1",
        "9.99",
        "50"
    ]

    mock_patch.return_value.status_code = 200

    cli.update_product()

    assert mock_patch.called


@patch("cli.requests.delete")
@patch("builtins.input")
def test_delete_product(mock_input, mock_delete):

    mock_input.return_value = "1"

    mock_delete.return_value.status_code = 200

    cli.delete_product()

    assert mock_delete.called

class MockBarcodeResponse:
     
    status_code = 200

    def json(self):
        return {
            "product_name": "Nutella",
            "brand": "Ferrero",
            "ingredients": "Sugar, Palm Oil",
            "barcode": "3017620422003"
        }


@patch("cli.requests.get")
@patch("builtins.input")
def test_search_barcode(mock_input, mock_get):

    mock_input.return_value = "3017620422003"

    mock_get.return_value = MockBarcodeResponse()

    cli.search_barcode()

    assert mock_get.called