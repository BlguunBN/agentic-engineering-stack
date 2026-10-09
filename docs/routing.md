# Deterministic Routing

`profiles/*.json` are consumed by `routing.py`; they are executable routing data, not illustrative configs. The module routes only exact canonical IDs from `stack.manifest.json` and never calls MCP tools, installs a skill, or executes third-party code.

## Decision behavior

1. Load the requested profile and its `extends` chain; reject unknown IDs, malformed routes, and invalid limits.
2. Match normalized task text against whole-word `match_any` aliases.
3. Rank matches by explicit route priority, then alias specificity. If equally ranked routes have different IDs, return `ambiguous` and ask for scope clarification; do not load both.
4. Return one primary suite plus only explicitly configured supporting suites. Alternative matched routes are diagnostic metadata, not preloads.
5. If no core route matches, return a Finder Tier 2 query (`search_capabilities`, limit 3) when Finder is available. The caller must inspect results and select one exact ID before loading. If Finder is down, return `unavailable`; the Stack does not fabricate a capability or invoke remote installation.
6. A supplied `skill_id` bypasses text classification only after exact manifest-ID validation.

The `strict` profile surfaces review gates in the decision; S4 adds enforceable workflow checks. Risk-sensitive infrastructure profiles surface approval/rollback gates. These metadata do not themselves replace host authorization.

## Use

```bash
python scripts/route_task.py --task "Fix the API crash and add a regression test" --profile core
python scripts/route_task.py --task "Find a specialist bioinformatics capability" --profile research
python scripts/route_task.py --task "Fix a bug" --profile core --finder-unavailable
```

Output is JSON with `tier`, `primary`, `supporting`, `alternatives`, matched intent/aliases, optional Finder query, gates, and a short reason. The caller can then load only the exact selected skill through the agreed capability interface; the Stack routing CLI does not assume that interface exists today.
