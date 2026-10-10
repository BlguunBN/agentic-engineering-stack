# Context Output Benchmark (RTK measured; sqz/provider comparison pending)

Ran `scripts/benchmark_context.py` on Windows/Python 3.13 with RTK 0.49.0,
three independent trials per variant, and the installed `tiktoken` `o200k_base`
encoding. Values below are medians. Token counts are exact for that encoding,
not provider billing; no provider-level usage was available. RTK and sqz were
never chained. Full raw output for each trial is retained under the ignored
`.agent-state/benchmarks/s6-repeat/` directory on the measured machine.

| Workload | Baseline bytes/tokens | RTK bytes/tokens | Token delta | Evidence and correctness |
|---|---:|---:|---:|---|
| Full test suite | 7,289 / 1,650 | 205 / 48 | -97.09% | `Ran`, `OK`, exit 0; all 3 trials |
| Git status | 455 / 119 | 532 / 141 | +18.49% | RTK wrapper overhead exceeds savings |
| Failing-test diagnostics | 1,920 / 388 | 386 / 101 | -73.97% | `Traceback`, exact `AssertionError`, expected exit 1 |
| Python syntax/build check | 0 / 0 | 79 / 24 | N/A | Both exit 0; baseline output empty |
| MCP-style search JSON | 1,030 / 253 | 1,003 / 250 | -1.19% | All required canonical/personal/untrusted IDs retained |

All configured baseline/RTK trials matched expected exit codes and required
markers (`quality_ok: true`). `coverage_complete` is false because sqz is not
configured/installed; it was not installed as part of this work. The result
supports a reduction in model-input output tokens for the full-test and
failure-diagnostic workloads under this tokenizer, but it is not a provider
usage or cost claim. RTK increased the short git-status workload.

Reproduce:

```bash
python scripts/benchmark_context.py \
  --output-dir .agent-state/benchmarks/s6-repeat \
  --repeats 3 --tokenizer o200k_base
```

The tokenizer option is optional and requires `tiktoken`; without it the
harness records output bytes only. Provider usage can be supplied through
`--provider-usage` only when directly measured. Do not infer tokens from bytes.

## Manual task checkpoints

```bash
python scripts/checkpoint.py --task-id auth-fix --objective "Fix login regression" \
  --constraint "Preserve existing API" --changed-file src/auth.py \
  --receipt .agent-state/evidence/regression.json --usage-ratio 0.82
```

By default this prints a redacted preview and writes nothing. Add `--persist` to
save only `state.md`, `handoff.md`, and `verification.json` under
`.agent-state/tasks/<task-id>/`; the directory is ignored by Git.
`--checkpoint-threshold` defaults to 0.75 but is configurable. The tool only
advises whether to checkpoint; it has no host token-usage hook and does not
automatically compact session history.
