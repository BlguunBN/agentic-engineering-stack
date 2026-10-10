# Host Compatibility and Delegation Evidence

Host-path mappings in `install.py` remain directory heuristics, not support guarantees. Record only what was inspected or exercised.

| Host | Local evidence | Stack integration status |
|---|---|---|
| Pi | Installed CLI reports `1.1.0`; `pi --help` exposes explicit extension loading. Pi `docs/extensions.md` documents `ExtensionAPI`, custom tools/events, lifecycle, and mode constraints. A local Learn package contains `extensions/subagent.ts` using isolated sessions and allowlists. | No Stack-distributed extension. The existing user package was inspected, not installed or modified by this project. |
| OMP | Installed CLI reports `18.4.4`; `omp --help` exposes `--extension`; local config has OMP extensions including an autopilot with delegation guidance. | No Stack adapter or dedicated worker acceptance test. Do not infer Pi extension API parity for every OMP release. |
| Current agent session (Pi harness) | A bounded `researcher` worker returned a schema-valid 2-finding JSON handoff (<50 words). The coordinator reproduced both issues in the wire fixture, added regression coverage, fixed the MCP initialization/notification handling, and reran the wire test successfully. | Minimum isolated-worker/report exit criterion met. No Stack-distributed Pi extension or concurrency/budget enforcement is shipped. |
| Hermes, OpenCode, Codex, CommandCode, other hosts | No versioned interface test in this phase. | Unverified. |

## Delegation policy

`delegation/policy.json` is host-neutral: no workers for small tasks; at most one for moderate tasks; at most two scoped workers for large/high-risk tasks; high-risk requires independent review and rollback planning. Hosts enforce these limits only when an adapter actually consumes the policy. `scripts/validate_handoff.py` validates the compact JSON contract before a handoff is accepted.

Example validation:

```bash
python scripts/validate_handoff.py --policy delegation/policy.json --handoff handoff.json
```

No host extension is auto-loaded, installed, or modified. Worker model, tool allowlist, timeout, and token budgets remain host-specific and must be tested before being advertised.
