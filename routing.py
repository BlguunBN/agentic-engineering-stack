"""Deterministic Tier 1 routing with explicit Finder fallback instructions."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
PROFILE_DIR = ROOT / "profiles"
MANIFEST_PATH = ROOT / "stack.manifest.json"


class RoutingError(ValueError):
    """Invalid profile or explicit capability ID."""


@dataclass(frozen=True)
class RoutingDecision:
    tier: str
    primary: str | None
    supporting: tuple[str, ...] = ()
    alternatives: tuple[str, ...] = ()
    intent: str | None = None
    matched_aliases: tuple[str, ...] = ()
    query: str | None = None
    reason: str = ""
    gates: tuple[str, ...] = ()

    def capabilities_to_load(self) -> tuple[str, ...]:
        return ((self.primary,) if self.primary else ()) + self.supporting


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RoutingError(f"Cannot read {path}: {exc}") from exc
    if not isinstance(value, dict) or value.get("schema_version") != 1:
        raise RoutingError(f"Unsupported configuration schema: {path}")
    return value


def _capability_ids() -> set[str]:
    manifest = _read_json(MANIFEST_PATH)
    return {entry["id"] for entry in manifest.get("capabilities", []) if isinstance(entry, dict) and isinstance(entry.get("id"), str)}


def load_profile(name: str, seen: set[str] | None = None) -> dict[str, Any]:
    if not re.fullmatch(r"[a-z][a-z0-9-]*", name):
        raise RoutingError(f"Invalid profile name: {name}")
    seen = set() if seen is None else seen
    if name in seen:
        raise RoutingError(f"Profile inheritance cycle at {name}")
    seen.add(name)
    profile = _read_json(PROFILE_DIR / f"{name}.json")
    if profile.get("name") != name:
        raise RoutingError(f"Profile name mismatch: {name}")
    routes = []
    parent_name = profile.get("extends")
    if parent_name is not None:
        if not isinstance(parent_name, str):
            raise RoutingError(f"Invalid extends value in {name}")
        routes.extend(load_profile(parent_name, seen)["routes"])
    own_routes = profile.get("routes", [])
    if not isinstance(own_routes, list):
        raise RoutingError(f"routes must be a list in {name}")
    routes.extend(own_routes)
    capability_ids = _capability_ids()
    for route in routes:
        if not isinstance(route, dict):
            raise RoutingError(f"Invalid route in {name}")
        primary = route.get("primary")
        aliases = route.get("match_any")
        supporting = route.get("supporting", [])
        priority = route.get("priority", 50)
        if not isinstance(route.get("intent"), str) or not route["intent"].strip():
            raise RoutingError(f"Route intent must be a non-empty string in {name}")
        if isinstance(priority, bool) or not isinstance(priority, int):
            raise RoutingError(f"Route priority must be an integer in {name}")
        if primary not in capability_ids:
            raise RoutingError(f"Route has unknown capability ID: {primary}")
        if not isinstance(aliases, list) or not aliases or not all(isinstance(item, str) and item.strip() for item in aliases):
            raise RoutingError(f"Route {route.get('intent')} requires non-empty match_any aliases")
        if not isinstance(supporting, list) or any(item not in capability_ids for item in supporting):
            raise RoutingError(f"Route has invalid supporting IDs: {route.get('intent')}")
    max_loaded = profile.get("max_loaded_suites", 1)
    if isinstance(max_loaded, bool) or not isinstance(max_loaded, int) or not 1 <= max_loaded <= 3:
        raise RoutingError(f"Invalid max_loaded_suites in {name}")
    gates = profile.get("gates", [])
    if not isinstance(gates, list) or not all(isinstance(gate, str) and gate for gate in gates):
        raise RoutingError(f"Invalid gates in {name}")
    return {**profile, "routes": routes}


def _normalize(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def _matched_aliases(task: str, aliases: list[str]) -> list[str]:
    normalized_task = f" {_normalize(task)} "
    return [alias for alias in aliases if f" {_normalize(alias)} " in normalized_task]


def route_task(
    task: str,
    profile: str = "core",
    *,
    skill_id: str | None = None,
    finder_available: bool = True,
) -> RoutingDecision:
    """Route one task; this function never executes MCP or installs a skill."""
    if not isinstance(task, str) or not task.strip():
        raise RoutingError("task must be a non-empty string")
    config = load_profile(profile)
    gates = tuple(config.get("gates", []))
    if skill_id is not None:
        if skill_id not in _capability_ids():
            raise RoutingError(f"Unknown exact capability ID: {skill_id}")
        return RoutingDecision("tier1", skill_id, reason="explicit exact canonical ID", gates=gates)
    matches = []
    for route in config["routes"]:
        aliases = _matched_aliases(task, route["match_any"])
        if aliases:
            best = max(aliases, key=lambda value: len(_normalize(value).split()))
            matches.append((int(route.get("priority", 50)), len(_normalize(best).split()), route, aliases))
    if matches:
        top_rank = max(item[:2] for item in matches)
        top = [item for item in matches if item[:2] == top_rank]
        top_ids = {item[2]["primary"] for item in top}
        if len(top_ids) > 1:
            return RoutingDecision(
                "ambiguous", None, alternatives=tuple(sorted(top_ids)),
                matched_aliases=tuple(sorted({a for item in top for a in item[3]})),
                reason="equally specific core routes match; request clarification rather than loading multiple suites",
                gates=gates,
            )
        chosen = top[0]
        primary = chosen[2]["primary"]
        supporting = tuple(dict.fromkeys(chosen[2].get("supporting", [])))
        if len(supporting) + 1 > config["max_loaded_suites"]:
            raise RoutingError(f"Route {chosen[2].get('intent')} exceeds profile load limit")
        alternatives = tuple(sorted({item[2]["primary"] for item in matches if item[2]["primary"] != primary}))
        return RoutingDecision(
            "tier1", primary, supporting, alternatives, chosen[2].get("intent"),
            tuple(sorted(chosen[3])), reason="deterministic intent alias match", gates=gates,
        )

    if finder_available:
        return RoutingDecision("tier2", None, query=task.strip(), reason="no core route; search Finder metadata, then load one exact selected ID", gates=gates)
    return RoutingDecision("unavailable", None, query=task.strip(), reason="no core route and Finder is unavailable; report missing capability", gates=gates)
