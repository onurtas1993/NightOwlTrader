import json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt6 import QtWidgets, uic
import matplotlib


class GraphView(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(GraphView, self).__init__(parent)
        # Load the UI from the .ui file located in the 'view' folder.
        uic.loadUi("view/graph_view.ui", self)

        # Apply the dark theme to Matplotlib charts.
        self.set_dark_theme_chart()

        # Retrieve UI elements defined in the .ui file.
        self.fileLabel = self.findChild(QtWidgets.QLabel, "fileLabel")
        self.canvasWidget = self.findChild(QtWidgets.QWidget, "canvasWidget")
        self.toolbarWidget = self.findChild(QtWidgets.QWidget, "toolbarWidget")

        # Create a Matplotlib figure and canvas.
        self.figure = plt.Figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
        # Add the canvas to the canvasWidget's layout.
        self.canvasWidget.layout().addWidget(self.canvas)

        # Create the navigation toolbar and add it to the toolbarWidget's layout.
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.toolbarWidget.layout().addWidget(self.toolbar)

    def set_dark_theme_chart(self):
        """
        Apply a dark theme to Matplotlib charts using values from a JSON file.
        """
        json_path = "resources/dark_chart_colors.json"
        try:
            with open(json_path, "r") as f:
                self.dark_theme = json.load(f)
            matplotlib.rcParams.update(self.dark_theme)
        except Exception as e:
            print(f"Failed to load dark_chart_colors.json: {e}")
            # Optionally, fall back to hardcoded defaults or do nothing

    def init_empty_chart(self):
        figure = self.figure
        figure.clear()
        ax = figure.add_subplot(111)
        ax.set_aspect("auto")
        ax.set_title("Estimated Earnings Will Be Shown Here", fontsize=14, fontweight="bold")
        ax.set_xlabel("Date")
        ax.set_ylabel("Price")
        ax.set_xticks([])
        ax.set_yticks([])
        figure.tight_layout()
        self.canvas.draw()

    def plot_chart(self, segments, labels, candlesticks, tick_positions, tick_labels, title):
        figure = self.figure
        figure.clear()
        ax = figure.add_subplot(111)
        ax.set_aspect("auto")
        ax.set_title(title, fontsize=14, fontweight="bold")

        # Plot alternating line segments
        for segment in segments:
            segment_x = list(range(segment["start_index"], segment["end_index"] + 1))
            ax.plot(
                segment_x,
                segment["line_values"],
                color=segment["color"],
                linewidth=2,
                label=(
                    f"{segment['color'].capitalize()} Line"
                    if f"{segment['color'].capitalize()} Line"
                    not in ax.get_legend_handles_labels()[1]
                    else None
                ),
            )

        # Plot labels
        for label in labels:
            ax.text(
                label["position"],
                label["value"],
                label["text"],
                color="white",
                fontsize=9,
                ha="center",
                va="bottom",
                bbox=dict(
                    boxstyle="round,pad=0.3", edgecolor="white", facecolor="black"
                ),
            )

        # Plot candlesticks
        from matplotlib.patches import Rectangle
        for pos, o, h, l, c in candlesticks:
            if c > o:
                color = self.dark_theme.get("bullish_candle_color", "green")  # Green for bullish candles
            elif c < o:
                color = self.dark_theme.get("bearish_candle_color", "red")  # Red for bearish candles
            else:
                color = color = self.dark_theme.get("neautral_candle_color", "gray")  # Gray for neutral candles
            # Draw the wick
            ax.plot([pos, pos], [l, h], color=color, linewidth=1)
            # Draw the body
            body_bottom = min(o, c)
            body_height = abs(c - o)
            ax.add_patch(
                Rectangle(
                    (pos - 0.3, body_bottom),
                    0.6,
                    body_height,
                    facecolor=color,
                    edgecolor=color,
                )
            )

        ax.set_xticks(tick_positions)
        ax.set_xticklabels(tick_labels, rotation=0, ha="right")
        ax.set_xlabel("Date")
        ax.set_ylabel("Price")
        ax.legend()
        figure.tight_layout()
        self.canvas.draw()
