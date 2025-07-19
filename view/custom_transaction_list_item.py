from PyQt6 import QtWidgets, uic


class CustomTransactionListItem(QtWidgets.QWidget):
    def __init__(self, timestamp, log, parent=None):
        super(CustomTransactionListItem, self).__init__(parent)
        uic.loadUi("view/custom_transaction_list_item.ui", self)
        self.groupBox.setTitle(timestamp)
        self.transactionHistoryLabel.setText(log)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Set label width to the groupBox's width minus some margin
        label_width = self.groupBox.width() - 24
        if label_width > 0:
            self.transactionHistoryLabel.setFixedWidth(label_width)
