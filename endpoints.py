import requests

API_URL = "http://127.0.0.1:5000/products"


def update_inventory(item_code, item_name, quantity):
    response = requests.get(f"{API_URL}/{item_code}")

    print(response.status_code)
