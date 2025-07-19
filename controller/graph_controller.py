from PyQt6 import QtWidgets
from algorithms.base_algorithm import Algorithm
from algorithms.to_the_moon_algorithm import ToTheMoonAlgorithm
from service.chart_data_service import ChartDataService


class GraphController:
    def __init__(self, graph_view):
        """
        Initialize the GraphController with the view object.
        This allows the controller to update the view directly.
        """
        self.graph_view = graph_view
        self.data = None
        self.graph_view.init_empty_chart()
        self.algorithm: Algorithm = ToTheMoonAlgorithm()

    def load_data(self, data):
        self.data = data
        self.plot_chart()

    def init_empty_chart(self):
        """
        Initialize an empty chart on the figure from the view.
        This is used when no data is available.
        """
        self.graph_view.init_empty_chart()

    def plot_chart(self):
        """
        Plot the candlestick chart onto the figure from the view using the loaded data.
        Raises a ValueError if no data is loaded.
        """
        if self.data is None:
            raise ValueError("No data loaded.")
        if self.data.empty:
            return

        # Prepare chart data using ChartDataService
        formatted_dates, positions, tick_positions, tick_labels, candlesticks = (
            ChartDataService.prepare_chart_data(self.data)
        )

        # Prepare segments and labels
        segments, labels = self.algorithm.create_trend_segments(self.data)
        potential_growth = self.algorithm.simulate_potential_profit(segments, labels)
        title = "100 USD → {:.2f} USD (Simulated)".format(potential_growth)

        # Delegate plotting to the view
        self.graph_view.plot_chart(
            segments, labels, candlesticks, tick_positions, tick_labels, title
        )

    def handle_plot_chart(self):
        """
        Handle the plot button click: plot the chart using the loaded data.
        """
        if self.data is None:
            QtWidgets.QMessageBox.warning(self.graph_view, "Error", "No data loaded.")
            return

        try:
            self.plot_chart()
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self.graph_view, "Error", f"Failed to plot chart: {e}"
            )
