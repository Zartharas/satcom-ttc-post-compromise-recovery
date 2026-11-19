#!/usr/bin/env python3
"""Build the two-part manuscript (Part I: Studies A-D, Part II: Study E) without editing any
checksum-locked Part I file.

Inputs (all read-only):
  paper/manuscript/manuscript.md           Part I, generated and locked by the repository manifest
  references/bibliography.bib              Part I bibliography, locked
  artifacts/manifests/repository-v0.1.1.sha256   used only to verify the two files above are unchanged
  paper/two_part/part-ii-study-e.md        Part II section
  paper/two_part/bibliography_study_e.bib  Part II bibliography entries
  paper/two_part/abstract_candidate_250w.md  combined abstract (author decision pending)

Outputs (written only under paper/two_part/out/):
  manuscript_two_part.md
  bibliography_two_part.bib

The framing edits below implement paper/two_part/FRAMING_TEXT_PROPOSAL_v1_2026-11-19.md. Keep the two in sync.
Every edit asserts that its anchor occurs exactly once, so a changed Part I text fails loudly instead of
being silently skipped.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TWO = ROOT / "paper" / "two_part"
MANIFEST = ROOT / "artifacts" / "manifests" / "repository-v0.1.1.sha256"
PART1_MANUSCRIPT = ROOT / "paper" / "manuscript" / "manuscript.md"
PART1_BIB = ROOT / "references" / "bibliography.bib"

INTRO_BRIDGE = (
    "Part I (Sections 3-9) studies the recovery-control exchange in a deterministic fault-injection model. "
    "Part II asks a complementary, parametric question: when message loss, spacecraft restarts and short "
    "contact windows disrupt the key-activation and verification exchange, how often does the exchange "
    "finish, diverge or stall, and how much do persistence, retry and resumability choices change that? "
    "CCSDS 355.1-B-1 specifies key activation and key verification as separate procedures, with no recovery "
    "procedure found in its text; CCSDS 354.0-M-1 places recovery procedures for master-key-protected "
    "procedures outside its scope; and SDLS-DR, a ratcheted extension, does not evaluate contact windows, "
    "handover, delay, Doppler or flight hardware "
    "[@ccsds_sdls_ep_355_1_b_1; @ccsds_key_mgmt_354_0_m_1; @ledin_sdls_dr_risc2026]."
)

CONTRIBUTION_5 = (
    "5. **A pre-specified parametric study of the activation exchange.** Hypotheses, grid and analysis rules "
    "were frozen before the confirmatory run, which was computed exactly and reproduced in a second "
    "environment. Some hypotheses were supported and others were falsified or only partly supported in the "
    "model; the falsifications are reported as model-rule effects, not link behavior."
)

SCOPE_ADDITION = (
    "Part II is a parametric model study: its loss values are stress parameters rather than measurements of a "
    "TT&C uplink, its six-message exchange has not been independently reviewed, and its recovery-association "
    "and resumption parameters are assumptions."
)

CONCLUSION_PART_II = (
    "Part II extended the question to the activation exchange itself. In an exact model of a six-message "
    "abstraction, plain retries could not remove the mass of indeterminate outcomes, while resumable "
    "verification could, provided the remaining messages are idempotent, which is an assumption and not a "
    "standard feature. Bursty loss changed outcomes relative to independent loss at the same average rate, in "
    "both directions. Several expected regularities did not hold: success was not monotone in loss or slot "
    "count when restarts occur and state is not journaled; durable persistence sometimes raised ground-ahead "
    "divergence; and volatile-state divergence did not always grow with restart probability. The recovery "
    "fraction reached the declared 0.95 level in 83-90% of multi-attempt configurations rather than almost "
    "always. These failures arise from the abstraction's rules, in which durable progress can carry more "
    "attempts into the window where ground has activated and the spacecraft has not, and they should not be "
    "read as behavior of a real link."
)

FUTURE_WORK_OLD = r"evaluate\s+protected\s+persistent-state\s+strategies\s+across\s+endpoint\s+restart,"
FUTURE_WORK_NEW = (
    "anchor the exchange model to measured TT&C link loss and contact data, obtain an independent review of "
    "the exchange abstraction,"
)

PROHIBITED = [
    "74% success rate under faults",
    "we are the first",
    "this is the first",
    "the first study",
    "the first work",
    "proves post-compromise security",
    "ccsds-compliant",
    "ccsds compliant",
]
DISSERTATION = [
    "this dissertation",
    "dissertation chapter",
    "doctoral study",
    "research participants",
    "interview participants",
]
PENDING_DECISIONS = [
    "combined abstract wording (paper/two_part/abstract_candidate_250w.md) and whether the descriptive-counts caveat stays",
    "statement that the six-message exchange has not been independently reviewed (scope sentence and conclusion)",
    "whether to keep the Part I locks (this builder assumes yes) and the abstract length rule for the journal",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_part1_unchanged() -> None:
    entries = {}
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        digest, _, name = line.partition("  ")
        entries[name] = digest
    for path in (PART1_MANUSCRIPT, PART1_BIB):
        rel = path.relative_to(ROOT).as_posix()
        if rel not in entries:
            raise SystemExit(f"{rel} is not in the manifest")
        if sha256(path) != entries[rel]:
            raise SystemExit(f"{rel} differs from the manifest; refusing to build on a changed Part I file")


def para_index(paras: list[str], startswith: str) -> int:
    hits = [i for i, p in enumerate(paras) if p.startswith(startswith)]
    if len(hits) != 1:
        raise SystemExit(f"Expected exactly one paragraph starting {startswith!r}, found {len(hits)}")
    return hits[0]


def exact_duplicate_paragraphs(text: str) -> list[str]:
    seen = []
    for block in re.split(r"\n\s*\n", text):
        block = block.strip()
        if not block or block.startswith(("#", "|", "```")):
            continue
        normalized = re.sub(r"\s+", " ", block)
        if len(normalized) >= 100:
            seen.append(normalized)
    return [p for p, c in Counter(seen).items() if c > 1]


def bib_keys(text: str) -> list[str]:
    return re.findall(r"@\w+\{([^,\s]+),", text)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--abstract", default=str(TWO / "abstract_candidate_250w.md"))
    args = parser.parse_args()

    verify_part1_unchanged()

    text = PART1_MANUSCRIPT.read_text(encoding="utf-8")
    paras = text.strip("\n").split("\n\n")

    # Abstract: replace the paragraph after the '## Abstract' heading.
    abstract = Path(args.abstract).read_text(encoding="utf-8").strip()
    abstract = re.sub(r"<!--.*?-->", "", abstract, flags=re.S)
    abstract = re.sub(r"^>\s*", "", abstract, flags=re.M)
    abstract = re.sub(r"\s+", " ", abstract)
    i = para_index(paras, "## Abstract")
    paras[i + 1] = abstract
    abstract_words = len(abstract.split())
    if not 200 <= abstract_words <= 300:
        raise SystemExit(f"Abstract word count outside 200-300: {abstract_words}")

    # Introduction: bridge paragraph, five contributions, scope sentence.
    i = para_index(paras, "The paper makes four contributions.")
    paras[i] = "The paper makes five contributions."
    paras.insert(i, INTRO_BRIDGE)
    j = para_index(paras, "1. **A conservative operational comparison framework.**")
    paras[j] = paras[j].rstrip() + "\n" + CONTRIBUTION_5
    k = para_index(paras, "The scope of the claims is deliberately narrow")
    paras[k] = paras[k].rstrip() + " " + SCOPE_ADDITION

    # Part II before the Conclusion.
    part2 = (TWO / "part-ii-study-e.md").read_text(encoding="utf-8").strip()
    c = para_index(paras, "## 10. Conclusion")
    paras.insert(c, part2)

    # Conclusion: Part II paragraph after the TLA+/Python paragraph; future-work sentence.
    t = para_index(paras, "Bounded TLA+/Python comparisons provide")
    paras.insert(t + 1, CONCLUSION_PART_II)
    f = para_index(paras, "Future work should instantiate")
    new, n = re.subn(FUTURE_WORK_OLD, FUTURE_WORK_NEW, paras[f])
    if n != 1:
        raise SystemExit(f"Future-work sentence anchor matched {n} times")
    paras[f] = new

    manuscript = "\n\n".join(paras) + "\n"

    # Checks mirroring the Part I builder.
    dups = exact_duplicate_paragraphs(manuscript)
    if dups:
        raise SystemExit(f"Exact duplicate long paragraphs: {len(dups)}")
    lower = manuscript.lower()
    for phrase in PROHIBITED:
        if phrase in lower:
            raise SystemExit(f"Prohibited claim wording: {phrase}")
    for phrase in DISSERTATION:
        if phrase in lower:
            raise SystemExit(f"Dissertation-style wording: {phrase}")
    if "citations to verify" in lower:
        raise SystemExit("Unresolved 'CITATIONS TO VERIFY' marker")

    # Bibliography: combine and check keys.
    b1, b2 = PART1_BIB.read_text(encoding="utf-8"), (TWO / "bibliography_study_e.bib").read_text(encoding="utf-8")
    k1, k2 = bib_keys(b1), bib_keys(b2)
    clash = sorted(set(k1) & set(k2))
    if clash:
        raise SystemExit("Bibliography key collision: " + ", ".join(clash))
    combined = b1.rstrip() + "\n\n" + b2.strip() + "\n"
    used = set(re.findall(r"@([A-Za-z0-9_:-]+)", manuscript))
    missing = sorted(u for u in used if u not in set(k1) | set(k2))
    if missing:
        raise SystemExit("Unresolved citation keys: " + ", ".join(missing))

    out = TWO / "out"
    out.mkdir(exist_ok=True)
    (out / "manuscript_two_part.md").write_text(manuscript, encoding="utf-8")
    (out / "bibliography_two_part.bib").write_text(combined, encoding="utf-8")

    print(f"part1_manuscript_sha256={sha256(PART1_MANUSCRIPT)} (matches manifest)")
    print(f"abstract_words={abstract_words}" + ("" if abstract_words == 250 else "  (Part I CI rule is exactly 250)"))
    print(f"citation_keys_used={len(used)}  new_bib_keys={len(k2)}")
    print("exact_duplicate_long_paragraphs=0")
    print("two_part_manuscript_written=PASS")
    print("AUTHOR DECISIONS STILL PENDING:")
    for d in PENDING_DECISIONS:
        print(f"  - {d}")


if __name__ == "__main__":
    sys.exit(main())
