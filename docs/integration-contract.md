# Stack ↔ Local Capability Finder Contract v1 (Proposed)

**Status: Stack-side proposal and mock only. This is not yet jointly implemented or compatible with the current Finder release.** Finder must publish the same versioned surface before S5 can be marked complete. Stack never imports Finder modules or writes Finder installation state.

## Ownership

- Stack is source-of-truth for 18 canonical suite IDs (`aes:skill:<folder>`), suite content, profiles, and workflow policies.
- Finder owns its derived index, content revisions/hashes, trust/compatibility evaluation, activation state, and durable native installs.
- Register Stack's manifest/source once under namespace `aes`; registration must be idempotent and must not duplicate native skill directories.

## Version handshake

Finder exposes `get_contract_info()` returning:

```json
{"contract": "local-capability-finder", "version": 1, "features": ["register_source", "search", "get", "load", "activation-preview"]}
```

Unsupported major versions produce `INCOMPATIBLE_CONTRACT`; unavailable methods/features produce `UNSUPPORTED_OPERATION`. Do not infer Contract v1 from an MCP server name or transport protocol version.

## Read-only operations

| Operation | Contract behavior |
|---|---|
| `register_source(namespace, manifest_path)` | Register/refresh derived source index; idempotent; no activation. |
| `search_capabilities(query, k=3, kind?, agent?, source?)` | Metadata only, at most `k` results; personal capabilities remain searchable. |
| `get_capability(id)` | Exact canonical ID metadata: kind, source, revision/hash, trust, host compatibility, requirements. |
| `load_skill(id, revision?)` | Return one exact skill body, optionally pinned. Reject blocked/untrusted content unless explicitly reviewed/allowed by caller policy. |
| `get_tool_schema(id)` | Return one selected indexed tool schema, when supported. |

Errors are structured with stable codes: `NOT_FOUND`, `AMBIGUOUS_ID`, `UNTRUSTED`, `UNSUPPORTED_AGENT`, `CONFLICT`, `STALE_REVISION`, `PERMISSION_DENIED`, `INCOMPATIBLE_CONTRACT`, `UNSUPPORTED_OPERATION`.

## State-changing operations

`prepare_activation(id, agent)` returns a preview plan and ownership/conflict details. `activate_skill(plan_id, approval)` applies only that approved plan; `deactivate_skill(id, agent, approval)` removes only a Finder-owned activation. Approval must identify the exact action, target, and plan/revision. Search/load never activates or executes content. Hosts without a safe approval flow must expose these operations through a user-invoked CLI instead of agent-callable MCP tools.

## Required joint compatibility tests

1. Register all 18 manifest entries with stable unique IDs.
2. Load one exact selected skill, not all 18; changing content updates revision/hash, not ID.
3. Personal capabilities remain discoverable via Tier 2.
4. Finder outage leaves Stack standalone Tier 1 and reports missing specialist capability.
5. Incompatible versions fail clearly with standalone fallback.
6. Untrusted/blocked capabilities cannot load or activate through search alone.
7. Activation requires an approval preview and exact authorized plan; deactivation only affects manager-owned state.
8. Duplicate names from distinct sources remain distinct by canonical ID.

## Current compatibility evidence

The inspected companion checkout exposes MCP `search_capabilities(query, kind?, limit, agent?, project_hint)`, `get_capability(capability_id)`, and `activate_skill(capability_id, agent)`. It does not currently expose the Contract v1 handshake, Stack registration, `load_skill`, activation preview, deactivation, pinned revisions, or the structured error set. Its search description returns `source_path`, which supports a manual/local read, but is not a versioned load API. Therefore the adapter tests in Stack use a mock contract fixture only; no joint end-to-end or activation claim is made.
