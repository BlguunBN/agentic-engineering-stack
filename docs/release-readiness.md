# Release Readiness Matrix

| Scenario | Local evidence | State |
|---|---|---|
| Stack only | Manifest, routing, workflows, lint, installer tests | Full tests pass locally on Windows and WSL Ubuntu; hosted Windows/Ubuntu CI passed for the Stack review snapshot |
| Finder standalone | Unit suite, portable retrieval evaluation, CLI package smoke | Hosted Windows/Ubuntu CI passed for Finder 0.2.x review snapshot `fcb6ce9` |
| Stack + Finder Contract v1 | Live stdio integration with a disposable home/library; hosted workflow pins Finder `fcb6ce9e9f977eb553ad7b8f23d9fa6db375bb76` | Local integration and hosted Windows/Ubuntu Python 3.11/3.12 paired run passed. See [release validation](release-validation.md). |
| Finder unavailable/legacy | Version-gated client; Tier 1 standalone routing remains usable | Unit-tested |
| Specialist search | Live personal-skill result plus mock blocked-result cases | Tested; search does not execute or activate content |
| Activation safety | Preview recheck, exact approval record, live create/remove in disposable home | Tested on Windows and WSL |
| Malicious third-party skill | Mock blocked load; Finder P8 blocked-import fixture | Fixture-tested; no live adversarial host test |
| Output compression | Three baseline/RTK trials, `o200k_base` token counts, required diagnostics markers | `quality_ok`; sqz/provider billing still unavailable; Git status output grew |
| Host delegation | Isolated Pi-session worker returned schema-valid compact findings; handoff checked | Minimum one-host exit met; no packaged cross-host enforcement |
| Clean-environment quickstart | Dry-run, disposable installer and Finder registration tests | Covered; native host discovery/approval UX not verified |

## Remaining release gates

1. Run real baseline/old-stack/new-stack engineering tasks and retain trial artifacts; deterministic fixtures are not a substitute.
2. Compare sqz with baseline/RTK only after explicit approval to install/use the third-party binary; capture provider usage only if the host exposes it.
3. Verify native skill discovery and approval UX on each host before advertising support.
4. Package a host adapter only if universal concurrency/budget enforcement is a release requirement; current delegation policy is host-neutral and validated after worker return.

No universal token or cost-reduction percentage is claimed. Exact `o200k_base`
output counts are tokenizer-specific and are not provider billing data.
