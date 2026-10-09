# Host and Finder Compatibility Baseline

## Coding-agent hosts

The installer contains static directory mappings for Claude, Codex, Pi, OpenCode, Cursor, OpenClaw, Hermes, Roo, Cline, generic Agents, Gemini and `agy`. A path in `install.py` is configuration evidence only; it does not prove that a given host version discovers or loads the installed skill. No host integration or clean-home installation was executed for this baseline. Support claims remain unverified until exercised against the named host/version.

The current installer maps both `gemini` and `agy` to different directories under `.gemini`; the in-file note also records uncertainty about the `agy` alias. Treat this as a mapping requiring verification, not an established host integration.

## Companion Local Capability Finder

The companion checkout currently exposes MCP tools named `search_capabilities`, `get_capability`, and `activate_skill` (`capability_mcp.py`). Search takes `query`, optional `kind`, `limit`, `agent`, and `project_hint`; exact lookup accepts `capability_id`. The inspected public surface does not currently expose the proposed `load_skill`, source registration, prepare-activation, or deactivate methods, nor a shared Contract v1 schema/version. Its search result documentation points callers to a `source_path` for direct skill-file reading.

Therefore Stack/Finder compatibility is **not yet Contract v1 compatible**. Do not import Finder internals, assume proposed APIs exist, or call the current activation method as a substitute for an approval-preview flow. S5 must be gated on joint contract agreement and a public compatible Finder implementation; until then, use a test fixture/mock and preserve standalone Stack behavior.

## Safe integration boundary

- Stack owns suite content, workflow policy, and its source manifest.
- Finder owns discovery indexes and durable activation/installation state.
- Stack must not maintain a competing cross-agent catalog or silently activate third-party capabilities.
- Contract version, exact schemas, structured errors, revisions/content hashes, registration ownership, and approval semantics are open decisions to settle with the companion project before S5.
