from abc import ABC, abstractmethod
import pandas as pd
from typing import List, Dict, Optional


class Algorithm(ABC):
    @abstractmethod
    def create_trend_segments(self, data: pd.DataFrame) -> None:
        """
        Draw lines based on the algorithm's logic.

        Args:
            data (pd.DataFrame): The input DataFrame containing the data.
        """
        pass

    @abstractmethod
    def get_last_signal(data: pd.DataFrame) -> Optional[str]:
        """
        Returns the last signal ("BUY" or "SELL") from the algorithm's logic.

        Args:
            data (pd.DataFrame): The input DataFrame containing the data.

        Returns:
            Optional[str]: The last signal, either "BUY", "SELL", or None if no signal is found.
        """
        pass

    @abstractmethod
    def simulate_potential_profit(segments: List[Dict], labels: List[Dict]) -> float:
        """
        Simulate a trading strategy where we buy at the start of blue segments
        and sell at the end of red segments, calculating potential profit.

        Args:
            data (pd.DataFrame): The input DataFrame containing the data.

        Returns:
            Optional[str]: A string representing the potential profit or None if no segments are found.
        """
        pass
