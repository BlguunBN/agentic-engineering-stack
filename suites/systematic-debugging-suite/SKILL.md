---
name: systematic-debugging-suite
description: "Master unified systematic debugging suite. Enforces the 4-phase diagnosis loop (Reproduce -> Isolate -> Root Cause -> Fix) with phase-gated safeguards, log analysis, stack trace correlation, and regression prevention. Prevents speculative patching."
use_when: "Diagnosing a bug, regression, crash, or unexpected behavior."
avoid_when: "Implementing a new feature without a failure to diagnose."
entry_inputs: "Observed symptom, reproduction steps, environment, logs, and expected behavior."
workflow: "Reproduce, isolate, establish root cause, apply minimal fix, add regression guard."
verification: "Demonstrate original failure and run the targeted regression test."
exit_output: "Evidence-backed cause, minimal change, and test result."
category: "software-engineering"
---

# Systematic Debugging Suite (Unified Master Skill)

A disciplined problem-solving protocol that eliminates guesswork and speculative code fixes.

## 1. The Iron Law of Debugging
> **NO FIXES WITHOUT CONFIRMED ROOT CAUSE FIRST.**
> If you cannot explain *why* the bug occurred and provide minimal reproduction steps, you are not ready to edit code.

## 2. The 4-Phase Debugging Protocol (GSD & Phase-Gated)

### Phase 1: Reproduce (Ground Truth)
- Capture the exact error message, stack trace, and environment context.
- Create a minimal, deterministic reproduction script or failing unit test.
- Verify that the failure is genuine and repeatable.

### Phase 2: Isolate (Binary Search / Trace)
- Narrow the blast radius: Which subsystem, file, and function is responsible?
- Inspect inputs and outputs across module boundaries.
- Distinguish between symptom (where it blew up) and source (where bad state originated).

### Phase 3: Root Cause Discovery
- Formulate a falsifiable hypothesis: *"The error happens because X receives Y under condition Z."*
- Prove the hypothesis with targeted logging or debugger inspection.
- Check recent commits (`git log -p`) or config changes if this is a regression.

### Phase 4: Surgical Fix & Regression Guard
- Apply the minimal responsible change (Ponytail ladder: don't rewrite surrounding code).
- Re-run the reproduction test: verify it now passes (green).
- Run the full test suite to confirm no collateral regressions.

## 3. Tool Selection for Investigation

| Scenario | Recommended Approach |
|---|---|
| Unit/integration test failure | Run failing test directly with verbose flags (`pytest -vv -s` / `vitest run`). |
| Silent UI failure / blank page | Use browser console & network tab logs (`web-debug` / `agent-browser`). |
| Complex distributed system / async flake | Correlate request IDs and timeline logs (`debugging-wizard`). |
| Repeated failed AI repair attempts | Engage `phase-gated-debugging` to lock code edits until causal proof is written. |
