from flask import Flask, jsonify, request

from data import inventory
from helpers import (
    fetch_product_by_barcode,
    fetch_product_by_name
)

app = Flask(__name__)


def next_id():
    if not inventory:
        return 1
    return max(item["id"] for item in inventory) + 1


@app.route("/")
def home():
    return {
        "message": "Inventory Management REST API"
    }

# GET ALL INVENTORY

@app.route("/inventory", methods=["GET"])
def get_inventory():
    return jsonify(inventory), 200

# GET SINGLE ITEM

@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_item(item_id):

    item = next(
        (i for i in inventory if i["id"] == item_id),
        None
    )

    if item is None:
        return jsonify({"error": "Item not found"}), 404

    return jsonify(item), 200

# CREATE ITEM

@app.route("/inventory", methods=["POST"])
def add_item():

    data = request.get_json()

    if not data:
        return jsonify({"error": "Missing JSON body"}), 400

    required = ["barcode", "price", "stock"]

    if not all(field in data for field in required):
        return jsonify({"error": "Missing required fields"}), 400

    product = fetch_product_by_barcode(data["barcode"])

    if product is None:
        return jsonify({
            "error": "Product not found on OpenFoodFacts"
        }), 404

    item = {
        "id": next_id(),
        "barcode": data["barcode"],
        "product_name": product["product_name"],
        "brand": product["brand"],
        "ingredients": product["ingredients"],
        "price": data["price"],
        "stock": data["stock"]
    }

    inventory.append(item)

    return jsonify(item), 201

# UPDATE ITEM

@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_item(item_id):

    item = next(
        (i for i in inventory if i["id"] == item_id),
        None
    )

    if item is None:
        return jsonify({"error": "Item not found"}), 404

    data = request.get_json()

    if not data:
        return jsonify({"error": "No data supplied"}), 400

    if "price" in data:
        item["price"] = data["price"]

    if "stock" in data:
        item["stock"] = data["stock"]

    return jsonify(item), 200

# DELETE ITEM

@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):

    item = next(
        (i for i in inventory if i["id"] == item_id),
        None
    )

    if item is None:
        return jsonify({"error": "Item not found"}), 404

    inventory.remove(item)

    return jsonify({
        "message": "Item deleted successfully"
    }), 200

# SEARCH BY BARCODE

@app.route("/search/barcode/<barcode>", methods=["GET"])
def search_barcode(barcode):

    product = fetch_product_by_barcode(barcode)

    if product is None:
        return jsonify({"error": "Product not found"}), 404

    return jsonify(product), 200

# SEARCH BY PRODUCT NAME

@app.route("/search/name", methods=["GET"])
def search_name():

    name = request.args.get("name")

    if not name:
        return jsonify({
            "error": "Missing product name"
        }), 400

    products = fetch_product_by_name(name)

    if not products:
        return jsonify({
            "error": "Product not found"
        }), 404

    return jsonify(products), 200


if __name__ == "__main__":
    app.run(debug=True)



