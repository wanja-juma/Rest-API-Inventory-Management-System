import requests

BASE_URL = "http://127.0.0.1:5000"


def display_menu():
    print("=== Inventory Management System ===")
    print("1. View Inventory")
    print("2. View Product")
    print("3. Add Product")
    print("4. Update Product")
    print("5. Delete Product")
    print("6. Search OpenFoodFacts")
    print("7. Exit")


# View all products

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
                print(f"ID: {item['id']}")
                print(f"Product: {item['product_name']}")
                print(f"Brand: {item['brand']}")
                print(f"Price: Ksh.{item['price']}")
                print(f"Stock: {item['stock']}")
                print("-" * 70)

        else:
            print("Unable to retrieve inventory.")

    except requests.ConnectionError:
        print("Cannot connect to Flask server.")

# View single product

def view_product():

    product_id = input("Enter Product ID: ")

    try:
        response = requests.get(
            f"{BASE_URL}/inventory/{product_id}"
        )

        if response.status_code == 200:

            product = response.json()

            print("\nProduct Details")
            print("-" * 50)

            for key, value in product.items():
                print(f"{key}: {value}")

        else:
            print(response.json()["error"])

    except requests.ConnectionError:
        print("Cannot connect to Flask server.")

# Add product


def add_product():

    product_name = input("Product Name: ")
    brand = input("Brand: ")
    ingredients = input("Ingredients: ")

    try:
        price = float(input("Price: "))
        stock = int(input("Stock: "))

    except ValueError:
        print("Invalid number entered.")
        return

    payload = {
        "product_name": product_name,
        "brand": brand,
        "ingredients": ingredients,
        "price": price,
        "stock": stock
    }

    try:
        response = requests.post(
            f"{BASE_URL}/inventory",
            json=payload
        )

        if response.status_code == 201:

            print("\nProduct added successfully.")
            print(response.json())

        else:
            print(response.json()["error"])

    except requests.ConnectionError:
        print("Cannot connect to Flask server.")

# Update product

def update_product():

    product_id = input("Product ID: ")

    update_data = {}

    product_name = input(
        "New Product Name (leave blank to skip): "
    )

    if product_name:
        update_data["product_name"] = product_name

    brand = input(
        "New Brand (leave blank to skip): "
    )

    if brand:
        update_data["brand"] = brand

    ingredients = input(
        "New Ingredients (leave blank to skip): "
    )

    if ingredients:
        update_data["ingredients"] = ingredients

    price = input(
        "New Price (leave blank to skip): "
    )

    if price:
        try:
            update_data["price"] = float(price)
        except ValueError:
            print("Invalid price.")
            return

    stock = input(
        "New Stock (leave blank to skip): "
    )

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

            print("\nProduct updated successfully.")
            print(response.json())

        else:
            print(response.json()["error"])

    except requests.ConnectionError:
        print("Cannot connect to Flask server.")


# Delete product


def delete_product():

    product_id = input("Enter Product ID: ")

    try:

        response = requests.delete(
            f"{BASE_URL}/inventory/{product_id}"
        )

        if response.status_code == 200:

            print(response.json()["message"])

        else:

            print(response.json()["error"])

    except requests.ConnectionError:
        print("Cannot connect to Flask server.")

# Search openfoodfacts


def search_name():

    name = input("Enter Product Name: ")

    try:

        response = requests.get(
            f"{BASE_URL}/search/name",
            params={"name": name}
        )

        if response.status_code == 200:

            products = response.json()

            print("\nProducts Found")
            print("-" * 70)

            for product in products:

                print(
                    f"Name: {product['product_name']}"
                )
                print(
                    f"Brand: {product['brand']}"
                )
                print(
                    f"Ingredients: {product['ingredients']}"
                )
                print(
                    f"Barcode: {product['barcode']}"
                )

                print("-" * 70)

        else:

            print(response.json()["error"])

    except requests.ConnectionError:
        print("Cannot connect to Flask server.")


# Main menu


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
            search_name()

        elif choice == "7":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
