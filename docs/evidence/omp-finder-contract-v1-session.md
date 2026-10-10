# OMP + Finder Contract v1 session evidence

**Purpose:** one model-driven smoke test of the joint integration, separate from hosted CI and synthetic routing evaluations.

## Environment

- Host: Oh My Pi (OMP) 18.4.4 on Windows.
- Model: `openai-codex/gpt-6-luna`.
- Workspace: disposable fixture under `%LOCALAPPDATA%\Temp\aes-finder-omp-release-y6qrcoat`.
- Finder: review branch `review/finder-contract-v1`, HEAD `1886809b5fce5e340251ca533e1dea89cdf2d50f`; source `aes` registered only in a temporary Finder home/library.
- Stack source: the `suites/` directory in the Stack review worktree; the loaded skill body revision was `sha256:ffcc9a60a4a4bc20dacc33834ba85bc6c3f72ab3712ecaed330eda4ae3469ec1`.
- OMP was launched with `--no-skills --no-rules --no-extensions`; its project `.mcp.json` named the disposable Finder server `finder-contract-v1-rc`. Thus the task loaded the suite body from Finder MCP rather than relying on OMP native skill discovery. The MCP audit log and OMP session transcript were retained alongside the fixture during validation.

## Observed results

1. Finder MCP `get_contract_info` returned Contract v1. The OMP transcript records calls to `search_capabilities`, `get_capability`, and `load_skill` against `finder-contract-v1-rc`; the last returned the exact capability ID and full body. The Finder audit log records all four calls as successful.
2. Exact capability: `aes:skill:systematic-debugging-suite`. Metadata reported `trust_status: approved`, `availability: on-demand`, and `managed_targets: []`.
3. The agent reproduced both failures with `python -m unittest discover -s tests -v`: 10% discount returned 250 rather than 2250; zero-percent discount returned 0 rather than 2500. `pytest` was unavailable; default unittest discovery found zero tests, so discovery was scoped to `tests/`.
4. The agent changed only disposable `src/pricing.py`, replacing the discount-amount result with `subtotal_cents - subtotal_cents * discount_percent // 100`.
5. The same targeted unittest command passed both tests (`Ran 2 tests ... OK`). A subsequent independent run in the fixture also passed.
6. A separate lifecycle check used `CAPFIND_HOME` and `CAPFIND_LIBRARY` under the temporary fixture: activation at `needs_review` was denied without `--yes` and left the target absent; explicit approval created only the isolated OMP target; deactivation removed that managed target and left the Stack source byte-identical. Finder joint-contract and safety tests passed (10 P8 tests; 16 P1 tests, one platform-specific skip).

## Limits

This proves one OMP version, one model session, one loaded skill, and one simple repair task—not model quality, comparative productivity, universal OMP support, or native approval UX. The model session did not activate a skill; lifecycle approval was exercised separately through Finder's documented CLI in a disposable home. A nonblocking OMP auto-thinking provider attempt returned HTTP 402 for unavailable OpenRouter credits; the configured OpenAI Codex model completed the task. OMP quota display rounded the five-hour bucket from 0% to 1%; that is not a task-attributed token or billing measurement. No baseline/old-stack/new-stack comparison was performed.
