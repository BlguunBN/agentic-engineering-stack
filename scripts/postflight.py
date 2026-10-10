#!/usr/bin/env python3
"""Require workflow-specific verification receipts before reporting completion."""

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from workflow_checks import WorkflowError, verify_postflight


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=ROOT)
    parser.add_argument("--workflow", required=True)
    parser.add_argument("--receipt", action="append", default=[], help="Evidence receipt, repeat per check")
    parser.add_argument("--report", type=Path, help="Draft completion report to validate")
    parser.add_argument("--not-run-reason", help="Explicit reason verification was not run (cannot waive required evidence)")
    args = parser.parse_args(argv)
    report_text = ""
    if args.report:
        try:
            report_path = (args.repo.resolve() / args.report).resolve()
            report_path.relative_to(args.repo.resolve())
            report_text = report_path.read_text(encoding="utf-8")
        except (OSError, ValueError) as exc:
            parser.error(f"Cannot read in-repository report: {exc}")
    try:
        result = verify_postflight(args.repo, args.workflow, args.receipt, report_text, args.not_run_reason)
    except WorkflowError as exc:
        parser.error(str(exc))
    print(json.dumps(result, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
