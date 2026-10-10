# Host and Finder Compatibility Baseline

## Coding-agent hosts

The installer contains static directory mappings for Claude, Codex, Pi, OpenCode, Cursor, OpenClaw, Hermes, Roo, Cline, generic Agents, Gemini and `agy`. A path in `install.py` is configuration evidence only; it does not prove that a given host version discovers or loads the installed skill. No host integration or clean-home installation was executed for this baseline. Support claims remain unverified until exercised against the named host/version.

The current installer maps both `gemini` and `agy` to different directories under `.gemini`; the in-file note also records uncertainty about the `agy` alias. Treat this as a mapping requiring verification, not an established host integration.

## Companion Local Capability Finder

The companion checkout currently exposes MCP tools named `search_capabilities`, `get_capability`, and `activate_skill` (`capability_mcp.py`). Search takes `query`, optional `kind`, `limit`, `agent`, and `project_hint`; exact lookup accepts `capability_id`. The inspected public surface does not currently expose the proposed `load_skill`, source registration, prepare-activation, or deactivate methods, nor a shared Contract v1 schema/version. Its search result documentation points callers to a `source_path` for direct skill-file reading.

The companion checkout now implements Contract v1 for skills
(`docs/integration-contract.md` in local-capability-finder):
`search_capabilities`, `get_capability`, `load_skill` (exact-ID SKILL.md
with revision check), `prepare_activation` (dry-run findings), and
trust-gated `activate_skill`. Live verification on 2026-10-10: the Finder
registers this repo's `suites/` as source `aes` and resolves all 18 suites
as `aes:skill:*` with no native installation required.

Therefore S5 is **unblocked for Stack-side adoption**: use only the public
MCP/CLI surface above, key suites by their `aes:skill:*` stable IDs, and
treat `prepare_activation` findings as the approval gate. Do not import
Finder internals. The compatibility table in the contract doc (not
`main`-coupling) governs pinned releases.

## Safe integration boundary

- Stack owns suite content, workflow policy, and its source manifest.
- Finder owns discovery indexes and durable activation/installation state.
- Stack must not maintain a competing cross-agent catalog or silently activate third-party capabilities.
- Contract version, exact schemas, structured errors, revisions/content hashes, registration ownership, and approval semantics are open decisions to settle with the companion project before S5.
