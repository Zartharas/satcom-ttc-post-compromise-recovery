from __future__ import annotations

import re
from typing import Dict, Iterable, Mapping


MATRIX_STATUS = "DEFINED_PENDING_VALIDATION_NOT_COMPARATIVE_EVIDENCE"
ALLOWED_CLASSIFICATIONS = {
    "QUALIFIED_MATCH",
    "DIAGNOSTIC_FAMILY_ONLY",
}
ALIGNMENT_CLASSES = {
    "SYNC",
    "G_AHEAD",
    "S_AHEAD",
    "DIVERGED",
    "LOCKED",
}

_SYNC_PATTERN = re.compile(r"^SYNC\([0-9]+\)$")


def normalize_alignment(value: object) -> str:
    """Return the treatment-independent categorical alignment class.

    Epoch-bearing synchronized states are reduced to ``SYNC``. Other declared
    abstract classes are preserved. Unknown values are rejected instead of
    being silently grouped.
    """

    text = str(value)
    if _SYNC_PATTERN.fullmatch(text):
        return "SYNC"
    if text in ALIGNMENT_CLASSES - {"SYNC"}:
        return text
    raise ValueError(f"Unsupported alignment value: {text}")


def project_allowed_metrics(
    metrics: Mapping[str, object],
    allowed_fields: Iterable[str],
) -> Dict[str, object]:
    """Project one result onto a pre-authorized family field set.

    ``alignment_class`` is derived from ``alignment``. Every other requested
    field must exist in the supplied metric record. This helper deliberately
    performs no aggregation or statistical comparison.
    """

    projection: Dict[str, object] = {}
    for field in allowed_fields:
        if field == "alignment_class":
            if "alignment" not in metrics:
                raise KeyError("alignment")
            projection[field] = normalize_alignment(metrics["alignment"])
            continue
        if field not in metrics:
            raise KeyError(field)
        projection[field] = metrics[field]
    return projection


def catalog_member_key(treatment: str, scenario_id: str) -> str:
    return f"{treatment}:{scenario_id}"


__all__ = [
    "ALIGNMENT_CLASSES",
    "ALLOWED_CLASSIFICATIONS",
    "MATRIX_STATUS",
    "catalog_member_key",
    "normalize_alignment",
    "project_allowed_metrics",
]
