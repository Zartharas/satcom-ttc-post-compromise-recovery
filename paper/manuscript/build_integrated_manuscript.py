#!/usr/bin/env python3
# Build the submission-facing integrated manuscript from tracked section/data sources.

from __future__ import annotations

import csv
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANUSCRIPT_DIR = ROOT / "paper" / "manuscript"
TABLE_DIR = ROOT / "paper" / "tables"
FIGURE_DIR = ROOT / "paper" / "figures"

TITLE = (
    "Post-Compromise Satellite TT&C Resynchronization Under Intermittent Links: "
    "A Controlled Fault-Injection Study"
)

ABSTRACT = '''Fresh key establishment does not by itself restore trusted telemetry, tracking, and command (TT&C) operation after compromise when intermittent contact, message loss, and endpoint state loss can leave ground and spacecraft on different recovery states. We study this operational resynchronization problem in a deterministic software model containing three project-defined baseline abstractions and a bounded resynchronization controller (T1). The final experiment was predeclared and retained without outcome-driven reruns. It includes four qualified matched families, 40 deterministic T1 schedules, a fixed 100-schedule mixed-fault population, a 3 x 3 sensitivity grid totaling 108 executions, and bounded TLA+/Python trace comparisons. The matched families showed categorical parity rather than treatment superiority. Across 31 canonical deterministic fault cells, 25 terminated successfully, four were indeterminate because post-convergence command or telemetry evidence was missing, one expired after spacecraft-state loss at COMMIT, and one produced an unsafe spacecraft-ahead state after restart at CONFIRM. Single message drops and contact closures during the recovery exchange were absorbed within the retry budget, whereas additional retransmissions could not repair destroyed endpoint protocol state. In the fixed challenge set, increasing the maximum transmission budget from two to three increased verification-complete executions from 5/12 to 11/12; a fourth transmission and candidate lifetimes from two through four contacts produced no additional observed benefit. The mixed-schedule population produced 74 successful terminations, but only 77 of 191 scheduled fault actions were reached at runtime, so those counts are descriptive rather than reliability estimates. The results support separating candidate state, activation, verification evidence, and persistent recovery state when designing post-compromise TT&C recovery.'''

KEYWORDS = [
    "satellite cybersecurity",
    "telemetry, tracking, and command (TT&C)",
    "post-compromise recovery",
    "key management",
    "resynchronization",
    "fault injection",
    "Space Data Link Security (SDLS)",
    "formal methods",
]

SECTIONS = [
    "introduction.md",
    "background-related-work.md",
    "system-threat-model.md",
    "recovery-designs.md",
    "experimental-method.md",
    "results.md",
    "discussion.md",
    "threats-to-validity.md",
    "reproducibility.md",
    "conclusion.md",
]


def load(path: Path) -> str:
    return path.read_text(encoding="utf-8").strip() + "\n"


def remove_tail_subsection(text: str, heading: str) -> str:
    marker = f"## {heading}"
    index = text.find(marker)
    if index == -1:
        raise SystemExit(f"Missing expected subsection: {marker}")
    return text[:index].rstrip() + "\n"


def demote_headings(text: str) -> str:
    lines = []
    for line in text.splitlines():
        if line.startswith("#"):
            line = "#" + line
        lines.append(line)
    return "\n".join(lines).strip() + "\n"


def markdown_escape(value: object) -> str:
    return str(value).replace("|", r"\|").replace("\n", " ")


def evidence_text(raw: str) -> str:
    data = json.loads(raw)
    parts = []
    for key in sorted(data):
        value = data[key]
        if isinstance(value, bool):
            value = str(value).lower()
        parts.append(f"{key}={value}")
    return "; ".join(parts)


def build_table1():
    path = TABLE_DIR / "table-1-matched-family-outcomes.csv"
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    headers = [
        "Family", "Treatment / policy", "Source", "Outcome",
        "Alignment", "Availability", "Authorized evidence",
    ]
    lines = [
        "**Table 1. Matched-family outcomes using only family-authorized comparison fields.**",
        "",
        "| " + " | ".join(headers) + " |",
        "|" + "|".join(["---"] * len(headers)) + "|",
    ]
    for row in rows:
        values = [
            row["family_id"],
            row["treatment_or_policy_variant"],
            row["source_id"],
            row["outcome"],
            row["alignment_class"],
            row["availability_state"],
            evidence_text(row["family_specific_authorized_evidence"]),
        ]
        lines.append("| " + " | ".join(markdown_escape(v) for v in values) + " |")
    lines.append(
        "\n*CF-02 contains two B1 policy traces for traceability; they constitute one B1 "
        "analysis unit rather than two independent replications.*"
    )
    return "\n".join(lines) + "\n", rows


