import requests
from requests.exceptions import RequestException
import hmac
import json
import hashlib
from urllib.parse import urlencode
from decimal import Decimal, ROUND_DOWN
import pandas  # Now importing pandas at the top, without alias

from api.base_trading_api import (
    BaseTradingApi,
)  # Ensure this exists in your project


class BinanceAPI(BaseTradingApi):
    """
    Adapter that interacts with the Binance API.
    Supports retrieving historical trading data, placing market sell and buy orders,
    and checking account balances.
    """

    BASE_URL = "https://api.binance.com"

    def __init__(self, api_key: str, api_secret: str):
        """
        Initialize with your Binance API key and secret.
        """
        self.api_key = api_key
        self.api_secret = api_secret

    def _get_server_time(self) -> int:
        """
        Fetch the server time from Binance.

        Returns:
            int: The server time in milliseconds.
        """
        endpoint = "/api/v3/time"
        url = self.BASE_URL + endpoint
        response = requests.get(url)
        response.raise_for_status()
        return response.json()["serverTime"]

    def _get_symbol_filters(self, symbol: str) -> dict:
        """
        Retrieve the filters for the given symbol from the exchangeInfo endpoint.

        Args:
            symbol (str): The trading pair (e.g., "BTCUSDT").

        Returns:
            dict: A dictionary mapping filter types (e.g., "LOT_SIZE", "MIN_NOTIONAL")
                  to their respective filter data.
        """
        url = self.BASE_URL + "/api/v3/exchangeInfo"
        params = {"symbol": symbol}
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        filters = {}
        if "symbols" in data and len(data["symbols"]) > 0:
            for f in data["symbols"][0]["filters"]:
                filters[f["filterType"]] = f
            return filters
        else:
            raise RuntimeError("Symbol information not found for " + symbol)

    def _sign_params(self, params: dict) -> dict:
        """
        Sign the given parameters using HMAC-SHA256 and append the signature.

        Args:
            params (dict): The parameters to sign.

        Returns:
            dict: The parameters with the appended 'signature'.
        """
        query_string = urlencode(params)
        signature = hmac.new(
            self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        params["signature"] = signature
        return params

    def get_historic_data(
        self, coin_name: str, interval: str = "1d"
    ) -> pandas.DataFrame:
        """
        Retrieve historical trading data (candlesticks) for the given coin.

        Args:
            coin_name (str): The coin symbol (e.g., "BTC").
            interval (str, optional): The candlestick interval. For example:
                                      "1d" for daily data (default) or "4h" for 4-hour data.

        Returns:
            pandas.DataFrame: A DataFrame containing the historical data.
        """
        symbol = coin_name.upper() + "USDT"
        endpoint = "/api/v3/klines"
        params = {
            "symbol": symbol,
            "interval": interval,  # Use the method parameter here
            "limit": 500,  # Adjust the limit as necessary.
        }
        url = self.BASE_URL + endpoint

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
        except RequestException as e:
            print(f"Error fetching historical data: {e}")
            return pandas.DataFrame()  # Return an empty DataFrame

        if not data:
            raise ValueError("No data returned from Binance API.")

        columns = [
            "timestamp",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "close_time",
            "quote_asset_volume",
            "number_of_trades",
            "taker_buy_base_asset_volume",
            "taker_buy_quote_asset_volume",
            "ignore",
        ]
        df = pandas.DataFrame(data, columns=columns)
        df = df[["timestamp", "open", "high", "low", "close", "volume"]]
        df["timestamp"] = pandas.to_datetime(df["timestamp"], unit="ms")
        df["open"] = df["open"].astype(float)
        df["high"] = df["high"].astype(float)
        df["low"] = df["low"].astype(float)
        df["close"] = df["close"].astype(float)
        df["volume"] = df["volume"].astype(float)
        return df

    def sell_order(self, coin_name: str, usdt_amount: float) -> dict:
        """
        Place a market sell order for an asset so that it sells approximately
        'usdt_amount' worth of the asset.

        The method calculates the asset quantity from the USDT amount using the current
        price and adjusts it according to the LOT_SIZE (and MIN_NOTIONAL) filters.

        Args:
            coin_name (str): The asset symbol (e.g., "BTC").
            usdt_amount (float): The USDT amount you want to sell.

        Returns:
            dict: The JSON response from Binance containing order details.
        """
        symbol = coin_name.upper() + "USDT"

        # 1. Fetch current price.
        price_endpoint = "/api/v3/ticker/price"
        price_url = self.BASE_URL + price_endpoint
        params_price = {"symbol": symbol}

        try:
            price_response = requests.get(price_url, params=params_price)
            price_response.raise_for_status()
            current_price = float(price_response.json()["price"])
        except RequestException as e:
            return {
                "status": "error",
                "message": f"Sell order could not be requested: {e}",
            }

        # 2. Compute raw quantity.
        raw_quantity = usdt_amount / current_price

        # 3. Adjust quantity to comply with LOT_SIZE.
        filters = self._get_symbol_filters(symbol)
        lot_filter = filters.get("LOT_SIZE")
        if not lot_filter:
            raise RuntimeError("LOT_SIZE filter not found for symbol " + symbol)
        min_qty = Decimal(lot_filter["minQty"])
        step_size = Decimal(lot_filter["stepSize"])

        quantity_dec = Decimal(str(raw_quantity))
        steps = (quantity_dec / step_size).quantize(Decimal("1"), rounding=ROUND_DOWN)
        adjusted_quantity = steps * step_size

        if adjusted_quantity < min_qty:
            return {
                "status": "error",
                "message": f"Adjusted quantity {adjusted_quantity} is below the minimum allowed {min_qty}.",
            }
        # 4. Validate order notional with MIN_NOTIONAL.
        notional_filter = filters.get("NOTIONAL")
        if not notional_filter:
            min_notional = Decimal("10")  # Default if not provided.
        else:
            min_notional = Decimal(notional_filter["minNotional"])

        order_notional = adjusted_quantity * Decimal(str(current_price))
        if order_notional < min_notional:
            return {
                "status": "error",
                "message": f"Order notional {order_notional} is below the minimum notional requirement of"
                "{min_notional}. Increase the USDT amount.",
            }

        quantity = float(adjusted_quantity)
        server_time = self._get_server_time()

        # 5. Place the market sell order.
        endpoint = "/api/v3/order"
        url = self.BASE_URL + endpoint
        params = {
            "symbol": symbol,
            "side": "SELL",
            "type": "MARKET",
            "quantity": quantity,
            "timestamp": server_time,
            "recvWindow": 10000,
        }
        signed_params = self._sign_params(params)
        headers = {"X-MBX-APIKEY": self.api_key}
        response = requests.post(url, params=signed_params, headers=headers)
        if response.status_code != 200:
            return {"status": "error", "message": json.loads(response.text)["msg"]}
        response.raise_for_status()
        return response.json()

    def buy_order(self, coin_name: str, usdt_amount: float) -> dict:
        """
        Place a market buy order for an asset so that it uses approximately
        'usdt_amount' USDT to purchase the asset.

        This method calculates the base asset quantity from the USDT amount using the current
        price and adjusts it according to the LOT_SIZE (and MIN_NOTIONAL) filters.
        (Note: Binance supports "quoteOrderQty" for market buys, but this method mimics the
         sell_order approach by calculating the quantity.)

        Args:
            coin_name (str): The asset symbol (e.g., "AST").
            usdt_amount (float): The USDT amount you want to spend.

        Returns:
            dict: The JSON response from Binance containing order details.
        """
        # return True
        symbol = coin_name.upper() + "USDT"

        # 1. Fetch current price.
        price_endpoint = "/api/v3/ticker/price"
        price_url = self.BASE_URL + price_endpoint
        params_price = {"symbol": symbol}

        try:
            price_response = requests.get(price_url, params=params_price)
            price_response.raise_for_status()
            current_price = float(price_response.json()["price"])
        except RequestException as e:
            return {
                "status": "error",
                "message": f"Buy order could not be requested: {e}",
            }

        # 2. Compute raw quantity.
        raw_quantity = usdt_amount / current_price

        # 3. Adjust quantity to comply with LOT_SIZE.
        filters = self._get_symbol_filters(symbol)
        lot_filter = filters.get("LOT_SIZE")
        if not lot_filter:
            raise RuntimeError("LOT_SIZE filter not found for symbol " + symbol)
        min_qty = Decimal(lot_filter["minQty"])
        step_size = Decimal(lot_filter["stepSize"])

        quantity_dec = Decimal(str(raw_quantity))
        steps = (quantity_dec / step_size).quantize(Decimal("1"), rounding=ROUND_DOWN)
        adjusted_quantity = steps * step_size

        if adjusted_quantity < min_qty:
            return {
                "status": "error",
                "message": f"Adjusted quantity {adjusted_quantity} is below the minimum allowed {min_qty}.",
            }

        # 4. Validate order notional with MIN_NOTIONAL.
        notional_filter = filters.get("NOTIONAL")
        if not notional_filter:
            min_notional = Decimal("10")  # Default if not provided.
        else:
            min_notional = Decimal(notional_filter["minNotional"])

        # Optionally override MIN_NOTIONAL for specific symbols (example for AST).
        if coin_name.upper() == "AST":
            min_notional = Decimal("5")

        order_notional = adjusted_quantity * Decimal(str(current_price))
        if order_notional < min_notional:
            return {
                "status": "error",
                "message": f"Order notional {order_notional} is below the minimum notional requirement of"
                "{min_notional}. Increase the USDT amount.",
            }

        quantity = float(adjusted_quantity)
        server_time = self._get_server_time()

        # 5. Place the market buy order.
        endpoint = "/api/v3/order"
        url = self.BASE_URL + endpoint
        params = {
            "symbol": symbol,
            "side": "BUY",
            "type": "MARKET",
            "quantity": quantity,
            "timestamp": server_time,
            "recvWindow": 10000,
        }
        signed_params = self._sign_params(params)
        headers = {"X-MBX-APIKEY": self.api_key}
        response = requests.post(url, params=signed_params, headers=headers)
        if response.status_code != 200:
            return {"status": "error", "message": json.loads(response.text)["msg"]}
        response.raise_for_status()
        return response.json()

    def fetch_asset_balance_and_value(self, asset: str) -> tuple:
        """
        Retrieve the total available (free) quantity for the given asset,
        and also return its total worth in USDT.

        Args:
            asset (str): The asset symbol (e.g., "BTC", "USDT").

        Returns:
            tuple: (quantity as float, total worth in USDT as float)
                   Returns (0.0, 0.0) if the asset is not found.
        """
        endpoint = "/api/v3/account"
        url = self.BASE_URL + endpoint
        server_time = self._get_server_time()
        params = {"timestamp": server_time, "recvWindow": 10000}
        signed_params = self._sign_params(params)
        headers = {"X-MBX-APIKEY": self.api_key}
        response = requests.get(url, params=signed_params, headers=headers)
        response.raise_for_status()

        account_info = response.json()
        balances = account_info.get("balances", [])
        asset = asset.upper()
        quantity = 0.0
        for bal in balances:
            if bal["asset"] == asset:
                quantity = float(bal["free"])
                break

        if asset == "USDT":
            return quantity, quantity

        symbol = asset + "USDT"
        price_endpoint = "/api/v3/ticker/price"
        price_url = self.BASE_URL + price_endpoint
        params_price = {"symbol": symbol}
        try:
            price_response = requests.get(price_url, params=params_price)
            price_response.raise_for_status()
            current_price = float(price_response.json()["price"])
            total_worth = quantity * current_price
        except Exception:
            total_worth = 0.0

        return quantity, total_worth
