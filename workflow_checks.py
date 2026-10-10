"""Shared workflow definitions, preflight scope checks, and postflight evidence gates."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
WORKFLOW_DIR = ROOT / "workflows"
SECRET_PATTERNS = [
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"(?i)(?:api[_-]?key|access[_-]?token|secret|password)\s*[:=]\s*['\"]?[A-Za-z0-9/+=_.-]{24,}"),
]
SENSITIVE_SUFFIXES = {".pem", ".p12", ".pfx", ".key"}
COMPLETION_WORDS = re.compile(r"(?i)\b(done|complete|completed|verified|passed|passes|successful|success)\b")
TEST_CLAIMS = re.compile(r"(?i)\btests?\s+(?:pass|passed|passes|succeeded|successful)\b")


class WorkflowError(ValueError):
    """Invalid workflow or verification evidence."""


def load_workflow(name: str) -> dict[str, Any]:
    if not re.fullmatch(r"[a-z][a-z0-9-]*", name):
        raise WorkflowError(f"Invalid workflow name: {name}")
    path = WORKFLOW_DIR / f"{name}.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise WorkflowError(f"Cannot load workflow {name}: {exc}") from exc
    if data.get("schema_version") != 1 or data.get("name") != name:
        raise WorkflowError(f"Invalid workflow definition: {name}")
    minimum = data.get("minimum_evidence")
    if not isinstance(minimum, list) or not all(isinstance(item, str) and item for item in minimum):
        raise WorkflowError(f"minimum_evidence must be a string list: {name}")
    actions = data.get("approval_actions")
    if not isinstance(actions, list) or not all(isinstance(item, str) and item for item in actions):
        raise WorkflowError(f"approval_actions must be a string list: {name}")
    return data


def changed_paths(repo: Path) -> list[str]:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo), "status", "--porcelain=v1", "-z", "--untracked-files=all"],
            check=True, capture_output=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise WorkflowError(f"Cannot inspect git status for {repo}: {exc}") from exc
    records = result.stdout.decode("utf-8", errors="replace").split("\0")
    paths = []
    index = 0
    while index < len(records):
        record = records[index]
        index += 1
        if len(record) < 4:
            continue
        status, path = record[:2], record[3:]
        paths.append(path)
        if "R" in status or "C" in status:
            if index < len(records) and records[index]:
                paths.append(records[index])
                index += 1
    return sorted(set(paths))


def _is_sensitive_path(path: str) -> bool:
    candidate = Path(path)
    lowered = candidate.name.lower()
    return (
        candidate.suffix.lower() in SENSITIVE_SUFFIXES
        or lowered in {".env", "id_rsa", "id_ed25519"}
        or (lowered.startswith(".env.") and lowered not in {".env.example", ".env.sample"})
    )


def preflight(repo: Path, workflow: str, scopes: list[str] | None = None) -> dict[str, Any]:
    root = repo.resolve()
    definition = load_workflow(workflow)
    paths = changed_paths(root)
    scope_errors = []
    normalized_scopes = [Path(item).as_posix().strip("/") for item in (scopes or [])]
    for path in paths:
        candidate = Path(path)
        if candidate.is_absolute() or ".." in candidate.parts:
            scope_errors.append(f"path escapes repository: {path}")
        if normalized_scopes and not any(
            candidate.as_posix() == scope or candidate.as_posix().startswith(scope + "/")
            for scope in normalized_scopes
        ):
            scope_errors.append(f"outside allowed scope: {path}")

    secret_findings = []
    for relative in paths:
        if _is_sensitive_path(relative):
            secret_findings.append(f"sensitive-path: {relative}")
            continue
        file_path = root / relative
        if not file_path.is_file():
            continue
        try:
            content = file_path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        for pattern in SECRET_PATTERNS:
            if pattern.search(content):
                secret_findings.append(f"credential-pattern: {relative} ({pattern.pattern[:32]}...)" )
                break

    return {
        "workflow": workflow,
        "changed_files": paths,
        "allowed_scopes": normalized_scopes,
        "minimum_evidence": definition["minimum_evidence"],
        "scope_errors": scope_errors,
        "secret_findings": secret_findings,
        "ok": not scope_errors and not secret_findings,
    }


def _contained_file(repo: Path, value: str, label: str) -> Path:
    candidate = (repo / value).resolve()
    try:
        candidate.relative_to(repo.resolve())
    except ValueError as exc:
        raise WorkflowError(f"{label} must be inside repository") from exc
    if not candidate.is_file():
        raise WorkflowError(f"{label} does not exist: {value}")
    return candidate


def verify_postflight(
    repo: Path,
    workflow: str,
    receipts: list[str],
    report_text: str = "",
    not_run_reason: str | None = None,
) -> dict[str, Any]:
    root = repo.resolve()
    definition = load_workflow(workflow)
    completed: dict[str, list[str]] = {}
    errors = []
    for value in receipts:
        try:
            receipt_path = _contained_file(root, value, "receipt")
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
            if not isinstance(receipt, dict) or receipt.get("schema_version") != 1:
                raise WorkflowError(f"invalid receipt schema: {value}")
            kind = receipt.get("kind")
            if not isinstance(kind, str) or not kind:
                raise WorkflowError(f"receipt missing kind: {value}")
            if receipt.get("exit_code") != 0:
                errors.append(f"{kind} command did not pass: {value}")
                continue
            command = receipt.get("command")
            if not isinstance(command, list) or not command or not all(isinstance(arg, str) for arg in command):
                raise WorkflowError(f"receipt missing command argv: {value}")
            log_value = receipt.get("log_path")
            if not isinstance(log_value, str):
                raise WorkflowError(f"receipt missing log_path: {value}")
            log_path = _contained_file(root, log_value, "log")
            expected_hash = receipt.get("log_sha256")
            actual_hash = hashlib.sha256(log_path.read_bytes()).hexdigest()
            if expected_hash != actual_hash:
                errors.append(f"evidence log hash mismatch: {value}")
                continue
            completed.setdefault(kind, []).append(value)
        except (WorkflowError, json.JSONDecodeError, OSError) as exc:
            errors.append(str(exc))

    missing = sorted(set(definition["minimum_evidence"]) - completed.keys())
    if missing:
        errors.append(f"missing required evidence: {', '.join(missing)}")
    if TEST_CLAIMS.search(report_text) and not any(completed.get(kind) for kind in ("test", "unit", "regression", "ui", "build")):
        errors.append("report claims tests passed without a successful test receipt")
    if COMPLETION_WORDS.search(report_text) and not completed and not not_run_reason:
        errors.append("completion claim lacks evidence; supply receipts or an explicit not-run reason")

    return {
        "workflow": workflow,
        "evidence_kinds": sorted(completed),
        "required_evidence": definition["minimum_evidence"],
        "missing_evidence": missing,
        "errors": errors,
        "not_run_reason": not_run_reason,
        "ok": not errors,
    }
