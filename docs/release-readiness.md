# Release Readiness Matrix

This matrix distinguishes implemented Stack-side checks from external integration gates. A green local test suite is not equivalent to a joint release.

| Scenario | Local evidence | State |
|---|---|---|
| Stack only | Manifest validator, deterministic Tier 1 routing, workflow gates, suite lint, tests | Implemented/tested on local Windows host |
| Stack + Finder, Contract v1 | Mock adapter contract tests only | Blocked: companion has no matching public Contract v1 |
| Finder unavailable | Tier 1 remains usable; niche tasks return unavailable | Implemented/tested |
| Specialist search | Mock returns personal and untrusted metadata; loading requires exact trusted ID | Mock-tested only |
| Activation safety | Approval-preview and exact-plan guard in proposed adapter; local standalone approval gate | Mock-tested; no live Finder activation |
| Windows + Linux | CI matrix configured; local Windows tests executed | Linux CI not executed in this workspace |
| Third-party/malicious capability | Trust checks prevent mock load without trusted metadata; no execution occurs on search | Mock-tested; no live Finder security test |
| Output compression | RTK 0.49.0 byte comparison, 5 workloads, one run each | Partial; sqz unavailable, no provider token accounting |
| Host delegation | Current session isolated-worker call and handoff validation | Partial; no Stack-distributed Pi/OMP extension, other hosts unverified |
| Clean-environment quickstart | Dry-run and disposable-root installer tests | Covered locally; actual native agent skill discovery not verified |

## Release blockers

1. Agree and implement Contract v1 in the companion Finder, then pin compatible versions and run the joint one-agent scenario.
2. Measure sqz separately from RTK (or record why it is unavailable), repeat trials, and capture provider usage where possible.
3. Implement and test at least one host-specific adapter that consumes delegation policy and returns a schema-valid bounded handoff.
4. Execute CI on both operating systems and verify actual host skill discovery before advertising host support.

No unsupported cost-reduction percentage is published as a measured result.
