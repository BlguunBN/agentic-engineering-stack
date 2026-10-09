# Host Compatibility and Delegation Evidence

Host-path mappings in `install.py` remain directory heuristics, not support guarantees. Record only what was inspected or exercised.

| Host | Local evidence | Stack integration status |
|---|---|---|
| Pi | Installed CLI reports `1.1.0`; `pi --help` exposes explicit extension loading. Pi `docs/extensions.md` documents `ExtensionAPI`, custom tools/events, lifecycle, and mode constraints. A local Learn package contains `extensions/subagent.ts` using isolated sessions and allowlists. | No Stack-distributed extension. The existing user package was inspected, not installed or modified by this project. |
| OMP | Installed CLI reports `18.4.4`; `omp --help` exposes `--extension`; local config has OMP extensions including an autopilot with delegation guidance. | No Stack adapter or dedicated worker acceptance test. Do not infer Pi extension API parity for every OMP release. |
| Current agent session | The session's isolated `subagent` tool successfully invoked a bounded `researcher` worker and returned its final report. The returned report was longer than the desired compact handoff, so this proves isolation/return plumbing only, not output-budget enforcement. | Generic host-tool use was observed; no Stack hook automatically dispatches workers. |
| Hermes, OpenCode, Codex, CommandCode, other hosts | No versioned interface test in this phase. | Unverified. |

## Delegation policy

`delegation/policy.json` is host-neutral: no workers for small tasks; at most one for moderate tasks; at most two scoped workers for large/high-risk tasks; high-risk requires independent review and rollback planning. Hosts enforce these limits only when an adapter actually consumes the policy. `scripts/validate_handoff.py` validates the compact JSON contract before a handoff is accepted.

Example validation:

```bash
python scripts/validate_handoff.py --policy delegation/policy.json --handoff handoff.json
```

No host extension is auto-loaded, installed, or modified. Worker model, tool allowlist, timeout, and token budgets remain host-specific and must be tested before being advertised.
