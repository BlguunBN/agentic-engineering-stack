#!/usr/bin/env python3
"""Validate a structured, compact delegation handoff using only Python stdlib."""

import argparse
import json
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SEVERITIES = {"critical", "high", "medium", "low", "info"}
STATUSES = {"completed", "blocked", "needs-review"}


def validate_policy(value: Any) -> list[str]:
    errors = []
    if not isinstance(value, dict) or value.get("schema_version") != 1:
        return ["policy must be an object with schema_version 1"]
    max_concurrency = value.get("max_concurrency")
    default_concurrency = value.get("default_concurrency")
    if (
        isinstance(max_concurrency, bool) or max_concurrency not in (1, 2)
        or isinstance(default_concurrency, bool) or default_concurrency not in (1, 2)
        or (isinstance(default_concurrency, int) and isinstance(max_concurrency, int) and default_concurrency > max_concurrency)
    ):
        errors.append("concurrency must be bounded to one or two workers")
    levels = value.get("levels")
    if not isinstance(levels, dict) or set(levels) != {"small", "moderate", "large", "high-risk"}:
        errors.append("policy must define small/moderate/large/high-risk levels")
    return errors


def validate_handoff(value: Any) -> list[str]:
    errors = []
    required = {"task_id", "status", "files_examined", "findings", "tests_run", "next_action"}
    if not isinstance(value, dict):
        return ["handoff must be a JSON object"]
    missing = required - value.keys()
    extra = value.keys() - required
    if missing:
        errors.append(f"missing fields: {', '.join(sorted(missing))}")
    if extra:
        errors.append(f"unsupported fields: {', '.join(sorted(extra))}")
    if not isinstance(value.get("task_id"), str) or not value["task_id"].strip():
        errors.append("task_id must be a non-empty string")
    if value.get("status") not in STATUSES:
        errors.append("status must be completed, blocked, or needs-review")
    for key in ("files_examined", "tests_run"):
        items = value.get(key)
        if not isinstance(items, list) or not all(isinstance(item, str) for item in items):
            errors.append(f"{key} must be a string list")
    for path in value.get("files_examined", []) if isinstance(value.get("files_examined"), list) else []:
        if Path(path).is_absolute() or ".." in Path(path).parts:
            errors.append(f"files_examined path must be repository-relative: {path}")
    findings = value.get("findings")
    if not isinstance(findings, list):
        errors.append("findings must be a list")
    else:
        for index, finding in enumerate(findings):
            if not isinstance(finding, dict) or set(finding) - {"path", "line", "issue", "severity"}:
                errors.append(f"finding {index} has invalid shape")
                continue
            if not isinstance(finding.get("path"), str) or not finding["path"].strip() or not isinstance(finding.get("issue"), str) or not finding["issue"].strip():
                errors.append(f"finding {index} requires path and issue")
            if Path(finding.get("path", "")).is_absolute() or ".." in Path(finding.get("path", "")).parts:
                errors.append(f"finding {index} path must be repository-relative")
            line = finding.get("line")
            if line is not None and (isinstance(line, bool) or not isinstance(line, int) or line < 1):
                errors.append(f"finding {index} line must be null or positive integer")
            if finding.get("severity") not in SEVERITIES:
                errors.append(f"finding {index} has invalid severity")
    if not isinstance(value.get("next_action"), str):
        errors.append("next_action must be a string")
    return errors


def _load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--policy", type=Path, default=ROOT / "delegation" / "policy.json")
    parser.add_argument("--handoff", type=Path)
    args = parser.parse_args(argv)
    errors = []
    try:
        errors.extend(f"policy: {error}" for error in validate_policy(_load(args.policy)))
        if args.handoff:
            errors.extend(f"handoff: {error}" for error in validate_handoff(_load(args.handoff)))
    except (OSError, json.JSONDecodeError) as exc:
        parser.error(f"Cannot read JSON input: {exc}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("Delegation policy/handoff valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
