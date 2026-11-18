#!/usr/bin/env python3
"""Build/check the complete, unmodified Study B 40-schedule supplementary table.

This is a formatting derivative. It never executes, changes or reclassifies
the retained research experiment. Only Python stdlib is required.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "paper/tables/table-2-deterministic-t1.csv"
OUT = ROOT / "paper/supplement/SUPPLEMENTARY_TABLE_S1.md"
SHA256 = "1b1caafd88f04ffc2d65cc589bf66169ca073568ba187ce909a36a50658f0ae7"

FIELDS = (
    "schedule_id",
    "schedule_class",
    "fault_kind_or_control",
    "phase_or_control",
    "outcome",
    "alignment",
    "security_state",
    "availability_state",
    "verification_complete",
    "rejection_evidence",
)


def load_rows() -> list[dict[str, str]]:
    original = SOURCE.read_bytes()
    actual = hashlib.sha256(original).hexdigest()
    if actual != SHA256:
        raise ValueError(f"Study B tracked source hash differs: {actual}")
    with SOURCE.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != list(FIELDS):
            raise ValueError(f"Study B source schema changed: {reader.fieldnames}")
        rows = list(reader)
    if len(rows) != 40 or len({r["schedule_id"] for r in rows}) != 40:
        raise ValueError("Study B population must be exactly 40 unique schedules")
    classes = Counter(r["schedule_class"] for r in rows)
    if classes != Counter({"CONTROL": 1, "CANONICAL_CELL": 31, "RETRY_EXHAUSTION": 8}):
        raise ValueError(f"Study B class population mismatch: {classes}")
    by_class = {
        name: Counter(r["outcome"] for r in rows if r["schedule_class"] == name)
        for name in classes
    }
    if by_class["CONTROL"] != Counter({"SUCCESS": 1}):
        raise ValueError("Control result changed")
    if by_class["CANONICAL_CELL"] != Counter(
        {"SUCCESS": 25, "INDETERMINATE": 4, "EXPIRED": 1, "SECURE_DEGRADED": 1}
    ):
        raise ValueError("Canonical result counts changed")
    if by_class["RETRY_EXHAUSTION"] != Counter({"EXPIRED": 6, "SECURE_DEGRADED": 2}):
        raise ValueError("Exhaustion results changed")
    for row in rows:
        evidence = json.loads(row["rejection_evidence"])
        if not isinstance(evidence, dict):
            raise ValueError("rejection evidence is not a dict")
        if row["verification_complete"] not in {"True", "False"}:
            raise ValueError("non-boolean verification_complete")
        if row["outcome"] == "SECURE_DEGRADED" and row["security_state"] != "UNSAFE":
            raise ValueError("The historical SECURE_DEGRADED enum must retain UNSAFE state")
    return rows


def md_escape(value: str) -> str:
    return value.replace("|", r"\|").replace("\n", " ")


def build_markdown(rows: list[dict[str, str]]) -> str:
    lines = [
        "# Supplementary Table S1 — Complete Study B Deterministic Schedule Matrix",
        "",
        "Source: `paper/tables/table-2-deterministic-t1.csv` from the frozen study.",
        "",
        f"Source SHA-256: `{SHA256}`.",
        "",
        "Population: 40 fixed schedules (1 no-fault control; 31 canonical cells; 8 retry-exhaustion cases).",
        "The table preserves all ten recorded fields in original source order; no row is excluded or aggregated.",
        "The historical outcome enum `SECURE_DEGRADED` does **not** imply security: affected rows retain `security_state=UNSAFE`.",
        "This is synthetic-model evidence, not an operational spacecraft reliability or cryptographic-security measurement.",
        "",
        "| " + " | ".join(FIELDS) + " |",
        "|" + "|".join("---" for _ in FIELDS) + "|",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_escape(row[key]) for key in FIELDS) + " |")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--write", action="store_true")
    group.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = build_markdown(load_rows())
    if args.write:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(expected, encoding="utf-8")
        print(f"S1_WRITE=PASS rows=40 sha256={hashlib.sha256(expected.encode()).hexdigest()}")
    else:
        if not OUT.exists() or OUT.read_text(encoding="utf-8") != expected:
            raise SystemExit("S1_CHECK=FAIL generated supplement differs from frozen CSV")
        print(f"S1_CHECK=PASS rows=40 sha256={hashlib.sha256(expected.encode()).hexdigest()}")


if __name__ == "__main__":
    main()
