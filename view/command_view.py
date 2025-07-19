from PyQt6 import QtWidgets, uic


class CommandView(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(CommandView, self).__init__(parent)
        uic.loadUi("view/command_view.ui", self)

        self.loadButton = self.findChild(QtWidgets.QPushButton, "loadButton")
        self.startButton = self.findChild(QtWidgets.QPushButton, "startButton")
        self.stopButton = self.findChild(QtWidgets.QPushButton, "stopButton")
