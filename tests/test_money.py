from types import SimpleNamespace
import unittest

from parameterized import parameterized

from money import Money, Portfolio, MissingExchangeRateError


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

    @parameterized.expand(
        [("same_currency_and_amount", Money(10, "USD"), Money(10, "USD"))]
    )
    def test_equality(self, _, first: Money, second: Money):
        self.assertEqual(first, second)

    @parameterized.expand(
        [
            (
                "five_dollars_should_be_not_equal_to_ten_dollars",
                Money(5, "USD"),
                Money(10, "USD"),
            ),
            (
                "five_dollars_should_be_not_equal_to_five_euros",
                Money(5, "USD"),
                Money(5, "EUR"),
            ),
            (
                "object_without_amount_should_be_not_equal_to_five_dollars",
                SimpleNamespace(currency="USD"),
                Money(5, "USD")
            ),
            (
                "object_without_currency_should_be_not_equal_to_five_dollars",
                SimpleNamespace(amount=5),
                Money(5, "USD")
            )
        ]
    )
    def test_non_equality(self, _, first: Money, second: Money):
        self.assertNotEqual(first, second)

    def test_representation(self):
        five_dollars = Money(5, "USD")
        self.assertEqual("Money(5, 'USD')", repr(five_dollars))
        self.assertEqual("Money(5, 'USD')", str(five_dollars))

class TestPortfolio(unittest.TestCase):
    @parameterized.expand([
        ("same_currency_5_dollars_and_5_dollars_make_10_dollars", Money(5, "USD"), Money(5, "USD"), Money(10, "USD")),
        ("mixed_currency_5_dollars_and_10_euros_make_17_dollars", Money(5, "USD"), Money(10, "EUR"), Money(17, "USD")),
        ("mixed_currency_1_dollar_and_1100_korrean_wons_make_2200_korrean_wons", Money(1, "USD"), Money(1100, "KRW"), Money(2200, "KRW")),
    ])
    def test_addition(self, _, first: Money, second: Money, expected: Money):
        portfolio = Portfolio()
        portfolio.add(first, second)
        actual_money= portfolio.evaluate(expected.currency)
        self.assertEqual(expected, actual_money)

    def test_evaluate_should_fail_with_MissingExchangeRate_when_exchange_rates_are_missing(self):
        one_dollar = Money(1, "USD")
        one_euro = Money(1, "EUR")
        one_won = Money(1, "KRW")
        portfolio = Portfolio()
        portfolio.add(one_dollar, one_euro, one_won)
        with self.assertRaisesRegex(MissingExchangeRateError, "Missing exchange rate\(s\): \[USD>Kalganid,EUR>Kalganid,KRW>Kalganid\]"):
            portfolio.evaluate("Kalganid")
