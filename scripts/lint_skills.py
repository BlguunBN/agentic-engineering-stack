#!/usr/bin/env python3
"""Lint canonical SKILL.md frontmatter, required metadata, and relative links."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUITES = ROOT / "suites"
FRONTMATTER = re.compile(r"\A---\s*\n(.*?)\n---(?:\s|\Z)", re.DOTALL)
LINK = re.compile(r"(?<!!)\[[^]]+\]\(([^)]+)\)")
REQUIRED_FIELDS = {
    "name",
    "description",
    "use_when",
    "avoid_when",
    "entry_inputs",
    "workflow",
    "verification",
    "exit_output",
}


def lint_skill_directory(suites_root: Path = SUITES) -> list[str]:
    errors: list[str] = []
    seen: set[str] = set()
    skill_files = sorted(suites_root.glob("*/SKILL.md"))
    if not skill_files:
        return [f"No SKILL.md files found under {suites_root}"]

    for path in skill_files:
        relative = path.relative_to(suites_root).as_posix()
        text = path.read_text(encoding="utf-8")
        match = FRONTMATTER.match(text)
        if not match:
            errors.append(f"{relative}: missing or malformed YAML frontmatter")
            continue
        frontmatter = match.group(1)
        fields = {}
        for line in frontmatter.splitlines():
            key_value = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$", line)
            if key_value:
                key, value = key_value.groups()
                if key in fields:
                    errors.append(f"{relative}: duplicate frontmatter field {key}")
                fields[key] = value
        missing = sorted(REQUIRED_FIELDS - fields.keys())
        if missing:
            errors.append(f"{relative}: missing fields {', '.join(missing)}")
        for key in REQUIRED_FIELDS & fields.keys():
            value = fields[key].strip()
            if key == "name":
                value = value.strip("'\"")
                if value != path.parent.name:
                    errors.append(f"{relative}: frontmatter name does not match directory")
                if value in seen:
                    errors.append(f"{relative}: duplicate skill name {value}")
                seen.add(value)
            elif not value.strip("'\"").strip():
                errors.append(f"{relative}: {key} must be non-empty")

        if not re.search(r"(?m)^##\s+\S", text[match.end():]):
            errors.append(f"{relative}: requires at least one workflow heading")
        for target in LINK.findall(text[match.end():]):
            target = target.strip().split()[0].split("#", 1)[0]
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            resolved = (path.parent / target).resolve()
            try:
                resolved.relative_to(path.parent.resolve())
            except ValueError:
                errors.append(f"{relative}: reference escapes suite directory: {target}")
                continue
            if not resolved.is_file():
                errors.append(f"{relative}: missing reference: {target}")

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--suites", type=Path, default=SUITES, help="Suite directory to lint")
    args = parser.parse_args(argv)
    errors = lint_skill_directory(args.suites)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"Validated {len(list(args.suites.glob('*/SKILL.md')))} skill files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
