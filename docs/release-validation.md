# Release validation report (review snapshots)

**State: review validation only.** No tag or package publication has been made from these review snapshots. Finder has a prior `v0.1.1` release; it predates this Contract v1 review and is not the paired candidate. No Stack release is published. The paired workflow pins Finder exactly; merge/release decisions remain separate.

## Reviewed revisions and hosted evidence

| Repository | Review ref | Revision | Hosted validation |
|---|---|---|---|
| Local Capability Finder | `review/finder-contract-v1` | `1886809b5fce5e340251ca533e1dea89cdf2d50f` | Latest hosted CI passed on Windows/Ubuntu, Python 3.11/3.12/3.13; CLI package smoke passed on both operating systems. Run: https://github.com/BlguunBN/local-capability-finder/actions/runs/38028202593. |
| Agentic Engineering Stack | `stack/verify-and-complete-s6-s8` | `da171055763c7808182a3d8167fe3966d2afef24` | Latest hosted Windows/Ubuntu CI passed on Python 3.11/3.12 with Finder pinned to the code-tested review commit below; latest run: https://github.com/BlguunBN/agentic-engineering-stack/actions/runs/38028441074. Paired integration run: https://github.com/BlguunBN/agentic-engineering-stack/actions/runs/38028435778. |

The paired Stack CI run passed all four OS/Python jobs with Finder pinned to `fcb6ce9e9f977eb553ad7b8f23d9fa6db375bb76`. The Finder review branch's current HEAD adds documentation on top of that tested code commit; its independent current-HEAD CI is linked above. Do not describe this review validation as a published release.

## Local integration and host evidence

- A disposable-home stdio integration registered all 18 `aes:skill:<name>` IDs, searched and loaded one exact skill, retained personal-skill search, and exercised approval-gated activation/deactivation.
- OMP 18.4.4 project MCP configuration connected to Finder; a real `openai-codex/gpt-6-luna` session searched, loaded `aes:skill:systematic-debugging-suite`, fixed a disposable regression fixture, and passed its two unittest regressions. A separate disposable CLI check denied unapproved activation, allowed explicit approval, and removed only the managed target. Details and limitations: [OMP session evidence](evidence/omp-finder-contract-v1-session.md). Native OMP profile discovery and approval UX remain unverified.
- A single isolated Pi-session worker produced a schema-valid compact report. This validates one worker handoff, not packaged host enforcement.
- Stack routing evaluation: 56/56 deterministic cases. Finder retrieval evaluation: 105/105 cases. Synthetic cases are not paid-model quality trials.

## Measured performance and limitations

Three RTK benchmark trials with `o200k_base` reported full-test output tokens down 97.09%, failing-diagnostic output down 73.97%, and `git status` output up 18.49%. These are exact tokenizer counts for captured output—not provider billing, universal context savings, or a model-quality result. RTK is disabled for `git status`. `sqz` was not installed/compared. OMP exposed a coarse five-hour quota change from 0% to 1% around the single coding session; this is rounded, not task-attributed provider usage. One new-stack OMP repair task passed, but no baseline/old-stack/new-stack comparison or model-quality trial is available.

## Remaining release gates

1. Run real baseline/old-stack/new-stack engineering tasks and retain artifacts; record model, prompts, environment, correctness, and timing.
2. Compare `sqz` only after approval to install/use it; capture provider usage only when the host exposes it.
3. Verify host-native discovery and approval UX per supported host; the OMP project-MCP smoke test is not native profile certification.
4. Decide whether universal delegation concurrency/budget enforcement is required; if so, package and test a host adapter.

Until those gates are addressed, keep both PRs in review and do not create compatibility tags or publish releases.
