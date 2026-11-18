#!/usr/bin/env python3
"""Fail-closed editorial readiness registry audit; does not approve submission.

Successful default execution confirms that unresolved author/publisher gates
are still present. `--require-ready` intentionally fails while this hold-only
registry is in force. Standard library only; no network or private data.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

REGISTRY = Path(__file__).with_name("taes_release_gates.json")
REQUIRED = frozenset({
    "official_template_and_final_pdf",
    "table_i_and_float_legibility",
    "supplements_reviewer_access",
    "claim_level_reference_audit",
    "author_identity_and_orcid",
    "ai_contribution_disclosure",
    "funding_conflicts_and_rights",
    "originality_and_submission_overlap",
    "raw_evidence_access_and_licenses",
    "final_author_signoff",
})


def audit(record: object) -> dict:
    errors = []
    if not isinstance(record, dict):
        return {"status": "FAIL", "errors": ["registry must be an object"]}
    if record.get("schema_version") != "1.0":
        errors.append("unsupported schema_version")
    if record.get("snapshot_date") != "2026-11-18":
        errors.append("unexpected snapshot date")
    if record.get("reviewed_main_sha") != "1bda511862f104e82bddcbf95db1ee97702e6c02":
        errors.append("unreviewed main revision")
    for key in (
        "publisher_submission_authorized",
        "author_approval_documented",
        "private_author_disclosures_committed",
        "publication_ready",
    ):
        if record.get(key) is not False:
            errors.append(f"{key} must explicitly be false")
    gates = record.get("gates")
    if not isinstance(gates, dict) or set(gates) != REQUIRED:
        errors.append("release gate set mismatch")
    else:
        for gate, state in sorted(gates.items()):
            if state != "HOLD":
                errors.append(f"{gate} must remain HOLD pending a separate reviewed release process")
    return {
        "status": "PASS_HOLDS_ENFORCED_ONLY" if not errors else "FAIL",
        "gate_count": len(REQUIRED),
        "publisher_submission_authorized": False,
        "publication_ready": False,
        "errors": errors,
    }


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--require-ready", action="store_true", help="Fail closed until a separately approved release process exists")
    p.add_argument("--json", type=Path, help="Write a machine-readable check report")
    args = p.parse_args()
    try:
        record = json.loads(REGISTRY.read_text(encoding="utf-8"))
        result = audit(record)
    except (OSError, ValueError) as exc:
        result = {"status": "FAIL", "errors": [f"cannot read registry: {exc}"]}
    if args.json:
        args.json.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "PASS_HOLDS_ENFORCED_ONLY":
        return 1
    return 3 if args.require_ready else 0


if __name__ == "__main__":
    raise SystemExit(main())
