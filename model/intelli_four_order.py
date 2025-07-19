from model.abstract_order import AbstractOrder
from model.order_action_mixin import OrderActionMixin
from helper.logger import log_message


class IntelliFourOrder(AbstractOrder, OrderActionMixin):
    def process(self) -> None:
        if not self.adapter:
            raise ValueError("No trading adapter assigned to this order.")

        data = self.adapter.get_historic_data(self.asset, "4h")
        if data.empty:
            self.state = self.State.FAILED
            log_message(f"No historic data for {self.asset} (4h). Order failed.")
            return

        signal = self.algorithm.get_last_signal(data)
        if signal is None:
            log_message(f"No signal generated for {self.asset}.")
            return

        if signal == "buy" and self.last_action != "buy":
            self._buy()
        elif signal == "sell" and self.last_action != "sell":
            self._sell()
        self.state = self.State.IN_PROGRESS
