# Inventory Management System

## Overview

The Inventory Management System is a Flask-based REST API that enables administrators and employees to manage inventory items for an e-commerce application. The system supports creating, retrieving, updating, and deleting inventory records while integrating with the OpenFoodFacts API to retrieve real-time product information.

A command-line interface (CLI) is provided to allow users to interact with the API, and a comprehensive test suite validates the application's functionality.

---

## Features

* RESTful Flask API
* Create, Read, Update, and Delete (CRUD) inventory items
* Search products using the OpenFoodFacts API
* Search by barcode
* Search by product name
* CLI application for interacting with the API
* Simulated inventory database using a Python list
* Automatic inventory ID generation
* Error handling for invalid requests and API failures
* Unit testing with `pytest`
* Mocked external API testing using `unittest.mock`

---

## Technologies Used

* Python 3
* Flask
* Requests
* Pytest
* Pytest-Mock
* OpenFoodFacts API

---

## Project Structure

```text
inventory-management-system/
│
├── app.py
├── cli.py
├── config.py
├── data.py
├── helpers.py
├── requirements.txt
├── README.md
├── pytest.ini
│
└── tests/
    ├── conftest.py
    ├── test_api.py
    ├── test_cli.py
    └── test_openfoodfacts.py
```

---

## Installation

### Clone the repository

```bash
git clone git@github.com:wanja-juma/Rest-API-Inventory-Management-System.git
```

### Navigate into the project directory

```bash
cd rest-api-inventory-management-system
```

### Create a virtual environment (optional)

Using Pipenv:

```bash
pipenv install
pipenv shell
```

Or using `venv`:

```bash
python -m venv venv
```

Activate the virtual environment.

Linux/macOS:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Application

Start the Flask API:

```bash
python app.py
```

The server starts at:

```text
http://127.0.0.1:5000
```

---

## Running the CLI

Open another terminal window while the Flask server is running.

Run:

```bash
python cli.py
```

The CLI menu allows you to:

* View all inventory items
* View a single inventory item
* Add a new inventory item
* Update product price or stock
* Delete inventory items
* Search OpenFoodFacts by barcode
* Search OpenFoodFacts by product name

---

## REST API Endpoints

### Home

| Method | Endpoint | Description   |
| ------ | -------- | ------------- |
| GET    | `/`      | API home page |

### Inventory

| Method | Endpoint          | Description                      |
| ------ | ----------------- | -------------------------------- |
| GET    | `/inventory`      | Retrieve all inventory items     |
| GET    | `/inventory/<id>` | Retrieve a single inventory item |
| POST   | `/inventory`      | Add a new inventory item         |
| PATCH  | `/inventory/<id>` | Update an inventory item         |
| DELETE | `/inventory/<id>` | Delete an inventory item         |

### OpenFoodFacts Search

| Method | Endpoint                      | Description            |
| ------ | ----------------------------- | ---------------------- |
| GET    | `/search/barcode/<barcode>`   | Search by barcode      |
| GET    | `/search/name?name=<product>` | Search by product name |

---

## Example POST Request

```json
{
    "barcode": "737628064502",
    "price": 5.99,
    "stock": 30
}
```

Example Response

```json
{
    "id": 4,
    "barcode": "737628064502",
    "product_name": "Organic Almond Milk",
    "brand": "Silk",
    "ingredients": "Filtered water, almonds, cane sugar",
    "price": 5.99,
    "stock": 30
}
```

---

## OpenFoodFacts Integration

The application retrieves product information from the OpenFoodFacts API using:

* Barcode lookup
* Product name search

The following product information is imported into the inventory:

* Product name
* Brand
* Ingredients

Inventory-specific information such as price and stock is managed locally within the application.

---

## Running Tests

Run all tests:

```bash
pytest
```

Run with verbose output:

```bash
pytest -v
```

Run a specific test file:

```bash
pytest tests/test_api.py
```

---

## Error Handling

The application handles:

* Invalid product IDs
* Missing request data
* Invalid barcode searches
* External API failures
* Network connection errors
* Invalid CLI input

---

## Future Improvements

* Replace the simulated inventory array with a relational database (SQLite or PostgreSQL).
* Add user authentication and authorization.
* Implement inventory categories.
* Add pagination for large inventories.
* Build a web-based frontend for administrators.
* Containerize the application using Docker.

---

## Author

Developed as a Flask REST API project demonstrating:

* RESTful API design
* External API integration
* CLI development
* Unit testing
* Python application architecture