def build_table2():
    path = TABLE_DIR / "table-2-deterministic-t1.csv"
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    headers = [
        "Schedule", "Class", "Fault", "Phase", "Outcome",
        "Alignment", "Security", "Availability", "Verified", "Reject evidence",
    ]
    lines = [
        "**Table 2. Full deterministic T1 fault-coverage matrix.**",
        "",
        "| " + " | ".join(headers) + " |",
        "|" + "|".join(["---"] * len(headers)) + "|",
    ]
    for row in rows:
        evidence = json.loads(row["rejection_evidence"])
        reject = (
            f"{evidence.get('rejection_count', 0)}/"
            f"{evidence.get('replay_rejection_count', 0)}/"
            f"{evidence.get('stale_state_rejection_count', 0)}"
        )
        values = [
            row["schedule_id"],
            row["schedule_class"],
            row["fault_kind_or_control"],
            row["phase_or_control"].replace("RECOVERY_", ""),
            row["outcome"],
            row["alignment"],
            row["security_state"],
            row["availability_state"],
            row["verification_complete"],
            reject,
        ]
        lines.append("| " + " | ".join(markdown_escape(v) for v in values) + " |")
    lines.append(
        "\n*Reject evidence is reported as "
        "`rejection_count/replay_rejection_count/stale_state_rejection_count`. "
        "The raw enum `SECURE_DEGRADED` is a retained reproducibility label; the separate "
        "`security_state` field is authoritative for security interpretation.*"
    )
    return "\n".join(lines) + "\n", rows


def insert_before(text: str, marker: str, inserted: str) -> str:
    if text.count(marker) != 1:
        raise SystemExit(f"Expected one insertion marker {marker!r}; found {text.count(marker)}")
    return text.replace(marker, inserted.rstrip() + "\n\n" + marker, 1)


def verify_lineage(table1_rows, table2_rows) -> None:
    if len(table1_rows) != 13:
        raise SystemExit(f"Table 1 expected 13 rows; found {len(table1_rows)}")
    if sorted({row["family_id"] for row in table1_rows}) != ["CF-01", "CF-02", "CF-05", "CF-06"]:
        raise SystemExit("Unexpected Table 1 family population")

    classes = Counter(row["schedule_class"] for row in table2_rows)
    if classes != Counter({"CANONICAL_CELL": 31, "RETRY_EXHAUSTION": 8, "CONTROL": 1}):
        raise SystemExit(f"Unexpected Study B schedule classes: {classes}")

    canonical = [row for row in table2_rows if row["schedule_class"] == "CANONICAL_CELL"]
    canonical_outcomes = Counter(row["outcome"] for row in canonical)
    expected_canonical = Counter(
        {"SUCCESS": 25, "INDETERMINATE": 4, "EXPIRED": 1, "SECURE_DEGRADED": 1}
    )
    if canonical_outcomes != expected_canonical:
        raise SystemExit(f"Unexpected canonical outcomes: {canonical_outcomes}")

    exhaustion = [row for row in table2_rows if row["schedule_class"] == "RETRY_EXHAUSTION"]
    if Counter(row["outcome"] for row in exhaustion) != Counter(
        {"EXPIRED": 6, "SECURE_DEGRADED": 2}
    ):
        raise SystemExit("Unexpected retry-exhaustion outcome counts")

    with (FIGURE_DIR / "figure-2-outcome-distribution-source.csv").open(
        newline="", encoding="utf-8"
    ) as handle:
        study_c = list(csv.DictReader(handle))
    c_counts = {row["outcome"]: int(row["count"]) for row in study_c}
    if c_counts != {
        "EXPIRED": 5,
        "INDETERMINATE": 15,
        "SECURE_DEGRADED": 6,
        "SUCCESS": 74,
    }:
        raise SystemExit(f"Unexpected Study C counts: {c_counts}")

    with (TABLE_DIR / "study-c-execution-coverage-audit.csv").open(
        newline="", encoding="utf-8"
    ) as handle:
        audit = list(csv.DictReader(handle))
    scheduled = sum(int(row["scheduled_action_count"]) for row in audit)
    applied = sum(int(row["applied_action_count"]) for row in audit)
    exercised = sum(row["runtime_exercised"] == "True" for row in audit)
    if (scheduled, applied, exercised) != (191, 77, 24):
        raise SystemExit(
            f"Unexpected Study C reachability totals: {scheduled}/{applied}/{exercised}"
        )

    with (FIGURE_DIR / "figure-3-sensitivity-source.csv").open(
        newline="", encoding="utf-8"
    ) as handle:
        study_d = list(csv.DictReader(handle))
    values = {
        (int(row["max_transmissions"]), int(row["candidate_lifetime_contacts"])):
        int(row["verification_complete_count"])
        for row in study_d
    }
    expected_values = {
        (2, 2): 5, (2, 3): 5, (2, 4): 5,
        (3, 2): 11, (3, 3): 11, (3, 4): 11,
        (4, 2): 11, (4, 3): 11, (4, 4): 11,
    }
    if values != expected_values:
        raise SystemExit(f"Unexpected Study D grid: {values}")


def exact_duplicate_paragraphs(text: str):
    paragraphs = []
    for block in re.split(r"\n\s*\n", text):
        block = block.strip()
        if not block or block.startswith("#") or block.startswith("|") or block.startswith("```"):
            continue
        normalized = re.sub(r"\s+", " ", block)
        if len(normalized) >= 100:
            paragraphs.append(normalized)
    counts = Counter(paragraphs)
    return [paragraph for paragraph, count in counts.items() if count > 1]


