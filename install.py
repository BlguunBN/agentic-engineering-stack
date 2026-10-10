#!/usr/bin/env python3
"""Install a selected subset of Agentic Engineering Stack skills safely.

Configured roots are discovery hints, not proof that an agent version supports
this skill layout. Finder remains the canonical cross-agent lifecycle manager.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

from stack_manifest import ManifestError, load_manifest

HOME = Path.home()
SCRIPT_DIR = Path(__file__).resolve().parent
SUITES_DIR = SCRIPT_DIR / "suites"
MANIFEST_PATH = SCRIPT_DIR / "stack.manifest.json"

# Keep aliases for backward compatibility. Gemini/AGY layout remains unverified.
AGENT_SKILL_ROOTS = {
    "claude": HOME / ".claude/skills",
    "codex": HOME / ".codex/skills",
    "pi": HOME / ".pi/agent/skills",
    "opencode": HOME / ".config/opencode/skills",
    "cursor": HOME / ".cursor/skills",
    "openclaw": HOME / ".openclaw/skills",
    "hermes": HOME / ".hermes/skills",
    "roo": HOME / ".roo/skills",
    "cline": HOME / ".cline/skills",
    "agents": HOME / ".agents/skills",
    "gemini": HOME / ".gemini/config/skills",
    "agy": HOME / ".gemini/skills",
}
DEFAULT_SKILLS = {
    "systematic-debugging-suite",
    "unit-testing-suite",
    "code-review-standards-suite",
    "git-workflow-suite",
}


class InstallError(ValueError):
    """Invalid install selection or unsafe target."""


@dataclass
class InstallReport:
    changed: list[str] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)
    conflicts: list[str] = field(default_factory=list)
    unavailable: list[str] = field(default_factory=list)

    @property
    def exit_code(self) -> int:
        return 1 if self.conflicts or self.unavailable else 0

    def print(self, dry_run: bool) -> None:
        action = "Would change" if dry_run else "Changed"
        print(f"{action}: {len(self.changed)}")
        print(f"Skipped: {len(self.skipped)}")
        print(f"Conflicts: {len(self.conflicts)}")
        print(f"Unavailable roots: {len(self.unavailable)}")
        for label, entries in (("SKIPPED", self.skipped), ("CONFLICT", self.conflicts), ("UNAVAILABLE", self.unavailable)):
            for entry in entries:
                print(f"{label}: {entry}")


def _manifest_suites() -> dict[str, Path]:
    try:
        manifest = load_manifest(MANIFEST_PATH)
    except ManifestError as exc:
        raise InstallError(str(exc)) from exc
    return {
        Path(entry["path"]).name: (SCRIPT_DIR / entry["path"]).resolve()
        for entry in manifest["capabilities"]
    }


def _link_or_copy(src: Path, dest: Path) -> str:
    """Create a directory junction/symlink, falling back to a managed copy."""
    if os.name == "nt":
        try:
            subprocess.run(
                ["cmd.exe", "/d", "/c", "mklink", "/J", str(dest), str(src)],
                capture_output=True,
                check=True,
            )
            return "junction"
        except (OSError, subprocess.CalledProcessError):
            pass
    else:
        try:
            dest.symlink_to(src, target_is_directory=True)
            return "symlink"
        except OSError:
            pass
    shutil.copytree(src, dest)
    return "copy"


def install(
    target_agents: list[str] | None = None,
    copy_rules: bool = True,
    dry_run: bool = False,
    skills: list[str] | None = None,
) -> InstallReport:
    """Install default core skills or explicit skills into verified roots.

    Existing directories are never overwritten. Symlinks resolving to the
    exact source are idempotently skipped; other existing targets are conflicts.
    """
    available = AGENT_SKILL_ROOTS
    if target_agents is not None:
        if not target_agents:
            raise InstallError("--agents requires at least one agent name")
        unknown = sorted(set(target_agents) - available.keys())
        if unknown:
            raise InstallError(f"Unknown agent(s): {', '.join(unknown)}")
        agents = list(dict.fromkeys(target_agents))
    else:
        agents = [name for name, root in available.items() if root.is_dir() or root.parent.is_dir()]

    suites = _manifest_suites()
    selected = DEFAULT_SKILLS if skills is None else set(skills)
    normalized = {value.removeprefix("aes:skill:") for value in selected}
    unknown_skills = sorted(normalized - suites.keys())
    if not normalized:
        raise InstallError("Select at least one skill; use --skills with one or more suite names")
    if unknown_skills:
        raise InstallError(f"Unknown skill(s): {', '.join(unknown_skills)}")

    report = InstallReport()
    for agent in agents:
        root = available[agent]
        # Parent presence is a conservative filesystem check, not host-version verification.
        if not root.is_dir() and not root.parent.is_dir():
            report.unavailable.append(f"{agent}: {root} (agent root/parent absent)")
            continue
        if not dry_run:
            root.mkdir(parents=True, exist_ok=True)
        for name in sorted(normalized):
            src = suites[name]
            dest = root / name
            label = f"{agent}/{name}: {dest}"
            if dest.exists():
                try:
                    same_source = dest.resolve(strict=True) == src.resolve(strict=True)
                except OSError:
                    same_source = False
                (report.skipped if same_source else report.conflicts).append(label)
            elif dest.is_symlink():
                # A broken link is still an occupied destination.
                report.conflicts.append(label)
            elif dry_run:
                report.changed.append(label)
            else:
                try:
                    method = _link_or_copy(src, dest)
                except (OSError, shutil.Error) as exc:
                    report.conflicts.append(f"{label} ({exc})")
                    continue
                # Verify the created target before calling it installed.
                if not dest.exists():
                    report.conflicts.append(f"{label} (target missing after {method})")
                else:
                    report.changed.append(f"{label} ({method})")

    if copy_rules:
        source = SCRIPT_DIR / "templates" / "AGENTS.md"
        target = HOME / "AGENTS.local.md"
        if not source.is_file():
            report.unavailable.append(f"template missing: {source}")
        elif target.exists() or target.is_symlink():
            report.conflicts.append(f"rules file exists; not overwritten: {target}")
        elif dry_run:
            report.changed.append(f"rules: {target}")
        else:
            try:
                shutil.copy2(source, target)
                if target.is_file() and target.read_bytes() == source.read_bytes():
                    report.changed.append(f"rules: {target}")
                else:
                    report.conflicts.append(f"rules copy verification failed: {target}")
            except OSError as exc:
                report.conflicts.append(f"rules: {target} ({exc})")

    report.print(dry_run)
    return report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Install selected Agentic Engineering Stack skills.")
    parser.add_argument("--agents", nargs="+", help="Agent aliases to target; omit to detect configured roots")
    parser.add_argument("--skills", nargs="+", help="Suite names or exact aes:skill:<name> IDs; defaults to core four")
    parser.add_argument("--dry-run", action="store_true", help="Show planned changes without filesystem mutation")
    parser.add_argument("--no-copy-rules", action="store_true", help="Do not copy templates/AGENTS.md")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        report = install(
            target_agents=args.agents,
            copy_rules=not args.no_copy_rules,
            dry_run=args.dry_run,
            skills=args.skills,
        )
    except InstallError as exc:
        parser.error(str(exc))
    return report.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
