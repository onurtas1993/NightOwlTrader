from model.abstract_order import AbstractOrder
from model.order_action_mixin import OrderActionMixin
from helper.logger import log_message


class TakeProfitOrder(AbstractOrder, OrderActionMixin):
    def process(self) -> None:
        if not self.adapter:
            raise ValueError("No trading adapter assigned to this order.")

        if self.state == self.State.COMPLETED:
            return

        # Use 'amount' as the target value for take profit
        _, total_value = self.adapter.fetch_asset_balance_and_value(self.asset)
        target_value = self.amount  # Use amount as the target value

        if target_value is None:
            log_message(f"No target value (amount) set for TakeProfitOrder {self.id}.")
            self.state = self.State.FAILED
            return

        if total_value >= target_value:
            self._sell()
            self.state = self.State.COMPLETED
        else:
            self.state = self.State.IN_PROGRESS
            log_message(
                f"TakeProfitOrder {self.id} is waiting for target value {target_value}."
            )
