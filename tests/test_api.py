from unittest.mock import patch

# GET ALL INVENTORY

def test_get_inventory(client):

    response = client.get("/inventory")

    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

# GET SINGLE ITEM

def test_get_single_item(client):

    response = client.get("/inventory/1")

    assert response.status_code == 200

    product = response.get_json()

    assert product["id"] == 1
    assert product["product_name"] == "Nutella"

# GET INVALID ITEM

def test_invalid_item(client):

    response = client.get("/inventory/999")

    assert response.status_code == 404
    assert response.get_json()["error"] == "Item not found"

# POST

@patch("app.fetch_product_by_barcode")
def test_add_item(mock_api, client):

    mock_api.return_value = {
        "product_name": "Fanta",
        "brand": "Coca Cola",
        "ingredients": "Water, Sugar"
    }

    response = client.post(
        "/inventory",
        json={
            "barcode": "987654321",
            "price": 4.99,
            "stock": 40
        }
    )

    assert response.status_code == 201

    product = response.get_json()

    assert product["product_name"] == "Fanta"
    assert product["price"] == 4.99
    assert product["stock"] == 40

# POST MISSING FIELDS

def test_post_missing_fields(client):

    response = client.post(
        "/inventory",
        json={
            "barcode": "11111"
        }
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == "Missing required fields"


# PATCH

def test_patch_item(client):

    response = client.patch(
        "/inventory/1",
        json={
            "price": 10.50,
            "stock": 99
        }
    )

    assert response.status_code == 200

    product = response.get_json()

    assert product["price"] == 10.50
    assert product["stock"] == 99

# PATCH INVALID ITEM

def test_patch_invalid_item(client):

    response = client.patch(
        "/inventory/999",
        json={
            "price": 10
        }
    )

    assert response.status_code == 404
    assert response.get_json()["error"] == "Item not found"