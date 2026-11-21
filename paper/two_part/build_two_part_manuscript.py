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
With --compact (opt-in; the default output is unchanged) the 40-row deterministic fault-coverage matrix is moved
out of the main text into a supplement (TAES accepts supplementary material and charges $200 per printed page
beyond 10):
  manuscript_two_part_compact.md
  supplement_S1_deterministic_matrix.md
  supplement_README.md

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
    "contact windows disrupt key activation and verification, how often does the exchange finish, diverge or "
    "stall, and how much do persistence, retry and resumability choices change that? "
    "CCSDS 355.1-B-1 separates key activation from verification and has no recovery procedure in the text "
    "read; CCSDS 354.0-M-1 excludes session-key recovery procedures; and SDLS-DR does not evaluate "
    "contact windows, handover, delay, Doppler or flight hardware "
    "[@ccsds_sdls_ep_355_1_b_1; @ccsds_key_mgmt_354_0_m_1; @ledin_sdls_dr_risc2026]."
)

CONTRIBUTION_3_FINDINGS = (
    "3. **Fault-response findings.** In predeclared deterministic experiments on the controller alone, 25 of 31 "
    "single-fault cells succeeded, four ended indeterminate, and two ended unsafe, with a compromised key still "
    "active; so did all eight retry-exhaustion schedules. Bounded retransmission absorbed isolated delivery faults "
    "but not lost verification evidence or endpoint-state loss around activation. On twelve designed schedules, "
    "six with two consecutive same-phase faults, a third transmission raised verification-complete executions from "
    "5/12 to 11/12, which illustrates the mechanism and is not a rate estimate. A fixed 100-schedule mixed "
    "population is reported descriptively, without reliability or prevalence claims."
)

CONTRIBUTION_4 = (
    "4. **A pre-specified parametric study of the activation exchange.** Hypotheses, grid and policy set "
    "were frozen before the confirmatory run, which was computed exactly and reproduced in a second "
    "environment. Some hypotheses were supported and others were falsified or only partly supported in the "
    "model; the falsifications are reported as model-rule effects, not link behavior."
)

SCOPE_EVIDENCE = (
    "Baselines B0-B2 appear in Study A's matched families, two of which inject no fault and two of which "
    "contain only B2 and T1, so Studies B-D document the mechanisms of T1 alone and show no advantage over any "
    "baseline. A later descriptive run, Study F (Supplementary Table S7), put B0-B2 through step-level faults: with "
    "up to three transmissions every cell with one or two losses succeeded, so retransmission alone absorbs isolated loss. That lost verification evidence yields `INDETERMINATE` and that a restart destroys volatile pending "
    "state are rules of the model, and the Study D threshold follows from fault multiplicity in a designed set "
    "(Table S2). Ten of the 40 deterministic schedules end unsafe (Tables S4 and S5)."
)

PARITY_OLD = re.compile(r"In the four\s+defensibly matched families, the treatments produced the same authorized categorical terminal\s+classifications\.")
PARITY_NEW = ("In the four matched families, the treatments present produced the same authorized categorical "
              "classifications, but two families inject no fault and the other two contain only B2 and T1, so these "
              "cases check consistency and cannot discriminate between treatments.")

SCOPE_ADDITION = (
    "Part II is a parametric model study: its loss values are stress parameters rather than measurements of a "
    "TT&C uplink, and its exchange has not been independently reviewed."
)

CONCLUSION_PART_II = (
    "Part II extended the question to the activation exchange. In an exact model, resumable verification (an "
    "assumption outside the standards) cleared indeterminate outcomes that plain retries could not, and recovery "
    "reached the declared 0.95 level in 83-90% of multi-attempt configurations with divergence, not almost always, "
    "in the model, not on a real link."
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
    "Part II examines two Part I mechanisms parametrically. Retransmission could not repair destroyed endpoint "
    "state in Part I; in Part II, volatile or commit-level persistence leaves endpoints divergent after restarts, "
    "whereas journaled progress made divergence invariant to restart probability. Convergence without verified "
    "recovery appears as `INDETERMINATE`, which plain retries could not clear and resumable verification could, "
    "if the remaining messages are idempotent, which neither Part I nor the standards establish. The two parts use "
    "different models, and no quantitative result is transferred between them. Part I has no Recovery SA fallback; "
    "Part II models one (H-E4)."
)

