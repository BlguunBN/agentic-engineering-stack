# Joint installation: Agentic Engineering Stack + Local Capability Finder

This guide connects the Stack as an indexed skill source to Finder as its discovery and lifecycle manager. Registration indexes the 18 suites; it does **not** install or activate them. Keep the two repositories pinned to reviewed commits; do not use floating branches for reproducible setups.

## Prerequisites

- Python 3.11 or newer
- Git
- A Finder-compatible MCP client (host-specific MCP configuration and discovery remain the host's responsibility)

The compatible review snapshot used by this repository is Finder commit `fcb6ce9e9f977eb553ad7b8f23d9fa6db375bb76` (Contract v1, Finder 0.2.x). No release tags or published package pair are implied by this review snapshot.

## Clone and register

Clone both repositories side by side, then pin Finder to the reviewed snapshot:

```sh
git clone https://github.com/BlguunBN/agentic-engineering-stack.git
git clone https://github.com/BlguunBN/local-capability-finder.git
cd local-capability-finder
git checkout fcb6ce9e9f977eb553ad7b8f23d9fa6db375bb76
cd ../agentic-engineering-stack
```

Use an isolated home/library for a first run. In Bash:

```sh
export CAPFIND_HOME="$(pwd)/.demo-home"
export CAPFIND_LIBRARY="$CAPFIND_HOME/ai-agent-library"
python scripts/register_finder_source.py \
  --finder-root ../local-capability-finder --dry-run
python scripts/register_finder_source.py \
  --finder-root ../local-capability-finder
```

PowerShell equivalent:

```powershell
$env:CAPFIND_HOME = Join-Path (Get-Location) ".demo-home"
$env:CAPFIND_LIBRARY = Join-Path $env:CAPFIND_HOME "ai-agent-library"
python scripts/register_finder_source.py --finder-root ..\local-capability-finder --dry-run
python scripts/register_finder_source.py --finder-root ..\local-capability-finder
```

The successful registration response lists the 18 `aes:skill:<suite-name>` IDs and reports `"activated": false`. The operation uses Finder's documented registration CLI and public stdio MCP contract; it does not change a host configuration. To inspect/search/load, configure the host to launch the Finder checkout's `capability_mcp.py` with Python 3.11+, then restart that host as required by its own documentation. Host config formats and approval UI differ; see [joint compatibility](joint-compatibility.md).

## Safe use

1. Ask the connected host to call `get_contract_info`; require Contract version 1 and required features.
2. Search with a short task query, select an exact `aes:skill:` ID, then fetch that exact record and load only its `SKILL.md`.
3. Treat loaded instructions as untrusted input; inspect them before following commands or external links.
4. Do not activate a skill unless the host needs an active skill directory and the exact target has been reviewed and approved. Finder remains the lifecycle owner; Stack workflows require exact-action approval and a fresh activation preview.
5. If Finder is missing or incompatible, use deterministic Stack Tier 1 routing or stop; do not fabricate an ID or silently install content.

For cleanup of the isolated example, stop the MCP process and remove `.demo-home` only after confirming it contains no user data. Do not use the demo environment for a real home/library.
