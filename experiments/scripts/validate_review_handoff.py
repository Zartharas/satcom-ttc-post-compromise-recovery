from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


CATALOG_PATH = Path("tests/scenarios/baseline-test-catalog.json")
FREEZE_PATH = Path("spec/baseline-oracle-freeze-candidate.json")
ORACLE_FIELDS = (
    "id",
    "baseline",
    "compromise",
    "activation_policy",
    "faults",
    "expected_alignment",
    "expected_joint_state",
    "expected_outcome",
)
ALLOWED_STATUSES = {
    "PENDING_INDEPENDENT_REVIEW",
    "ACCEPTED",
    "ACCEPTED_WITH_CORRECTIONS",
    "REJECTED",
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_oracle(item: dict[str, Any]) -> dict[str, Any]:
    return {
        field: item.get(field)
        for field in ORACLE_FIELDS
        if field in item or field in {"activation_policy", "expected_joint_state"}
    }


def validate_candidate(root: Path) -> list[str]:
    errors: list[str] = []
    catalog = load_json(root / CATALOG_PATH)
    freeze = load_json(root / FREEZE_PATH)

    status = freeze.get("status")
    if status not in ALLOWED_STATUSES:
        errors.append(f"Unsupported freeze status: {status!r}")

    catalog_items = catalog.get("tests", [])
    freeze_items = freeze.get("oracles", [])

    catalog_ids = [item.get("id") for item in catalog_items]
    freeze_ids = [item.get("id") for item in freeze_items]

    if len(catalog_ids) != len(set(catalog_ids)):
        errors.append("Scenario catalog contains duplicate IDs.")
    if len(freeze_ids) != len(set(freeze_ids)):
        errors.append("Oracle freeze candidate contains duplicate IDs.")

    catalog_by_id = {item["id"]: canonical_oracle(item) for item in catalog_items}
    freeze_by_id = {item["id"]: canonical_oracle(item) for item in freeze_items}

    missing = sorted(set(catalog_by_id) - set(freeze_by_id))
    extra = sorted(set(freeze_by_id) - set(catalog_by_id))
    if missing:
        errors.append(f"Freeze candidate is missing scenario IDs: {', '.join(missing)}")
    if extra:
        errors.append(f"Freeze candidate has unknown scenario IDs: {', '.join(extra)}")

    for scenario_id in sorted(set(catalog_by_id) & set(freeze_by_id)):
        if catalog_by_id[scenario_id] != freeze_by_id[scenario_id]:
            errors.append(
                f"{scenario_id} differs between catalog and freeze candidate: "
                f"catalog={catalog_by_id[scenario_id]!r}, "
                f"freeze={freeze_by_id[scenario_id]!r}"
            )

    review = freeze.get("review", {})
    if status == "ACCEPTED":
        required = (
            "reviewer_name",
            "review_date",
            "approved_commit",
            "ci_run_id",
        )
        for field in required:
            if not review.get(field):
                errors.append(f"Accepted freeze is missing review.{field}.")
        if review.get("decision") != "ACCEPT":
            errors.append("Accepted freeze must record review.decision as ACCEPT.")
        if review.get("manifest_verified") is not True:
            errors.append("Accepted freeze must record manifest_verified=true.")

    return errors


def markdown_table(root: Path) -> str:
    freeze = load_json(root / FREEZE_PATH)
    lines = [
        "| ID | Baseline | Compromise | Activation policy | Faults | Alignment | Joint state | Outcome |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for item in freeze.get("oracles", []):
        faults = "<br>".join(item.get("faults", [])) or "None"
        lines.append(
            "| {id} | {baseline} | {compromise} | {policy} | {faults} | "
            "{alignment} | {joint} | {outcome} |".format(
                id=item["id"],
                baseline=item["baseline"],
                compromise=item["compromise"],
                policy=item.get("activation_policy", "N/A"),
                faults=faults,
                alignment=item["expected_alignment"],
                joint=item.get("expected_joint_state", "N/A"),
                outcome=item["expected_outcome"],
            )
        )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate the Phase 05 review handoff and oracle-freeze candidate."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[2],
        help="Repository root. Defaults to the root inferred from this script.",
    )
    parser.add_argument(
        "--markdown",
        action="store_true",
        help="Print the candidate oracle matrix as Markdown after validation.",
    )
    args = parser.parse_args()

    errors = validate_candidate(args.root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    freeze = load_json(args.root / FREEZE_PATH)
    print(
        f"Review handoff valid: {len(freeze['oracles'])} scenario oracles, "
        f"status={freeze['status']}."
    )
    if args.markdown:
        print()
        print(markdown_table(args.root))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
