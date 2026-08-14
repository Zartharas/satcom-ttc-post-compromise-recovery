# Project Status — Paper Completion Mode

**Active branch:** `paper/hands-on-recovery-study`
**Source:** `phase-15/publication-preparation` at
`ff10a51ffbd986ef875fe462472d134fdf59695d`
**Mode:** `FINAL_EXPERIMENT_AND_MANUSCRIPT_COMPLETION`

## Current position

```text
MODEL_AND_IMPLEMENTATION=SUBSTANTIALLY_COMPLETE
BASELINE_AND_T1_TESTING=SUBSTANTIALLY_COMPLETE
FORMAL_ASSURANCE=SUFFICIENT_FOR_SUPPORTING_EVIDENCE
COMPARABILITY_DESIGN=COMPLETE_FOR_FOUR_QUALIFIED_FAMILIES
D4_REVIEW_DECISION=ACCEPT
D4_EXACT_REVIEWED_OBJECTS_FROZEN=true
FINAL_EXPERIMENT_PLAN=DRAFT_NOT_FROZEN
FINAL_PUBLICATION_DATASET=NOT_EXECUTED
RESULTS_ANALYSIS=NOT_EXECUTED
MANUSCRIPT=IN_PROGRESS
INDEPENDENT_CRYPTOGRAPHY_REVIEW=OPEN_PARALLEL_ACTIVITY
PUBLICATION_EVIDENCE=false
```

## Complete enough to stop expanding

Retain the following as the research foundation rather than creating more process phases:

- system/threat model;
- B0/B1/B2 semantics and deterministic scenario catalog;
- T1 bounded-resynchronization controller;
- fault engine and recovery metrics;
- descriptive/sensitivity tooling;
- bounded TLA+ execution, negative controls, adverse witnesses, and Python/formal comparison;
- Phase 14 review package and claims traceability;
- Phase 15 metric parity, comparability matrix, matched-family population, capture controls,
  D4 planning objects, review, and ACCEPT decision;
- regression, checksum, and reproducibility tooling.

## Frozen objects remain untouched

The restructuring does not modify or reopen:

- D4 observation cutoffs;
- D4 treatment-within-family analysis-unit denominators;
- D4 member registry; or
- D4 allowed planning-display registry.

The publication analysis plan, final robustness population, final sensitivity population,
result tables/figures, and manuscript conclusions remain separate pre-run decisions.

## Active workstreams

1. **Final experiment** — matched families, deterministic T1 fault coverage, fixed mixed-fault
   T1 panel, and retry/retention sensitivity.
2. **Results analysis** — family-specific categorical comparisons plus T1-only descriptive
   robustness/sensitivity analysis.
3. **Manuscript** — methods/limitations now; results/discussion after the retained run.
4. **Reproducible release** — exact config, commit, schedules, checksums, summary data, figure
   source data, and release/archive.
5. **Independent review in parallel** — strengthens baseline mapping but does not stop ordinary
   experiment preparation or manuscript drafting.

## Process simplification rules

1. No new numbered phases for administrative state changes.
2. No commits solely to record earlier CI.
3. New gates only when they protect validity, reproducibility, safety, legality, or an
   irreversible analysis decision.
4. Raw final outputs remain immutable; corrections create a new run.
5. Never rerun solely to obtain a preferred result.
6. Do not alter frozen D4 identities/cutoffs/denominators after comparative values are viewed
   without explicitly labeling a new post-observation protocol version.
7. Keep incomparable treatment metrics separate.
8. Treat older trackers and PRs as historical provenance, not the active task queue.

## Immediate next work

1. Finalize `paper/EXPERIMENT_EXECUTION_PLAN.md` without inspecting new final comparative output.
2. Generate the exact deterministic T1 coverage matrix and fixed 100-seed list.
3. Freeze the lean final execution/analysis plan once.
4. Execute the retained final experiment.
5. Generate tables/figures from retained outputs.
6. Complete Results, Discussion, Limitations, and Reproducibility.
7. Reconcile independent-review feedback in parallel before submission.

## Deferred from this paper

Unless needed to answer the research questions or requested during peer review:

- new formal expansion phases;
- NOS3/cFS integration;
- concrete cryptographic implementation;
- live RF/operational-spacecraft testing;
- individual cleanup/merge ceremonies for the historical PR stack; and
- additional governance-only work packages.
