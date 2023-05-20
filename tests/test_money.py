import unittest

from parameterized import parameterized


class Dollar:
    def __init__(self, amount):
        self.amount = amount

    def times(self, multiplier):
        return Dollar(self.amount * multiplier)


class TestMoney(unittest.TestCase):
    @parameterized.expand(
        [
            ("five_times_two_should_be_ten", Dollar(5), 2, 10),
            ("ten_times_two_should_be_twenty", Dollar(10), 2, 20),
            ("five_times_three_should_be_fifteen", Dollar(5), 3, 15),
        ]
    )
    def test_times(
        self, _, initial: Dollar, multiplier, expected_amount
    ):
        result = initial.times(multiplier)
        self.assertEqual(expected_amount, result.amount)

