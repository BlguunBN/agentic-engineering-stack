# Context Output Benchmark (Partial)

Measured locally with RTK 0.49.0 on Windows/Python 3.13 using `benchmarks/context_workloads.json`. One run per variant; output bytes are the metric, not provider tokens. No provider usage data was available. `sqz` was not installed/configured, so the baseline/RTK/sqz comparison and S6 exit criterion remain incomplete.

| Workload | Baseline bytes | RTK bytes | Byte change | Expected evidence retained |
|---|---:|---:|---:|---|
| Full unittest suite (40 tests at capture) | 6,406 | 205 | -96.8% | `Ran`, `OK`; exit 0 |
| Git status | 168 | 245 | +45.8% | Exit 0; RTK wrapper overhead exceeded output savings |
| Failing-test diagnostics | 1,920 | 386 | -79.9% | `Traceback`, exact `AssertionError`; expected exit 1 |
| Python syntax/build check | 0 | 79 | N/A | Both exit 0; RTK emitted a concise completion summary |
| MCP-style search JSON | 1,030 | 1,003 | -2.6% | All three canonical/personal/untrusted IDs retained |

This is a small local sample, not a universal savings claim. RTK reduced passing/failing test output while retaining checked markers, but increased Git-status output; JSON compaction had only a small byte reduction. The harness stores full independent raw logs and reports missing markers/exit mismatches. No RTK+sqz chaining was used.

Reproduce with:

```bash
python scripts/benchmark_context.py --output-dir .agent-state/benchmarks/s6
```

The benchmark output is ignored by Git by default. Configure `sqz` command vectors in the workload spec only after validating the installed version's CLI. Supply actual provider accounting with `--provider-usage` when available; do not infer tokens from bytes.

## Manual task checkpoints

```bash
python scripts/checkpoint.py --task-id auth-fix --objective "Fix login regression" \
  --constraint "Preserve existing API" --changed-file src/auth.py \
  --receipt .agent-state/evidence/regression.json --usage-ratio 0.82
```

By default this prints a redacted preview and writes nothing. Add `--persist` to save only `state.md`, `handoff.md`, and `verification.json` under `.agent-state/tasks/<task-id>/`; the directory is ignored by Git. `--checkpoint-threshold` defaults to 0.75 but is configurable. The tool only advises whether to checkpoint; it has no host token-usage hook and does not automatically compact session history.
