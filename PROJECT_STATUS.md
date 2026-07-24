# Project Status

## Completed

- Phase One related-work and novelty framing
- Phase Two system and threat model
- Phase Three machine-readable abstract design
- repository foundation and automated Python test workflow
- B1 Triple-KEM source-semantic review
- B2 construction selection: Poettering-Roesler URKE-inspired strict baseline
- machine-readable Phase 04 baseline semantics
- adversarial review of B1 activation and B2 compromise scope
- corrected deterministic B1 and B2 fault tests
- Phase 05 independent-review handoff and 21-oracle freeze candidate
- automated handoff validation and stacked-pull-request CI
- provisional Phase 06 T1 bounded-resynchronization controller
- deterministic provisional T1 fault and guard tests
- Phase 07 seeded and explicit fault-schedule framework
- provisional contact-window recovery metrics and JSON/CSV export
- preserved-run checksum and provenance workflow outside the Git repository
- provisional Phase 08 aggregation, trace-audit, and sensitivity analysis layer
- Phase 09 explicit adversarial coverage, bounded reachability, and formal-model scaffold
- Phase 10 command-line SANY/TLC execution and counterexample-capture workflow
- Phase 11 formal/Python success-trace cross-validation and finite bound panel
- Phase 12 adverse-outcome witnesses and abstraction-gap diagnostics
- Phase 13 opt-in abstraction-gap outcome expansion and baseline-preservation diagnostics

## Current phase

Phase 13 preserves the Phase 12 `T1Recovery.tla` module as the exact baseline and adds a separate opt-in
module with one provisional path each for `DIVERGED`, `AVAILABLE_UNSAFE`, and `LOCKED`, while the Phase
04/05 independent-review gate remains open.

The Phase 13 layer provides:

- an exact SHA-256 gate for the preserved baseline module;
- mandatory reproduction of the 50-generated / 28-distinct / depth-10 Phase 12 absence state space;
- separate `T1RecoveryOutcomeExpansion.tla` diagnostic modeling;
- expansion-only `gapCause` values for confirmation loss, an adversary-known candidate, and prior sender-state
  deletion;
- one testing-only TLC witness for each previously absent outcome;
- Python replay under the existing 16-field projection;
- an independent canonical B1/B2 simulator scenario check for each final outcome;
- a source-level assignment audit distinguishing zero baseline assignments from one opt-in expansion
  assignment;
- JSON, CSV, raw SANY/TLC logs, and a SHA-256 derived manifest; and
- a real Java/TLC CI gate with a short-lived evidence artifact.

The first successful Phase 13 CI execution recorded:

- baseline and expanded SANY status: `PARSE_SUCCESS`;
- all three preserved baseline checks: 50 generated states, 28 distinct states, zero queued states, depth 10,
  zero outcome assignments, and `BASELINE_PRESERVED`;
- `DIVERGED`: four-state witness, 7 generated states, 7 distinct states, depth 4;
- `DIVERGED` comparison: 68 matched rows, zero mismatches;
- `AVAILABLE_UNSAFE`: seven-state witness, 16 generated states, 16 distinct states, depth 7;
- `AVAILABLE_UNSAFE` comparison: 119 matched rows, zero mismatches;
- `LOCKED`: five-state witness, 10 generated states, 10 distinct states, depth 5;
- `LOCKED` comparison: 85 matched rows, zero mismatches;
- combined expansion comparison: 272 matched rows and zero mismatches;
- all three canonical Python baseline checks: expected final outcome reproduced; and
- assignment diagnosis: `EXPLICITLY_ADDED_IN_OPT_IN_EXPANSION` for all three outcomes.

## Review status

- Baseline oracle candidate: `PENDING_INDEPENDENT_REVIEW`
- Independent cryptography review: not yet performed
- T1 treatment status: `PROVISIONAL_INTERNAL_REVIEW_ONLY`
- Phase 07 seed and parameter status: `UNFROZEN`
- Phase 08 denominator and grid status: `UNFROZEN`
- Phase 09 scenario population: `PROVISIONAL_EXPLICIT_REGRESSION_SET`
- Phase 09/10/11/12/13 formal property set: `PROVISIONAL_ONLY`
- Formal model review status: `NOT_INDEPENDENTLY_REVIEWED`
- Phase 10 execution status: `FORMAL_EXECUTION_GATES_PASSED`
- Phase 11 success-trace status: `MATCH_WITHIN_DECLARED_ABSTRACTION`
- Phase 12 adverse-trace status: `MATCH_WITHIN_DECLARED_ABSTRACTION`
- Phase 13 baseline status: `BASELINE_PRESERVED`
- Phase 13 expansion status: `EXPANDED_OUTCOME_POPULATION_DIAGNOSTIC_ONLY`
- Phase 13 expansion-trace status: `MATCH_WITHIN_DECLARED_ABSTRACTION`
- Phase 13 formal-model-completeness claim: `NOT_PERMITTED`
- Phase 13 implementation-equivalence claim: `NOT_PERMITTED`
- Phase 13 publication-evidence status: `NOT_PERMITTED`
- Publication, treatment-effectiveness, causal, or PCS claim status: not permitted

