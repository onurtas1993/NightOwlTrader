import threading
from PyQt6.QtCore import pyqtSignal, QObject
import helper.utils


class OrderProcessor(QObject):
    order_processed = pyqtSignal()  # Signal to update UI safely
    processing_finished = pyqtSignal()  # Signal when stopping

    def __init__(self, orders):
        super().__init__()
        self.orders = orders
        self.running = False
        self.stop_event = threading.Event()  # 🔹 Event to interrupt sleep

    def process_orders(self):
        """Continuously processes orders every 10 seconds until stopped."""
        self.running = True
        self.stop_event.clear()  # Ensure event is reset

        while self.running:
            for order in self.orders:
                if not self.running:
                    break  # Exit early if stopped

                order.process()
                helper.utils.write_orders(self.orders)
                self.order_processed.emit()  # UI safe update

            # 🔹 Instead of time.sleep(10), wait but allow early exit
            if self.stop_event.wait(20):
                break  # 🔹 Exit immediately if stop is triggered

        self.processing_finished.emit()  # Notify when stopped

    def stop(self):
        """Stops processing immediately."""
        self.running = False
        self.stop_event.set()  # 🔹 Wake up immediately
