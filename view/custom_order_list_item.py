from PyQt6 import QtWidgets, uic
from model.abstract_order import AbstractOrder


class CustomOrderListItem(QtWidgets.QWidget):
    def __init__(self, order: AbstractOrder, parent=None):
        super(CustomOrderListItem, self).__init__(parent)
        # Build the path to the UI file. Adjust the path if necessary.
        uic.loadUi("view/custom_order_list_item.ui", self)

        self.order = order
        # Set the text for the labels
        self.groupBox.setTitle("Order " + str(order.id))
        # self.idLabel.setText("Order: " + str(order.id))
        self.assetLabel.setText(order.asset)
        self.amountLabel.setText(str(order.amount) + " USD")
        self.positionLabel.setText(order.position)
        self.platformLabel.setText(order.platform)
        self.stateLabel.setText(order.state.value)

        # Set the color of the stateLabel based on the order state
        if order.state == order.State.NEW:
            self.stateLabel.setStyleSheet("color: yellow;")
        elif order.state == order.State.IN_PROGRESS:
            self.stateLabel.setStyleSheet("color: yellow;")
        elif order.state == order.State.COMPLETED:
            self.stateLabel.setStyleSheet("color: green;")
        elif order.state == order.State.FAILED:
            self.stateLabel.setStyleSheet("color: red;")
