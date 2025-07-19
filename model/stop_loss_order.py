from model.abstract_order import AbstractOrder
from model.order_action_mixin import OrderActionMixin
from helper.logger import log_message


class StopLossOrder(AbstractOrder, OrderActionMixin):
    def process(self) -> None:
        if not self.adapter:
            raise ValueError("No trading adapter assigned to this order.")

        if self.state == self.State.COMPLETED:
            return

        # Use 'amount' as the stop-loss threshold for total value
        _, total_value = self.adapter.fetch_asset_balance_and_value(self.asset)
        stop_value = self.amount  # Use amount as the stop-loss threshold

        if stop_value is None:
            log_message(f"No stop value (amount) set for StopLossOrder {self.id}.")
            self.state = self.State.FAILED
            return

        if total_value <= stop_value:
            self._sell()
            self.state = self.State.COMPLETED
        else:
            self.state = self.State.IN_PROGRESS
            log_message(
                f"StopLossOrder {self.id} is waiting for stop value {stop_value}."
            )