Development may continue on internal witness review, expansion-cause review, mismatch regression handling,
toolchain reproducibility, and external-review preparation.

## Mandatory stop point

Independent cryptography review becomes mandatory before:

- accepting or freezing baseline or T1 outcome oracles;
- freezing the experiment population, fault distribution, scenario exclusions, or formal property set;
- freezing the formal/Python projection or claiming refinement or implementation equivalence;
- treating the baseline or expanded formal outcome population as complete or realistic;
- accepting, replacing the baseline with, or freezing any Phase 13 expansion transition or cause;
- treating a single captured witness as evidence that a cause is necessary, sufficient, likely, or exhaustive;
- freezing retry budgets, candidate lifetimes, passive intervals, model constants, or other parameters;
- selecting T1 as the final treatment;
- mapping the abstract model to a concrete cryptographic protocol or implementation;
- interpreting formal or simulation output as post-compromise-security evidence;
- claiming CCSDS/SDLS conformance, flight-software correctness, or operational-spacecraft behavior;
- using Phase 08/09/10/11/12/13, NOS3/cFS, or formal-model output as publication evidence; or
- manuscript submission or any external security claim.

At that point, development must pause until the review record is complete and all corrections are
revalidated.

## Provisional Phase 13 decisions

- `T1Recovery.tla` remains the authoritative preserved baseline for the Phase 10–12 results.
- `T1RecoveryOutcomeExpansion.tla` is opt-in and diagnostic-only.
- The three expanded reachability properties are intentionally false testing properties.
- Their expected TLC counterexamples are witnesses, not discovered violations of claimed safety properties.
- `gapCause` is a provisional diagnostic classification and not a validated causal model.
- Every expanded witness is compared under the existing Phase 11 16-field projection.
- Each final outcome is also checked against an existing canonical B1/B2 Python scenario.
- A future mismatch remains `MISMATCH_REQUIRES_REVIEW`; it is not automatically reconciled.
- One explicit assignment per expanded outcome does not establish outcome or transition completeness.
- No expansion transition, cause, witness, projection, property, parameter, or interpretation is frozen.

## Phase 13 artifacts

- `src/ttc_recovery/formal_outcome_expansion.py`
- `spec/phase-13-abstraction-gap-outcomes.json`
- `experiments/scripts/run_phase13_outcome_expansion.py`
- `experiments/scripts/validate_phase13_outcome_expansion.py`
- `tests/test_formal_outcome_expansion.py`
- `tests/test_phase13_spec.py`
- `formal/tla/T1RecoveryOutcomeExpansion.tla`
- `formal/tla/expansion/DivergedWitness.cfg`
- `formal/tla/expansion/AvailableUnsafeWitness.cfg`
- `formal/tla/expansion/LockedWitness.cfg`
- `formal/tla/T1Recovery.tla` as the unchanged baseline
- `docs/phase-13-abstraction-gap-outcomes.md`
- `.github/workflows/python-tests.yml`

## Next internal work

- run the complete Phase 13 local gate and preserve an external evidence bundle;
- inspect all 272 formal/Python comparison rows and the raw expansion traces;
- review whether the three cause labels are defensible abstractions or should be split or renamed;
- identify which expansion assumptions require cryptography, protocol, or space-systems review;
- add reviewer-facing baseline-versus-expansion summaries; and
- prepare the independent-review package before any expansion transition, cause, property, projection,
  parameter, or claim freeze.

## Deferred

- completed independent cryptography review
- completed space-systems review
- frozen baseline and T1 oracles
- accepted or frozen Phase 13 expansion transitions or causes
- frozen formal/Python projection or implementation-equivalence argument
- frozen formal outcome population or completeness argument
- frozen experiment population, parameters, thresholds, and statistical analysis plan
- frozen and independently reviewed formal property set
- publication-grade formal evidence
- concrete cryptographic implementation
- CCSDS/SDLS conformance testing
- NOS3/cFS integration
- pilot experiment
- frozen full experiment protocol
- journal manuscript results
