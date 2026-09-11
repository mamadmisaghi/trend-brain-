import json
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
POLICY = json.loads((ROOT / "config" / "coinability.v1.json").read_text(encoding="utf-8"))
SCHEMA = json.loads(
    (ROOT / "schemas" / "hermes-analysis-v2.schema.json").read_text(encoding="utf-8")
)


def score(factors: dict[str, str]) -> int:
    points = POLICY["rating_points"]
    weights = POLICY["weights"]
    if set(factors) != set(weights):
        raise ValueError("factor set does not match policy")
    return round(sum(points[factors[name]] * weight for name, weight in weights.items()))


class CoinabilityPolicyTests(unittest.TestCase):
    def test_weights_sum_to_one(self):
        self.assertAlmostEqual(sum(POLICY["weights"].values()), 1.0)

    def test_factor_extremes_are_deterministic(self):
        self.assertEqual(score({name: "NONE" for name in POLICY["weights"]}), 0)
        self.assertEqual(score({name: "STRONG" for name in POLICY["weights"]}), 100)

    def test_partial_factor_set_fails_closed(self):
        with self.assertRaises(ValueError):
            score({"remixability": "STRONG"})

    def test_policy_reasons_are_supported_by_v2_schema(self):
        schema_reasons = set(
            SCHEMA["properties"]["hard_reject_reasons"]["items"]["enum"]
        )
        self.assertEqual(set(POLICY["hard_reject_classes"]), schema_reasons)

    def test_policy_content_classes_are_supported_by_v2_schema(self):
        schema_classes = set(SCHEMA["properties"]["content_class"]["enum"])
        self.assertEqual(set(POLICY["content_classes"]), schema_classes)

    def test_public_threshold_is_stricter_than_review_threshold(self):
        public_minimum = POLICY["thresholds"]["public_candidate"][
            "minimum_coinability_score"
        ]
        review_minimum = POLICY["thresholds"]["human_review"][
            "minimum_coinability_score"
        ]
        self.assertGreater(public_minimum, review_minimum)

    def test_numeric_coinability_belongs_to_backend(self):
        self.assertTrue(
            POLICY["policy"]["deterministic_code_owns_numeric_coinability_score"]
        )
        self.assertNotIn("coinability_score", SCHEMA["properties"])


if __name__ == "__main__":
    unittest.main()
