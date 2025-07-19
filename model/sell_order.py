from model.abstract_order import AbstractOrder
from model.order_action_mixin import OrderActionMixin
from helper.logger import log_message


class SellOrder(AbstractOrder, OrderActionMixin):
    def process(self) -> None:
        if not self.adapter:
            raise ValueError("No trading adapter assigned to this order.")

        if self.state == self.State.COMPLETED:
            return

        self._sell()

    def _handle_sell_response(self, response):
        if response.get("status") == "FILLED":
            self.state = self.State.COMPLETED
            self.last_action = "sell"
            log_message(f"Sell order succeeded for {self.id} ({self.asset})")
        else:
            self.state = self.State.FAILED
            log_message(
                f"Sell order failed for {self.id} ({self.asset}): {response.get('message')}"
            )
