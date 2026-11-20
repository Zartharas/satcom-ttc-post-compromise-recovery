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

# IEEE TAES template: no abbreviations in the title unless unavoidable. Revised 2026-11-19 on the author's instruction to follow the TAES guidelines.
TITLE_TWO_PART = "Post-Compromise Resynchronization of Satellite Telemetry, Tracking, and Command Under Intermittent Links: Fault-Injection and Parametric Studies"

SECTION_7_10 = (
    "### 7.10 Part II and the Part I mechanisms\n\n"
    "Part II examines two of the mechanisms discussed above in a parametric abstraction. The Part I result that "
    "retransmission cannot repair destroyed endpoint state has a counterpart in the persistence levels of Part II: "
    "under volatile or commit-level persistence, restarts can leave the endpoints divergent, whereas journaled "
    "progress made divergence invariant to the restart probability. The Part I distinction between convergence and "
    "verified recovery appears in Part II as the `INDETERMINATE` outcome, which plain retries could not clear; "
    "resumable verification could, but only under an assumption that the remaining messages are idempotent, which "
    "neither Part I nor the cited standards establish. Part II also shows that more durable persistence can raise "
    "ground-ahead divergence under gated activation in the abstraction, so persistence is not a monotone improvement, and that this is a "
    "property of the model's rules rather than of a measured link. The two parts use different models, the T1 "
    "controller and a six-message exchange, and no quantitative result is transferred between them."
)

SECTION_8_10 = (
    "### 8.10 Part II validity\n\n"
    "Part II states its own limitations in Section II.5; the points below bear on how far Part II supports the rest "
    "of the paper. For construct validity, the six-message exchange is an abstraction that has not been independently "
    "reviewed, and its loss values are stress parameters rather than TT&C uplink measurements. For external validity, "
    "the anchors are proxies (satellite observation windows, a broadband ping dataset and published loss ranges), "
    "and the broadband statistics were inspected before the Gilbert-Elliott rule was written, so the anchors are not "
    "blind. For conclusion validity, the hypotheses were frozen in the repository and not in an external registry, "
    "the analysis script was added after the freeze under a disclosed amendment, and the reading of \"fallback "
    "required\" in H-E2c as total divergence is one operationalization of ambiguous wording. Reproduction was "
    "performed by the same author in a second environment. The falsified hypotheses describe the rules of the model "
    "and should not be transferred to Part I or to real links."
)

