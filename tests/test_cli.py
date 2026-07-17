from unittest.mock import patch, Mock

from cli import (
    view_inventory,
    view_product,
    add_product,
    update_product,
    delete_product,
    search_name
)

# VIEW INVENTORY

@patch("cli.requests.get")
def test_view_inventory(mock_get, capsys):

    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [
        {
            "id": 1,
            "product_name": "Milk",
            "brand": "Brookside",
            "ingredients": "Milk",
            "price": 65.0,
            "stock": 20
        }
    ]

    view_inventory()

    captured = capsys.readouterr()

    assert "Milk" in captured.out
    assert "Brookside" in captured.out

# EMPTY INVENTORY

@patch("cli.requests.get")
def test_view_empty_inventory(mock_get, capsys):

    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = []

    view_inventory()

    captured = capsys.readouterr()

    assert "Inventory is empty." in captured.out

# VIEW PRODUCT

@patch("builtins.input", return_value="1")
@patch("cli.requests.get")
def test_view_product(mock_get, mock_input, capsys):

    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "id": 1,
        "product_name": "Milk",
        "brand": "Brookside",
        "ingredients": "Milk",
        "price": 65.0,
        "stock": 20
    }

    view_product()

    captured = capsys.readouterr()

    assert "Milk" in captured.out
    assert "Brookside" in captured.out

# ADD PRODUCT

@patch(
    "builtins.input",
    side_effect=[
        "Milk",
        "Brookside",
        "Milk",
        "65",
        "20"
    ]
)
@patch("cli.requests.post")
def test_add_product(mock_post, mock_input, capsys):

    mock_post.return_value.status_code = 201
    mock_post.return_value.json.return_value = {
        "id": 1,
        "product_name": "Milk",
        "brand": "Brookside",
        "ingredients": "Milk",
        "price": 65.0,
        "stock": 20
    }

    add_product()

    captured = capsys.readouterr()

    assert "Product added successfully." in captured.out

# UPDATE PRODUCT

@patch(
    "builtins.input",
    side_effect=[
        "1",
        "",
        "",
        "",
        "80",
        "30"
    ]
)
@patch("cli.requests.patch")
def test_update_product(mock_patch, mock_input, capsys):

    mock_patch.return_value.status_code = 200
    mock_patch.return_value.json.return_value = {
        "id": 1,
        "product_name": "Milk",
        "brand": "Brookside",
        "ingredients": "Milk",
        "price": 80.0,
        "stock": 30
    }

    update_product()

    captured = capsys.readouterr()

    assert "Product updated successfully." in captured.out

# DELETE PRODUCT


@patch("builtins.input", return_value="1")
@patch("cli.requests.delete")
def test_delete_product(mock_delete, mock_input, capsys):

    mock_delete.return_value.status_code = 200
    mock_delete.return_value.json.return_value = {
        "message": "Product deleted successfully"
    }

    delete_product()

    captured = capsys.readouterr()

    assert "Product deleted successfully" in captured.out

# SEARCH OPENFOODFACTS

@patch("builtins.input", return_value="milk")
@patch("cli.requests.get")
def test_search_name(mock_get, mock_input, capsys):

    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [
        {
            "product_name": "Milk",
            "brand": "Brookside",
            "ingredients": "Milk",
            "barcode": "123456789"
        }
    ]

    search_name()

    captured = capsys.readouterr()

    assert "Milk" in captured.out
    assert "Brookside" in captured.out

# SEARCH NOT FOUND

@patch("builtins.input", return_value="unknown")
@patch("cli.requests.get")
def test_search_not_found(mock_get, mock_input, capsys):

    mock_get.return_value.status_code = 404
    mock_get.return_value.json.return_value = {
        "error": "No matching products found."
    }

    search_name()

    captured = capsys.readouterr()

    assert "No matching products found." in captured.out