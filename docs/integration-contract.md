# Stack ↔ Local Capability Finder Contract v1

**Status: Contract v1 integrated; review snapshot pin and hosted joint validation in progress.** The Stack does not import Finder modules or write Finder-managed state.

## Ownership

- Stack owns the 18 suite definitions, their content, routing profiles, and workflow rules.
- Finder owns the derived catalog, stable source IDs, revisions/hashes, trust decisions, installation state, and activation manifests.
- Register the Stack's `suites/` directory once under namespace `aes` using Finder's documented `library_catalog.py register-source` CLI. Registration indexes source content; it does not activate suites.

## Version gate

Before using contract features, call MCP `get_contract_info`. It must return:

```json
{
  "contract": "local-capability-finder",
  "version": 1,
  "features": ["register_source", "search", "get", "load", "activation-preview", "activation", "deactivation", "tool-schema"],
  "registration": "library_catalog.py register-source"
}
```

Reject a missing/unknown major version or a missing required feature. MCP transport protocol version and Finder package version are separate from Contract v1.

## Stable identity and read operations

Canonical IDs are `aes:skill:<suite-folder>`. Editing a skill changes its SHA-256 revision, not its ID. Same-name capabilities from other sources remain distinct IDs.

1. `search_capabilities(query, kind?, limit?, agent?, project_hint?)` returns bounded metadata, never full skill bodies.
2. `get_capability(capability_id)` returns exact metadata, source, trust, compatibility, and current revision.
3. `load_skill(capability_id, revision?)` returns only that SKILL.md. A stale revision or untrusted source is rejected by the Stack adapter.
4. `get_tool_schema(capability_id)` reads one selected schema when Finder has captured it.

The Stack's `FinderContractClient` normalizes Finder's public fields. Its transport is `adapters/finder_mcp.py`; source registration invokes only the documented Finder CLI and then verifies all expected IDs through public MCP lookups.

## State-changing operations and approval

`prepare_activation` is a dry-run and must not change files. The Stack adapter fingerprints the plan, requires an approval record matching the exact action, plan, and target, then obtains a fresh preview before invoking `activate_skill`. Stale or conflicted plans fail closed. For deactivation, approval must match the exact capability and action; Finder removes only a manager-owned target.

Direct activation tools must not be called by Stack workflows outside this adapter gate. Finder separately blocks untrusted content according to its trust state.

## Errors and fallback

Structured errors retain stable codes such as `NOT_FOUND`, `UNTRUSTED`, `UNSUPPORTED_AGENT`, `CONFLICT`, `STALE_REVISION`, `PERMISSION_DENIED`, and `INCOMPATIBLE_CONTRACT`. If Finder is unavailable or incompatible, deterministic Tier 1 routing and the standalone profile remain usable; niche capabilities are reported unavailable rather than fabricated or installed.

## Verification

The Stack suite includes mock tests, a JSON-RPC stdio fixture, and a live integration test against the companion checkout. The live test registers all 18 IDs in a temporary Finder library, searches and loads one exact suite, retains a personal Tier 2 result, and exercises approved activation/deactivation in a disposable home. The companion Finder has independent joint-fixture tests for stable revisions, blocked imports, source conflicts, and downtime fallback.

The review pairing pins Finder commit `fcb6ce9e9f977eb553ad7b8f23d9fa6db375bb76`; see the [joint installation guide](joint-installation.md), [compatibility matrix](joint-compatibility.md), and [release validation report](release-validation.md) for exact evidence. Do not float on `main`, and do not infer a published compatibility release from a review pin.
