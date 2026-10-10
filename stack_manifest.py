"""Validation helpers for the Stack's source-of-truth capability manifest."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
MANIFEST_PATH = ROOT / "stack.manifest.json"
FRONTMATTER = re.compile(r"\A---\s*\n(.*?)\n---(?:\s|\Z)", re.DOTALL)


class ManifestError(ValueError):
    """Raised when manifest content or a referenced suite is invalid."""


def load_manifest(path: Path = MANIFEST_PATH) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ManifestError(f"Cannot read manifest {path}: {exc}") from exc
    validate_manifest(data, path.parent)
    return data


def validate_manifest(data: Any, repo_root: Path = ROOT) -> None:
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        raise ManifestError("manifest must be an object with schema_version 1")
    if data.get("namespace") != "aes" or data.get("package") != "agentic-engineering-stack":
        raise ManifestError("unexpected manifest namespace or package")
    entries = data.get("capabilities")
    if not isinstance(entries, list):
        raise ManifestError("capabilities must be a list")

    root = repo_root.resolve()
    ids: set[str] = set()
    paths: set[str] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            raise ManifestError("each capability must be an object")
        capability_id = entry.get("id")
        relative = entry.get("path")
        if not isinstance(capability_id, str) or not isinstance(relative, str):
            raise ManifestError("each capability requires string id and path")
        if capability_id in ids:
            raise ManifestError(f"duplicate capability ID: {capability_id}")
        if relative in paths:
            raise ManifestError(f"duplicate capability path: {relative}")
        ids.add(capability_id)
        paths.add(relative)

        if capability_id != f"aes:skill:{Path(relative).name}":
            raise ManifestError(f"ID/path mismatch: {capability_id} -> {relative}")
        if entry.get("kind") != "skill" or entry.get("activation") != "on-demand":
            raise ManifestError(f"unsupported kind or activation for {capability_id}")
        tags = entry.get("profile_tags")
        requires = entry.get("requires")
        if not isinstance(tags, list) or not all(isinstance(tag, str) for tag in tags):
            raise ManifestError(f"profile_tags must be a string list for {capability_id}")
        if not isinstance(requires, list) or not all(isinstance(req, str) for req in requires):
            raise ManifestError(f"requires must be a string list for {capability_id}")

        target = (root / relative).resolve()
        try:
            target.relative_to(root)
        except ValueError as exc:
            raise ManifestError(f"path escapes repository root: {relative}") from exc
        skill_file = target / "SKILL.md"
        if not skill_file.is_file():
            raise ManifestError(f"missing SKILL.md for {capability_id}: {relative}")
        text = skill_file.read_text(encoding="utf-8")
        match = FRONTMATTER.match(text)
        if not match:
            raise ManifestError(f"invalid frontmatter for {capability_id}")
        name = re.search(r"(?m)^name:\s*([A-Za-z0-9_-]+)\s*$", match.group(1))
        description = re.search(r"(?m)^description:\s*(['\"])(.+)\1\s*$", match.group(1))
        if not name or name.group(1) != target.name or not description:
            raise ManifestError(f"unusable name/description frontmatter for {capability_id}")

    expected = {p.parent.name for p in (root / "suites").glob("*/SKILL.md")}
    actual = {Path(entry["path"]).name for entry in entries}
    if expected != actual:
        raise ManifestError(f"manifest suite inventory mismatch: missing={expected-actual}, extra={actual-expected}")


def main() -> int:
    manifest = load_manifest()
    print(f"Valid manifest: {len(manifest['capabilities'])} canonical skills")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
