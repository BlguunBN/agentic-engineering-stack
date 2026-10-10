"""Tests for conservative delegation policy and structured handoff shape."""

from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.validate_handoff import validate_handoff, validate_policy


class DelegationTests(unittest.TestCase):
    def test_policy_caps_workers_and_matches_risk_levels(self):
        import json
        policy = json.loads((ROOT / "delegation" / "policy.json").read_text(encoding="utf-8"))
        self.assertEqual(validate_policy(policy), [])
        self.assertFalse(policy["levels"]["small"]["delegate"])
        self.assertEqual(policy["levels"]["high-risk"]["max_workers"], 2)
        self.assertTrue(policy["levels"]["high-risk"]["requires_independent_review"])

    def test_compact_handoff_is_accepted(self):
        import json
        example = json.loads((ROOT / "delegation" / "examples" / "worker-handoff.json").read_text(encoding="utf-8"))
        self.assertEqual(validate_handoff(example), [])
        handoff = {
            "task_id": "review-auth-001",
            "status": "completed",
            "files_examined": ["src/auth/session.py"],
            "findings": [{"path": "src/auth/session.py", "line": 87, "issue": "Refresh-token check absent", "severity": "high"}],
            "tests_run": ["python -m unittest tests.test_auth"],
            "next_action": "Add refresh-token validation and regression coverage",
        }
        self.assertEqual(validate_handoff(handoff), [])

    def test_unbounded_or_malformed_handoffs_are_rejected(self):
        handoff = {
            "task_id": "task", "status": "completed", "files_examined": ["../../secrets.env"],
            "findings": [{"path": "/etc/passwd", "issue": "bad", "severity": "urgent"}],
            "tests_run": [], "next_action": "fix", "transcript": "not allowed",
        }
        errors = validate_handoff(handoff)
        self.assertTrue(any("unsupported fields" in error for error in errors))
        self.assertTrue(any("repository-relative" in error for error in errors))
        self.assertTrue(any("invalid severity" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
