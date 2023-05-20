import unittest

from parameterized import parameterized


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


class TestMoney(unittest.TestCase):
    @parameterized.expand(
        [
            ("five_times_two_should_be_ten", Money(5, "USD"), 2, Money(10, "USD")),
            ("ten_times_two_should_be_twenty", Money(10, "USD"), 2, Money(20, "USD")),
            ("five_times_three_should_be_fifteen", Money(5, "USD"), 3, Money(15, "USD")),
            ("five_euros_times_two_should_be_ten_euros", Money(5, "EUR"), 2, Money(10, "EUR")),
        ]
    )
    def test_multiplication(self, _, initial: Money, multiplier, expected):
        result = initial.times(multiplier)
        self.assertEqual(expected, result)

    @parameterized.expand(
        [
            ("should divide korean wons", Money(4002, "KRW"), 4, Money(1000.5, "KRW")),
            ("should divide korean wons with different amount and divisor", Money(500, "KRW"), 2, Money(250, "KRW")),
            ("should devide euros", Money(200, "EUR"), 4, Money(50, "EUR")),
        ]
    )
    def test_division(self, _, initial: Money, divisor, expected):
        result = initial.divide(divisor)
        self.assertEqual(expected, result)
