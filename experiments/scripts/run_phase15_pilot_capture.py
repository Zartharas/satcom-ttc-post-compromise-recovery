#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG = ROOT / "experiments" / "configs" / "phase-15-pilot.json"
DEFAULT_BASELINE_CONFIG = (
    ROOT / "experiments" / "configs" / "phase-15-baseline-parity.json"
)
DEFAULT_PROTOCOL = ROOT / "spec" / "phase-15-experiment-protocol-candidate.json"
ANALYSIS_CONFIG = ROOT / "experiments" / "configs" / "phase-08-provisional.json"
BASELINE_CATALOG = ROOT / "tests" / "scenarios" / "baseline-test-catalog.json"


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def utc_text(value: datetime) -> str:
    return value.isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git_text(*args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=False,
        text=True,
        capture_output=True,
    )
    if completed.returncode != 0:
        return "UNKNOWN"
    return completed.stdout.strip()


def build_run_id(start: datetime, commit_sha: str) -> str:
    timestamp = start.strftime("%Y%m%dT%H%M%SZ")
    short_commit = commit_sha[:7] if commit_sha and commit_sha != "UNKNOWN" else "unknown"
    return f"phase15-pilot-{timestamp}-g{short_commit}"


def ensure_new_directory(path: Path) -> None:
    if path.exists():
        raise FileExistsError(f"Run directory already exists: {path}")
    path.mkdir(parents=True)


def relative_files(base: Path, paths: Iterable[Path]) -> list[Path]:
    return sorted(
        (path for path in paths if path.is_file()),
        key=lambda path: path.relative_to(base).as_posix(),
    )


def write_manifest(base: Path, paths: Iterable[Path], destination: Path) -> None:
    lines = []
    for path in relative_files(base, paths):
        if path.resolve() == destination.resolve():
            continue
        relative = path.relative_to(base).as_posix()
        lines.append(f"{sha256_file(path)}  {relative}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        "\n".join(lines) + ("\n" if lines else ""),
        encoding="utf-8",
    )


def verify_manifest(base: Path, manifest: Path) -> None:
    for line in manifest.read_text(encoding="utf-8").splitlines():
        expected, relative = line.split("  ", 1)
        path = base / relative
        if not path.is_file():
            raise RuntimeError(f"Manifest path is missing: {relative}")
        actual = sha256_file(path)
        if actual != expected:
            raise RuntimeError(f"Checksum mismatch for {relative}")


