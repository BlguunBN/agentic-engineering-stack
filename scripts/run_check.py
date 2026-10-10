#!/usr/bin/env python3
"""Run one argv-based verification command and write an integrity-linked receipt."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
KINDS = ("test", "unit", "regression", "lint", "syntax", "build", "ui", "validate", "plan", "review", "security")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kind", required=True, choices=KINDS)
    parser.add_argument("--repo", type=Path, default=ROOT)
    parser.add_argument("--receipt", type=Path, required=True, help="Receipt path inside repository")
    parser.add_argument("--timeout", type=int, default=1800)
    parser.add_argument("command", nargs=argparse.REMAINDER, help="Command argv after --; no shell is used")
    args = parser.parse_args(argv)
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    if not command:
        parser.error("provide a command after --")
    root = args.repo.resolve()
    receipt_path = (root / args.receipt).resolve()
    try:
        receipt_path.relative_to(root)
    except ValueError:
        parser.error("--receipt must be inside --repo")
    if args.timeout <= 0:
        parser.error("--timeout must be positive")

    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    log_path = receipt_path.with_suffix(".log")
    started = datetime.now(timezone.utc).isoformat()
    timed_out = False
    try:
        with log_path.open("wb") as log_file:
            result = subprocess.run(command, cwd=root, stdout=log_file, stderr=subprocess.STDOUT, timeout=args.timeout, check=False)
        exit_code = result.returncode
    except subprocess.TimeoutExpired:
        exit_code = 124
        timed_out = True
    except OSError as exc:
        log_path.write_text(f"Unable to start command: {exc}\n", encoding="utf-8")
        exit_code = 127

    log_hash = hashlib.sha256(log_path.read_bytes()).hexdigest()
    receipt = {
        "schema_version": 1,
        "kind": args.kind,
        "command": command,
        "cwd": ".",
        "started_at": started,
        "finished_at": datetime.now(timezone.utc).isoformat(),
        "exit_code": exit_code,
        "timed_out": timed_out,
        "log_path": log_path.relative_to(root).as_posix(),
        "log_sha256": log_hash,
    }
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(f"{args.kind}: exit={exit_code}; receipt={receipt_path.relative_to(root).as_posix()}; log={log_path.relative_to(root).as_posix()}")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
