"""End-to-end tests for workflow preflight, receipts, and approvals."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.approval_gate import main as approval_main
from scripts.run_check import main as run_check_main
from workflow_checks import load_workflow, preflight, verify_postflight


class WorkflowCheckTests(unittest.TestCase):
    def test_all_workflow_profiles_load(self):
        names = {path.stem for path in (ROOT / "workflows").glob("*.json")}
        self.assertEqual(names, {"bugfix", "feature", "refactor", "ui", "review", "infrastructure", "small-change"})
        for name in names:
            self.assertEqual(load_workflow(name)["name"], name)

    def test_bugfix_cannot_claim_completion_without_regression_receipt(self):
        result = verify_postflight(ROOT, "bugfix", [], "Fix complete. Tests passed.")
        self.assertFalse(result["ok"])
        self.assertIn("regression", result["missing_evidence"])
        self.assertTrue(any("tests passed without" in error for error in result["errors"]))

    def test_receipt_gates_bugfix_completion_and_detects_log_tampering(self):
        with tempfile.TemporaryDirectory(prefix="aes-evidence-", dir=ROOT) as temp:
            receipt = (Path(temp) / "regression.json").relative_to(ROOT).as_posix()
            with redirect_stdout(StringIO()):
                result_code = run_check_main([
                    "--kind", "regression", "--repo", str(ROOT), "--receipt", receipt, "--",
                    sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_bugfix_fixture.py",
                ])
            self.assertEqual(result_code, 0)
            result = verify_postflight(ROOT, "bugfix", [receipt], "Fix verified; regression test passed.")
            self.assertTrue(result["ok"], result["errors"])
            receipt_data = json.loads((ROOT / receipt).read_text(encoding="utf-8"))
            (ROOT / receipt_data["log_path"]).write_text("tampered", encoding="utf-8")
            tampered = verify_postflight(ROOT, "bugfix", [receipt])
            self.assertTrue(any("hash mismatch" in error for error in tampered["errors"]))

    def test_preflight_reports_scope_and_secret_issues(self):
        with tempfile.TemporaryDirectory(prefix="aes-preflight-") as temp:
            repo = Path(temp)
            subprocess.run(["git", "init", "--quiet", str(repo)], check=True)
            (repo / "src").mkdir()
            (repo / "src" / "safe.py").write_text("print('ok')\n", encoding="utf-8")
            allowed = preflight(repo, "small-change", ["src"])
            self.assertTrue(allowed["ok"], allowed)
            (repo / "elsewhere").mkdir()
            secret_value = "ABCDEFGHIJKLMNOP" + "QRSTUVWX"
            (repo / "elsewhere" / "credentials.txt").write_text(f"secret = '{secret_value}'\n", encoding="utf-8")
            blocked = preflight(repo, "small-change", ["src"])
            self.assertFalse(blocked["ok"])
            self.assertTrue(blocked["scope_errors"])
            self.assertTrue(blocked["secret_findings"])

    def test_approval_gate_requires_exact_human_record(self):
        with redirect_stdout(StringIO()):
            self.assertEqual(approval_main(["--action", "deploy", "--target", "production"]), 3)
        with tempfile.TemporaryDirectory() as temp:
            record = Path(temp) / "approval.json"
            record.write_text(json.dumps({
                "approved": True, "action": "deploy", "target": "production",
                "approved_by": "reviewer", "reference": "CHANGE-123", "approved_at": "2026-09-29T00:00:00Z"
            }), encoding="utf-8")
            with redirect_stdout(StringIO()):
                self.assertEqual(approval_main(["--action", "deploy", "--target", "production", "--approval-file", str(record)]), 0)
                self.assertEqual(approval_main(["--action", "delete", "--target", "production", "--approval-file", str(record)]), 3)


if __name__ == "__main__":
    unittest.main()
