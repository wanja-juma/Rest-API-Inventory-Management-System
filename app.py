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