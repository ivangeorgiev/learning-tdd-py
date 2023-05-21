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
    def __init__(self):
        self.moneys = []

    def add(self, *moneys):
        self.moneys.extend(moneys)

    def evaluate(self, bank, currency):
        total = reduce(add, self.__convert_all(bank, self.moneys, currency), 0)
        return Money(total, currency)

    def __convert_all(self, bank, moneys, currency):
        amounts = []
        errors = []
        for m in moneys:
            try:
                amounts.append(bank.convert(m, currency).amount)
            except MissingExchangeRateError as error:
                errors.append(error.args[0])
        if errors:
            msg = f"Missing exchange rate(s): [{','.join(errors)}]"
            raise MissingExchangeRateError(msg)
        return amounts


class Bank:
    def __init__(self):
        self._exchange_rates = {}

    def add_exchange_rate(self, from_currency, to_currency, rate):
        self._exchange_rates[f"{from_currency}>{to_currency}"] = rate

    def convert(self, from_money: Money, to_currency) -> Money:
        if from_money.currency == to_currency:
            return Money(from_money.amount, to_currency)
        exchange_key = f"{from_money.currency}>{to_currency}"
        if exchange_key in self._exchange_rates:
            rate = self._exchange_rates[exchange_key]
            return Money(from_money.amount * rate, to_currency)
        raise MissingExchangeRateError(exchange_key)
