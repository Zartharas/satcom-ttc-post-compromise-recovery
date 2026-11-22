"""Round 17: restructure the review manuscript into journal-paper form (output only).

Frozen Part I files, CSVs and result manifests are untouched. The condensed prose lives in r17_text_*.py; reused blocks
(tables, figures, Part II model text, Study F/G paragraphs) are taken verbatim from the generated text, and the material
moved out of the main text is written verbatim to supplement S10. Every anchor must occur exactly once.
"""
import re

from r17_text_a import INTRO, REL, SYS, DES_HEAD
from r17_text_b import METHOD_HEAD, RESULTS_HEAD, RES_B, RES_C, DISC_HEAD
from r17_text_c import THREATS_HEAD, REPRO, II1_POS, II3_HEAD, II4, CONCL

HEAD_RE = re.compile(r"(?m)^#{2,4} .*$")


def _idx(t: str, s: str) -> int:
    if t.count(s) != 1:
        raise SystemExit(f"Round 17 anchor not unique ({t.count(s)}): {s[:60]!r}")
    return t.index(s)


def _between(t: str, start: str, end: str) -> str:
    a = _idx(t, start)
    b = _idx(t, end)
    if b < a:
        raise SystemExit(f"Round 17 anchors out of order: {start[:40]!r}")
    return t[a:b].rstrip() + "\n\n"


def _sec(t: str, prefix: str) -> str:
    """Heading line through the line before the next heading."""
    a = _idx(t, "\n" + prefix) + 1
    m = HEAD_RE.search(t, a + 1)
    return t[a:(m.start() if m else len(t))].rstrip() + "\n"


def _body(t: str, prefix: str) -> str:
    s = _sec(t, prefix)
    return s.split("\n", 1)[1].strip() + "\n\n"


def _retitle(sec: str, level: str = "###") -> str:
    first, rest = sec.split("\n", 1)
    title = re.sub(r"^#+\s*(?:[0-9IVX]+(?:\.[0-9]+)*\.?\s+)?", "", first).strip()
    return f"{level} {title}\n{rest}"


S10_XREF = [
    (r"Section 5\.1[12]", "Section 5.5 of the paper"),
    (r"Section 9\.1", "Section 9 of the paper"),
    (r"Section 8\.10", "Section 8 of the paper"),
    (r"Section 6\.3", "Section 6.3 of the paper"),
]


def build_s10(t: str) -> str:
    parts = [
        ("S10.1 Research questions and answers", ["### 5.1 ", "### 6.6 "]),
        ("S10.2 Study designs (Studies B to D)", ["### 5.6 ", "### 5.7 ", "### 5.8 "]),
        ("S10.3 Formal assurance", ["### 5.9 ", "### 6.5 "]),
        ("S10.4 Predeclaration, retention and rerun policy", ["### 5.10 "]),
        ("S10.5 Treatment boundaries and out-of-scope threats", ["### 4.5 ", "### 3.7 "]),
        ("S10.6 Reproducibility detail", ["### 9.1 ", "### 9.2 ", "### 9.3 ", "### 9.4 ", "### 9.5 "]),
    ]
    out = [
        "# Supplementary Material S10: method and policy detail moved from the main text (DRAFT)\n\n"
        "The passages below are moved unchanged from the previous review draft of the paper; no number or claim differs from it. "
        "Section references inside them have been updated to the current numbering. Nothing here was submitted or published.\n"
    ]
    for title, prefixes in parts:
        out.append(f"## {title}\n")
        for p in prefixes:
            out.append(_retitle(_sec(t, p), "###"))
    s = "\n".join(out)
    for pat, rep in S10_XREF:
        s = re.sub(pat, rep, s)
    return s.rstrip() + "\n"


def apply_restructure(t: str):
    s10 = build_s10(t)

    head = t[: _idx(t, "## 1. Introduction")]
    fig1 = _between(t, "![Figure 1.", "### 4.5 ")
    f_body = _body(t, "### 5.11 ") + _body(t, "### 5.12 ")
    table1 = _between(t, "**Table 1.", "### 6.2 ")
    fig2 = _between(t, "![Figure 2.", "### 6.4 ")
    rel75 = "### 7.5 Relation between Part II and Part I\n\n" + _body(t, "### 7.10 ")
    part2_valid = "**Part II.** " + _body(t, "### 8.10 ").lstrip()
    part2_intro = _between(t, "## Part II.", "### II.1 ")
    model = _between(t, "The exchange is a six-message abstraction", "### II.2 ")
    ii2 = _sec(t, "### II.2 ") + "\n"
    table3 = _between(t, "**Table 3.", "### II.4 ")
    concl_paras = [p for p in re.split(r"\n\s*\n", _body(t, "## 10. Conclusion").strip())]
    concl_tail = "\n\n".join(concl_paras[2:]) + "\n\n"
    ack = t[_idx(t, "## Acknowledgment {-}"):]

    new = (
        head
        + INTRO + "\n"
        + REL + "\n"
        + SYS + "\n"
        + DES_HEAD + fig1
        + METHOD_HEAD + f_body
        + RESULTS_HEAD + table1 + RES_B + fig2 + RES_C
        + DISC_HEAD + rel75
        + THREATS_HEAD + part2_valid
        + REPRO
        + part2_intro
        + II1_POS + model
        + ii2
        + II3_HEAD + table3
        + II4
        + CONCL + concl_tail
        + ack
    )
    new = re.sub(r"\n{3,}", "\n\n", new)
    # Pointers to the supplement are already in the text; sanity checks follow.
    if "—" in new:
        raise SystemExit("Round 17 text contains an em dash")
    heads = re.findall(r"(?m)^#{2,4} (\S+)", new)
    valid = set()
    for h in heads:
        m = re.match(r"(\d+(?:\.\d+)?)\.?$", h)
        if m:
            valid.add(m.group(1))
    for m in re.finditer(r"Sections? (\d+(?:\.\d+)?)\b(?!\.\d)", new):
        if m.group(1) not in valid:
            raise SystemExit("Round 17 dangling cross-reference: " + m.group(0))
    return new, s10
