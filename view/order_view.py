from PyQt6 import QtWidgets, uic, QtCore
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QComboBox
from view.custom_order_list_item import CustomOrderListItem
from model.abstract_order import AbstractOrder
from typing import List
import threading


class OrderView(QtWidgets.QWidget):
    # Define a custom signal that carries a string.
    order_deleted_signal = pyqtSignal(int)  # id of the order

    def __init__(self, parent=None):
        super(OrderView, self).__init__(parent)
        uic.loadUi("view/order_view.ui", self)

        # Find the QListWidget in the UI.
        self.orderListWidget = self.findChild(QtWidgets.QListWidget, "orderListWidget")
        self.positionComboBox = self.findChild(QComboBox, "positionComboBox")
        self.orders_lock = threading.Lock()  # Lock for thread safety

    def add_custom_list_item(self, order: AbstractOrder):
        """
        Create a new custom list item and add it to the listWidget.
        """
        item = QtWidgets.QListWidgetItem()
        custom_widget = CustomOrderListItem(order)

        custom_widget.deleteOrderButton.clicked.connect(
            lambda: self.delete_button_clicked(order.id)  # Use order.id
        )
        item.setSizeHint(QtCore.QSize(190, 90))  # Adjust the width and height as needed
        self.orderListWidget.addItem(item)
        self.orderListWidget.setItemWidget(item, custom_widget)

    def delete_button_clicked(self, id):
        self.order_deleted_signal.emit(id)

    def update_list(self, orders: List[AbstractOrder]):
        with self.orders_lock:
            # Ensure the update is performed on the main GUI thread
            QtCore.QMetaObject.invokeMethod(
                self,
                "perform_update",
                QtCore.Qt.ConnectionType.QueuedConnection,
                QtCore.Q_ARG(list, orders),
            )

    @QtCore.pyqtSlot(list)
    def perform_update(self, orders: List[AbstractOrder]):
        with self.orders_lock:
            self.orderListWidget.clear()
            for order in orders:
                self.add_custom_list_item(order)

    def clear_input_fields(self):
        self.assetLineEdit.clear()
        self.amountLineEdit.clear()
