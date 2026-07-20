import requests

from config import OPENFOODFACTS_URL


def fetch_product_by_name(name, page_size=50):

    params = {
        "search_terms": name,
        "search_simple": 1,
        "action": "process",
        "json": 1,
        "page": 1,
        "page_size": page_size
    }

    headers = {
        "User-Agent": (
        "InventoryManagementSystem/1.0 "
        "(Educational Project; Python Requests)"
    )
    }

    try:

        response = requests.get(
            OPENFOODFACTS_URL,
            params=params,
            headers=headers,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        return [
            {
                "product_name": product.get(
                    "product_name",
                    "Unknown"
                ),
                "brand": product.get(
                    "brands",
                    "Unknown"
                ),
                "ingredients": product.get(
                    "ingredients_text",
                    "Not Available"
                )
            }
            for product in data.get("products", [])
        ]

    except requests.RequestException:
        return []