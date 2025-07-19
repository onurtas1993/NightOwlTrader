from PyQt6 import QtWidgets, uic, QtCore
from view.custom_transaction_list_item import CustomTransactionListItem


class TransactionsView(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(TransactionsView, self).__init__(parent)
        uic.loadUi("view/transactions_view.ui", self)

        # Find the QListWidget in the UI.
        self.listWidget = self.findChild(QtWidgets.QListWidget, "listWidget")

    def add_custom_list_item(self, timestamp, log):
        """
        Create a new custom list item and add it to the listWidget.
        """
        item = QtWidgets.QListWidgetItem(self.listWidget)
        custom_widget = CustomTransactionListItem(timestamp, log)

        # Use the sizeHint method of the custom widget to set the size of the item
        item.setSizeHint(custom_widget.sizeHint())

        self.listWidget.addItem(item)
        self.listWidget.setItemWidget(item, custom_widget)

    def update_transactions(self, history):
        self.history = history
        # Ensure the update is performed on the main GUI thread
        QtCore.QMetaObject.invokeMethod(
            self, "perform_update", QtCore.Qt.ConnectionType.QueuedConnection
        )

    @QtCore.pyqtSlot()
    def perform_update(self):
        self.listWidget.clear()
        for transaction in self.history:
            timestamp = transaction.get("timestamp")
            log = transaction.get("log")
            self.add_custom_list_item(timestamp, log)
        self.resize_list_items()  # Ensure resize after update

    def resize_list_items(self):
        # Update both width and height based on the new width
        for i in range(self.listWidget.count()):
            item = self.listWidget.item(i)
            widget = self.listWidget.itemWidget(item)
            if widget:
                widget.setFixedWidth(self.listWidget.viewport().width())
                widget.adjustSize()
                item.setSizeHint(widget.sizeHint())

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.resize_list_items()
