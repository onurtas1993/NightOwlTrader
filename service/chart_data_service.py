import pandas as pd


class ChartDataService:
    @staticmethod
    def prepare_chart_data(data):
        data["timestamp"] = pd.to_datetime(data["timestamp"], format="%Y-%m-%d")
        formatted_dates = data["timestamp"].dt.strftime("%d.%m").tolist()
        positions = list(range(len(formatted_dates)))
        grouped = data.groupby(data["timestamp"].dt.to_period("M"))
        tick_positions = [group.index[0] for _, group in grouped]
        tick_labels = [
            group.iloc[0]["timestamp"].strftime("%d.%m") for _, group in grouped
        ]
        candlesticks = list(
            zip(
                positions,
                data["open"],
                data["high"],
                data["low"],
                data["close"],
            )
        )
        return formatted_dates, positions, tick_positions, tick_labels, candlesticks
