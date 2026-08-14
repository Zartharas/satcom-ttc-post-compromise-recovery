# Research Completion Map

## Purpose

Separate the scientific core from supporting assurance, historical provenance, and the work
still required to finish the hands-on paper.

## Scientific core

| Component | State | Paper use |
|---|---|---|
| System/threat model | Complete internally | Methods |
| B0/B1/B2 semantics | Implemented/tested | Baseline design |
| T1 controller | Implemented/tested | Proposed treatment |
| Fault engine and metrics | Implemented | Robustness experiment |
| Matched-family matrix | 4 qualified families | Cross-treatment comparison |
| Matched population | 13 rows / 12 units | Primary case comparison |
| D4 planning objects | Exact reviewed objects frozen | Predeclared boundary |
| Capture/lineage tooling | Implemented | Reproducibility |

No major expansion is planned unless a correctness defect is found.

## Supporting assurance

Phase 09-13 formal work is retained as supporting evidence:

- bounded TLA+ execution;
- positive/negative controls;
- adverse witnesses;
- Python/formal projection comparison; and
- diagnostic abstraction-gap analysis.

Use it in one assurance subsection plus supplementary material. Do not keep expanding it unless
the final experiment exposes a specific issue.

## Historical provenance

Keep, but remove from the active critical path:

- Phase 04-15 trackers;
- old stacked PR workflow;
- historical handoff/freeze records;
- CI reconciliation records already completed; and
- development compliance archives.

## Work still required

### Final experiment plan
- Exact deterministic T1 fault-coverage matrix.
- Fixed 100-seed mixed-fault T1 population.
- Fixed 12-schedule sensitivity population.
- Final descriptive analysis fields and table/figure schemas.
- Confirmation that frozen D4 objects are referenced unchanged.

### Final execution
- Matched-family Study A.
- Deterministic T1 Study B.
- Fixed mixed-fault T1 Study C.
- Retry/retention Study D.
- Exact provenance, logs, schedules, outputs, and checksums.

### Results
- Matched-family categorical table.
- Deterministic fault-coverage table.
- Mixed-fault T1 distribution.
- Sensitivity figure/table.
- Representative adverse traces.
- Reproducible source data for every manuscript value.

### Manuscript
- Methods from existing artifacts.
- Results only from retained final outputs.
- Mechanism-focused Discussion.
- Explicit validity/independent-review limitations.
- Reproducibility and artifact-availability statement.

### Release/submission
- Compact reproducibility bundle/tagged release.
- Final checksums and figure/table source data.
- One pre-submission claim/consistency audit.
- Venue formatting and submission.

## Not required to finish this paper

- NOS3/cFS integration;
- operational RF testing;
- concrete cryptographic primitives;
- CCSDS/SDLS conformance certification;
- another formal outcome-expansion phase;
- pooled cross-family treatment scoring; or
- inferential statistics on non-equivalent timing/retry units.

## Completion rule

A new task enters the critical path only if it materially improves experimental validity,
reproducibility, evidence quality, analysis quality, claim accuracy, reviewer comprehension, or
manuscript quality.
