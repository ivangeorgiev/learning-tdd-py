from functools import reduce
from operator import add, attrgetter

class MissingExchangeRateError(Exception):
    pass

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
    _rates = {
        "EUR>USD": 1.2,
        "USD>KRW": 1100,
    }
    def __init__(self):
        self.moneys = []

    def add(self, *moneys):
        self.moneys.extend(moneys)

    def evaluate(self, currency):
        total = reduce(add, self.__convert_all(self.moneys, currency), 0)
        return Money(total, currency)

    def __convert_all(self, moneys, currency):
        amounts = []
        errors = []
        for m in moneys:
            try:
                amounts.append(self.__convert(m, currency))
            except KeyError as error:
                errors.append(error.args[0])
        if errors:
            msg = f"Missing exchange rate(s): [{','.join(errors)}]"
            raise MissingExchangeRateError(msg)
        return amounts
        
    def __convert(self, money, currency):
        if money.currency == currency:
            return money.amount
        rate = self._rates[f"{money.currency}>{currency}"]
        return money.amount * rate
    