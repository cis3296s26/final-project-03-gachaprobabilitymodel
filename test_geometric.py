import unittest
from unittest.mock import patch
import io
import sys
import geometric


class TestGachaModel(unittest.TestCase):

    def test_not_enough_currency(self):
        captured = io.StringIO()
        sys.stdout = captured

        result = geometric.gachaModel(currency=5, cost=10, rate=0.01, seed=42)

        sys.stdout = sys.__stdout__

        self.assertIsNone(result)
        self.assertIn("Not enough currency to pull.", captured.getvalue())

    @patch("gacha.rateCalculator", lambda roll: 0.0)
    def test_total_rolls_and_no_successes(self):
        result = geometric.gachaModel(currency=100, cost=10, rate=0.01, seed=1)

        self.assertEqual(result["total_rolls"], 10)
        self.assertEqual(result["successes"], 0)
        self.assertEqual(result["featured_successes"], 0)
        self.assertIsNone(result["first_success_at"])
        self.assertIsNone(result["first_featured_at"])
        self.assertEqual(result["success_positions"], [])
        self.assertEqual(result["featured_positions"], [])
        self.assertEqual(result["empirical_mean"], 0)
        self.assertEqual(result["empirical_median"], 0)
        self.assertEqual(result["empirical_success_rate"], 0)
        self.assertEqual(result["featured_rate_empirical"], 0)

    @patch("gacha.rateCalculator", lambda roll: 1.0)
    def test_all_successes(self):
        result = geometric.gachaModel(currency=50, cost=10, rate=0.5, seed=1)

        self.assertEqual(result["total_rolls"], 5)
        self.assertEqual(result["successes"], 5)
        self.assertEqual(result["first_success_at"], 1)
        self.assertEqual(result["success_positions"], [1, 2, 3, 4, 5])
        self.assertEqual(result["empirical_mean"], 3.0)
        self.assertEqual(result["empirical_median"], 3)
        self.assertEqual(result["empirical_success_rate"], 1.0)

    @patch("gacha.rateCalculator", lambda roll: 1.0)
    def test_featured_rate_all_featured(self):
        result = geometric.gachaModel(
            currency=30,
            cost=10,
            rate=0.5,
            seed=1,
            featuredRate=1.0
        )

        self.assertEqual(result["successes"], 3)
        self.assertEqual(result["featured_successes"], 3)
        self.assertEqual(result["first_featured_at"], 1)
        self.assertEqual(result["featured_positions"], [1, 2, 3])
        self.assertEqual(result["featured_rate_empirical"], 1.0)

    @patch("gacha.rateCalculator", lambda roll: 1.0)
    def test_check_external_used_when_provided(self):
        def fake_check_external(roll):
            return (roll % 2 == 0, f"Unit {roll}")

        result = geometric.gachaModel(
            currency=40,
            cost=10,
            rate=0.5,
            seed=1,
            checkExternal=fake_check_external
        )

        self.assertEqual(result["successes"], 4)
        self.assertEqual(result["featured_successes"], 2)
        self.assertEqual(result["first_featured_at"], 2)
        self.assertEqual(result["featured_positions"], [2, 4])


if __name__ == "__main__":
    unittest.main(exit=False)