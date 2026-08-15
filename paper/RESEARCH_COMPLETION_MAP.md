# Research Completion Map

## Purpose

Separate completed scientific evidence from supporting assurance, historical provenance, and the
remaining work needed to submit the hands-on paper.

## Scientific core — complete for current paper

| Component | State | Paper use |
|---|---|---|
| System/threat model | Complete internally | Methods |
| B0/B1/B2 semantics | Implemented/tested | Baseline design |
| T1 controller | Implemented/tested | Proposed treatment |
| Fault engine/metrics | Implemented | Robustness experiment |
| Matched-family matrix | 4 qualified families | Cross-treatment comparison |
| Matched population | 13 rows / 12 units | Primary matched comparison |
| D4 planning objects | Exact reviewed objects frozen | Predeclared comparison boundary |
| Final experiment plan | Committed outcome-blind | Methods / analysis boundary |
| Final runner | Committed/validated | Reproducibility |
| Retained Studies A-D | Completed | Results |
| Retained bundle integrity | 16/16 verified | Reproducibility |
| Initial result analysis | Complete | Results / Discussion input |

No additional experiment is required to begin or complete the current manuscript unless a
specific correctness defect or peer-review requirement is identified.

## Supporting assurance — preserve, do not expand by default

Phase 09-13 formal work remains supporting evidence:

- bounded TLA+ execution;
- positive/negative controls;
- adverse witnesses;
- Python/formal projection comparison; and
- diagnostic abstraction-gap analysis.

Use this in a concise assurance subsection/supplement. Do not start another formal phase without
a result-driven scientific reason.

## Historical provenance — preserve, not active work

- Phase 04-15 trackers;
- stacked development PR history;
- historical handoff/freeze records;
- already-completed CI reconciliation records;
- historical provisional configs/specs; and
- ignored development compliance archives.

Historical status strings are not rewritten after the fact.

## Remaining manuscript work

### Results and discussion
- Results, Discussion, and Threats to Validity are integrated in `paper/manuscript/manuscript.md`; the component section files remain editable evidence-linked sources.
- Tighten final narrative and table/figure callouts during the venue-specific editorial pass.
- Select a small number of representative adverse traces for the final narrative.

### Literature and positioning
- Submission-stage related-work search completed on 2026-08-14 and incorporated into Section 2.
- Recheck standards/bibliographic metadata immediately before submission.
- Run one venue-specific final search and avoid unsupported “first” or “to our knowledge” claims.

### Figures and manuscript
- Sections 1-10 remain as evidence-linked component drafts under `paper/manuscript/`.
- `paper/manuscript/manuscript.md` is now the integrated submission-facing draft with title, abstract, and keywords.
- Figures 1-3 are reproducibly rendered as vector SVGs; Tables 1-2 are inserted from tracked retained-run CSV sources.
- Perform the final editorial/venue-length pass and choose only a minimal representative adverse-trace supplement.
- Keep source-to-model limitations and the absence of independent cryptography review explicit.

### Release/submission
- Create a compact reproducibility release/archive using the retained bundle identity.
- Perform one final claim/number consistency audit.
- Recheck the selected journal's current author instructions and format.
- Submit.

## Not required to finish this paper

- NOS3/cFS integration;
- operational RF testing;
- concrete cryptographic primitives;
- CCSDS/SDLS conformance certification;
- another formal outcome-expansion phase;
- a replacement random experiment solely to improve Study C;
- pooled cross-family treatment scoring; or
- inferential statistics on non-equivalent timing/retry units.

## Completion rule

A new task enters the critical path only if it materially improves experimental validity,
reproducibility, evidence quality, analysis quality, claim accuracy, reviewer comprehension, or
manuscript quality.
