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


def delete_product():
    product_id = input("Enter product ID: ")

    try:
        response = requests.delete(
            f"{BASE_URL}/inventory/{product_id}"
        )

        if response.status_code == 200:
            print(response.json()["message"])
        else:
            print(response.json()["error"])

    except requests.ConnectionError:
        print("Server unavailable.")


def search_barcode():
    barcode = input("Barcode: ")

    try:
        response = requests.get(
            f"{BASE_URL}/search/barcode/{barcode}"
        )

        if response.status_code == 200:
            product = response.json()

            print("\nProduct Found")
            print("-" * 50)

            for key, value in product.items():
                print(f"{key}: {value}")

        else:
            print(response.json()["error"])

    except requests.ConnectionError:
        print("Cannot connect to server.")


def search_name():
    name = input("Product name: ")

    try:
        response = requests.get(
            f"{BASE_URL}/search/name",
            params={"name": name}
        )

        if response.status_code == 200:
            products = response.json()

            if not products:
                print("No products found.")
                return

            print(f"\nFound {len(products)} products\n")

            for product in products[:5]:
                print("-" * 60)
                print(
                    f"Name: {product.get('product_name', 'Unknown')}"
                )
                print(
                    f"Brand: {product.get('brands', 'Unknown')}"
                )
                print(
                    f"Barcode: {product.get('code', 'N/A')}"
                )

        else:
            print(response.json()["error"])

    except requests.ConnectionError:
        print("Server unavailable.")


def main():
    while True:
        display_menu()

        choice = input("\nChoose an option: ")

        if choice == "1":
            view_inventory()

        elif choice == "2":
            view_product()

        elif choice == "3":
            add_product()

        elif choice == "4":
            update_product()

        elif choice == "5":
            delete_product()

        elif choice == "6":
            search_barcode()

        elif choice == "7":
            search_name()

        elif choice == "8":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
