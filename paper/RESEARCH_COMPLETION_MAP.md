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
- Convert `paper/RESULTS_SUMMARY.md` and tracked tables into polished Results prose.
- Explain deterministic fault mechanisms and endpoint-restart boundary.
- Explain Study C runtime-reachability limitation.
- Discuss retry-budget sensitivity without claiming universal optimum.
- Select a small number of representative adverse traces.

### Literature and positioning
- Perform one submission-stage literature search for novelty/related-work completeness.
- Recheck standards/bibliographic metadata immediately before submission.
- Avoid unverified “first” or “to our knowledge” novelty language until that search is complete.

### Figures and manuscript
- Render final publication figures from tracked source CSVs.
- Complete Introduction, Related Work, Results, Discussion, Threats to Validity,
  Reproducibility, and Conclusion.
- Keep source-to-model and independent-review limitations explicit.

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
