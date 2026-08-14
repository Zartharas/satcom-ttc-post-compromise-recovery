# Project Status — Paper Completion Mode

**Active branch:** `paper/hands-on-recovery-study`
**Source lineage:** `phase-15/publication-preparation` through
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
FINAL_EXPERIMENT_PLAN=PREDECLARED_PRE_RUN_NOT_EXECUTED
FINAL_PUBLICATION_DATASET=NOT_EXECUTED
RESULTS_ANALYSIS=NOT_EXECUTED
MANUSCRIPT=IN_PROGRESS
INDEPENDENT_CRYPTOGRAPHY_REVIEW=OPEN_PARALLEL_ACTIVITY
PUBLICATION_EVIDENCE=false
```

## Complete enough to stop expanding

Retain the existing system/threat model, B0/B1/B2 semantics, T1 controller, fault engine,
metrics, formal evidence, Phase 14 review package, Phase 15 comparability/capture/D4 artifacts,
and regression/reproducibility tooling as the research foundation. Do not create new process
phases merely to re-close already completed work.

## Frozen objects remain untouched

The paper-completion branch does not modify or reopen:

- D4 observation cutoffs;
- D4 treatment-within-family analysis-unit denominators;
- D4 member registry; or
- D4 allowed planning-display registry.

The final paper experiment references those byte-identical objects.

## Final pre-run design

`experiments/configs/paper-final-experiment.json` is the authoritative pre-run design.

It fixes, before final-study outcome execution:

- Study A: the existing four qualified D4 families;
- Study B: 40 deterministic T1 schedules (control + 31 canonical cells + 8 retry-exhaustion
  boundaries);
- Study C: seeds `10001–10100`, 100 serialized schedules, and their SHA-256 identities;
- Study D: 12 fixed challenge schedules across a 3 x 3 retry/retention grid (108 executions);
- permitted descriptive summaries and paper output schemas; and
- SHA-256 identities of protected D2/D3/D4 and execution inputs.

The only modeling correction made while defining the final pre-run design is to restrict
`DUPLICATE` to the four message-bearing recovery phases. TEST_COMMAND and STATUS_TELEMETRY are
boolean evidence opportunities in the current simulator, so treating duplicate injection there
as executed duplicate-message behavior would be misleading.

No final-study outcomes are executed or inspected by the plan-preparation step.

## Active workstreams

1. **Final runner** — implement the lean runner against the committed pre-run config.
2. **Retained execution** — run Studies A-D once from a clean committed tree.
3. **Results analysis** — family-specific Study A, deterministic Study B, T1-only Study C/D.
4. **Manuscript** — Methods/Limitations now; Results/Discussion after the retained run.
5. **Reproducible release** — exact config, schedules, checksums, summary data, and figure data.
6. **Independent review in parallel** — strengthens baseline mapping without stopping ordinary
   paper preparation.

## Process simplification rules

1. No new numbered phases for administrative state changes.
2. No commits solely to record earlier CI.
3. New gates only when they protect validity, reproducibility, safety, legality, or an
   irreversible analysis decision.
4. Raw final outputs remain immutable; corrections create a new run.
5. Never rerun solely to obtain a preferred result.
6. Changes to the committed pre-run schedules/summary definitions after viewing final outcomes
   require a versioned, disclosed plan rather than an in-place rewrite.
7. Keep incomparable cross-treatment metrics separate.
8. Treat older trackers and PRs as historical provenance, not the active task queue.

## Immediate next work

1. Implement and validate the lean final runner using the committed machine-readable plan.
2. Execute the retained final experiment from a clean exact commit.
3. Generate Tables 1-2 and Figures 2-3 from retained outputs.
4. Complete Results, Discussion, Limitations, and Reproducibility.
5. Reconcile independent-review feedback in parallel before submission.

## Deferred from this paper

Unless needed to answer the research questions or requested during peer review:

- new formal expansion phases;
- NOS3/cFS integration;
- concrete cryptographic implementation;
- live RF/operational-spacecraft testing;
- individual cleanup/merge ceremonies for the historical PR stack; and
- additional governance-only work packages.
