# Implementation Status

Phases follow `AGENTIC_ENGINEERING_STACK_IMPLEMENTATION_PLAN.md`; a phase is complete only after its exit criteria pass. “Planned” is not implemented.

| Phase | Status | Evidence / remaining gate |
|---|---|---|
| S0 — baseline, tests, integration decisions | Complete | Inventory/compatibility docs, 18 route examples, standard-library inventory tests, Windows/Linux CI, and honest README claims. Two unit tests pass; disposable-home installer smoke test created 18 targets and preserved a pre-existing unmanaged directory. |
| S1 — manifest, profiles, safe installer | Complete | `stack.manifest.json` validates all 18 stable IDs; six routing profiles; installer rejects invalid selections, supports dry-run, installs only core four by default, verifies targets, and reports skips/conflicts. Isolated installer/manifest tests pass. |
| S2 — progressive disclosure and suite linting | Complete | All 18 suites now expose use/avoid/inputs/workflow/verification/exit metadata; four bulky examples moved to relative references. `scripts/lint_skills.py` validates required metadata, unique names, workflow headings, and safe existing links. Semantic routing evaluation is deferred to S3 because no runtime router existed before it. |
| S3 — deterministic routing | Complete | `routing.py` consumes profile JSON; `scripts/route_task.py` emits explicit decisions. Coverage includes all 18 canonical suites, ambiguity/specificity, exact IDs, Finder outage, niche fallback, and strict gates. Routing only returns a bounded search request; it does not call or emulate Finder APIs. |
| S4 — enforceable workflows and checks | Complete | Seven workflow JSON definitions; tested preflight scope/secret checks, argv-only check receipts with hash-verified logs, bugfix regression-required postflight, unsupported test-claim rejection, and exact action/target approval records. Gates are opt-in CLI/CI checks, not universal host hooks. |
| S5 — Finder integration | Stack side implemented; joint phase blocked | Proposed Contract v1 documentation, version-gated adapter, and mock tests cover exact IDs, one-skill load, trust, personal search, activation approval, and fallback. Companion currently exposes only search/get/activate MCP tools; no handshake, registration, load, activation preview, deactivation, or versioned contract. Requires joint agreement and Finder release before end-to-end claim. |
| S6 — context/token mechanisms | Partial; external comparison pending | User-opt-in redacted checkpoints, configurable manual threshold, independent raw/RTK/sqz benchmark harness, and local RTK 0.49.0 results recorded. `sqz` is not installed/configured and provider token accounting unavailable; byte results are not token savings. S6 exit criterion remains open. |
| S7 — optional host subagents | Not started | Test actual host APIs; otherwise document as unverified. |
| S8 — evals, CI, release readiness | Not started | Depends on delivered phases and pinned compatible Finder. |

This status file is updated at phase boundaries. Host mappings, target architecture, and proposed API names are not evidence of implemented or verified support.