def run_command(command: list[str], stdout_path: Path, stderr_path: Path) -> int:
    completed = subprocess.run(
        command,
        cwd=ROOT,
        check=False,
        text=True,
        capture_output=True,
        env={**os.environ, "PYTHONPATH": str(ROOT / "src")},
    )
    stdout_path.write_text(completed.stdout, encoding="utf-8")
    stderr_path.write_text(completed.stderr, encoding="utf-8")
    return completed.returncode


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Execute and preserve a Phase 15 T1 pipeline and deterministic "
            "B0/B1/B2 metric-parity pilot run."
        )
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        required=True,
        help="Parent directory under which a new immutable run directory is created.",
    )
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument(
        "--baseline-config",
        type=Path,
        default=DEFAULT_BASELINE_CONFIG,
    )
    parser.add_argument("--protocol", type=Path, default=DEFAULT_PROTOCOL)
    parser.add_argument("--run-id", default=None)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    start = utc_now()
    commit_sha = git_text("rev-parse", "HEAD")
    branch = git_text("rev-parse", "--abbrev-ref", "HEAD")
    git_status = git_text("status", "--porcelain")

    config_source = args.config.expanduser().resolve()
    baseline_config_source = args.baseline_config.expanduser().resolve()
    protocol_source = args.protocol.expanduser().resolve()
    for source in (
        config_source,
        baseline_config_source,
        protocol_source,
        ANALYSIS_CONFIG,
        BASELINE_CATALOG,
    ):
        if not source.is_file():
            raise FileNotFoundError(source)

    config_payload = json.loads(config_source.read_text(encoding="utf-8"))
    baseline_config_payload = json.loads(
        baseline_config_source.read_text(encoding="utf-8")
    )
    protocol_payload = json.loads(protocol_source.read_text(encoding="utf-8"))
    if config_payload.get("run_class") != "PILOT_INTERNAL_VALIDATION_ONLY":
        raise ValueError("Phase 15 capture requires PILOT_INTERNAL_VALIDATION_ONLY.")
    if baseline_config_payload.get("run_class") != (
        "PILOT_INTERNAL_VALIDATION_ONLY"
    ):
        raise ValueError("Baseline parity capture requires the pilot run class.")
    if baseline_config_payload.get("metric_parity_status") != (
        "IMPLEMENTED_PENDING_VALIDATION"
    ):
        raise ValueError("Unexpected baseline metric-parity status.")
    if protocol_payload.get("status") != (
        "PROVISIONAL_PROTOCOL_CANDIDATE_NOT_PUBLICATION_EVIDENCE"
    ):
        raise ValueError("Unexpected Phase 15 protocol status.")

    run_id = args.run_id or build_run_id(start, commit_sha)
    run_dir = args.output_root.expanduser().resolve() / run_id
    ensure_new_directory(run_dir)

    config_dir = run_dir / "config"
    raw_dir = run_dir / "raw"
    logs_dir = run_dir / "logs"
    governance_dir = run_dir / "governance"
    manifests_dir = run_dir / "manifests"
    for directory in (config_dir, raw_dir, logs_dir, governance_dir, manifests_dir):
        directory.mkdir(parents=True, exist_ok=True)

    retained_config = config_dir / "phase-15-pilot.json"
    retained_baseline_config = config_dir / "phase-15-baseline-parity.json"
    retained_protocol = config_dir / "phase-15-experiment-protocol-candidate.json"
    retained_analysis_config = config_dir / "phase-08-provisional.json"
    retained_baseline_catalog = config_dir / "baseline-test-catalog.json"
    shutil.copyfile(config_source, retained_config)
    shutil.copyfile(baseline_config_source, retained_baseline_config)
    shutil.copyfile(protocol_source, retained_protocol)
    shutil.copyfile(ANALYSIS_CONFIG, retained_analysis_config)
    shutil.copyfile(BASELINE_CATALOG, retained_baseline_catalog)

    environment_lines = [
        f"python={sys.version.replace(chr(10), ' ')}",
        f"executable={sys.executable}",
        f"platform={platform.platform()}",
        f"machine={platform.machine()}",
        f"processor={platform.processor()}",
    ]
    (logs_dir / "environment.txt").write_text(
        "\n".join(environment_lines) + "\n", encoding="utf-8"
    )
    (logs_dir / "git-status.txt").write_text(
        (git_status if git_status else "CLEAN") + "\n", encoding="utf-8"
    )

    results_json = raw_dir / "phase15-pilot-results.json"
    metrics_csv = raw_dir / "phase15-pilot-metrics.csv"
    runner_command = [
        sys.executable,
        str(ROOT / "experiments" / "scripts" / "run_seeded_fault_experiments.py"),
        "--config",
        str(retained_config),
        "--json-output",
        str(results_json),
        "--csv-output",
        str(metrics_csv),
    ]
    (logs_dir / "command-runner.txt").write_text(
        json.dumps(runner_command) + "\n", encoding="utf-8"
    )
    runner_exit = run_command(
        runner_command,
        logs_dir / "runner-stdout.log",
        logs_dir / "runner-stderr.log",
    )

    baseline_results_json = raw_dir / "phase15-baseline-parity-results.json"
    baseline_metrics_csv = raw_dir / "phase15-baseline-parity-metrics.csv"
    baseline_command = [
        sys.executable,
        str(ROOT / "experiments" / "scripts" / "run_phase15_baseline_parity.py"),
        "--config",
        str(retained_baseline_config),
        "--json-output",
        str(baseline_results_json),
        "--csv-output",
        str(baseline_metrics_csv),
    ]
    (logs_dir / "command-baseline.txt").write_text(
        json.dumps(baseline_command) + "\n", encoding="utf-8"
    )
    baseline_exit = run_command(
        baseline_command,
        logs_dir / "baseline-stdout.log",
        logs_dir / "baseline-stderr.log",
    )

    analysis_exit = None
    analysis_command: list[str] | None = None
    analysis_dir = run_dir / "analysis"
    if runner_exit == 0:
        analysis_command = [
            sys.executable,
            str(ROOT / "experiments" / "scripts" / "analyze_phase07_results.py"),
            "--input-json",
            str(results_json),
            "--metrics-csv",
            str(metrics_csv),
            "--config",
            str(retained_analysis_config),
            "--output-dir",
            str(analysis_dir),
        ]
        (logs_dir / "command-analysis.txt").write_text(
            json.dumps(analysis_command) + "\n", encoding="utf-8"
        )
        analysis_exit = run_command(
            analysis_command,
            logs_dir / "analysis-stdout.log",
            logs_dir / "analysis-stderr.log",
        )

    exclusions = {
        "schema_version": "0.1.0",
        "run_id": run_id,
        "records": [],
        "note": "No exclusion is implied by an empty list.",
    }
    reruns = {
        "schema_version": "0.1.0",
        "run_id": run_id,
        "records": [],
        "note": "No rerun is implied by an empty list.",
    }
    (governance_dir / "exclusions.json").write_text(
        json.dumps(exclusions, indent=2) + "\n", encoding="utf-8"
    )
    (governance_dir / "reruns.json").write_text(
        json.dumps(reruns, indent=2) + "\n", encoding="utf-8"
    )

    end = utc_now()
    overall_exit = runner_exit or baseline_exit or int(analysis_exit or 0)
    metadata = {
        "schema_version": "0.1.0",
        "run_id": run_id,
        "run_class": "PILOT_INTERNAL_VALIDATION_ONLY",
        "publication_evidence": False,
        "repository": "Zartharas/satcom-ttc-post-compromise-recovery",
        "branch": branch,
        "commit_sha": commit_sha,
        "git_status": git_status if git_status else "CLEAN",
        "start_time_utc": utc_text(start),
        "end_time_utc": utc_text(end),
        "config_path": retained_config.relative_to(run_dir).as_posix(),
        "config_sha256": sha256_file(retained_config),
        "baseline_config_path": retained_baseline_config.relative_to(
            run_dir
        ).as_posix(),
        "baseline_config_sha256": sha256_file(retained_baseline_config),
        "baseline_catalog_path": retained_baseline_catalog.relative_to(
            run_dir
        ).as_posix(),
        "baseline_catalog_sha256": sha256_file(retained_baseline_catalog),
        "protocol_path": retained_protocol.relative_to(run_dir).as_posix(),
        "protocol_sha256": sha256_file(retained_protocol),
        "analysis_config_path": retained_analysis_config.relative_to(run_dir).as_posix(),
        "analysis_config_sha256": sha256_file(retained_analysis_config),
        "python_version": sys.version.replace("\n", " "),
        "platform": platform.platform(),
        "runner_command": runner_command,
        "runner_exit_code": runner_exit,
        "baseline_command": baseline_command,
        "baseline_exit_code": baseline_exit,
        "analysis_command": analysis_command,
        "analysis_exit_code": analysis_exit,
        "overall_exit_code": overall_exit,
        "stdout_paths": [
            "logs/runner-stdout.log",
            "logs/baseline-stdout.log",
            "logs/analysis-stdout.log" if analysis_command else None,
        ],
        "stderr_paths": [
            "logs/runner-stderr.log",
            "logs/baseline-stderr.log",
            "logs/analysis-stderr.log" if analysis_command else None,
        ],
        "claim_boundary": {
            "comparative_claim": "NOT_PERMITTED",
            "cryptographic_security_or_pcs": "NOT_PERMITTED",
            "independent_validation": "NOT_PERMITTED",
            "publication_evidence": "NOT_PERMITTED",
        },
    }
    metadata["stdout_paths"] = [value for value in metadata["stdout_paths"] if value]
    metadata["stderr_paths"] = [value for value in metadata["stderr_paths"] if value]
    (governance_dir / "run-metadata.json").write_text(
        json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
    )

    raw_manifest = manifests_dir / "raw.sha256"
    analysis_manifest = manifests_dir / "analysis.sha256"
    bundle_manifest = manifests_dir / "run-bundle.sha256"

    raw_paths = list(config_dir.rglob("*")) + list(raw_dir.rglob("*"))
    write_manifest(run_dir, raw_paths, raw_manifest)
    analysis_paths = list(analysis_dir.rglob("*")) if analysis_dir.exists() else []
    write_manifest(run_dir, analysis_paths, analysis_manifest)
    bundle_paths = [
        path
        for path in run_dir.rglob("*")
        if path.is_file() and path.resolve() != bundle_manifest.resolve()
    ]
    write_manifest(run_dir, bundle_paths, bundle_manifest)

    for manifest in (raw_manifest, analysis_manifest, bundle_manifest):
        verify_manifest(run_dir, manifest)

    print(f"run_id={run_id}")
    print(f"run_directory={run_dir}")
    print(f"runner_exit_code={runner_exit}")
    print(f"baseline_exit_code={baseline_exit}")
    print(f"analysis_exit_code={analysis_exit}")
    print(f"overall_exit_code={overall_exit}")
    print("publication_evidence=false")
    print("capture_manifests=VERIFIED")
    return overall_exit


if __name__ == "__main__":
    raise SystemExit(main())
