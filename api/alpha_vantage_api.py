import requests
import tempfile
import helper.utils  # assuming utils.read_csv exists and is accessible
import pandas as pd
from api.base_trading_api import BaseTradingApi


class AlphaVantageAPI(BaseTradingApi):
    """
    Adapter that interacts with the Alpha Vantage API.
    Currently, it supports retrieving historical trading data.
    Other trading operations (buy/sell orders, chart generation) are not implemented.
    """

    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_historic_data(self, asset_name: str) -> pd.DataFrame:
        # Build the remote CSV URL using the Alpha Vantage API.
        url = (
            "https://www.alphavantage.co/query?"
            "function=TIME_SERIES_DAILY&symbol={asset}USD&apikey={apikey}&outputsize=compact&datatype=csv"
        ).format(asset=asset_name, apikey=self.api_key)

        try:
            # Download the CSV data.
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors.
            csv_data = response.text

            # Write CSV data to a temporary file.
            with tempfile.NamedTemporaryFile(
                mode="w+", delete=False, suffix=".csv"
            ) as tmp_file:
                tmp_file.write(csv_data)
                tmp_file.flush()  # Ensure data is written to disk.
                temp_file_path = tmp_file.name

            # Use the utility to read the CSV data.
            success, result = helper.utils.read_csv(
                temp_file_path, date_parsing=["timestamp"]
            )
            if not success:
                raise ValueError(f"Failed to load CSV file: {result}")

            # Reverse the order as needed (oldest first).
            result_reversed = result.iloc[::-1].reset_index(drop=True)
            return result_reversed

        except Exception as e:
            raise RuntimeError(f"Error retrieving historical data: {str(e)}")

    def buy_order(self, asset_name: str, amount: float) -> dict:
        raise NotImplementedError(
            "Buy order functionality is not implemented in AlphaVantageAPI."
        )

    def sell_order(self, asset_name: str, amount: float) -> dict:
        raise NotImplementedError(
            "Sell order functionality is not implemented in AlphaVantageAPI."
        )

    def fetch_asset_balance_and_value(self, asset: str) -> tuple:
        raise NotImplementedError(
            "Fetch asset info functionality is not implemented in AlphaVantageAPI."
        )
