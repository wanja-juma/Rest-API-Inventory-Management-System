
from flask import Flask, jsonify, request

from data import inventory


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