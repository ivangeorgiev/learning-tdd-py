import unittest

from parameterized import parameterized

from money import Money, Portfolio


class TestMoney(unittest.TestCase):
    @parameterized.expand(
        [
            ("five_times_two_should_be_ten", Money(5, "USD"), 2, Money(10, "USD")),
            (
                "ten_euros_times_three_should_be_thirty_euros",
                Money(10, "EUR"),
                3,
                Money(30, "EUR"),
            ),
        ]
    )
    def test_multiplication(self, _, initial: Money, multiplier, expected: Money):
        result = initial.times(multiplier)
        self.assertEqual(expected, result)

    @parameterized.expand(
        [
            ("should divide korean wons", Money(4002, "KRW"), 4, Money(1000.5, "KRW")),
            ("should devide euros", Money(200, "EUR"), 4, Money(50, "EUR")),
        ]
    )
    def test_division(self, _, initial: Money, divisor, expected: Money):
        result = initial.divide(divisor)
        self.assertEqual(expected, result)


class TestPortfolio(unittest.TestCase):
    def test_addition(self):
        fiveDollars = Money(5, "USD")
        tenDollars = Money(10, "USD")
        fifteenDollars = Money(15, "USD")
        portfolio = Portfolio()
        portfolio.add(fiveDollars, tenDollars)
        self.assertEqual(fifteenDollars, portfolio.evaluate("USD"))
