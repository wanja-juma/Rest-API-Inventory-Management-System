import json
import os

DATA_FILE = "inventory.json"


def load_inventory():
    
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r") as file:
        return json.load(file)


def save_inventory(inventory):
   
    with open(DATA_FILE, "w") as file:
        json.dump(inventory, file, indent=4)


inventory = load_inventory()