
import requests

from config import (
    OPENFOODFACTS_BARCODE_URL,
    OPENFOODFACTS_NAME_URL
)


def fetch_product_by_barcode(barcode):
    
    url = OPENFOODFACTS_BARCODE_URL.format(barcode)

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()

        if data.get("status") != 1:
            return None

        product = data.get("product", {})

        return {
            "product_name": product.get("product_name", "Unknown"),
            "brand": product.get("brands", "Unknown"),
            "ingredients": product.get(
                "ingredients_text",
                "Not Available"
            )
        }

    except requests.RequestException:
        return None


def fetch_product_by_name(name):
    
    params = {
        "search_terms": name,
        "search_simple": 1,
        "action": "process",
        "json": 1
    }

    try:

        response = requests.get(
            OPENFOODFACTS_NAME_URL,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        return data.get("products", [])

    except requests.RequestException:

        return []