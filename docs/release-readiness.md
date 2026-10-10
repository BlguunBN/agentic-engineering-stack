# Release Readiness Matrix

| Scenario | Local evidence | State |
|---|---|---|
| Stack only | Manifest, routing, workflows, lint, installer tests | Full tests pass on Windows and WSL Ubuntu |
| Stack + Finder Contract v1 | Live stdio integration with Finder 0.2.0 in disposable home/library | Passes locally; paired revisions not published/pinned for hosted CI |
| Finder unavailable/legacy | Version-gated client; Tier 1 standalone routing remains usable | Unit-tested |
| Specialist search | Live personal-skill result plus mock blocked-result cases | Tested; search does not execute or activate content |
| Activation safety | Preview recheck, exact approval record, live create/remove in disposable home | Tested on Windows and WSL |
| Malicious third-party skill | Mock blocked load; Finder P8 blocked-import fixture | Fixture-tested; no live adversarial host test |
| Output compression | Three baseline/RTK trials, `o200k_base` token counts, required diagnostics markers | `quality_ok`; sqz/provider billing still unavailable; Git status output grew |
| Host delegation | Isolated Pi-session worker returned schema-valid compact findings; handoff checked | Minimum one-host exit met; no packaged cross-host enforcement |
| Clean-environment quickstart | Dry-run, disposable installer and Finder registration tests | Covered; native host discovery/approval UX not verified |

## Remaining release gates

1. Publish/pin Finder 0.2.x and Stack Contract v1 revisions together, then trigger hosted CI against that pair.
2. Compare sqz with baseline/RTK after explicit approval to install/use the third-party binary; capture provider billing only if the host exposes it.
3. Package a host adapter only if universal concurrency/budget enforcement is a release requirement; current delegation policy is host-neutral and validated after worker return.
4. Verify native skill discovery and approval UX on each host before advertising support.

No universal token or cost-reduction percentage is claimed. Exact `o200k_base`
output counts are tokenizer-specific and are not provider billing data.
