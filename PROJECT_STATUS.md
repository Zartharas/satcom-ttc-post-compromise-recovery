# Project Status — Publication Preparation Mode

**Active development branch:** `paper/hands-on-recovery-study`
**Retained experiment execution commit:** `c630fb4f65ad78211fd3ffb0391000d7ed3629b1`
**Mode:** `PUBLICATION_PREPARATION_AND_SUBMISSION_READINESS`

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
RESULTS_ANALYSIS=COMPLETE_FOR_CURRENT_MANUSCRIPT
MANUSCRIPT=INTEGRATED_DRAFT_WITH_TITLE_ABSTRACT_TABLES_FIGURES
INTERNAL_EXPERIMENTAL_EVIDENCE=RETAINED_AND_ANALYZED
INDEPENDENT_CRYPTOGRAPHY_REVIEW=NOT_COMPLETED_NOT_ACTIVE_REQUIREMENT
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

1. Perform the integrated-manuscript editorial pass for concision, transitions, and venue length.
2. Select the final journal and run its venue-specific literature/claim audit.
3. Select a minimal representative adverse-trace supplement and finalize figure/table placement.
4. Prepare and publish the immutable reproducibility bundle/archive.
5. Apply venue formatting and citation style.
6. Perform final author review and submit.

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

## Update 2026-11-21 (branch `study-e-freeze-candidate`)

```text
STUDIES_A_D=FROZEN_UNCHANGED
PART_II_STUDY_E=PRE_REGISTERED_CONFIRMATORY_RESULTS_RETAINED
STUDY_F=DESCRIPTIVE_BASELINE_STEP_FAULT_RUN_NOT_PART_OF_FROZEN_PART_I
TWO_PART_MANUSCRIPT_BUILD=19_PAGES_0_OVERFULL_0_UNDEFINED
PART_I_TESTS=256_OF_256_PASS
INDEPENDENT_VALIDATION=false
PUBLISHER_SUBMISSION_AUTHORIZED=false
F1_F4_RUNTIME=SOFTWARE_ONLY_AUTHORIZED_2026-11-21
```

- Part II and Study F are additions; Studies A-D are not rerun, reclassified or pooled. The two-part manuscript is generated output (`paper/two_part/out/`, git-ignored); Part I `paper/manuscript/manuscript.md` is unchanged.
- The Part II pre-registration is frozen at annotated tag `study-e-prereg-v1` (author approval 2026-11-19). The registration document itself still carries its freeze-candidate header; this is disclosed in the manuscript.
- A four-agent independent review found no fatal integrity defect (verdict: scientifically defensible but editorially weak). Verified fixes were applied to the generated manuscript only.
- Open, author-only: full PDF read, overlength-fee decision, PR #26/#27/#30/#31 decisions, final sign-off, any submission.
- CCSDS source checks complete: 350.5-G-2 is an approved Green Book Issue 2 (Jan 2024; the public PDF cover keeps a Draft Report template label), 350.11-G-1 is Issue 1, July 2024.
- Prospective work needing a separate protocol: adversary that uses the compromised key; ground-compromise variant; protected-command implementation.

## Update 2026-11-21 (F1-F4 software-only authorization)

The author lifted the F1-F4 hold for a software-only run only: isolated sandbox, no hardware, no RF, no restricted or vendor images, no operational-spacecraft or live-network experiments, public NASA source only, pinned commits recorded. Output is evidence for the persistence mapping (Part II volatile/commit/journal); results and non-exercised steps are reported without editing frozen records. PR #31: mark ready for review only after CI is green; merge remains author-only.
