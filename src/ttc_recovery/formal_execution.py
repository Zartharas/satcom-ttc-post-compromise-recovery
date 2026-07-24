from __future__ import annotations

import hashlib
import json
import platform
import re
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Sequence


NO_COUNTEREXAMPLE_STATUS = "NO_COUNTEREXAMPLE_WITHIN_RECORDED_BOUND"
EXPECTED_NEGATIVE_STATUS = "EXPECTED_NEGATIVE_CONTROL_COUNTEREXAMPLE_CAPTURED"
COUNTEREXAMPLE_STATUS = "COUNTEREXAMPLE_FOUND"
TOOL_ERROR_STATUS = "TOOL_ERROR"


@dataclass(frozen=True)
class CommandResult:
    command: tuple[str, ...]
    returncode: int
    output: str


@dataclass(frozen=True)
class TlcSummary:
    status: str
    generated_states: int | None
    distinct_states: int | None
    queued_states: int | None
    search_depth: int | None
    violated_invariant: str | None
    trace_state_count: int


def sha1_file(path: Path) -> str:
    digest = hashlib.sha1()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _integer(value: str) -> int:
    return int(value.replace(",", ""))


def parse_tlc_summary(output: str, returncode: int) -> TlcSummary:
    states_match = re.search(
        r"([\d,]+) states generated, ([\d,]+) distinct states found, "
        r"([\d,]+) states left on queue",
        output,
    )
    depth_match = re.search(
        r"depth of the complete state graph search is ([\d,]+)",
        output,
        re.IGNORECASE,
    )
    violation_match = re.search(
        r"Invariant\s+([A-Za-z0-9_]+)\s+is violated",
        output,
        re.IGNORECASE,
    )
    trace_state_count = len(re.findall(r"(?m)^State\s+\d+:", output))

    if violation_match:
        status = COUNTEREXAMPLE_STATUS
    elif returncode == 0 and "No error has been found" in output:
        status = NO_COUNTEREXAMPLE_STATUS
    else:
        status = TOOL_ERROR_STATUS

    return TlcSummary(
        status=status,
        generated_states=_integer(states_match.group(1)) if states_match else None,
        distinct_states=_integer(states_match.group(2)) if states_match else None,
        queued_states=_integer(states_match.group(3)) if states_match else None,
        search_depth=_integer(depth_match.group(1)) if depth_match else None,
        violated_invariant=violation_match.group(1) if violation_match else None,
        trace_state_count=trace_state_count,
    )


def extract_counterexample_trace(output: str) -> list[dict[str, object]]:
    matches = list(re.finditer(r"(?m)^State\s+(\d+):\s*(.*)$", output))
    states: list[dict[str, object]] = []
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(output)
        body = output[start:end].strip()
        assignments: dict[str, str] = {}
        for line in body.splitlines():
            assignment = re.match(r"\s*/\\\s+([A-Za-z0-9_]+)\s*=\s*(.+?)\s*$", line)
            if assignment:
                assignments[assignment.group(1)] = assignment.group(2)
        states.append(
            {
                "state_number": int(match.group(1)),
                "label": match.group(2).strip(),
                "assignments": assignments,
                "raw_body": body,
            }
        )
    return states


def run_command(
    command: Sequence[str],
    *,
    cwd: Path,
    timeout_seconds: int,
) -> CommandResult:
    completed = subprocess.run(
        list(command),
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        timeout=timeout_seconds,
        check=False,
    )
    return CommandResult(tuple(command), completed.returncode, completed.stdout)


def _command_record(result: CommandResult) -> dict[str, object]:
    return {
        "command": list(result.command),
        "returncode": result.returncode,
    }


def _write_manifest(output_dir: Path, names: Iterable[str]) -> Path:
    manifest = output_dir / "phase10-derived-bundle.sha256"
    lines = [f"{sha256_file(output_dir / name)}  {name}" for name in sorted(names)]
    manifest.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return manifest


