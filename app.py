from flask import Flask, jsonify, request

from data import inventory
from helpers import fetch_product_by_name

app = Flask(__name__)


def next_id():
    if not inventory:
        return 1

    return max(item["id"] for item in inventory) + 1


@app.route("/")
def home():
    return jsonify({
        "message": "Inventory Management REST API"
    })

# View all products

@app.route("/inventory", methods=["GET"])
def get_inventory():
    print("Current inventory:", inventory)
    return jsonify(inventory), 200

# View product

@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_item(item_id):

    item = next(
        (product for product in inventory if product["id"] == item_id),
        None
    )

    if item is None:
        return jsonify({
            "error": "Product not found"
        }), 404

    return jsonify(item), 200

# Add product

@app.route("/inventory", methods=["POST"])
def add_item():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Missing JSON body"
        }), 400

    required = [
        "product_name",
        "brand",
        "price",
        "stock"
    ]

    if not all(field in data for field in required):
        return jsonify({
            "error": "Missing required fields"
        }), 400

    item = {
        "id": next_id(),
        "product_name": data["product_name"],
        "brand": data["brand"],
        "price": data["price"],
        "stock": data["stock"]
    }

    inventory.append(item)

    print(inventory)

    return jsonify(item), 201

# Update product

@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_item(item_id):

    item = next(
        (product for product in inventory if product["id"] == item_id),
        None
    )

    if item is None:
        return jsonify({
            "error": "Product not found"
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "No data supplied"
        }), 400

    if "product_name" in data:
        item["product_name"] = data["product_name"]

    if "brand" in data:
        item["brand"] = data["brand"]

    if "ingredients" in data:
        item["ingredients"] = data["ingredients"]

    if "price" in data:
        item["price"] = data["price"]

    if "stock" in data:
        item["stock"] = data["stock"]

    return jsonify(item), 200

# Delete product

@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):

    item = next(
        (product for product in inventory if product["id"] == item_id),
        None
    )

    if item is None:
        return jsonify({
            "error": "Product not found"
        }), 404

    inventory.remove(item)

    return jsonify({
        "message": "Product deleted successfully"
    }), 200

# Search openfoodfacts

@app.route("/search/name", methods=["GET"])
def search_name():

    name = request.args.get("name")

    if not name:
        return jsonify({
            "error": "Please provide a product name."
        }), 400

    products = fetch_product_by_name(name)

    if not products:
        return jsonify({
            "error": "No matching products found."
        }), 404

    return jsonify(products), 200


if __name__ == "__main__":
    app.run(debug=True)