SECTION_8_10 = (
    "### 8.10 Part II validity\n\n"
    "For construct and external validity, the six-message "
    "exchange is an unreviewed abstraction whose loss values are stress parameters anchored to proxies. For "
    "conclusion validity, the hypotheses were frozen in the repository and not an external registry, the analysis "
    "script was added after the freeze under a disclosed amendment, and reading \"fallback required\" in H-E2c as "
    "total divergence is one operationalization of ambiguous wording. Reproduction was same-author. The "
    "falsified hypotheses describe the model's rules and should not be transferred to Part I or to real links."
)

SECTION_9_7 = (
    "### 9.7 Part II artifacts\n\n"
    "The Part II code, tests, TLA+ specifications, frozen pre-registration, analysis-script amendment and "
    "confirmatory results are in the project repository [@study_e_repository]. The frozen versions are identified "
    "by two permanent labels in that repository (tags `study-e-prereg-v1` and `study-e-analysis-script-v1`), and "
    "the results table carries a SHA-256 checksum for checking a reproduction. "
    "The arithmetic is deterministic; the checksum was reproduced in a second environment by the same author, "
    "and the test suite has 99 tests. A public deposit of the summary data is planned but not made; a "
    "SatNOGS-derived summary would carry the CC BY-SA 4.0 licence of its source. Reproducing Part II establishes "
    "the arithmetic of the model, not link behavior or cryptographic security."
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

TABLE2_CAPTION = "**Table 2. Full deterministic T1 fault-coverage matrix; exact source fields are retained in Supplementary Table S1.**"
TABLE3_CAPTION = "**Table 3. Study E hypotheses and outcomes over the full grid (exact arithmetic).**"
COMPACT_POINTER = (
    "The complete 40-row deterministic fault-coverage matrix (schedule, class, fault, phase, outcome, alignment, "
    "security, availability, verification and reject evidence for every schedule) is provided as Supplementary "
    "Table S1 in the supplementary material."
)

CONCLUSION_TRIM_START = "The deterministic T1 study provided the clearest mechanism-level evidence."
CONCLUSION_TRIM_END = "Bounded TLA+/Python comparisons provide"
CONCLUSION_TRIM_NEW = (
    "The deterministic T1 study provided the clearest mechanism-level evidence. Isolated loss and contact closure "
    "were absorbed within the retry budget, and delayed, duplicated, reordered, stale-counter and stale-replay cases "
    "completed while invalid material was rejected. Lost post-convergence evidence left the controller synchronized "
    "but `INDETERMINATE` rather than successful. Endpoint restart around COMMIT or CONFIRM destroyed or separated "
    "pending or activated state and produced unsafe asymmetric outcomes. Raising the transmission budget from two to "
    "three repaired the repeated omission and contact challenges in that fixed set, a fourth opportunity added no observed benefit, and "
    "none of them repaired the COMMIT-stage restart failure. Retransmission can recover missing messages; it cannot "
    "reconstruct protocol state that no longer exists. The fixed 100-schedule population is descriptive only: many "
    "later-attempt faults were never reached at runtime, so its 74 successful schedules are not a fault-conditioned "
    "success rate."
)

INTRO_INVENTORY_SENTENCE = (
    "The retained study contains four matched comparison families, 40 deterministic T1 schedules, a fixed "
    "100-schedule mixed-fault population, a 3 x 3 sensitivity grid producing 108 executions, and bounded "
    "TLA+/Python cross-validation evidence."
)

PENDING_DECISIONS = [
    "approved by the author 2026-11-21: abstract v7, Sections 7.10, 8.10 and 9.7, Supplementary Table S7 and the Study F scope sentence",
    "approval of the chosen title and of the four keywords (fault injection, key management, post-compromise recovery, satellite cybersecurity); Part I keeps its own eight-term line",
    "approval of the figures after the 0.9-width change (checked for legibility on pages 7 and 11 only)",
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



def build_supplement_s2() -> str:
    """Supplementary Tables S2-S6, generated read-only from the frozen CSV/JSON inputs plus fixed glossary text."""
    import collections
    import csv
    import json
    cfg = json.loads((ROOT / "experiments" / "configs" / "paper-final-experiment.json").read_text(encoding="utf-8"))
    sched = cfg["studies"]["study_d_sensitivity_t1"]["schedules"]
    lines = ["# Supplementary Tables S2-S7 (S2-S6 derived read-only from frozen Part I inputs; S7 from the Study F run)", ""]
    lines += ["**Supplementary Table S2. Study D challenge set: fault structure of the 12 designed schedules.**", "",
              "| Schedule | Faults | Same-phase consecutive faults | Transmissions needed for that phase |", "|---|---|---|---|"]
    rows = []
    for s in sched:
        acts = s["actions"]
        label = "none" if not acts else "; ".join(f"{a['kind']} {a['phase'].replace('RECOVERY_', '')} (attempt {a['attempt']}, {a['contacts']} contact(s))" for a in acts)
        kinds = {a["kind"] for a in acts}
        n = len(acts)
        if not acts:
            need = "1"
        elif kinds <= {"DROP", "CONTACT_CLOSE"}:
            need = str(n + 1)
        elif kinds == {"ENDPOINT_RESTART"}:
            need = "no budget in the grid repairs it"
        else:
            need = "not set by the budget (delay or replay)"
        rows.append((n if kinds <= {"DROP", "CONTACT_CLOSE"} else 0, need))
        lines.append(f"| {s['id']} | {label} | {n if kinds <= {'DROP', 'CONTACT_CLOSE'} else '-'} | {need} |")
    two = sum(1 for n, _ in rows if n == 2)
    lines += ["", f"{two} of {len(sched)} schedules carry two consecutive drops or contact closures in one phase and therefore need three transmissions; one is an endpoint restart that no budget in the grid repaired; the other {len(sched) - two - 1} carry at most one drop, a delay or a stale replay, or no fault. "
              "The counts in the sensitivity summary (5 verification-complete at a budget of two; 11 at three and four) match the five schedules with no repeated drop or closure and no restart, and those five plus the six repeated-fault schedules, "
              "and the three candidate lifetimes gave identical counts. Per-schedule outcomes are not tabulated here because they are not in the tracked tables.", ""]
    cov = list(csv.DictReader((ROOT / "paper" / "tables" / "study-c-execution-coverage-audit.csv").open(encoding="utf-8")))
    un = [x for x in cov if x["runtime_exercised"] != "True"]
    lines += [f"**Supplementary Table S3. Study C: the {len(un)} of {len(cov)} fault cells never exercised at runtime.**", "",
              "| Fault | Phase | Scheduled | Applied |", "|---|---|---|---|"]
    for x in un:
        lines.append(f"| {x['fault_kind']} | {x['phase'].replace('RECOVERY_', '')} | {x['scheduled_action_count']} | {x['applied_action_count']} |")
    lines += ["", f"Across all {len(cov)} cells, {sum(int(x['scheduled_action_count']) for x in cov)} fault actions were scheduled and {sum(int(x['applied_action_count']) for x in cov)} were applied.", ""]
    t2 = list(csv.DictReader((ROOT / "paper" / "tables" / "table-2-deterministic-t1.csv").open(encoding="utf-8")))
    ct = collections.Counter((x["schedule_class"], x["outcome"], x["security_state"]) for x in t2)
    lines += ["**Supplementary Table S4. Outcome by security state in the 40 deterministic schedules.**", "",
              "| Schedule class | Raw outcome | Security state | Schedules |", "|---|---|---|---|"]
    for (k1, k2, k3), v in sorted(ct.items()):
        lines.append(f"| {k1} | {k2} | {k3} | {v} |")
    unsafe = sum(v for (k1, k2, k3), v in ct.items() if k3 == "UNSAFE")
    lines += ["", f"{unsafe} of {len(t2)} schedules end `UNSAFE`.", ""]
    lines += ["**Supplementary Table S5. Terms.**", "", "| Term | Meaning in this paper |", "|---|---|",
        "| `G_AHEAD`, `S_AHEAD` (Part I) | Ground (spacecraft) epoch counter exceeds the other endpoint's at the end of the run. The base scenario starts with the ground at epoch 2 and the spacecraft at epoch 1, with active keys marked compromised, so `G_AHEAD` after expiry is the starting divergence left unresolved; `S_AHEAD` arises when the spacecraft activates the new epoch and ground never confirms. |",
        "| `UNSAFE` (security state) | At the end, a compromised key is still marked active at the ground or the spacecraft, or the recovery authority is marked compromised. It means recovery did not complete, not that an attack occurred during the run. |",
        "| `SECURE_DEGRADED` (raw outcome) | Historical enum name kept for reproducibility; its security state is `UNSAFE` in all three deterministic schedules in which it occurs, so it is not a secure state. |",
        "| `SUCCESS` | Endpoints converged and verification evidence (test command and authenticated status) completed. |",
        "| `INDETERMINATE` | Endpoints converged but verification evidence is missing. |",
        "| `DIVERGED_G_AHEAD`, `DIVERGED_S_AHEAD` (Part II) | Ground has activated the new epoch and the spacecraft has not, or the reverse. |",
        "| gated activation (Part II) | The spacecraft activates only on authenticated status; local activation activates on COMMIT. |",
        "| $B$ | Transmission budget per phase. Part I uses 2-4; Part II grid uses 4-12; it is unrelated to baseline B0-B2. |", ""]
    kinds = ", ".join(cfg["base_t1_parameters"]["allowed_faults"])
    lines += ["**Supplementary Table S6. Fault kinds exercised and not exercised.**", "",
              f"Fault kinds the plan allows: {kinds}. Faults are single, scheduled and non-adaptive. Not exercised: adaptive fault timing; injected messages other than stale-counter and stale-replay cases; wall-clock timing, clock drift or link budgets (contacts are abstract slots); and any baseline under Studies B-D (baselines are covered only by Study F, Table S7).", ""]
    lines += build_supplement_s7()
    return "\n".join(lines)


def build_supplement_s7() -> list:
    """Supplementary Table S7 from the Study F results CSV (read-only). Asserts the counts quoted in the text."""
    import collections
    import csv
    path = ROOT / "study_f_out" / "mac" / "study_f_results.csv"
    if not path.exists():
        return []
    rows = list(csv.DictReader(path.open(encoding="utf-8")))
    outcomes = ["SUCCESS", "EXPIRED", "DIVERGED", "LOCKED", "INDETERMINATE"]
    names = {"B0": "B0 OTAR", "B1_LOCAL": "B1 local activation", "B1_DEFERRED": "B1 deferred activation", "B2": "B2 strict URKE"}
    out = ["**Supplementary Table S7. Study F: baselines under step-level faults (descriptive; a later run, plan tag `study-f-plan-v1`, not part of the frozen Part I).**", "",
           "Cells exist only where the frozen baseline abstraction defines the fault; other fault kinds and steps are recorded as not defined. Budget 1 transmits each message once, as specified; budget 3 allows up to three transmissions of a lost message, an assumption favorable to the baselines (COP-1 retransmits telecommand frames). Start state: ground epoch 2, spacecraft epoch 1, current keys attacker-known. Unsafe means a compromised key is still active.", "",
           "| Baseline | Budget | Cells | " + " | ".join(o.title() for o in outcomes) + " | Unsafe |", "|---|---|---|" + "---|" * (len(outcomes) + 1)]
    for flow in names:
        for b in ("1", "3"):
            sel = [r for r in rows if r["flow"] == flow and r["budget"] == b]
            c = collections.Counter(r["outcome"] for r in sel)
            out.append(f"| {names[flow]} | {b} | {len(sel)} | " + " | ".join(str(c.get(o, 0)) for o in outcomes)
                       + f" | {sum(r['security_state'] == 'UNSAFE' for r in sel)} |")
    nd_path = ROOT / "study_f_out" / "mac" / "study_f_not_defined.csv"
    nd_count = len(list(csv.DictReader(nd_path.open(encoding="utf-8")))) if nd_path.exists() else 0
    assert nd_count == 44, "not-defined count changed"
    loss = ("DROP", "CONTACT_CLOSE")
    b1 = [r for r in rows if r["budget"] == "1"]
    b3 = [r for r in rows if r["budget"] == "3"]
    single = [r for r in b1 if r["kind"] in loss and r["lost_transmissions"] == "1"]
    absorbed = [r for r in b3 if r["kind"] in loss and r["lost_transmissions"] in ("1", "2")]
    fails3 = [r for r in b3 if r["outcome"] != "SUCCESS"]
    exhaustion = [r for r in fails3 if r["kind"] in loss]
    assert single and all(r["outcome"] != "SUCCESS" for r in single), "single-loss claim no longer holds"
    assert absorbed and all(r["outcome"] == "SUCCESS" for r in absorbed), "absorbed-loss claim no longer holds"
    assert all(r["lost_transmissions"] == "3" for r in exhaustion)
    other = collections.Counter(r["kind"] for r in fails3 if r["kind"] not in loss)
    out += ["", f"At budget 1, all {len(single)} single-loss cells ended without success. At budget 3, all {len(absorbed)} cells with one or two consecutive losses succeeded; the {len(fails3)} non-successes were {len(exhaustion)} cells with three consecutive losses, "
            + ", ".join(f"{n} {k.lower().replace('_', ' ')}" for k, n in sorted(other.items())) + ". "
            f"Cells per budget: " + ", ".join(f"{names[f]} {sum(1 for r in b1 if r['flow'] == f)}" for f in names) + f"; the controller has 31 canonical cells. {nd_count} flow-step-kind combinations are not defined for the baseline abstractions and are not run (study_f_not_defined.csv). "
            "Budget 3 also lets B2 re-request a lost status, whereas the controller treats lost verification evidence as indeterminate by rule, so those cells are not like for like. Baseline cells map to the controller's fault kinds by family, not one to one, and the same author wrote the engine and the model.", ""]
    return out


def remove_em_dashes(text):
    """Output-only: replace every em dash (the template does not require any) with plain punctuation."""
    text = re.sub(r"(?m)^(#{2,4} [^\n]*?) \u2014 ", r"\1: ", text)
    text = re.sub(r"\*\*(RQ\d) \u2014 ", r"**\1: ", text)
    for old, new in (
        ("baseline abstractions\u2014an SDLS", "baseline abstractions (an SDLS"),
        ("(B2)\u2014and compare", "(B2)) and compare"),
        ("and\u2014after response\u2014the candidate", "and, after response, the candidate"),
    ):
        if text.count(old) != 1:
            raise SystemExit("em-dash anchor not found exactly once: " + old)
        text = text.replace(old, new)
    if "\u2014" in text:
        raise SystemExit("unhandled em dash remains in the manuscript output")
    return text


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--abstract", default=str(TWO / "abstract_candidate_250w.md"))
    parser.add_argument("--acknowledgment", default=str(TWO / "acknowledgment_candidate.md"),
                        help="AI-use Acknowledgment; inserted only when it has no [AUTHOR ...] tag left")
    parser.add_argument("--title", default=TITLE_TWO_PART, help="Title of the two-part paper (default revised 2026-11-19 to follow the TAES no-abbreviation guidance)")
    parser.add_argument("--compact", action="store_true",
                        help="Move the 40-row deterministic matrix (Part I Table 2) to a supplement; writes *_compact outputs only")
    parser.add_argument("--trim", action="store_true",
                        help="Opt-in, only with --compact: condense the three results-recap paragraphs of the Conclusion and drop the Introduction's study-inventory sentence (about 100 words together; every number stays in the abstract and Sections 5-6); writes *_compact_trim outputs")
    args = parser.parse_args()
    if args.trim and not args.compact:
        raise SystemExit("--trim requires --compact")

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

    # Introduction: bridge paragraph, four contributions (items 3-4 of Part I merged into findings; Part II added), scope sentence.
    i = para_index(paras, "The paper makes four contributions.")
    paras.insert(i, INTRO_BRIDGE)
    j = para_index(paras, "1. **A conservative operational comparison framework.**")
    cut = paras[j].index("\n3. **Predeclared fault and sensitivity experiments.**")
    paras[j] = paras[j][:cut].rstrip() + "\n" + CONTRIBUTION_3_FINDINGS + "\n" + CONTRIBUTION_4
    k = para_index(paras, "The scope of the claims is deliberately narrow")
    paras[k] = paras[k].rstrip() + " " + SCOPE_EVIDENCE + " " + SCOPE_ADDITION
    pk = para_index(paras, "The results do not support a universal superiority claim")
    paras[pk], npar = PARITY_OLD.subn(PARITY_NEW, paras[pk])
    if npar != 1:
        raise SystemExit("Parity sentence anchor not found exactly once")

    # Title (optional, author decision).
    if args.title:
        t0 = para_index(paras, "# ")
        paras[t0] = "# " + args.title.strip()

    # Essential-roadmap wording fixes (output only; Part I file untouched).
    i76 = para_index(paras, "The distinctive T1 contribution appears instead")
    paras[i76] = (
        "Studies B and D instead document T1's mechanisms alone and show no advantage over any baseline: Study F "
        "(Supplementary Table S7) found that, with retransmission, a baseline absorbs a lost status message that T1 "
        "leaves indeterminate by rule."
    )
    pat79 = re.compile(r"an\s+independently\s+encoded\s+control-state\s+view")
    h79 = [i for i, x in enumerate(paras) if pat79.search(x)]
    if len(h79) != 1:
        raise SystemExit("Section 7.9 anchor not found exactly once")
    paras[h79[0]] = pat79.sub("a second encoding of the control-state view", paras[h79[0]], count=1)

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

    # Optional Conclusion trim (output only; every number and the not-a-success-rate caveat are kept and asserted).
    if args.trim:
        a = para_index(paras, CONCLUSION_TRIM_START)
        b = para_index(paras, CONCLUSION_TRIM_END)
        if b - a != 3:
            raise SystemExit(f"Conclusion trim expects exactly 3 paragraphs to replace, found {b - a}")
        for token in ("two to three", "a fourth opportunity", "COMMIT-stage restart failure", "74 successful schedules", "not a fault-conditioned success rate"):
            if token not in CONCLUSION_TRIM_NEW:
                raise SystemExit("Conclusion trim lost required content: " + token)
        paras[a:b] = [CONCLUSION_TRIM_NEW]
        pat = re.compile(r"\s+" + r"\s+".join(re.escape(w) for w in INTRO_INVENTORY_SENTENCE.split()))
        hits = [i for i, x in enumerate(paras) if pat.search(x)]
        if len(hits) != 1 or len(pat.findall(paras[hits[0]])) != 1:
            raise SystemExit("Introduction inventory sentence not found exactly once")
        paras[hits[0]] = pat.sub("", paras[hits[0]], count=1)

    # Optional compact mode: move Part I Table 2 (40 rows) to a supplement. Output only; Part I is untouched.
    supplement_table = None
    if args.compact:
        a = para_index(paras, TABLE2_CAPTION)
        if not (paras[a + 1].startswith("| Schedule |") and paras[a + 2].startswith("*Reject evidence is reported as")):
            raise SystemExit("Table 2 layout changed: caption, table and note paragraphs not found in expected order")
        supplement_table = "\n\n".join(paras[a:a + 3])
        rows = [ln for ln in paras[a + 1].split("\n") if ln.startswith("|")]
        if len(rows) - 2 != 40:
            raise SystemExit(f"Expected 40 data rows in Table 2, found {len(rows) - 2}")
        paras[a:a + 3] = [COMPACT_POINTER]
        hits = [i for i, x in enumerate(paras) if TABLE3_CAPTION in x]  # Part II is inserted as one block
        if len(hits) != 1 or paras[hits[0]].count(TABLE3_CAPTION) != 1:
            raise SystemExit("Table 3 caption anchor not found exactly once")
        paras[hits[0]] = paras[hits[0]].replace("**Table 3.", "**Table 2.", 1)

    # Acknowledgment (IEEE/AESS: AI-generated content must be disclosed here). Inserted only when complete.
    extra_pending = []
    ack_inserted = False
    ack_path = Path(args.acknowledgment)
    if ack_path.is_file():
        ack = re.sub(r"<!--.*?-->", "", ack_path.read_text(encoding="utf-8"), flags=re.S)
        ack = re.sub(r"\s+", " ", ack).strip()
        if re.search(r"\[AUTHOR", ack):
            extra_pending.append("Acknowledgment (AI-use disclosure) NOT inserted: unresolved [AUTHOR ...] tags in " + ack_path.name)
        else:
            paras.append("## Acknowledgment {-}\n\n" + ack)
            ack_inserted = True
    else:
        extra_pending.append("Acknowledgment file missing: " + str(ack_path))

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
    combined = combined.replace("Extended Procedures---Summary of Concept and Rationale", "Extended Procedures, Summary of Concept and Rationale")  # output-only; Part I .bib untouched
    _d = "number      = {CCSDS 355.0-B-2},\n  month       = aug,"
    if _d not in combined:
        raise SystemExit("355.0-B-2 date anchor missing")
    combined = combined.replace(_d, "number      = {CCSDS 355.0-B-2},\n  month       = jul,")  # issued date July 2022
    combined = re.sub(r"(?m)^(\s*title\s*=\s*\{[^\n]*?)---", lambda m: m.group(1) + ": ", combined)
    if re.search(r"(?m)^\s*title\s*=.*---", combined):
        raise SystemExit("bibliography title still contains an em dash")
    used = set(re.findall(r"@([A-Za-z0-9_:-]+)", manuscript))
    missing = sorted(u for u in used if u not in set(k1) | set(k2))
    if missing:
        raise SystemExit("Unresolved citation keys: " + ", ".join(missing))

    from safe_trims import apply_safe_trims
    manuscript = apply_safe_trims(manuscript)
    from review_fixes import apply_review_fixes
    manuscript = apply_review_fixes(manuscript)
    manuscript = remove_em_dashes(manuscript)
    out = TWO / "out"
    out.mkdir(exist_ok=True)
    (out / "supplement_S2_evidence_details.md").write_text(build_supplement_s2() + "\n", encoding="utf-8")
    if args.compact:
        suffix = "_trim" if args.trim else ""
        (out / f"manuscript_two_part_compact{suffix}.md").write_text(manuscript, encoding="utf-8")
        supp = supplement_table.replace("**Table 2.", "**Supplementary Table S1.", 1)
        supp = supp.replace("; exact source fields are retained in Supplementary Table S1.**", ".**", 1)
        (out / "supplement_S1_deterministic_matrix.md").write_text(supp + "\n", encoding="utf-8")
        (out / "supplement_README.md").write_text(
            "# Supplementary material for the two-part TT&C resynchronization paper (DRAFT)\n\n"
            "- `supplement_S1_deterministic_matrix.md`: Supplementary Table S1, the 40-row deterministic T1 fault-coverage matrix.\n"
            "  It is copied unchanged from Table 2 of the Part I manuscript (paper/manuscript/manuscript.md, sha256 "
            + sha256(PART1_MANUSCRIPT) + "); only the label changes from Table 2 to Supplementary Table S1, and the self-referring clause in the caption (\"; exact source fields are retained in Supplementary Table S1\") is dropped.\n"
            "- `supplement_S2_evidence_details.md`: Supplementary Tables S2-S6 (Study D challenge-set structure, unreached Study C cells, outcome by security state, terms, fault scope), generated read-only from frozen CSV/JSON inputs.\n"
            "- The main text keeps a one-paragraph pointer to S1; every other table, figure and result is in the main text.\n"
            "- Source data and code: see Section 9 (Reproducibility and Artifact Availability) of the paper.\n"
            "- Frozen Part II versions: tags `study-e-prereg-v1` (commit 93636b1777e7865f5f3c0480e0ce1d3e6be6c3cf) and "
            "`study-e-analysis-script-v1` (commit 6eb87f272444c6965e2fd9b36bbe2c4aec53212d); full list in docs/study_e/FROZEN_VERSIONS.md.\n"
            "- Status: draft. Nothing here has been submitted or published.\n", encoding="utf-8")
    else:
        (out / "manuscript_two_part.md").write_text(manuscript, encoding="utf-8")
    (out / "bibliography_two_part.bib").write_text(combined, encoding="utf-8")

    print(f"part1_manuscript_sha256={sha256(PART1_MANUSCRIPT)} (matches manifest)")
    print(f"abstract_words={abstract_words}" + ("" if abstract_words == 250 else "  (Part I CI rule is exactly 250)"))
    print(f"citation_keys_used={len(used)}  new_bib_keys={len(k2)}")
    print("exact_duplicate_long_paragraphs=0")
    print("two_part_manuscript_written=PASS" + ("  (compact: Table 2 moved to supplement S1, Table 3 renumbered 2)" if args.compact else ""))
    print(f"acknowledgment_inserted={ack_inserted}")
    print("AUTHOR DECISIONS STILL PENDING:")
    for d in PENDING_DECISIONS + extra_pending:
        print(f"  - {d}")


if __name__ == "__main__":
    sys.exit(main())
