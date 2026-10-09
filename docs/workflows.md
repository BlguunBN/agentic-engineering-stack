# Executable Workflow Gates

`workflows/*.json` define minimum evidence for bugfix, feature, refactor, UI, review, infrastructure, and small-change work. `workflow_checks.py` consumes them; the scripts are host-neutral Python and run without a shell.

## Commands

```bash
python scripts/preflight.py --workflow bugfix --scope src tests
python scripts/run_check.py --kind regression --receipt .agent-state/evidence/regression.json -- python -m unittest discover -s tests -v
python scripts/postflight.py --workflow bugfix --receipt .agent-state/evidence/regression.json --report .agent-state/draft-report.md
```

`preflight` lists Git-changed paths, enforces optional allowed path prefixes, and flags sensitive file names and common credential patterns. It reports findings; it does not delete, rewrite, deploy, or install anything.

`run_check.py` executes an argv vector with no shell, records its exit code, command, timestamps, log path, and SHA-256 of the full output log. Failed runs retain the complete log. The receipt proves that the wrapper ran a command and that its output file is unchanged relative to the receipt; it is **not signed or tamper-proof** and does not prove the selected test is semantically sufficient.

`postflight` requires all workflow evidence kinds. A bugfix requires a passing `regression` receipt; a report claiming “tests passed” without a test receipt fails. A not-run reason cannot waive mandatory evidence. Small changes may use `--not-run-reason` when no test is warranted.

## Approval checkpoint

Before any deletion, deployment, infrastructure apply, secret modification, or third-party install, request explicit human approval. `scripts/approval_gate.py` requires a record matching the exact action and target, plus approver, timestamp, and reference. It only emits an authorization decision; it never executes the operation. The record is an auditable local declaration, not cryptographic identity proof.

## Verification limits

The checks can be bypassed by a caller who avoids the scripts, and a test receipt can be mislabeled. CI can enforce the checks for repository changes; host-specific hooks remain optional. No automatic deployment, MCP activation, or skill execution is implemented here.
