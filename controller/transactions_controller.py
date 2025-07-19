from PyQt6.QtCore import QObject, pyqtSignal
import helper.utils
import datetime
from helper.logger import log_message, set_log_callback  # Import the logger module
import threading  # Import threading for thread safety


class TransactionsController(QObject):
    # Define a custom signal that carries a string.
    update_transaction_history = pyqtSignal(object)

    def __init__(self, transactionsView):
        super(TransactionsController, self).__init__()
        self.transactionsView = transactionsView

        # Lock for thread safety
        self.history_lock = threading.Lock()

        # Connect the signal to the view's update_transactions slot.
        self.update_transaction_history.connect(
            self.transactionsView.update_transactions
        )

        # Load history from file on startup.
        self.load_history()

        # Set the log callback to the log_transaction method
        set_log_callback(self.log_transaction)

    def load_history(self):
        """Load history from the JSON file and populate both the class variable and the view."""
        with self.history_lock:
            self.history = helper.utils.read_history()
        self.update_transaction_history.emit(self.history)

    def callback_new_order_added(self, order):
        log_message(f"New order added: {order.asset}")

    def callback_order_removed(self, order):
        log_message(f"Order removed: {order.asset}")

    def log_transaction(self, message):
        transaction_history_item = {
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "log": message,
        }
        with self.history_lock:
            self.history.insert(0, transaction_history_item)  # Insert at the beginning
            helper.utils.write_history(self.history)
        self.update_transaction_history.emit(self.history)
