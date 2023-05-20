from functools import reduce
from operator import add, attrgetter

class Money:
    def __init__(self, amount, currency):
        self.amount = amount
        self.currency = currency

    def times(self, multiplier):
        return Money(self.amount * multiplier, self.currency)
    
    def divide(self, divisor):
        return Money(self.amount / divisor, self.currency)
    
    def __eq__(self, other):
        if not all(hasattr(other, attr) for attr in ["currency", "amount"]):
            return False
        return self.amount == other.amount and self.currency == other.currency

    def __repr__(self):
        return f"{self.__class__.__name__}({self.amount}, '{self.currency}')"

class Portfolio:
    def __init__(self):
        self.moneys = []

    def add(self, *moneys):
        self.moneys.extend(moneys)

    def evaluate(self, currency):
        total = reduce(add, map(attrgetter("amount"), self.moneys), 0)
        return Money(total, currency)
