#!/usr/bin/env python3
"""Generate/check complete Study A authorized-field Supplement S0 from frozen CSV.

Do not modify, re-label, re-aggregate or execute Studies A–D. Uses stdlib only.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "paper/tables/table-1-matched-family-outcomes.csv"
OUT = ROOT / "paper/supplement/SUPPLEMENTARY_TABLE_S0.md"
SOURCE_SHA256 = "ef29a216b3de050a219e83a0e78c68e3f2f207160418bdafe0a3424a3b94a140"
FIELDS = (
    "family_id",
    "treatment_or_policy_variant",
    "source_id",
    "outcome",
    "alignment_class",
    "availability_state",
    "family_specific_authorized_evidence",
)
EVIDENCE = {
    "CF-01": {"active_key_compromised": False, "security_state": "SECURE_PROVISIONAL"},
    "CF-02": {"security_state": "SECURE_PROVISIONAL", "verification_complete": True},
    "CF-05": {"drop_count": 1, "security_state": "NOT_ESTABLISHED",
              "telemetry_complete": False, "verification_complete": False},
    "CF-06": {"rejection_count": 1, "replay_count": 1, "replay_rejection_count": 1},
}
EXPECTED_ROW_COUNTS = {"CF-01": 4, "CF-02": 5, "CF-05": 2, "CF-06": 2}
EXPECTED_TREATMENTS = {
    "CF-01": ["B0", "B1", "B2", "T1"],
    "CF-02": ["B0", "B1 / B1-01", "B1 / B1-05", "B2", "T1"],
    "CF-05": ["B2", "T1"],
    "CF-06": ["B2", "T1"],
}


def load_rows() -> list[dict[str, str]]:
    digest = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    if digest != SOURCE_SHA256:
        raise ValueError("Frozen Study A source SHA-256 mismatch: " + digest)
    with SOURCE.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != list(FIELDS):
            raise ValueError("Study A source schema mismatch")
        rows = list(reader)
    if len(rows) != 13 or len({(r["family_id"], r["source_id"]) for r in rows}) != 13:
        raise ValueError("Study A must contain 13 unique family/source member rows")
    counts = Counter(r["family_id"] for r in rows)
    if counts != Counter(EXPECTED_ROW_COUNTS):
        raise ValueError(f"Study A family counts changed: {counts}")
    for family, expected in EXPECTED_TREATMENTS.items():
        actual = [r["treatment_or_policy_variant"] for r in rows if r["family_id"] == family]
        if actual != expected:
            raise ValueError(f"Study A treatment/order changed: {family}")
    for r in rows:
        family = r["family_id"]
        if json.loads(r["family_specific_authorized_evidence"]) != EVIDENCE[family]:
            raise ValueError(f"Study A authorized evidence changed: {family}")
        expected_outcome = "INDETERMINATE" if family == "CF-05" else "SUCCESS"
        expected_availability = "DEGRADED" if family == "CF-05" else "AVAILABLE"
        if (r["outcome"], r["alignment_class"], r["availability_state"]) != (
            expected_outcome, "SYNC", expected_availability
        ):
            raise ValueError("Study A terminal label altered")
    return rows


def build_markdown(rows: list[dict[str, str]]) -> str:
    lines = [
        "# Supplementary Table S0 — Full matched-family Study A authorized evidence",
        "",
        "Source: `paper/tables/table-1-matched-family-outcomes.csv` (frozen study).",
        "",
        f"Source SHA-256: `{SOURCE_SHA256}`.",
        "",
        "Population: 4 qualified families, 13 member rows, 12 treatment-within-family analysis units.",
        "CF-02's B1-01 and B1-05 rows are alternative activation-policy traces in **one B1 analysis unit**, not independent replications.",
        "All seven source fields and complete original evidence JSON are retained in source order.",
        "The security labels are synthetic/provisional classifications, not independently verified cryptographic-security claims.",
        "",
        "| " + " | ".join(FIELDS) + " |",
        "|" + "|".join("---" for _ in FIELDS) + "|",
    ]
    for row in rows:
        lines.append("| " + " | ".join(row[k].replace("|", r"\|").replace("\n", " ") for k in FIELDS) + " |")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = build_markdown(load_rows())
    if args.write:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(expected, encoding="utf-8")
        print(f"S0_WRITE=PASS members=13 units=12 sha256={hashlib.sha256(expected.encode()).hexdigest()}")
    else:
        if not OUT.is_file() or OUT.read_text(encoding="utf-8") != expected:
            raise SystemExit("S0_CHECK=FAIL source-locked supplement mismatch")
        print(f"S0_CHECK=PASS members=13 units=12 sha256={hashlib.sha256(expected.encode()).hexdigest()}")


if __name__ == "__main__":
    main()
