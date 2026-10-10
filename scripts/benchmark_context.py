#!/usr/bin/env python3
"""Compare raw, RTK-only, and sqz-only command output without chaining filters."""

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import statistics
import subprocess
import sys
import time
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def _expand(command: list[str]) -> list[str]:
    return [sys.executable if part == "{python}" else part for part in command]


def _run(command: list[str] | None, cwd: Path, output_dir: Path, name: str, expected: int, markers: list[str], timeout: int, tokenizer: Any = None) -> dict:
    if command is None:
        return {"status": "not-configured"}
    argv = _expand(command)
    if not shutil.which(argv[0]):
        return {"status": "unavailable", "reason": f"executable not found: {argv[0]}", "command": argv}
    started = time.perf_counter()
    try:
        result = subprocess.run(argv, cwd=cwd, capture_output=True, timeout=timeout, check=False)
        output = result.stdout + result.stderr
        exit_code = result.returncode
        timed_out = False
    except subprocess.TimeoutExpired as exc:
        output = (exc.stdout or b"") + (exc.stderr or b"")
        exit_code = 124
        timed_out = True
    log_path = output_dir / f"{name}.log"
    log_path.write_bytes(output)
    text = output.decode("utf-8", errors="replace")
    markers_missing = [marker for marker in markers if marker not in text]
    token_count = len(tokenizer.encode(text, disallowed_special=())) if tokenizer is not None else None
    return {
        "status": "ran",
        "command": argv,
        "exit_code": exit_code,
        "expected_exit_code": expected,
        "exit_matches": exit_code == expected,
        "timed_out": timed_out,
        "elapsed_ms": round((time.perf_counter() - started) * 1000, 2),
        "output_bytes": len(output),
        "tokenizer_tokens": token_count,
        "markers_missing": markers_missing,
        "evidence_preserved": not markers_missing,
        "raw_log_path": log_path.name,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", type=Path, default=ROOT / "benchmarks" / "context_workloads.json")
    parser.add_argument("--repo", type=Path, default=ROOT)
    parser.add_argument("--output-dir", type=Path, default=Path(".agent-state/benchmarks"))
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument("--repeats", type=int, default=1, help="Independent trials per command variant (1-10)")
    parser.add_argument("--tokenizer", help="Optional tiktoken encoding name for exact local output-token counts")
    parser.add_argument("--provider-usage", type=Path, help="Optional JSON map of externally measured usage per workload/variant")
    args = parser.parse_args(argv)
    try:
        spec = json.loads(args.spec.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        parser.error(f"Cannot read benchmark spec: {exc}")
    if spec.get("schema_version") != 1 or not isinstance(spec.get("workloads"), list):
        parser.error("Invalid benchmark spec schema")
    if not 1 <= args.repeats <= 10:
        parser.error("--repeats must be between 1 and 10")
    tokenizer = None
    if args.tokenizer:
        try:
            import tiktoken
            tokenizer = tiktoken.get_encoding(args.tokenizer)
        except (ImportError, ValueError) as exc:
            parser.error(f"Cannot load tokenizer {args.tokenizer!r}: {exc}")
    repo = args.repo.resolve()
    output_dir = args.output_dir if args.output_dir.is_absolute() else repo / args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    usage = {}
    if args.provider_usage:
        try:
            usage = json.loads(args.provider_usage.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            parser.error(f"Cannot read provider usage data: {exc}")

    results = {"schema_version": 1, "created_at": datetime.now(timezone.utc).isoformat(), "provider_usage_source": str(args.provider_usage) if args.provider_usage else None, "tokenizer_encoding": args.tokenizer, "repeats": args.repeats, "workloads": []}
    all_quality_ok = True
    coverage_complete = True
    for workload in spec["workloads"]:
        name = workload["name"]
        if not isinstance(name, str) or not name:
            parser.error("Each workload needs a name")
        entry = {"name": name, "variants": {}}
        for variant in ("baseline", "rtk", "sqz"):
            command = workload["commands"].get(variant)
            trials = []
            if command is not None:
                for trial in range(1, args.repeats + 1):
                    suffix = f"{name}.{variant}" if args.repeats == 1 else f"{name}.{variant}.r{trial}"
                    trials.append(_run(command, repo, output_dir, suffix, workload["expected_exit_code"], workload.get("must_contain", []), args.timeout, tokenizer))
            if not trials or trials[0].get("status") != "ran":
                run = trials[0] if trials else {"status": "not-configured"}
                coverage_complete = False
                if variant == "baseline":
                    all_quality_ok = False
            else:
                output_bytes = [trial["output_bytes"] for trial in trials]
                elapsed = [trial["elapsed_ms"] for trial in trials]
                token_counts = [trial["tokenizer_tokens"] for trial in trials if trial["tokenizer_tokens"] is not None]
                markers_missing = sorted({marker for trial in trials for marker in trial["markers_missing"]})
                run = {
                    "status": "ran", "command": trials[0]["command"], "trial_count": len(trials),
                    "trials": trials, "exit_codes": [trial["exit_code"] for trial in trials],
                    "exit_matches": all(trial["exit_matches"] for trial in trials),
                    "timed_out": any(trial["timed_out"] for trial in trials),
                    "elapsed_ms": round(statistics.median(elapsed), 2),
                    "output_bytes": int(statistics.median(output_bytes)),
                    "tokenizer_tokens": int(statistics.median(token_counts)) if token_counts else None,
                    "markers_missing": markers_missing, "evidence_preserved": all(trial["evidence_preserved"] for trial in trials),
                    "raw_log_paths": [trial["raw_log_path"] for trial in trials],
                    "provider_usage": usage.get(name, {}).get(variant) if isinstance(usage.get(name, {}), dict) else None,
                }
                if variant == "baseline":
                    baseline_size = run["output_bytes"]
                    baseline_tokens = run["tokenizer_tokens"]
                else:
                    baseline = entry["variants"].get("baseline", {})
                    baseline_size = baseline.get("output_bytes")
                    baseline_tokens = baseline.get("tokenizer_tokens")
                if baseline_size:
                    run["byte_reduction_vs_baseline_pct"] = round((baseline_size - run["output_bytes"]) / baseline_size * 100, 2)
                if baseline_tokens and run["tokenizer_tokens"] is not None:
                    run["tokenizer_token_reduction_vs_baseline_pct"] = round((baseline_tokens - run["tokenizer_tokens"]) / baseline_tokens * 100, 2)
                all_quality_ok = all_quality_ok and run["exit_matches"] and run["evidence_preserved"]
            entry["variants"][variant] = run
        results["workloads"].append(entry)
    results["quality_ok"] = all_quality_ok
    results["coverage_complete"] = coverage_complete
    results["limits"] = [
        "Each variant ran independently; RTK and sqz were not chained.",
        "Tokenizer counts are exact only for the named tiktoken encoding; provider usage is shown only when supplied from external accounting.",
        "Output bytes are not provider tokens. Provider usage is shown only when supplied from external accounting.",
        "Unavailable tools are reported, not installed."
    ]
    report_path = output_dir / "report.json"
    report_path.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(results, indent=2))
    print(f"Report: {report_path}")
    return 0 if all_quality_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
