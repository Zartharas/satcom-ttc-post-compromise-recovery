# Project Status — Results and Manuscript Mode

**Active development branch:** `paper/hands-on-recovery-study`
**Retained experiment execution commit:** `c630fb4f65ad78211fd3ffb0391000d7ed3629b1`
**Mode:** `RESULTS_ANALYSIS_AND_MANUSCRIPT_COMPLETION`

## Current position

```text
MODEL_AND_IMPLEMENTATION=COMPLETE_FOR_CURRENT_PAPER
BASELINE_AND_T1_REGRESSION=256_OF_256_PASS_AT_EXECUTION_BOUNDARY
FORMAL_ASSURANCE=SUFFICIENT_FOR_SUPPORTING_EVIDENCE
COMPARABILITY_DESIGN=COMPLETE_FOR_FOUR_QUALIFIED_FAMILIES
D4_REVIEW_DECISION=ACCEPT
D4_EXACT_REVIEWED_OBJECTS_FROZEN=true
FINAL_EXPERIMENT_PLAN=COMMITTED_PREDECLARED
FINAL_RUNNER=COMMITTED_AND_VALIDATED
FINAL_RETAINED_EXPERIMENT=PASS
RETAINED_RUN_ID=20260814T022506Z-gc630fb4
RETAINED_BUNDLE_INTEGRITY=16_OF_16_PASS
INITIAL_RESULTS_ANALYSIS=COMPLETE
MANUSCRIPT=IN_PROGRESS
INTERNAL_EXPERIMENTAL_EVIDENCE=RETAINED_AND_ANALYZED
INDEPENDENT_CRYPTOGRAPHY_REVIEW=OPEN_PARALLEL_ACTIVITY
INDEPENDENT_VALIDATION=false
PUBLICATION_EVIDENCE=false
```

The run metadata intentionally retains `publication_evidence=false` and
`independent_validation=false`. The retained outputs are usable as internal experimental
evidence for the manuscript with the declared limitations; they are not self-certifying
cryptographic or external validation.

## Retained experiment identity

- plan commit: `cfb730a8191d37863e9e419823686b3c3afe18a2`;
- plan SHA-256: `3570834a70c76e020dada459e036786f690698125fe1d9e171e9f945748a1012`;
- runner/execution commit: `c630fb4f65ad78211fd3ffb0391000d7ed3629b1`;
- run: `20260814T022506Z-gc630fb4`;
- bundle SHA-256:
  `b3b8c55a9e522ffe3f7898d7b786583e46a4dc3db0aba9d3947fd6ebdaeecaa1`;
- internal final-bundle manifest: 16/16 files verified.

The retained experiment is not rerun merely to obtain preferred outcomes. A proven execution or
implementation defect would require a separately identified correction run while preserving
this bundle.

## Current findings

### Study A — matched families

The four qualified families showed categorical parity on the pre-authorized fields. This does
not support a categorical-superiority claim for T1 over B0/B1/B2.

### Study B — deterministic T1 faults

Across 31 canonical fault-kind/phase cells:

- 25 `SUCCESS`;
- 4 `INDETERMINATE`;
- 1 `EXPIRED`;
- 1 `SECURE_DEGRADED`.

Endpoint restart around activation/confirmation is the clearest observed hard boundary. Missing
verification evidence is conservatively classified as `INDETERMINATE`.

### Study C — fixed mixed schedules

The fixed 100-schedule population produced 74 `SUCCESS`, 15 `INDETERMINATE`, 6
`SECURE_DEGRADED`, and 5 `EXPIRED`. A post-execution reachability audit found that 77 of 191
scheduled fault actions were actually applied, 43 schedules reached no fault action, and 24 of
31 scheduled fault-kind/phase cells were exercised at runtime.

Therefore Study C is reported as a fixed synthetic schedule-population characterization, not as
a 74% success rate under faults.

### Study D — sensitivity

Across each candidate-lifetime setting:

- max transmissions 2: 5/12 verification complete;
- max transmissions 3: 11/12;
- max transmissions 4: 11/12.

Candidate lifetime from 2–4 contacts produced no observed change in this fixed challenge set.
The persistent failure was COMMIT-stage spacecraft restart.

## Frozen and preserved scientific history

The paper-completion work does not rewrite:

- D4 observation cutoffs;
- D4 treatment-within-family analysis-unit denominators;
- D4 member registry;
- D4 allowed planning-display registry;
- the predeclared final experiment plan;
- the retained final run; or
- historical phase/governance status records.

Older phase records remain historical provenance even when their status text differs from the
current project state.

## Active workstreams

1. Draft Results, Discussion, Threats to Validity, and Reproducibility from the retained
   evidence.
2. Complete the submission-stage literature/standards verification.
3. Render publication figures from tracked figure-source data.
4. Prepare a compact reproducibility release/archive without changing the retained result.
5. Continue independent baseline cryptography review in parallel and scope any resulting
   correction transparently.
6. Select/final-check venue formatting and submit.

## Process rule

No new phase, tracker, freeze package, or decision-only commit is created unless it directly
protects scientific validity, reproducibility, safety, legality, or an irreversible result
decision.

## Deferred from this paper

Unless required by peer review:

- new formal outcome-expansion work;
- NOS3/cFS integration;
- concrete cryptographic primitive implementation;
- live RF/operational-spacecraft testing; and
- new cross-treatment timing/retry comparisons.
