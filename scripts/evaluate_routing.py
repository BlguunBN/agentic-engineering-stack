#!/usr/bin/env python3
"""Evaluate deterministic routing cases and report positive/negative accuracy."""

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from routing import RoutingError, route_task
from stack_manifest import load_manifest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", type=Path, default=ROOT / "evals" / "routing" / "cases.json")
    args = parser.parse_args(argv)
    try:
        cases = json.loads(args.cases.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        parser.error(f"Cannot read routing cases: {exc}")
    if not isinstance(cases, dict) or cases.get("schema_version") != 1 or not isinstance(cases.get("cases"), list):
        parser.error("Invalid routing eval schema")
    if not all(isinstance(case, dict) for case in cases["cases"]):
        parser.error("Every routing case must be a JSON object")
    expected_suites = {entry["id"].removeprefix("aes:skill:") for entry in load_manifest()["capabilities"]}
    positive_suites = {case.get("suite") for case in cases["cases"] if case.get("label") == "positive"}
    negative_suites = {case.get("suite") for case in cases["cases"] if case.get("label") == "negative"} & expected_suites
    positive_counts = {suite: sum(case.get("suite") == suite and case.get("label") == "positive" for case in cases["cases"]) for suite in expected_suites}
    if positive_suites != expected_suites:
        parser.error(f"Positive cases must cover all canonical suites; missing={sorted(expected_suites-positive_suites)}, extra={sorted(positive_suites-expected_suites)}")
    if negative_suites != expected_suites:
        parser.error(f"Negative cases must cover all canonical suites; missing={sorted(expected_suites-negative_suites)}")
    undercovered = sorted(suite for suite, count in positive_counts.items() if count < 2)
    if undercovered:
        parser.error(f"Each canonical suite needs at least two positive cases; undercovered={undercovered}")

    results = []
    totals = {"positive": [0, 0], "negative": [0, 0]}
    for index, case in enumerate(cases["cases"]):
        try:
            if not isinstance(case, dict):
                raise KeyError("case must be an object")
            decision = route_task(case["task"], case["profile"], finder_available=True)
            passed = decision.tier == case["expected_tier"] and decision.primary == case["expected_primary"]
            actual = {"tier": decision.tier, "primary": decision.primary, "alternatives": list(decision.alternatives)}
        except (KeyError, RoutingError) as exc:
            passed = False
            actual = {"error": str(exc)}
        label = case.get("label")
        if label not in totals:
            parser.error(f"Case {index} label must be positive or negative")
        totals[label][1] += 1
        totals[label][0] += int(passed)
        results.append({"case": index, "suite": case.get("suite"), "label": label, "passed": passed, "expected": {"tier": case.get("expected_tier"), "primary": case.get("expected_primary")}, "actual": actual})
    report = {"schema_version": 1, "total": len(results), "passed": sum(result["passed"] for result in results), "positive": {"passed": totals["positive"][0], "total": totals["positive"][1]}, "negative": {"passed": totals["negative"][0], "total": totals["negative"][1]}, "failures": [result for result in results if not result["passed"]]}
    print(json.dumps(report, indent=2))
    return 0 if not report["failures"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
