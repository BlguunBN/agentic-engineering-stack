#!/usr/bin/env python3
"""Check changed-file scope and likely secret exposure before work proceeds."""

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from workflow_checks import WorkflowError, preflight


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=ROOT)
    parser.add_argument("--workflow", required=True)
    parser.add_argument("--scope", nargs="*", default=[], help="Optional allowed changed-file path prefixes")
    args = parser.parse_args(argv)
    try:
        result = preflight(args.repo, args.workflow, args.scope)
    except WorkflowError as exc:
        parser.error(str(exc))
    print(json.dumps(result, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
