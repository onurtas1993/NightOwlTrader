import sys
from PyQt6 import QtWidgets, QtGui
from app_manager import ApplicationManager
import resources.resources_rc  # noqa: F401


def main():
    app = QtWidgets.QApplication(sys.argv)
    with open("resources/dark_theme.qss", "r") as f:
        app.setStyleSheet(f.read())

    app.setWindowIcon(QtGui.QIcon(":/resources/icon.ico"))

    app_manager = ApplicationManager()
    app_manager.show()
    app.setStyle("Fusion")
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
