from abc import ABC, abstractmethod


class DiscountStrat(ABC):
    @abstractmethod
    def apply(self, total:float) -> float:
        pass


class NoDiscount(DiscountStrat):
    def apply(self, total:float) -> float:
        return total


class PercentageDiscount(DiscountStrat):
    def __init__(self, percentage: float) -> None:
        self.percentage: float = percentage

    def apply(self, total: float) -> float:
        return total * (1-self.percentage/100)


class BulkDiscount(DiscountStrat):
    def __init__(self, threshold:float, discount:float) -> None:
        self.threshold: float = threshold
        self.discount: float = discount

    def apply(self, total: float) -> float:
        if total >= self.threshold:
            return total - self.discount
        return total


class StudentDiscount(DiscountStrat):
    def apply(self, total: float) -> float:
        return total * 0.95
