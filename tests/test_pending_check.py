import importlib.util
import pathlib
import unittest


SCRIPT_PATH = (
    pathlib.Path(__file__).resolve().parents[1]
    / "hermes"
    / "scripts"
    / "trnd-pending-check.py"
)
SPEC = importlib.util.spec_from_file_location("trnd_pending_check", SCRIPT_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


class PendingCheckTests(unittest.TestCase):
    def test_zero_candidates_skips_agent(self):
        self.assertEqual(MODULE.build_gate_output(0), {"wakeAgent": False})

    def test_candidates_wake_agent_with_context(self):
        self.assertEqual(
            MODULE.build_gate_output(3),
            {
                "wakeAgent": True,
                "context": {
                    "pending_candidates": 3,
                    "source": "trend-brain-internal-api",
                },
            },
        )

    def test_valid_pending_count(self):
        self.assertEqual(MODULE.parse_pending_count({"pending_count": 4}), 4)

    def test_rejects_boolean(self):
        with self.assertRaises(ValueError):
            MODULE.parse_pending_count({"pending_count": True})

    def test_rejects_negative_count(self):
        with self.assertRaises(ValueError):
            MODULE.parse_pending_count({"pending_count": -1})

    def test_rejects_missing_count(self):
        with self.assertRaises(ValueError):
            MODULE.parse_pending_count({})


if __name__ == "__main__":
    unittest.main()
