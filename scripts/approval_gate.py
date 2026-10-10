#!/usr/bin/env python3
"""Require an explicit matching approval record before a risky operation."""

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path

ACTIONS = ("delete", "deploy", "apply", "modify-secrets", "install-third-party")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--action", choices=ACTIONS, required=True)
    parser.add_argument("--target", required=True, help="Exact resource/path/environment in scope")
    parser.add_argument("--approval-file", type=Path, help="Human-authored approval JSON record")
    args = parser.parse_args(argv)
    if not args.approval_file:
        print(json.dumps({"authorized": False, "action": args.action, "target": args.target, "reason": "explicit approval record required"}))
        return 3
    try:
        record = json.loads(args.approval_file.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        parser.error(f"Cannot read approval record: {exc}")
    required = ("approved_by", "reference", "approved_at")
    valid = (
        isinstance(record, dict)
        and record.get("approved") is True
        and record.get("action") == args.action
        and record.get("target") == args.target
        and all(isinstance(record.get(field), str) and record[field].strip() for field in required)
    )
    if not valid:
        print(json.dumps({"authorized": False, "action": args.action, "target": args.target, "reason": "approval record missing or does not exactly match request"}))
        return 3
    print(json.dumps({
        "authorized": True,
        "action": args.action,
        "target": args.target,
        "approved_by": record["approved_by"],
        "reference": record["reference"],
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "note": "Gate decision only; this tool does not execute the operation.",
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
