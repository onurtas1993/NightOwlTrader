from PyQt6 import QtCore
from view.main_view import MainView
from view.order_view import OrderView
from view.command_view import CommandView
from view.graph_view import GraphView
from view.transactions_view import TransactionsView
from controller.order_controller import OrderController
from controller.command_controller import CommandController
from controller.graph_controller import GraphController
from controller.transactions_controller import TransactionsController


class ApplicationManager(QtCore.QObject):
    def __init__(self, parent=None):
        super(ApplicationManager, self).__init__(parent)

        # Create the views
        self.orderView = OrderView(None)
        self.command_view = CommandView(None)
        self.graphView = GraphView(None)
        self.transactionsView = TransactionsView(None)
        self.mainView = MainView(
            None,
            self.orderView,
            self.command_view,
            self.graphView,
            self.transactionsView,
        )

        # Create the controllers (pass self and the views)
        self.orderController = OrderController(self.orderView)
        self.commandController = CommandController(self.command_view)
        self.graphController = GraphController(self.graphView)
        self.transactionsController = TransactionsController(self.transactionsView)

        self.command_view.startButton.clicked.connect(
            self.orderController.handle_start_processing_orders
        )
        self.command_view.stopButton.clicked.connect(
            self.orderController.handle_stop_processing_orders
        )

        self.commandController.data_loaded_signal.connect(
            self.graphController.load_data
        )

        self.orderController.reset_graph_signal.connect(
            self.graphController.init_empty_chart
        )

        self.orderController.selected_order_changed_signal.connect(
            self.commandController.retrieve_historic_data
        )

        # Change statusLabel background color and text in main_view when start and stop Button is clicked
        self.command_view.startButton.clicked.connect(
            lambda: (
                self.mainView.statusLabel.setStyleSheet(
                    "background-color: rgb(156, 204, 101);color: rgb(48, 48, 48);"
                ),
                self.mainView.statusLabel.setText("Status: Processing..."),
            )
        )

        self.command_view.stopButton.clicked.connect(
            lambda: (
                self.mainView.statusLabel.setStyleSheet(
                    "background-color: rgb(255, 112, 67);color: rgb(48, 48, 48);"
                ),
                self.mainView.statusLabel.setText("Status: Inactive..."),
            )
        )

    def show(self):
        self.mainView.show()
