"""Regression check for the maintained routing evaluation fixture."""

import json
from pathlib import Path
import sys
import unittest
from contextlib import redirect_stdout
from io import StringIO

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.evaluate_routing import main


class RoutingEvalTests(unittest.TestCase):
    def test_all_18_suites_have_positive_and_negative_cases(self):
        output = StringIO()
        with redirect_stdout(output):
            status = main(["--cases", str(ROOT / "evals" / "routing" / "cases.json")])
        report = json.loads(output.getvalue())
        self.assertEqual(status, 0, report["failures"])
        self.assertEqual(report["total"], 38)
        self.assertEqual(report["positive"], {"passed": 18, "total": 18})
        self.assertEqual(report["negative"], {"passed": 20, "total": 20})


if __name__ == "__main__":
    unittest.main()
