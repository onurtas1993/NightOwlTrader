from model.abstract_order import AbstractOrder


class SimulateOrder(AbstractOrder):
    def process(self) -> None:
        # This order type does nothing (simulation only)
        pass