SECTION_9_7 = (
    "### 9.7 Part II artifacts\n\n"
    "The Part II code, tests, TLA+ specifications, frozen pre-registration, analysis-script amendment and "
    "confirmatory results are in the same repository at the tags `study-e-prereg-v1` and "
    "`study-e-analysis-script-v1`. Outcome probabilities are computed in exact rational arithmetic and are "
    "deterministic; the results-table digest dfed99fa...a47d was reproduced in a second environment, and the test "
    "suite has 99 tests. A public deposit of the summary data has been planned but has not been made, and a "
    "SatNOGS-derived summary would carry the CC BY-SA 4.0 licence of its source. The reproduction boundary of "
    "Section 9.6 applies: reproducing Part II establishes the arithmetic of the model, not link behavior or "
    "cryptographic security."
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
# IEEE-ready figure copies (paper/two_part/figures_ieee). Part I's SVGs stay locked and unused here.
# The in-figure descriptive notes of Part I Figures 2 and 3 move into the captions (IEEE: no caption text inside figures).
FIGURES_IEEE = {
    "../figures/rendered/figure-1-architecture.svg": ("../figures_ieee/fig1.pdf", ""),
    "../figures/rendered/figure-2-outcome-distribution.svg": (
        "../figures_ieee/fig2.pdf",
        " Descriptive fixed-population counts; not a real-world fault-prevalence or reliability estimate.",
    ),
    "../figures/rendered/figure-3-retry-retention-sensitivity.svg": (
        "../figures_ieee/fig3.pdf",
        " No observed lifetime effect over 2-4 contacts; change occurs between transmission budgets 2 and 3.",
    ),
}

# IEEE TAES template: three or four keywords or phrases, alphabetical, comma-separated.
# Part I's eight-term, semicolon-separated line is hash-locked, so it is replaced here, in the output only.
KEYWORDS_TWO_PART = "fault injection, key management, post-compromise recovery, satellite cybersecurity"

PENDING_DECISIONS = [
    "read-through and approval of the combined abstract text (paper/two_part/abstract_candidate_250w.md; you chose to keep the descriptive-counts caveat)",
    "read-through of the new 7.10, 8.10 and 9.7 text and of the chosen title",
    "approval of the four keywords (fault injection, key management, post-compromise recovery, satellite cybersecurity); Part I keeps its own eight-term line",
    "journal abstract length limit: the TAES page found did not state one; IEEE-wide guidance found says 150-250 words, so 250 fits",
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
    parser.add_argument("--title", default=TITLE_TWO_PART, help="Title of the two-part paper (default revised 2026-11-19 to follow the TAES no-abbreviation guidance)")
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

    # Keywords: replace Part I's line with the template-conformant list (output only).
    ki = para_index(paras, "**Keywords:**")
    paras[ki] = "**Keywords:** " + KEYWORDS_TWO_PART
    kw = [w.strip() for w in KEYWORDS_TWO_PART.split(",")]
    if not 3 <= len(kw) <= 4 or kw != sorted(kw, key=str.lower):
        raise SystemExit("Keywords must be 3-4 terms in alphabetical order")

    # Introduction: bridge paragraph, five contributions, scope sentence.
    i = para_index(paras, "The paper makes four contributions.")
    paras[i] = "The paper makes five contributions."
    paras.insert(i, INTRO_BRIDGE)
    j = para_index(paras, "1. **A conservative operational comparison framework.**")
    paras[j] = paras[j].rstrip() + "\n" + CONTRIBUTION_5
    k = para_index(paras, "The scope of the claims is deliberately narrow")
    paras[k] = paras[k].rstrip() + " " + SCOPE_ADDITION

    # Title (optional, author decision).
    if args.title:
        t0 = para_index(paras, "# ")
        paras[t0] = "# " + args.title.strip()

    # Discussion 7.10 and Threats 8.10, before the next top-level sections.
    d = para_index(paras, "## 8. Threats to Validity and Limitations")
    paras.insert(d, SECTION_7_10)
    v = para_index(paras, "## 9. Reproducibility and Artifact Availability")
    paras.insert(v, SECTION_8_10)

    # Reproducibility 9.7 and Part II, before the Conclusion (9.7 first, then Part II).
    part2 = (TWO / "part-ii-study-e.md").read_text(encoding="utf-8").strip()
    c = para_index(paras, "## 10. Conclusion")
    paras.insert(c, part2)
    paras.insert(c, SECTION_9_7)

    # Conclusion: Part II paragraph after the TLA+/Python paragraph; future-work sentence.
    t = para_index(paras, "Bounded TLA+/Python comparisons provide")
    paras.insert(t + 1, CONCLUSION_PART_II)
    f = para_index(paras, "Future work should instantiate")
    new, n = re.subn(FUTURE_WORK_OLD, FUTURE_WORK_NEW, paras[f])
    if n != 1:
        raise SystemExit(f"Future-work sentence anchor matched {n} times")
    paras[f] = new

    manuscript = "\n\n".join(paras) + "\n"

    # Figures: point at the IEEE-ready copies and add the moved notes to the captions.
    for old_path, (new_path, note) in FIGURES_IEEE.items():
        pat = re.compile(r"!\[([^\]]*)\]\(" + re.escape(old_path) + r"\)")
        hits = pat.findall(manuscript)
        if len(hits) != 1:
            raise SystemExit(f"Expected exactly one reference to {old_path}, found {len(hits)}")
        if not (TWO / "figures_ieee" / Path(new_path).name).is_file():
            raise SystemExit(f"Missing IEEE figure file: {new_path}")
        manuscript = pat.sub(lambda m: f"![{m.group(1).rstrip()}{note}]({new_path})", manuscript)

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
