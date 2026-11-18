#!/usr/bin/env python3
"""Deterministic citation and supplemental-preservation audit for the TAES draft.

PASS means only that referenced BibTeX keys reconcile and source-locked
supplements exist. It NEVER implies editorial approval, verified DOI metadata,
author declaration approval, copyright clearance or publisher submission.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANUSCRIPT = ROOT / "paper/manuscript/manuscript.md"
BIB = ROOT / "references/bibliography.bib"
SUPPLEMENT = ROOT / "paper/supplement"
ENTRY_RE = re.compile(r"^\s*@[A-Za-z]+\s*\{\s*([A-Za-z0-9_:-]+)\s*,", re.M)
CITATION_RE = re.compile(r"(?<![A-Za-z0-9_.])@([A-Za-z][A-Za-z0-9_:-]*)")
REQUIRED = ("SUPPLEMENTARY_TABLE_S0.md", "SUPPLEMENTARY_TABLE_S1.md", "README.md")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit() -> dict:
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    bibliography = BIB.read_text(encoding="utf-8")
    keys = ENTRY_RE.findall(bibliography)
    citations = CITATION_RE.findall(manuscript)
    keyset, citedset = set(keys), set(citations)
    duplicates = sorted(k for k in keyset if keys.count(k) > 1)
    missing = sorted(citedset - keyset)
    unused = sorted(keyset - citedset)
    missing_supplements = sorted(p for p in REQUIRED if not (SUPPLEMENT / p).is_file())
    # Explicit strings avoid relying on an inferred filename-to-label mapping.
    refs = {
        "S0": "Supplementary Table S0" in manuscript,
        "S1": "Supplementary Table S1" in manuscript,
    }
    failed = bool(duplicates or missing or missing_supplements or not all(refs.values()))
    return {
        "status": "FAIL" if failed else "PASS_CITATION_AND_SUPPLEMENT_LINKAGE_ONLY",
        "manuscript_sha256": digest(MANUSCRIPT),
        "bibliography_sha256": digest(BIB),
        "unique_cited_keys": len(citedset),
        "bibliography_entry_count": len(keys),
        "missing_citation_entries": missing,
        "duplicate_bibliography_keys": duplicates,
        "library_entries_not_cited_or_printed": unused,
        "supplement_main_text_links": refs,
        "missing_supplement_files": missing_supplements,
        "author_metadata_approved": False,
        "funding_and_competing_interest_facts_confirmed": False,
        "ai_use_disclosure_approved": False,
        "all_doi_and_source_claims_verified_by_this_script": False,
        "official_taes_template_compilation_completed": False,
        "complete_raw_data_archived_with_doi": False,
        "publisher_submission_authorized": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", type=Path, help="write optional machine-readable audit")
    args = parser.parse_args()
    report = audit()
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 1 if report["status"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
