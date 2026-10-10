#!/usr/bin/env python3
"""Validate and summarize repeated baseline/Stack engineering-eval trials."""

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import statistics
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from stack_manifest import load_manifest

TRIAL_FIELDS = {
    "task_id", "variant", "trial", "task_success", "regression_tests_passed",
    "startup_tokens", "provider_tokens", "latency_ms", "tool_calls",
    "skill_activations", "artifact_path",
}


def _median(rows: list[dict[str, Any]], field: str) -> int | None:
    values = [row[field] for row in rows if row[field] is not None]
    return int(statistics.median(values)) if values else None


def build_report(cases: dict[str, Any], trials: Any, repo_root: Path, repeats: int) -> dict[str, Any]:
    errors: list[str] = []
    if cases.get("schema_version") != 1 or not isinstance(cases.get("cases"), list):
        return {"errors": ["invalid engineering case schema"]}
    variants = cases.get("variants")
    if not isinstance(variants, list) or not variants or not all(isinstance(v, str) for v in variants):
        return {"errors": ["variants must be a non-empty string list"]}
    if not isinstance(trials, list):
        return {"errors": ["trials must be a JSON list"]}
    by_task = {case.get("task_id"): case for case in cases["cases"] if isinstance(case, dict) and isinstance(case.get("task_id"), str)}
    if len(by_task) != len(cases["cases"]):
        return {"errors": ["case task_id values must be unique strings"]}
    for task_id, case in by_task.items():
        required = case.get("required_skill_ids")
        if not isinstance(required, list) or not all(isinstance(skill, str) for skill in required):
            errors.append(f"case {task_id}: required_skill_ids must be a string list")
    known_ids = {entry["id"] for entry in load_manifest()["capabilities"]}
    for task_id, case in by_task.items():
        if isinstance(case.get("required_skill_ids"), list):
            unknown = sorted(set(case["required_skill_ids"]) - known_ids)
            if unknown:
                errors.append(f"case {task_id}: required skills are not canonical IDs: {unknown}")
    expected = {(task_id, variant, trial_no) for task_id in by_task for variant in variants for trial_no in range(1, repeats + 1)}
    observed: dict[tuple[str, str, int], dict[str, Any]] = {}
    seen_artifacts: set[str] = set()
    for index, row in enumerate(trials):
        if not isinstance(row, dict) or set(row) != TRIAL_FIELDS:
            errors.append(f"trial {index}: fields must be exactly {sorted(TRIAL_FIELDS)}")
            continue
        task_id, variant, trial_no = row["task_id"], row["variant"], row["trial"]
        if not isinstance(task_id, str) or not isinstance(variant, str) or isinstance(trial_no, bool) or not isinstance(trial_no, int):
            errors.append(f"trial {index}: task_id/variant must be strings and trial must be an integer")
            continue
        key = (task_id, variant, trial_no)
        if key not in expected:
            errors.append(f"trial {index}: unexpected task/variant/trial key {key!r}")
            continue
        if key in observed:
            errors.append(f"trial {index}: duplicate trial key {key!r}")
            continue
        for field in ("task_success", "regression_tests_passed"):
            if not isinstance(row[field], bool):
                errors.append(f"trial {index}: {field} must be boolean")
        for field in ("startup_tokens", "latency_ms", "tool_calls"):
            if isinstance(row[field], bool) or not isinstance(row[field], int) or row[field] < 0:
                errors.append(f"trial {index}: {field} must be a non-negative integer")
        provider = row["provider_tokens"]
        if provider is not None and (isinstance(provider, bool) or not isinstance(provider, int) or provider < 0):
            errors.append(f"trial {index}: provider_tokens must be null or a non-negative integer")
        activated = row["skill_activations"]
        if not isinstance(activated, list) or not all(isinstance(item, str) for item in activated):
            errors.append(f"trial {index}: skill_activations must be a string list")
        artifact = row["artifact_path"]
        if not isinstance(artifact, str) or not artifact:
            errors.append(f"trial {index}: artifact_path must be a non-empty path")
        else:
            path = (repo_root / artifact).resolve()
            try:
                path.relative_to(repo_root.resolve())
            except ValueError:
                errors.append(f"trial {index}: artifact escapes repository root")
            else:
                normalized_artifact = str(path)
                if normalized_artifact in seen_artifacts:
                    errors.append(f"trial {index}: artifact path must be unique: {artifact}")
                seen_artifacts.add(normalized_artifact)
                if not path.is_file():
                    errors.append(f"trial {index}: artifact does not exist: {artifact}")
        observed[key] = row
    missing = sorted(expected - observed.keys())
    if missing:
        errors.append(f"missing repeated trials: {missing[:10]}" + (" ..." if len(missing) > 10 else ""))
    if errors:
        return {"schema_version": 1, "errors": errors}

    summary = {}
    for variant in variants:
        rows = [observed[key] for key in sorted(observed) if key[1] == variant]
        total = len(rows)
        task_successes = sum(row["task_success"] for row in rows)
        regression_passes = sum(row["regression_tests_passed"] for row in rows)
        unnecessary = 0
        required_count = 0
        for row in rows:
            required = set(by_task[row["task_id"]].get("required_skill_ids", []))
            required_count += len(required)
            unnecessary += sum(skill not in required for skill in row["skill_activations"])
        summary[variant] = {
            "trials": total,
            "task_success_rate": round(task_successes / total, 4) if total else None,
            "regression_test_pass_rate": round(regression_passes / total, 4) if total else None,
            "startup_tokens_median": _median(rows, "startup_tokens"),
            "provider_tokens_median": _median(rows, "provider_tokens"),
            "latency_ms_median": _median(rows, "latency_ms"),
            "tool_calls_median": _median(rows, "tool_calls"),
            "invalid_activations": sum(1 for row in rows for skill in row["skill_activations"] if skill not in known_ids),
            "unnecessary_activations": unnecessary,
            "required_skill_reference_count": required_count,
        }
    return {
        "schema_version": 1,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "repeats_per_task_variant": repeats,
        "case_count": len(by_task),
        "variants": summary,
        "trials": trials,
        "limitations": [
            "Provider token values remain null unless measured by the host/provider and supplied in trial data.",
            "The evaluator validates and aggregates external trials; it does not claim synthetic fixture runs are model-quality comparisons.",
            "Successes and failures are retained verbatim with artifact paths.",
        ],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", type=Path, default=ROOT / "evals" / "engineering" / "cases.json")
    parser.add_argument("--trials", type=Path, required=True, help="JSON list containing every variant/task/repeat result")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--repo", type=Path, default=ROOT)
    parser.add_argument("--repeats", type=int, default=3)
    args = parser.parse_args(argv)
    if not 1 <= args.repeats <= 20:
        parser.error("--repeats must be between 1 and 20")
    try:
        cases = json.loads(args.cases.read_text(encoding="utf-8"))
        trials = json.loads(args.trials.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        parser.error(f"Cannot read evaluation input: {exc}")
    report = build_report(cases, trials, args.repo.resolve(), args.repeats)
    output = args.output if args.output.is_absolute() else args.repo / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    print(f"Report: {output}")
    return 1 if report.get("errors") else 0


if __name__ == "__main__":
    raise SystemExit(main())
