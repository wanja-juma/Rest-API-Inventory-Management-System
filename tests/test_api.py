import pytest

from data import inventory

# HOME

def test_home(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.get_json()["message"] == "Inventory Management REST API"

# GET EMPTY INVENTORY

def test_get_empty_inventory(client):
    response = client.get("/inventory")

    assert response.status_code == 200
    assert response.get_json() == []

# ADD PRODUCT

def test_add_product(client):

    payload = {
        "product_name": "Milk",
        "brand": "Brookside",
        "ingredients": "Milk",
        "price": 65.0,
        "stock": 20
    }

    response = client.post(
        "/inventory",
        json=payload
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["id"] == 1
    assert data["product_name"] == "Milk"
    assert data["brand"] == "Brookside"
    assert data["price"] == 65.0
    assert data["stock"] == 20

# GET INVENTORY

def test_get_inventory(client):

    inventory.append({
        "id": 1,
        "product_name": "Milk",
        "brand": "Brookside",
        "ingredients": "Milk",
        "price": 65.0,
        "stock": 20
    })

    response = client.get("/inventory")

    assert response.status_code == 200

    data = response.get_json()

    assert len(data) == 1
    assert data[0]["product_name"] == "Milk"

# GET SINGLE PRODUCT

def test_get_single_product(client):

    inventory.append({
        "id": 1,
        "product_name": "Milk",
        "brand": "Brookside",
        "ingredients": "Milk",
        "price": 65.0,
        "stock": 20
    })

    response = client.get("/inventory/1")

    assert response.status_code == 200

    data = response.get_json()

    assert data["product_name"] == "Milk"

# PRODUCT NOT FOUND


def test_get_missing_product(client):

    response = client.get("/inventory/100")

    assert response.status_code == 404
    assert response.get_json()["error"] == "Product not found"

# UPDATE PRODUCT


def test_update_product(client):

    inventory.append({
        "id": 1,
        "product_name": "Milk",
        "brand": "Brookside",
        "ingredients": "Milk",
        "price": 65.0,
        "stock": 20
    })

    response = client.patch(
        "/inventory/1",
        json={
            "price": 80.0,
            "stock": 35
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["price"] == 80.0
    assert data["stock"] == 35

# DELETE PRODUCT


def test_delete_product(client):

    inventory.append({
        "id": 1,
        "product_name": "Milk",
        "brand": "Brookside",
        "ingredients": "Milk",
        "price": 65.0,
        "stock": 20
    })

    response = client.delete("/inventory/1")

    assert response.status_code == 200

    assert response.get_json()["message"] == (
        "Product deleted successfully"
    )

    assert len(inventory) == 0

# DELETE MISSING PRODUCT


def test_delete_missing_product(client):

    response = client.delete("/inventory/99")

    assert response.status_code == 404
    assert response.get_json()["error"] == "Product not found"


# SEARCH OPENFOODFACTS

def test_search_name(client, monkeypatch):

    def mock_fetch_product_by_name(name):
        return [
            {
                "product_name": "Milk",
                "brand": "Brookside",
                "ingredients": "Milk",
                "barcode": "123456789"
            }
        ]

    monkeypatch.setattr(
        "app.fetch_product_by_name",
        mock_fetch_product_by_name
    )

    response = client.get(
        "/search/name?name=milk"
    )

    assert response.status_code == 200

    data = response.get_json()

    assert len(data) == 1
    assert data[0]["product_name"] == "Milk"

# SEARCH WITH NO RESULTS

def test_search_name_not_found(client, monkeypatch):

    def mock_fetch_product_by_name(name):
        return []

    monkeypatch.setattr(
        "app.fetch_product_by_name",
        mock_fetch_product_by_name
    )

    response = client.get(
        "/search/name?name=unknown"
    )

    assert response.status_code == 404

    assert response.get_json()["error"] == (
        "No matching products found."
    )