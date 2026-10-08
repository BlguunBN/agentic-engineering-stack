#!/usr/bin/env python3
"""Universal Installer for Agentic Engineering Stack.

Installs the 10 Master Mega-Skills and links them to your active AI coding agents:
- Claude Code (~/.claude/skills)
- OpenAI Codex (~/.codex/skills)
- Pi Coding Agent (~/.pi/agent/skills)
- OpenCode (~/.config/opencode/skills)
- Cursor (~/.cursor/skills)
- OpenClaw (~/.openclaw/skills)
- Hermes (~/.hermes/skills)
- Roo / Cline (~/.roo/skills, ~/.cline/skills)
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

HOME = Path.home()
SCRIPT_DIR = Path(__file__).resolve().parent
SUITES_DIR = SCRIPT_DIR / "suites"

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
}


def link_or_copy(src: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        return
    try:
        # Try directory junction on Windows
        if os.name == "nt":
            subprocess.run(
                ["cmd.exe", "/d", "/c", "mklink", "/J", str(dest), str(src)],
                capture_output=True,
                check=True,
            )
        else:
            dest.symlink_to(src, target_is_directory=True)
    except Exception:
        # Fallback to copy
        shutil.copytree(src, dest)


def install(target_agents: list[str] | None = None, copy_rules: bool = True) -> None:
    print("🚀 Installing Agentic Engineering Stack...")

    if not SUITES_DIR.is_dir():
        print(f"❌ Suites directory not found at {SUITES_DIR}")
        sys.exit(1)

    suites = [d for d in SUITES_DIR.iterdir() if d.is_dir() and (d / "SKILL.md").exists()]
    print(f"📦 Found {len(suites)} Master Mega-Skills to install.")

    # Detect active agents
    installed_count = 0
    for agent, root in AGENT_SKILL_ROOTS.items():
        if target_agents and agent not in target_agents:
            continue
        if root.parent.exists() or root.exists():
            root.mkdir(parents=True, exist_ok=True)
            print(f"  👉 Linking to {agent} ({root})...")
            for suite in suites:
                dest = root / suite.name
                link_or_copy(suite, dest)
                installed_count += 1

    # Copy template rules to workspace root if requested
    if copy_rules:
        target_rule = HOME / "AGENTS.local.md"
        src_rule = SCRIPT_DIR / "templates" / "AGENTS.md"
        if src_rule.exists() and not target_rule.exists():
            shutil.copy2(src_rule, target_rule)
            print(f"  📄 Installed default AGENTS.local.md at {target_rule}")

    print("✅ Installation complete! All master suites are active across your agents.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Install Master Agentic Suites.")
    parser.add_argument("--agents", nargs="*", help="Specific agents to install into")
    args = parser.parse_args()
    install(target_agents=args.agents)
