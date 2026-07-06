import requests

BASE_URL = "http://127.0.0.1:5000"


def display_menu():
    print("\n" + "=" * 50)
    print(" Inventory Management System ")
    print("=" * 50)
    print("1. View Inventory")
    print("2. View Product")
    print("3. Add Product")
    print("4. Update Product")
    print("5. Delete Product")
    print("6. Search OpenFoodFacts by Barcode")
    print("7. Search OpenFoodFacts by Name")
    print("8. Exit")


def view_inventory():
    try:
        response = requests.get(f"{BASE_URL}/inventory")

        if response.status_code == 200:
            items = response.json()

            if not items:
                print("\nInventory is empty.")
                return

            print("\nCurrent Inventory")
            print("-" * 70)

            for item in items:
                print(
                    f"ID: {item['id']}"
                    f"\nProduct: {item['product_name']}"
                    f"\nBrand: {item['brand']}"
                    f"\nPrice: ${item['price']}"
                    f"\nStock: {item['stock']}"
                    f"\nBarcode: {item['barcode']}"
                )
                print("-" * 70)

        else:
            print("Unable to retrieve inventory.")

    except requests.ConnectionError:
        print("Cannot connect to Flask server.")

def view_product():
    product_id = input("Enter product ID: ")

    try:
        response = requests.get(
            f"{BASE_URL}/inventory/{product_id}"
        )

        if response.status_code == 200:
            item = response.json()

            print("\nProduct Details")
            print("-" * 40)

            for key, value in item.items():
                print(f"{key}: {value}")

        else:
            print(response.json()["error"])

    except requests.ConnectionError:
        print("Server unavailable.")
    

def add_product():
    barcode = input("Barcode: ")

    try:
        price = float(input("Price: "))
        stock = int(input("Stock: "))
    except ValueError:
        print("Invalid number entered.")
        return

    payload = {
        "barcode": barcode,
        "price": price,
        "stock": stock
    }

    try:
        response = requests.post(
            f"{BASE_URL}/inventory",
            json=payload
        )

        if response.status_code == 201:
            print("\nProduct successfully added.")
            print(response.json())

        else:
            print(response.json()["error"])

    except requests.ConnectionError:
        print("Cannot connect to server.")

def update_product():
    product_id = input("Product ID: ")

    update_data = {}

    price = input("New price (leave blank to skip): ")

    if price:
        try:
            update_data["price"] = float(price)
        except ValueError:
            print("Invalid price.")
            return

    stock = input("New stock (leave blank to skip): ")

    if stock:
        try:
            update_data["stock"] = int(stock)
        except ValueError:
            print("Invalid stock.")
            return

    if not update_data:
        print("Nothing to update.")
        return

    try:
        response = requests.patch(
            f"{BASE_URL}/inventory/{product_id}",
            json=update_data
        )

        if response.status_code == 200:
            print("Product updated successfully.")
            print(response.json())

        else:
            print(response.json()["error"])

    except requests.ConnectionError:
        print("Cannot connect to server.")