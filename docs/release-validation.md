# Release validation report (review snapshots)

**State: review validation only.** No release tags, published Finder/Stack versions, package publication, or production rollout have been created. The paired workflow pins Finder exactly; merge/release decisions remain separate.

## Reviewed revisions and hosted evidence

| Repository | Review ref | Revision | Hosted validation |
|---|---|---|---|
| Local Capability Finder | `review/finder-contract-v1` | `fcb6ce9e9f977eb553ad7b8f23d9fa6db375bb76` | CI passed on Windows and Ubuntu, Python 3.11/3.12/3.13; CLI package smoke passed on both operating systems. |
| Agentic Engineering Stack | `stack/verify-and-complete-s6-s8` | `6bff1d582c037f86bce365ae8a5011266eac20b2` | Hosted Windows/Ubuntu CI passed on Python 3.11/3.12 with the exact Finder pin above; the run exercised live MCP contract tests. |

[Joint Stack CI run](https://github.com/BlguunBN/agentic-engineering-stack/actions/runs/38028044978) passed all four OS/Python jobs with Finder pinned to `fcb6ce9e9f977eb553ad7b8f23d9fa6db375bb76`. The Stack commit under test was `6bff1d582c037f86bce365ae8a5011266eac20b2`; the subsequent report-only documentation update does not change code or workflow behavior. Do not describe this review validation as a published release.

## Local integration and host evidence

- A disposable-home stdio integration registered all 18 `aes:skill:<name>` IDs, searched and loaded one exact skill, retained personal-skill search, and exercised approval-gated activation/deactivation.
- OMP 18.4.4 connected to Finder and exposed all nine Contract v1 tools. No model turn or end-to-end skill use occurred.
- A single isolated Pi-session worker produced a schema-valid compact report. This validates one worker handoff, not packaged host enforcement.
- Stack routing evaluation: 56/56 deterministic cases. Finder retrieval evaluation: 105/105 cases. Synthetic cases are not paid-model quality trials.

## Measured performance and limitations

Three RTK benchmark trials with `o200k_base` reported full-test output tokens down 97.09%, failing-diagnostic output down 73.97%, and `git status` output up 18.49%. These are exact tokenizer counts for captured output—not provider billing, universal context savings, or a model-quality result. RTK is disabled for `git status`. `sqz` was not installed/compared; provider token usage was not captured. No real baseline/old-stack/new-stack engineering-task trials are available.

## Remaining release gates

1. Run real baseline/old-stack/new-stack engineering tasks and retain artifacts; record model, prompts, environment, correctness, and timing.
2. Compare `sqz` only after approval to install/use it; capture provider usage only when the host exposes it.
3. Verify host-native discovery, search/load, and approval UX per supported host before advertising support.
4. Decide whether universal delegation concurrency/budget enforcement is required; if so, package and test a host adapter.

Until those gates are addressed, keep both PRs in review and do not create compatibility tags or publish releases.
