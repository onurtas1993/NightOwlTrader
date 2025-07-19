from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from api.base_trading_api import BaseTradingApi
from algorithms.base_algorithm import Algorithm
from algorithms.to_the_moon_algorithm import ToTheMoonAlgorithm


@dataclass
class AbstractOrder(ABC):
    class State(Enum):
        NEW = "new"
        IN_PROGRESS = "in_progress"
        COMPLETED = "completed"
        FAILED = "failed"

    id: int
    asset: str
    amount: float
    position: str
    platform: str
    adapter: BaseTradingApi = None
    algorithm: Algorithm = ToTheMoonAlgorithm()
    state: State = State.NEW
    last_action: str = ""

    def to_dict(self):
        return {
            "id": self.id,
            "asset": self.asset,
            "amount": self.amount,
            "position": self.position,
            "platform": self.platform,
            "state": self.state.value,
            "last_action": self.last_action,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            asset=data["asset"],
            amount=data["amount"],
            position=data["position"],
            platform=data["platform"],
            state=cls.State(data["state"]),
            last_action=data.get("last_action", ""),
        )

    def __eq__(self, other):
        if isinstance(other, AbstractOrder):
            return self.id == other.id
        return False

    @abstractmethod
    def process(self) -> None:
        pass
