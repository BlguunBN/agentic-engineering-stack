# Evaluation Plan and Current Evidence

## Deterministic routing

`evals/routing/cases.json` contains 56 labeled examples: 36 positive and 20
negative. Every canonical suite has two positive phrasings and one negative
routing contrast. Run:

```bash
python scripts/evaluate_routing.py
```

The evaluator requires at least two positive cases and one negative per suite;
failures include the actual tier/ID and expected decision. This measures the
rule-based router, not model task quality.

## Engineering task trials

`evals/engineering/cases.json` defines three identical tasks for `baseline`,
`old-stack`, and `new-stack`, with verification commands and expected skill
IDs. `scripts/evaluate_engineering.py` validates repeated trial records and
aggregates task success, regression-test pass rate, startup/provider tokens,
latency, tool calls, and invalid/unnecessary activations. It requires a unique
artifact path per trial and retains every success/failure row in the report.

Generate trials only from actual agent runs; do not fill reports with synthetic
results. Example after collecting a complete three-repeat `trials.json` and
artifacts under the repository:

```bash
python scripts/evaluate_engineering.py \
  --trials .agent-state/evals/trials.json \
  --output .agent-state/evals/report.json --repeats 3
```

Provider tokens may be null when unavailable, but must never be inferred from
bytes. The schema fixture tests report aggregation and missing-trial rejection.
No baseline/old-stack/new-stack model comparison is claimed yet; use identical
model, host, task prompts, repository snapshot, and verification commands for
each variant, retaining failures as well as successes.

## Fixtures and coverage

`evals/fixtures/README.md` maps deterministic regression fixtures to engineering
cases. Current measured local evidence is in `docs/context-benchmarks.md` and
`docs/release-readiness.md`.
