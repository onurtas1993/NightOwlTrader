from PyQt6 import QtWidgets
from PyQt6.QtCore import QObject, pyqtSignal
from service.file_service import FileService
from service.historic_data_service import HistoricDataService


class CommandController(QObject):
    # Define a custom signal that carries the data.
    data_loaded_signal = pyqtSignal(object)

    def __init__(self, command_view):
        super(CommandController, self).__init__()
        self.command_view = command_view

        # Connect the signal to the view's update_transactions slot.
        # self.update_signal.connect(self.transactionsView.update_transactions)

        # Connect the view's buttons to the controller's handler methods.
        self.command_view.loadButton.clicked.connect(self.handle_load_file)
        self.command_view.remoteLoadButton.clicked.connect(self.handle_remote_file)

    def handle_load_file(self):
        """
        Handle the load file button click: open a file dialog, load the CSV data,
        and update the view accordingly.
        """
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self.command_view, "Open CSV File", "", "CSV files (*.csv)"
        )
        if file_path:
            success, result = FileService.read_local_csv(file_path)
            if success:
                self.command_view.fileLabel.setText(
                    f"Loaded: {file_path.split('/')[-1]}"
                )
                self.data_loaded_signal.emit(result)
            else:
                QtWidgets.QMessageBox.critical(
                    self.command_view, "Error", f"Failed to load CSV file: {result}"
                )

    def handle_remote_file(self):
        """
        Handle the load file button click: download the remote CSV data,
        and update the view accordingly.
        """
        QtWidgets.QMessageBox.information(
            self.command_view,
            "Functionality Disabled",
            "Remote CSV file read has been disabled",
        )
        return
        # Remote CSV URL
        url = (
            "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AAPL&apikey=PYI5VHWQXB88XALF&"
            "outputsize=compact&datatype=csv"
        )
        try:
            success, result = FileService.read_remote_csv(url)
            if success:
                self.command_view.fileLabel.setText("Loaded: Remote CSV File")
                self.data_loaded_signal.emit(result)
            else:
                QtWidgets.QMessageBox.critical(
                    self.command_view, "Error", f"Failed to load CSV file: {result}"
                )
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self.command_view,
                "Error",
                f"Error retrieving remote CSV file: {str(e)}",
            )

    def retrieve_historic_data(self, order_id):
        try:
            historic_data = HistoricDataService.get_historic_data(order_id)
            self.data_loaded_signal.emit(historic_data)
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self.command_view, "Error", f"Error retrieving remote data: {str(e)}"
            )
