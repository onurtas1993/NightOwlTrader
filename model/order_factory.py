from model.buy_order import BuyOrder
from model.sell_order import SellOrder
from model.take_profit_order import TakeProfitOrder
from model.stop_loss_order import StopLossOrder
from model.intelli_four_order import IntelliFourOrder
from model.simulate_order import SimulateOrder


def create_order(data):
    position = data.get("position", "").lower()
    if position == "buy":
        return BuyOrder.from_dict(data)
    elif position == "sell":
        return SellOrder.from_dict(data)
    elif position in ("autopilot-4h"):
        return IntelliFourOrder.from_dict(data)
    elif position == "take profit":
        return TakeProfitOrder.from_dict(data)
    elif position == "stop loss":
        return StopLossOrder.from_dict(data)
    elif position == "simulate":
        return SimulateOrder.from_dict(data)
    else:
        raise ValueError(f"Unknown order position: {position}")
