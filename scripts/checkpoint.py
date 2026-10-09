#!/usr/bin/env python3
"""Create a redacted task checkpoint only when the user explicitly opts in."""

import argparse
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SECRET_ASSIGNMENT = re.compile(r"(?i)\b(api[_-]?key|access[_-]?token|secret|password)\s*([:=])\s*(['\"]?)[A-Za-z0-9/+=_.-]{12,}")
PRIVATE_KEY = re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----.*?-----END (?:RSA |EC |OPENSSH )?PRIVATE KEY-----", re.DOTALL)
AWS_KEY = re.compile(r"\bAKIA[0-9A-Z]{16}\b")


def redact(value: str) -> str:
    value = PRIVATE_KEY.sub("[REDACTED_PRIVATE_KEY]", value)
    value = AWS_KEY.sub("[REDACTED_AWS_KEY]", value)
    return SECRET_ASSIGNMENT.sub(lambda match: f"{match.group(1)}{match.group(2)}[REDACTED]", value)


def _list(values: list[str]) -> str:
    return "\n".join(f"- {redact(value)}" for value in values) if values else "- None recorded"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--objective", required=True)
    parser.add_argument("--constraint", action="append", default=[])
    parser.add_argument("--decision", action="append", default=[])
    parser.add_argument("--changed-file", action="append", default=[])
    parser.add_argument("--remaining", action="append", default=[])
    parser.add_argument("--receipt", action="append", default=[], help="In-repository verification receipt; only summary is saved")
    parser.add_argument("--repo", type=Path, default=ROOT)
    parser.add_argument("--state-root", type=Path, default=Path(".agent-state/tasks"))
    parser.add_argument("--usage-ratio", type=float, help="Optional host-provided used-context ratio from 0 to 1")
    parser.add_argument("--checkpoint-threshold", type=float, default=0.75)
    parser.add_argument("--persist", action="store_true", help="Write state.md, handoff.md and verification.json")
    args = parser.parse_args(argv)
    if not re.fullmatch(r"[a-zA-Z0-9_-]+", args.task_id):
        parser.error("--task-id may contain only letters, digits, underscore, and hyphen")
    for value, label in ((args.checkpoint_threshold, "--checkpoint-threshold"), (args.usage_ratio, "--usage-ratio")):
        if value is not None and not 0 <= value <= 1:
            parser.error(f"{label} must be between 0 and 1")

    repo = args.repo.resolve()
    evidence = []
    for value in args.receipt:
        path = (repo / value).resolve()
        try:
            relative = path.relative_to(repo).as_posix()
            receipt = json.loads(path.read_text(encoding="utf-8"))
        except (ValueError, OSError, json.JSONDecodeError) as exc:
            parser.error(f"Invalid in-repository receipt {value}: {exc}")
        if not isinstance(receipt, dict):
            parser.error(f"Invalid receipt object: {value}")
        evidence.append({"path": relative, "kind": receipt.get("kind"), "exit_code": receipt.get("exit_code"), "log_sha256": receipt.get("log_sha256")})

    ratio = args.usage_ratio
    recommended = ratio is not None and ratio >= args.checkpoint_threshold
    state = (
        f"# Task checkpoint: {args.task_id}\n\n"
        f"## Objective\n{redact(args.objective)}\n\n"
        f"## Constraints\n{_list(args.constraint)}\n\n"
        f"## Decisions\n{_list(args.decision)}\n\n"
        f"## Changed files\n{_list(args.changed_file)}\n\n"
        f"## Verification\n{_list([item['path'] + ': ' + str(item['kind']) + ' exit=' + str(item['exit_code']) for item in evidence])}\n\n"
        f"## Remaining work\n{_list(args.remaining)}\n\n"
        f"Context usage ratio: {ratio if ratio is not None else 'not provided'}; checkpoint recommended: {recommended}.\n"
    )
    handoff = (
        f"# Handoff: {args.task_id}\n\n"
        f"Objective: {redact(args.objective)}\n\n"
        f"Decisions:\n{_list(args.decision)}\n\n"
        f"Next steps:\n{_list(args.remaining)}\n"
    )
    result = {"task_id": args.task_id, "persisted": args.persist, "checkpoint_recommended": recommended, "evidence": evidence}
    if args.persist:
        state_root = args.state_root if args.state_root.is_absolute() else repo / args.state_root
        target = state_root / args.task_id
        target.mkdir(parents=True, exist_ok=True)
        (target / "state.md").write_text(state, encoding="utf-8")
        (target / "handoff.md").write_text(handoff, encoding="utf-8")
        (target / "verification.json").write_text(json.dumps({"evidence": evidence}, indent=2) + "\n", encoding="utf-8")
        result["directory"] = str(target)
    else:
        result["preview"] = state
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
