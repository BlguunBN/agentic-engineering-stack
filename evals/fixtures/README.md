# Evaluation Fixtures

Existing deterministic fixtures, not synthetic model-trial results:

| Fixture | Purpose | Verification |
|---|---|---|
| `examples/bugfix_fixture.py` + `tests/test_bugfix_fixture.py` | Regression-fix acceptance and invalid-status rejection | `python -m unittest tests.test_bugfix_fixture -v` |
| Manifest installer tests | Dry-run, explicit subsets, conflicts, and non-overwrite safety | `python -m unittest tests.test_manifest_installer -v` |
| Routing eval cases | Positive and negative deterministic route selection | `python scripts/evaluate_routing.py` |
| Finder MCP wire/live tests | Contract handshake, exact load, approval, and lifecycle | `python -m unittest tests.test_finder_mcp_wire tests.test_finder_mcp_integration -v` |

Agent-task artifacts must be produced by real runs and passed to the engineering
evaluation report validator; this directory does not contain fabricated
success metrics.
