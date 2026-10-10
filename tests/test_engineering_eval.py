"""Tests for the auditable repeated engineering-evaluation aggregator."""

import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.evaluate_engineering import TRIAL_FIELDS, build_report


class EngineeringEvalTests(unittest.TestCase):
    def _fixture_trials(self, cases, root):
        rows = []
        for case in cases["cases"]:
            for variant in cases["variants"]:
                artifact = root / "artifacts" / f"{case['task_id']}.{variant}.log"
                artifact.parent.mkdir(parents=True, exist_ok=True)
                artifact.write_text("captured success or failure evidence\n", encoding="utf-8")
                rows.append({
                    "task_id": case["task_id"], "variant": variant, "trial": 1,
                    "task_success": variant != "baseline", "regression_tests_passed": True,
                    "startup_tokens": 100 if variant == "baseline" else 50,
                    "provider_tokens": None if variant == "baseline" else 120,
                    "latency_ms": 1000, "tool_calls": 3,
                    "skill_activations": [case["required_skill_ids"][0]],
                    "artifact_path": str(artifact.relative_to(root)),
                })
        rows[-1]["skill_activations"].append("aes:skill:not-real")
        return rows

    def test_report_preserves_trials_and_reports_invalid_activations(self):
        cases = json.loads((ROOT / "evals" / "engineering" / "cases.json").read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as temp:
            repo = Path(temp)
            trials = self._fixture_trials(cases, repo)
            report = build_report(cases, trials, repo, repeats=1)
        self.assertNotIn("errors", report)
        self.assertEqual(3, report["case_count"])
        self.assertEqual(3, report["variants"]["new-stack"]["trials"])
        self.assertEqual(1, report["variants"]["new-stack"]["invalid_activations"])
        self.assertIsNone(report["variants"]["baseline"]["provider_tokens_median"])
        self.assertEqual(9, len(report["trials"]))

    def test_missing_or_escaping_trials_are_rejected(self):
        cases = json.loads((ROOT / "evals" / "engineering" / "cases.json").read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as temp:
            repo = Path(temp)
            trials = self._fixture_trials(cases, repo)
            trials.pop()
            report = build_report(cases, trials, repo, repeats=1)
        self.assertTrue(any("missing repeated trials" in error for error in report["errors"]))
        self.assertEqual({
            "task_id", "variant", "trial", "task_success", "regression_tests_passed",
            "startup_tokens", "provider_tokens", "latency_ms", "tool_calls",
            "skill_activations", "artifact_path",
        }, TRIAL_FIELDS)


if __name__ == "__main__":
    unittest.main()
