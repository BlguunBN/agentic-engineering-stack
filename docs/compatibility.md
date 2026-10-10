# Host and Finder Compatibility

## Coding-agent hosts

`install.py` contains static mappings for several agent skill directories. A
configured path is not proof that a given host discovers or loads the skill.
See `docs/host-compatibility.md` for per-host evidence. No unsupported host is
advertised as verified.

## Local Capability Finder Contract v1

The Stack uses only Finder's documented public MCP/CLI boundary:

- Contract handshake: MCP `get_contract_info` must report
  `local-capability-finder`, version 1, and the required features.
- Source registration: the documented `library_catalog.py register-source`
  command registers `suites/` under `aes`; a catalog refresh follows. This
  indexes content but does not install/activate skills.
- Read-only flow: bounded `search_capabilities`, exact `get_capability`, then
  `load_skill` for the chosen ID/revision only.
- State changes: Stack checks an exact approval record and rechecks the
  activation preview before calling Finder's activation tool. Deactivation is
  limited to Finder-managed targets.

`adapters/finder_mcp.py` is a stdio MCP client; it does not import Finder
modules or write Finder indexes, trust state, locks, or activation manifests.
`tests/test_finder_mcp_integration.py` runs against a compatible Finder
checkout in a disposable home/library. `tests/test_finder_mcp_wire.py` covers
the protocol independently of that checkout.

Finder 0.2.x / Contract v1 is the compatible range. Missing or incompatible
handshakes fail explicitly; standalone Stack routing remains available. Release
validation must pin the two repository revisions together. Source registration
is documented in `README.md` and is not an automatic activation.