def execute_formal_model(
    *,
    jar_path: Path,
    output_dir: Path,
    repository_root: Path,
    java_command: str = "java",
    expected_jar_sha1: str,
    tool_version: str,
    timeout_seconds: int = 120,
) -> dict[str, object]:
    jar_path = jar_path.resolve()
    output_dir = output_dir.resolve()
    repository_root = repository_root.resolve()
    formal_dir = repository_root / "formal" / "tla"
    spec_path = formal_dir / "T1Recovery.tla"
    positive_config = formal_dir / "MC.cfg"
    negative_config = formal_dir / "NegativeControl.cfg"

    for required in (jar_path, spec_path, positive_config, negative_config):
        if not required.is_file():
            raise FileNotFoundError(required)

    actual_sha1 = sha1_file(jar_path)
    if actual_sha1.lower() != expected_jar_sha1.lower():
        raise ValueError(
            f"tla2tools.jar SHA-1 mismatch: expected {expected_jar_sha1}, got {actual_sha1}"
        )

    output_dir.mkdir(parents=True, exist_ok=True)
    positive_meta = output_dir / "tlc-meta-positive"
    negative_meta = output_dir / "tlc-meta-negative-control"
    positive_meta.mkdir(exist_ok=True)
    negative_meta.mkdir(exist_ok=True)

    java_version = run_command(
        [java_command, "-version"],
        cwd=formal_dir,
        timeout_seconds=timeout_seconds,
    )
    sany = run_command(
        [java_command, "-cp", str(jar_path), "tla2sany.SANY", spec_path.name],
        cwd=formal_dir,
        timeout_seconds=timeout_seconds,
    )
    positive = run_command(
        [
            java_command,
            "-XX:+UseParallelGC",
            "-cp",
            str(jar_path),
            "tlc2.TLC",
            "-workers",
            "1",
            "-config",
            positive_config.name,
            "-metadir",
            str(positive_meta),
            spec_path.name,
        ],
        cwd=formal_dir,
        timeout_seconds=timeout_seconds,
    )
    negative = run_command(
        [
            java_command,
            "-XX:+UseParallelGC",
            "-cp",
            str(jar_path),
            "tlc2.TLC",
            "-workers",
            "1",
            "-config",
            negative_config.name,
            "-metadir",
            str(negative_meta),
            spec_path.name,
        ],
        cwd=formal_dir,
        timeout_seconds=timeout_seconds,
    )

    positive_summary = parse_tlc_summary(positive.output, positive.returncode)
    negative_summary = parse_tlc_summary(negative.output, negative.returncode)
    negative_trace = extract_counterexample_trace(negative.output)

    if sany.returncode != 0:
        overall_status = TOOL_ERROR_STATUS
    elif positive_summary.status != NO_COUNTEREXAMPLE_STATUS:
        overall_status = TOOL_ERROR_STATUS
    elif (
        negative_summary.status == COUNTEREXAMPLE_STATUS
        and negative_summary.violated_invariant == "NegativeControlNoActivation"
        and negative_trace
    ):
        overall_status = EXPECTED_NEGATIVE_STATUS
    else:
        overall_status = TOOL_ERROR_STATUS

    logs = {
        "phase10-java-version.log": java_version.output,
        "phase10-sany.log": sany.output,
        "phase10-tlc-positive.log": positive.output,
        "phase10-tlc-negative-control.log": negative.output,
    }
    for name, content in logs.items():
        (output_dir / name).write_text(content, encoding="utf-8")

    counterexample_record = {
        "schema_version": "0.1.0",
        "status": EXPECTED_NEGATIVE_STATUS
        if negative_summary.status == COUNTEREXAMPLE_STATUS
        else negative_summary.status,
        "testing_role": "INTENTIONAL_PIPELINE_NEGATIVE_CONTROL",
        "violated_invariant": negative_summary.violated_invariant,
        "trace_state_count": len(negative_trace),
        "trace": negative_trace,
        "interpretation_boundary": (
            "This counterexample is intentionally induced to test capture and does not represent "
            "a discovered flaw in the provisional recovery treatment."
        ),
    }
    counterexample_name = "phase10-negative-control-counterexample.json"
    (output_dir / counterexample_name).write_text(
        json.dumps(counterexample_record, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    report = {
        "schema_version": "0.1.0",
        "phase": "Phase 10",
        "status": overall_status,
        "claim_status": "PROVISIONAL_INTERNAL_REVIEW_ONLY",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "toolchain": {
            "tool": "TLA+ command-line tools",
            "tool_version": tool_version,
            "jar_path": str(jar_path),
            "jar_sha1": actual_sha1,
            "jar_sha256": sha256_file(jar_path),
            "java_version_output": java_version.output.strip(),
            "platform": platform.platform(),
            "worker_count": 1,
        },
        "inputs": {
            "spec": str(spec_path.relative_to(repository_root)),
            "spec_sha256": sha256_file(spec_path),
            "positive_config": str(positive_config.relative_to(repository_root)),
            "positive_config_sha256": sha256_file(positive_config),
            "negative_config": str(negative_config.relative_to(repository_root)),
            "negative_config_sha256": sha256_file(negative_config),
        },
        "sany": {
            "status": "PARSE_SUCCESS" if sany.returncode == 0 else "PARSE_FAILURE",
            **_command_record(sany),
        },
        "positive_model_check": {
            "status": positive_summary.status,
            "interpretation": (
                "No counterexample was found within the exact finite constants and TLC execution "
                "recorded here; this is not a proof of concrete cryptographic security."
            ),
            "generated_states": positive_summary.generated_states,
            "distinct_states": positive_summary.distinct_states,
            "queued_states": positive_summary.queued_states,
            "search_depth": positive_summary.search_depth,
            **_command_record(positive),
        },
        "negative_control": {
            "status": counterexample_record["status"],
            "violated_invariant": negative_summary.violated_invariant,
            "trace_state_count": len(negative_trace),
            "testing_role": "INTENTIONAL_PIPELINE_NEGATIVE_CONTROL",
            **_command_record(negative),
        },
        "publication_evidence_status": "NOT_PERMITTED",
        "review_boundary": (
            "Independent review is required before freezing the formal property set, mapping this "
            "abstraction to a concrete protocol, or using model-checking output as publication or "
            "security evidence."
        ),
    }
    report_name = "phase10-formal-execution.json"
    (output_dir / report_name).write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    derived_names = [report_name, counterexample_name, *logs.keys()]
    _write_manifest(output_dir, derived_names)

    if overall_status != EXPECTED_NEGATIVE_STATUS:
        raise RuntimeError(
            "Phase 10 formal execution did not satisfy parse, positive-model, and negative-control gates."
        )
    return report


__all__ = [
    "COUNTEREXAMPLE_STATUS",
    "CommandResult",
    "EXPECTED_NEGATIVE_STATUS",
    "NO_COUNTEREXAMPLE_STATUS",
    "TOOL_ERROR_STATUS",
    "TlcSummary",
    "execute_formal_model",
    "extract_counterexample_trace",
    "parse_tlc_summary",
    "run_command",
    "sha1_file",
    "sha256_file",
]
