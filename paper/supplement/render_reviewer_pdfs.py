#!/usr/bin/env python3
"""Render source-locked Study A/B supplemental PDFs; never run experiments.

Requires reportlab. These are REVIEW COPIES, not approved publisher uploads.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import html
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A3, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import LongTable, Paragraph, SimpleDocTemplate, Spacer, TableStyle

ROOT = Path(__file__).resolve().parents[2]
SPECS = {
    "S0": {
        "source": "paper/tables/table-1-matched-family-outcomes.csv",
        "sha256": "ef29a216b3de050a219e83a0e78c68e3f2f207160418bdafe0a3424a3b94a140",
        "count": 13,
        "columns": (
            "family_id", "treatment_or_policy_variant", "source_id", "outcome",
            "alignment_class", "availability_state", "family_specific_authorized_evidence",
        ),
        "widths": (91, 130, 85, 103, 92, 112, 529),
        "title": "Supplementary Table S0 | Study A matched-family evidence",
        "interpretation": (
            "Four qualified families; 13 member rows; 12 treatment-within-family analysis units. "
            "CF-02 B1-01/B1-05 are alternative policy traces in one B1 analysis unit."
        ),
    },
    "S1": {
        "source": "paper/tables/table-2-deterministic-t1.csv",
        "sha256": "1b1caafd88f04ffc2d65cc589bf66169ca073568ba187ce909a36a50658f0ae7",
        "count": 40,
        "columns": (
            "schedule_id", "schedule_class", "fault_kind_or_control", "phase_or_control",
            "outcome", "alignment", "security_state", "availability_state",
            "verification_complete", "rejection_evidence",
        ),
        "widths": (116, 91, 88, 100, 87, 66, 101, 89, 82, 322),
        "title": "Supplementary Table S1 | Study B deterministic schedule matrix",
        "interpretation": (
            "40 schedules: 1 no-fault control, 31 canonical cells, 8 retry-exhaustion. "
            "SECURE_DEGRADED is a historical outcome enum; affected security_state values remain UNSAFE."
        ),
    },
}

PAGE_W, PAGE_H = landscape(A3)
COLLATE = colors.HexColor("#27364B")
FAINT = colors.HexColor("#E9EEF2")
MUTED = colors.HexColor("#44566A")


def source_rows(spec: dict) -> list[dict[str, str]]:
    source = ROOT / spec["source"]
    actual = hashlib.sha256(source.read_bytes()).hexdigest()
    if actual != spec["sha256"]:
        raise ValueError(f"frozen-source mismatch: {source} {actual}")
    with source.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if tuple(reader.fieldnames or ()) != spec["columns"]:
            raise ValueError(f"unexpected columns: {source}")
        rows = list(reader)
    if len(rows) != spec["count"]:
        raise ValueError(f"unexpected row count: {source}")
    key = spec["columns"][0]
    if len({row[key] for row in rows}) != spec["count"] and key == "schedule_id":
        raise ValueError(f"duplicate schedule IDs: {source}")
    if spec["count"] == 40:
        bad = [row["schedule_id"] for row in rows
               if row["outcome"] == "SECURE_DEGRADED" and row["security_state"] != "UNSAFE"]
        if bad:
            raise ValueError(f"historical outcome semantics changed: {bad}")
    return rows


def make_pdf(supplement: str, dest: Path) -> dict:
    spec = SPECS[supplement]
    rows = source_rows(spec)
    dest.parent.mkdir(parents=True, exist_ok=True)
    document = SimpleDocTemplate(
        str(dest), pagesize=landscape(A3), leftMargin=24, rightMargin=24,
        topMargin=60, bottomMargin=46, pageCompression=1,
        title=spec["title"], author="TT&C recovery research | source-locked supplement",
        subject="Synthetic-model research supplementary table; reviewer draft",
    )
    body = ParagraphStyle("intro", fontName="Helvetica", fontSize=9, leading=13,
                          textColor=COLLATE, alignment=TA_LEFT)
    small = ParagraphStyle("metadata", parent=body, fontSize=8, leading=11,
                           textColor=MUTED, spaceAfter=5)
    th = ParagraphStyle("tablehead", parent=body, fontName="Helvetica-Bold",
                        fontSize=7.2, leading=9, textColor=colors.white, splitLongWords=True)
    td = ParagraphStyle("tablecell", parent=body, fontSize=7.4, leading=10.2,
                        textColor=COLLATE, splitLongWords=True)
    escape = lambda v: html.escape(str(v), quote=False).replace("\n", " ")
    table_data = [[Paragraph("verification_<br/>complete" if col == "verification_complete" else escape(col), th)
                   for col in spec["columns"]]]
    table_data += [[Paragraph(escape(row[col]), td) for col in spec["columns"]] for row in rows]
    assert len(table_data) - 1 == spec["count"]
    assert abs(sum(spec["widths"]) - document.width) < 1
    table = LongTable(table_data, colWidths=spec["widths"], repeatRows=1,
                      hAlign="LEFT", splitByRow=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), COLLATE),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F5F7F9")]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEBELOW", (0, 0), (-1, 0), 0.55, COLLATE),
        ("LINEBELOW", (0, 1), (-1, -1), 0.25, FAINT),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story = [
        Paragraph(escape(spec["interpretation"]), body), Spacer(1, 6),
        Paragraph("Frozen source: <b>" + escape(spec["source"]) + "</b>", small),
        Paragraph("Source SHA-256: " + escape(spec["sha256"]), small),
        Paragraph("Source order and all original fields retained. This is synthetic-model evidence, "
                  "not verified flight, RF, cryptographic or cFS integration performance.", small),
        Spacer(1, 11), table,
    ]

    def decorate(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica-Bold", 13)
        canvas.setFillColor(COLLATE)
        canvas.drawString(24, PAGE_H - 31, spec["title"])
        canvas.setStrokeColor(FAINT)
        canvas.line(24, PAGE_H - 38, PAGE_W - 24, PAGE_H - 38)
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(MUTED)
        canvas.drawString(24, 23, "REVIEW COPY | Frozen synthetic evidence | Not publisher-approved")
        canvas.drawRightString(PAGE_W - 24, 23, f"{supplement} | page {doc.page}")
        canvas.restoreState()

    document.build(story, onFirstPage=decorate, onLaterPages=decorate)
    return {"supplement": supplement, "rows": len(rows), "fields": len(spec["columns"]),
            "source_sha256": spec["sha256"], "pdf": str(dest),
            "pdf_sha256": hashlib.sha256(dest.read_bytes()).hexdigest()}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--only", choices=("S0", "S1", "both"), default="both")
    args = parser.parse_args()
    import json
    for name in SPECS if args.only == "both" else (args.only,):
        print(json.dumps(make_pdf(name, args.out_dir / f"TAES_Supplementary_Table_{name}.pdf"),
                         sort_keys=True))


if __name__ == "__main__":
    main()
