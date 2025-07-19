from helper.logger import log_message


class OrderActionMixin:
    def _buy(self):
        response = self.adapter.buy_order(self.asset, self.amount)
        if response.get("status") == "FILLED":
            self.state = self.State.COMPLETED
            self.last_action = "buy"
            log_message(f"Buy order succeeded for {self.id} ({self.asset})")
        else:
            self.state = self.State.FAILED
            log_message(
                f"Buy order failed for {self.id} ({self.asset}): {response.get('message')}"
            )

    def _sell(self):
        response = self.adapter.sell_order(self.asset, self.amount)
        if response.get("status") == "FILLED":
            self.state = self.State.COMPLETED
            self.last_action = "sell"
            log_message(f"Sell order succeeded for {self.id} ({self.asset})")
        else:
            self.state = self.State.FAILED
            log_message(
                f"Sell order failed for {self.id} ({self.asset}): {response.get('message')}"
            )
