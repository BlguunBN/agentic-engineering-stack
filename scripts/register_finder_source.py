#!/usr/bin/env python3
"""Register the Stack source through Finder Contract v1 without activating skills."""

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from adapters.finder_contract import FinderContractClient
from adapters.finder_mcp import FinderMCPClient
from stack_manifest import load_manifest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--finder-root", type=Path, required=True, help="Finder checkout containing capability_mcp.py and library_catalog.py")
    parser.add_argument("--python", default=sys.executable, help="Python executable used to start Finder")
    parser.add_argument("--agent", help="Optional host name for compatibility checks")
    parser.add_argument("--dry-run", action="store_true", help="Check contract and manifest without registration")
    args = parser.parse_args(argv)
    manifest = ROOT / "stack.manifest.json"
    data = load_manifest(manifest)
    finder_root = args.finder_root.resolve()
    command = [args.python, str(finder_root / "capability_mcp.py")]
    try:
        with FinderMCPClient(command, finder_root=finder_root, agent=args.agent) as finder:
            client = FinderContractClient(finder)
            if args.dry_run:
                print(json.dumps({"contract_version": 1, "namespace": data["namespace"], "skills": len(data["capabilities"]), "registration": "not-performed"}, indent=2))
                return 0
            ids = client.register_stack(manifest)
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"Finder registration failed: {exc}", file=sys.stderr)
        return 1
    print(json.dumps({"contract_version": 1, "namespace": data["namespace"], "registered_ids": ids, "activated": False}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
