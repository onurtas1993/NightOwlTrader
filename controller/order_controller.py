from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6 import QtWidgets
from typing import List
import threading
import helper.utils
from helper.logger import log_message
from model.order_factory import create_order  # Use the factory for order creation
from controller.order_processor import OrderProcessor
from model.abstract_order import AbstractOrder  # For type hints
from api.adapter_factory import AdapterFactory


class OrderController(QObject):
    orders_updated_signal = pyqtSignal(object)
    selected_order_changed_signal = pyqtSignal(int)  # id of the selected order
    reset_graph_signal = pyqtSignal()

    def __init__(self, orderView):
        super(OrderController, self).__init__()
        self.orderView = orderView

        self.orders: List[AbstractOrder] = []
        self.orders_lock = threading.Lock()  # Lock for thread safety
        self.thread = None  # Store reference to the thread
        self.worker = None
        self.currently_selected_order_id = None

        # Connect the Add button click to the add_order method.
        self.orderView.addOrderButton.clicked.connect(self.add_order_clicked)
        self.orders_updated_signal.connect(self.orderView.update_list)
        self.orderView.order_deleted_signal.connect(self.delete_order_clicked)
        self.orderView.orderListWidget.itemClicked.connect(self.on_item_clicked)

        # Load orders from file on startup.
        self.load_orders()

    def handle_start_processing_orders(self):
        """
        Starts continuous order processing in a separate thread.
        """
        if self.thread and self.thread.is_alive():
            print("Processing is already running!")
            return

        self.worker = OrderProcessor(self.orders)  # Create worker
        self.worker.order_processed.connect(
            self.handle_order_processed
        )  # UI safe updates
        self.worker.processing_finished.connect(self.handle_processing_finished)

        # Run in a separate Python thread
        self.thread = threading.Thread(target=self.worker.process_orders, daemon=True)
        self.thread.start()

    def handle_stop_processing_orders(self):
        """
        Stops order processing safely.
        """
        if self.worker:
            self.worker.stop()

    def handle_order_processed(self):
        """Runs in the main thread, so it's safe to update the UI"""
        with self.orders_lock:
            self.orders_updated_signal.emit(self.orders)

    def handle_processing_finished(self):
        """Called when the worker signals completion"""
        print("Order processing stopped.")

    def on_item_clicked(self, item):
        """
        Slot method that gets triggered when an item is clicked.
        Retrieves the custom widget associated with the item.
        """
        custom_widget = self.orderView.orderListWidget.itemWidget(item)
        if custom_widget:
            self.currently_selected_order_id = custom_widget.order.id
            print("Clicked on item with id:", self.currently_selected_order_id)

        self.selected_order_changed_signal.emit(self.currently_selected_order_id)

    def delete_order_clicked(self, id: int):
        # Find and remove the order with the given id from the orders list
        with self.orders_lock:
            order_to_remove = None
            for order in self.orders:
                if order.id == id:
                    order_to_remove = order
                    break
            if order_to_remove:
                self.orders.remove(order_to_remove)
        helper.utils.write_orders(self.orders)

        self.orders_updated_signal.emit(self.orders)

        if self.currently_selected_order_id == id:
            # Reset the graph if the currently selected order is removed
            self.reset_graph_signal.emit()

        log_message(f"Order removed: id: {id}")
        QtWidgets.QMessageBox.information(
            None, "Order has been removed", f"Order with id {id} has been removed."
        )

    def add_order_clicked(self):
        # Retrieve input values.
        asset = self.orderView.assetLineEdit.text()
        position = self.orderView.positionComboBox.currentText()
        amount_text = self.orderView.amountLineEdit.text()
        platform = self.orderView.platformComboBox.currentText()

        if not asset or not amount_text:
            QtWidgets.QMessageBox.warning(
                None, "Input Error", "Please fill in all required fields."
            )
            return

        amount = float(amount_text)

        adapter = AdapterFactory.get_adapter(platform)

        with self.orders_lock:
            new_order_id = max([order.id for order in self.orders], default=0) + 1
            order_data = {
                "id": new_order_id,
                "asset": asset,
                "amount": amount,
                "position": position,
                "platform": platform,
                "state": "new",
                "last_action": "",
            }

            new_order = create_order(order_data)
            new_order.adapter = adapter
            self.orders.append(new_order)

        helper.utils.write_orders(self.orders)
        self.orders_updated_signal.emit(self.orders)

        log_message(
            f"Order added:{new_order_id}, asset: {asset}, amount: {amount}, position: {position}, platform: {platform}"
        )

        # Use the view's method to clear input fields
        self.orderView.clear_input_fields()

    def load_orders(self):
        """Load orders from the JSON file, convert them into Order objects, and populate the class and the view."""
        try:
            # Read orders and convert them to AbstractOrder objects
            orders_data: List[AbstractOrder] = helper.utils.read_orders()
            with self.orders_lock:
                self.orders = orders_data

            # Emit signal to update the view
            self.orders_updated_signal.emit(self.orders)
        except Exception as e:
            print(f"Error loading orders: {e}")
