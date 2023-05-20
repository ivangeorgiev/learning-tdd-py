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


class TestMoney(unittest.TestCase):
    @parameterized.expand(
        [
            ("five_times_two_should_be_ten", Money(5, "USD"), 2, 10),
            ("ten_times_two_should_be_twenty", Money(10, "USD"), 2, 20),
            ("five_times_three_should_be_fifteen", Money(5, "USD"), 3, 15),
            ("five_euros_times_two_should_be_ten_euros", Money(5, "EUR"), 2, 10),
        ]
    )
    def test_multiplication(self, _, initial: Money, multiplier, expected_amount):
        result = initial.times(multiplier)
        self.assertEqual(expected_amount, result.amount)
        self.assertEqual(initial.currency, result.currency)

    @parameterized.expand(
        [
            ("should divide korean wons", Money(4002, "KRW"), 4, 1000.5,),
            ("should divide korean wons with different amount and divisor", Money(500, "KRW"), 2, 250,),
            ("should devide euros", Money(200, "EUR"), 4, 50,),
        ]
    )
    def test_division(self, _, initial: Money, divisor, expected_amount):
        result = initial.divide(divisor)
        self.assertEqual(expected_amount, result.amount)
        self.assertEqual(initial.currency, result.currency)
