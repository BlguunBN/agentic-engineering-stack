"""Tests for explicit checkpoints and independent output benchmark variants."""

import json
from pathlib import Path
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.benchmark_context import main as benchmark_main
from scripts.checkpoint import main as checkpoint_main


class ContextToolTests(unittest.TestCase):
    def test_rtk_is_disabled_for_the_counterproductive_git_status_workload(self):
        spec = json.loads((ROOT / "benchmarks" / "context_workloads.json").read_text(encoding="utf-8"))
        workload = next(row for row in spec["workloads"] if row["name"] == "git-status")
        self.assertIsNone(workload["commands"]["rtk"])
        self.assertEqual(["git", "status", "--short"], workload["commands"]["baseline"])

    def test_checkpoint_preview_is_redacted_and_does_not_persist(self):
        with tempfile.TemporaryDirectory() as temp:
            state_root = Path(temp) / "state"
            output = StringIO()
            with redirect_stdout(output):
                code = checkpoint_main([
                    "--task-id", "task-1", "--objective", "Use api_key=ABCDEFGHIJKLMNOPQRST safely",
                    "--usage-ratio", "0.82", "--checkpoint-threshold", "0.75",
                    "--repo", temp, "--state-root", str(state_root),
                ])
            result = json.loads(output.getvalue())
            self.assertEqual(code, 0)
            self.assertFalse(result["persisted"])
            self.assertTrue(result["checkpoint_recommended"])
            self.assertIn("[REDACTED]", result["preview"])
            self.assertFalse(state_root.exists())

    def test_checkpoint_persistence_requires_opt_in_and_writes_three_small_files(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            output = StringIO()
            with redirect_stdout(output):
                checkpoint_main([
                    "--task-id", "task-2", "--objective", "Refactor parser", "--remaining", "Run integration tests",
                    "--repo", temp, "--state-root", ".state", "--persist",
                ])
            target = root / ".state" / "task-2"
            self.assertEqual({path.name for path in target.iterdir()}, {"state.md", "handoff.md", "verification.json"})
            self.assertIn("Run integration tests", (target / "handoff.md").read_text(encoding="utf-8"))

    def test_compression_variants_run_independently_and_keep_required_markers(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            spec = root / "workloads.json"
            spec.write_text(json.dumps({
                "schema_version": 1,
                "workloads": [{
                    "name": "diagnostic", "expected_exit_code": 0,
                    "must_contain": ["Traceback", "AssertionError"],
                    "commands": {
                        "baseline": [sys.executable, "-c", "print('Traceback'); print('AssertionError')"],
                        "rtk": [sys.executable, "-c", "print('Traceback'); print('AssertionError')"],
                        "sqz": None,
                    },
                }],
            }), encoding="utf-8")
            with redirect_stdout(StringIO()):
                code = benchmark_main(["--spec", str(spec), "--repo", temp, "--output-dir", "results", "--repeats", "2"])
            report = json.loads((root / "results" / "report.json").read_text(encoding="utf-8"))
            self.assertEqual(code, 0)
            self.assertTrue(report["quality_ok"])
            self.assertFalse(report["coverage_complete"])
            self.assertEqual(report["workloads"][0]["variants"]["sqz"]["status"], "not-configured")
            baseline = report["workloads"][0]["variants"]["baseline"]
            self.assertEqual(2, baseline["trial_count"])
            self.assertEqual(2, len(baseline["trials"]))
            self.assertTrue((root / "results" / "diagnostic.baseline.r1.log").is_file())
            self.assertTrue((root / "results" / "diagnostic.rtk.r2.log").is_file())


if __name__ == "__main__":
    unittest.main()
