from model.abstract_order import AbstractOrder
from model.order_action_mixin import OrderActionMixin
from helper.logger import log_message


class BuyOrder(AbstractOrder, OrderActionMixin):
    def process(self) -> None:
        if not self.adapter:
            raise ValueError("No trading adapter assigned to this order.")

        if self.state == self.State.COMPLETED:
            return

        self._buy()

    def _handle_buy_response(self, response):
        if response.get("status") == "FILLED":
            self.state = self.State.COMPLETED
            self.last_action = "buy"
            log_message(f"Buy order succeeded for {self.id} ({self.asset})")
        else:
            self.state = self.State.FAILED
            log_message(
                f"Buy order failed for {self.id} ({self.asset}): {response.get('message')}"
            )
