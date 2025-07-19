import abc
import pandas


class BaseTradingApi(abc.ABC):
    """
    Interface for trading operations in the application.
    Implementations should provide methods for retrieving historical data,
    placing orders, and obtaining visualizations.
    """

    @abc.abstractmethod
    def get_historic_data(self, asset_name: str, interval: str) -> pandas.DataFrame:
        """
        Retrieve historical trading data for the given asset.

        Args:
            asset_name (str): The altasset name.

        Returns:
            pandas.DataFrame: A DataFrame containing the historical trading data.
        """
        pass

    @abc.abstractmethod
    def buy_order(self, asset_name: str, amount: float) -> bool:
        """
        Place a buy order for the specified asset and amount.

        Args:
            asset_name (str): The altasset name.
            amount (float): The amount (USDT) to buy.

        Returns:
            Any: Information regarding the placed order.
        """
        pass

    @abc.abstractmethod
    def sell_order(self, asset_name: str, amount: float) -> bool:
        """
        Place a sell order for the specified asset and amount.

        Args:
            asset_name (str): The altasset name.
            amount (float): The amount (USDT) to sell.

        Returns:
            Any: Information regarding the placed order.
        """
        pass

    @abc.abstractmethod
    def fetch_asset_balance_and_value(self, asset: str) -> tuple:
        """
        Retrieve the total available (free) quantity for the given asset,
        and also return its total worth in USDT.

        Args:
            asset (str): The asset symbol (e.g., "BTC", "USDT").

        Returns:
            tuple: (quantity as float, total worth in USDT as float)
        """
        pass
