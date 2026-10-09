#!/usr/bin/env python3
"""Emit one deterministic Stack routing decision as JSON."""

import argparse
from dataclasses import asdict
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from routing import RoutingError, route_task


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task", required=True, help="Task description to route")
    parser.add_argument("--profile", default="core", help="minimal/core/frontend/infrastructure/research/strict")
    parser.add_argument("--skill-id", help="Optional exact canonical aes:skill:<name> ID")
    parser.add_argument("--finder-unavailable", action="store_true", help="Report an explicit standalone fallback")
    args = parser.parse_args(argv)
    try:
        decision = route_task(
            args.task,
            args.profile,
            skill_id=args.skill_id,
            finder_available=not args.finder_unavailable,
        )
    except RoutingError as exc:
        parser.error(str(exc))
    print(json.dumps(asdict(decision), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
