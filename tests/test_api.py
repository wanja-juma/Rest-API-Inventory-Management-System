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