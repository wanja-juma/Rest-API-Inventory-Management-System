import requests

from config import OPENFOODFACTS_URL


def fetch_product_by_name(name):
    """
    Search OpenFoodFacts for products matching the given name.
    Returns a list of matching products.
    """

    params = {
        "search_terms": name,
        "search_simple": 1,
        "action": "process",
        "json": 1
    }

    try:
        response = requests.get(
            OPENFOODFACTS_URL,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        products = data.get("products", [])

        results = []

        for product in products[:10]:
            results.append({
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
                ),
                "barcode": product.get(
                    "code",
                    "Unknown"
                )
            })

        return results

    except requests.RequestException:
        return []