def main() -> None:
    section_text = {name: load(MANUSCRIPT_DIR / name) for name in SECTIONS}

    section_text["discussion.md"] = remove_tail_subsection(
        section_text["discussion.md"],
        "7.10 What the paper can and cannot conclude",
    )
    section_text["threats-to-validity.md"] = remove_tail_subsection(
        section_text["threats-to-validity.md"],
        "8.10 Summary of claim boundaries",
    )

    table1, table1_rows = build_table1()
    table2, table2_rows = build_table2()
    verify_lineage(table1_rows, table2_rows)

    figure1 = (
        "![Figure 1. Bounded post-compromise TT&C resynchronization architecture.]"
        "(../figures/rendered/figure-1-architecture.svg)\n\n"
        "*Figure 1. Recovery authority, ground/space endpoint state, fault-controlled "
        "intermittent link, and append-only evidence boundary used by the T1 experiment.*\n"
    )
    figure2 = (
        "![Figure 2. Terminal outcomes in the fixed 100-schedule population.]"
        "(../figures/rendered/figure-2-outcome-distribution.svg)\n\n"
        "*Figure 2. Descriptive terminal-outcome counts for the fixed Study C population. "
        "The population is not a real-world fault-prevalence or reliability sample.*\n"
    )
    figure3 = (
        "![Figure 3. Verification-complete executions across the Study D parameter grid.]"
        "(../figures/rendered/figure-3-retry-retention-sensitivity.svg)\n\n"
        "*Figure 3. Verification-complete executions per fixed 12-schedule challenge set. "
        "Candidate lifetime produced no observed change over the tested range.*\n"
    )

    section_text["recovery-designs.md"] = insert_before(
        section_text["recovery-designs.md"], "## 4.5 Treatment boundaries", figure1
    )
    section_text["results.md"] = insert_before(
        section_text["results.md"], "## 6.2 Deterministic T1 fault behavior", table1
    )
    section_text["results.md"] = insert_before(
        section_text["results.md"], "## 6.3 Fixed mixed-schedule characterization", table2
    )
    section_text["results.md"] = insert_before(
        section_text["results.md"], "## 6.4 Retry and candidate-retention sensitivity", figure2
    )
    section_text["results.md"] = insert_before(
        section_text["results.md"], "## 6.5 Supporting bounded formal/Python agreement", figure3
    )

    front = (
        f"# {TITLE}\n\n"
        "## Abstract\n\n"
        f"{ABSTRACT}\n\n"
        "**Keywords:** " + "; ".join(KEYWORDS) + "\n\n"
        "---\n\n"
    )
    body = "\n\n".join(
        demote_headings(section_text[name]).strip()
        for name in SECTIONS
    )
    manuscript = front + body + "\n"

    duplicates = exact_duplicate_paragraphs(manuscript)
    if duplicates:
        raise SystemExit(
            f"Exact duplicate long body paragraphs remain after integration: {len(duplicates)}"
        )

    abstract_words = len(ABSTRACT.split())
    if not 200 <= abstract_words <= 300:
        raise SystemExit(f"Abstract word count outside 200-300: {abstract_words}")

    lower = manuscript.lower()
    prohibited = [
        "74% success rate under faults",
        "we are the first",
        "this is the first",
        "the first study",
        "the first work",
        "proves post-compromise security",
        "ccsds-compliant",
        "ccsds compliant",
    ]
    for phrase in prohibited:
        if phrase in lower:
            raise SystemExit(f"Prohibited claim wording in integrated manuscript: {phrase}")

    dissertation_terms = [
        "this dissertation",
        "dissertation chapter",
        "doctoral study",
        "research participants",
        "interview participants",
    ]
    for phrase in dissertation_terms:
        if phrase in lower:
            raise SystemExit(f"Dissertation-style manuscript wording found: {phrase}")

    bibliography = load(ROOT / "references" / "bibliography.bib")
    cite_keys = set(re.findall(r"@\w+\{([^,]+),", bibliography))
    used = set(re.findall(r"@([A-Za-z0-9_:-]+)", manuscript))
    missing = sorted(key for key in used if key not in cite_keys)
    if missing:
        raise SystemExit("Unresolved manuscript citation keys: " + ", ".join(missing))

    output = MANUSCRIPT_DIR / "manuscript.md"
    output.write_text(manuscript, encoding="utf-8")

    print(f"title={TITLE}")
    print(f"abstract_words={abstract_words}")
    print(f"keywords={len(KEYWORDS)}")
    print(f"sections={len(SECTIONS)}")
    print(f"citation_keys_used={len(used)}")
    print("table_1_lineage=PASS")
    print("table_2_lineage=PASS")
    print("study_c_numerical_lineage=PASS")
    print("study_d_numerical_lineage=PASS")
    print("exact_duplicate_long_paragraphs=0")
    print("dissertation_style_scan=PASS")
    print("integrated_manuscript_written=PASS")


if __name__ == "__main__":
    main()
