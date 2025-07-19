import json
import pandas
from typing import List, Optional
from PyQt6.QtWidgets import QFileDialog
from api.binance_api import BinanceAPI
from model.order_factory import create_order
from model.abstract_order import AbstractOrder


def read_csv(file_path, date_parsing=None):
    """
    Load CSV data from the given file_path.
    Returns a tuple (success, result): on success, result is the DataFrame; on failure, an error message.
    """
    try:
        data = pandas.read_csv(file_path, parse_dates=date_parsing)
        return True, data
    except Exception as e:
        return False, str(e)


def load_file(parent_widget):
    """
    Prompts a file dialog to load a CSV file.
    Returns (file_path, DataFrame) if successful, otherwise (None, None).
    """
    file_path, _ = QFileDialog.getOpenFileName(
        parent_widget, "Open CSV File", "", "CSV files (*.csv)"
    )
    if file_path:
        df = pandas.read_csv(file_path)
        return file_path, df
    return None, None


def read_history(file_path="config/history.json"):
    """
    Reads the history from the given JSON file.
    Returns a list of history dictionaries.
    """
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
        return data.get("transactions", [])
    except Exception as e:
        print(f"Error reading history from {file_path}: {e}")
        return []


def write_history(history, file_path="config/history.json"):
    """
    Writes the history (a list of transaction history) to the given JSON file.
    """
    try:
        with open(file_path, "w") as f:
            json.dump({"transactions": history}, f, indent=4)
    except Exception as e:
        print(f"Error writing history to {file_path}: {e}")


def get_binance_api_credentials(file_path: str = "config/config.json") -> dict:
    """
    Reads the JSON config file and extracts the API credentials for Binance.

    :param file_path: Path to the configuration file.
    :return: A dictionary containing 'name' and 'api_key' if Binance is found, otherwise an empty dictionary.
    """
    try:
        with open(file_path, "r") as f:
            data = json.load(f)

        # Ensure 'endpoints' exists and is a list
        endpoints = data.get("endpoints", [])

        # Find the Binance endpoint
        for endpoint in endpoints:
            if endpoint.get("name").lower() == "binance":
                return {
                    "api_key": endpoint.get("api_key"),
                    "api_secret": endpoint.get("api_secret"),
                }

        # If Binance is not found, return an empty dict
        return {}

    except Exception as e:
        print(f"Error reading config file: {e}")
        return {}


def read_orders(file_path: str = "config/orders.json") -> List[AbstractOrder]:
    """
    Reads the orders from the given JSON file and returns a list of Order objects.
    """
    try:
        with open(file_path, "r") as f:
            data = json.load(f)

        orders: List[AbstractOrder] = []
        for order_data in data.get("orders", []):
            # Select the appropriate adapter based on the platform
            adapter = None
            if order_data.get("platform").lower() == "binance":
                binance_credentials = get_binance_api_credentials()
                adapter = BinanceAPI(
                    binance_credentials.get("api_key"),
                    binance_credentials.get("api_secret"),
                )

            order = create_order(order_data)
            order.adapter = adapter
            orders.append(order)

        return orders
    except Exception as e:
        print(f"Error reading orders from {file_path}: {e}")
        return []


def write_orders(orders, file_path="config/orders.json"):
    """
    Writes the orders (a list of Order dataclass instances) to the given JSON file,
    excluding the 'adapter' field.
    """
    try:
        orders_dict = [order.to_dict() for order in orders]

        with open(file_path, "w") as f:
            json.dump({"orders": orders_dict}, f, indent=4)
    except Exception as e:
        print(f"Error writing orders to {file_path}: {e}")


def get_order(order_id: int, file_path: str = "config/orders.json") -> Optional[AbstractOrder]:
    """
    Retrieves the order with the given ID from the JSON file.
    """
    try:
        with open(file_path, "r") as f:
            data = json.load(f)

        for order_data in data.get("orders", []):
            if order_data.get("id") == order_id:
                adapter = None
                if order_data.get("platform").lower() == "binance":
                    binance_credentials = get_binance_api_credentials()
                    adapter = BinanceAPI(
                        binance_credentials.get("api_key"),
                        binance_credentials.get("api_secret"),
                    )

                order = create_order(order_data)
                order.adapter = adapter
                return order

        return None
    except Exception as e:
        print(f"Error retrieving order with ID {order_id} from {file_path}: {e}")
        return None
