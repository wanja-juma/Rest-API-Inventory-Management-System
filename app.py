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