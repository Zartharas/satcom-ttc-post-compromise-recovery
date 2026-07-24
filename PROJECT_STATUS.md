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

## Current phase

Phase 12 captures bounded formal witnesses for adverse outcomes, replays them through the Python T1
controller under the declared 16-field projection, and diagnoses why three other outcomes remain absent while
the Phase 04/05 independent-review gate remains open.

The Phase 12 layer provides:

- testing-only reachability properties for `INDETERMINATE`, `SECURE_DEGRADED`, `EXPIRED`, `DIVERGED`,
  `AVAILABLE_UNSAFE`, and `LOCKED`;
- explicit formal witness capture for the first three outcomes;
- Python replay with per-field comparison and `MISMATCH_REQUIRES_REVIEW` retention;
- an explicit retained-receipt-evidence projection for post-activation terminal cleanup;
- bounded non-reachability checks for the final three outcomes;
- a source-level transition-assignment audit;
- `ABSENT_FROM_CURRENT_TRANSITION_ASSIGNMENTS` diagnosis instead of an impossibility claim;
- JSON, CSV, raw SANY/TLC logs, and a SHA-256 derived manifest; and
- a real Java/TLC CI gate with a short-lived evidence artifact.

The first successful Phase 12 CI execution recorded:

- SANY: `PARSE_SUCCESS`;
- `INDETERMINATE`: seven-state witness, 22 generated states, 17 distinct states, depth 7;
- `INDETERMINATE` comparison: 119 matched rows, zero mismatches;
- `SECURE_DEGRADED`: seven-state witness, 25 generated states, 20 distinct states, depth 7;
- `SECURE_DEGRADED` comparison: 119 matched rows, zero mismatches;
- `EXPIRED`: five-state witness, 14 generated states, 11 distinct states, depth 5;
- `EXPIRED` comparison: 85 matched rows, zero mismatches;
- `DIVERGED`, `AVAILABLE_UNSAFE`, and `LOCKED`: each 50 generated states, 28 distinct states,
  zero queued states, and depth 10;
- all three currently absent outcomes: `NOT_REACHED_WITHIN_RECORDED_BOUND`; and
- all three absence diagnoses: `ABSENT_FROM_CURRENT_TRANSITION_ASSIGNMENTS`.

## Review status

- Baseline oracle candidate: `PENDING_INDEPENDENT_REVIEW`
- Independent cryptography review: not yet performed
- T1 treatment status: `PROVISIONAL_INTERNAL_REVIEW_ONLY`
- Phase 07 seed and parameter status: `UNFROZEN`
- Phase 08 denominator and grid status: `UNFROZEN`
- Phase 09 scenario population: `PROVISIONAL_EXPLICIT_REGRESSION_SET`
- Phase 09/10/11/12 formal property set: `PROVISIONAL_ONLY`
- Formal model review status: `NOT_INDEPENDENTLY_REVIEWED`
- Phase 10 execution status: `FORMAL_EXECUTION_GATES_PASSED`
- Phase 11 success-trace status: `MATCH_WITHIN_DECLARED_ABSTRACTION`
- Phase 12 adverse-trace status: `MATCH_WITHIN_DECLARED_ABSTRACTION`
- Phase 12 formal-model-completeness claim: `NOT_PERMITTED`
- Phase 12 implementation-equivalence claim: `NOT_PERMITTED`
- Phase 12 publication-evidence status: `NOT_PERMITTED`
- Publication, treatment-effectiveness, causal, or PCS claim status: not permitted

Development may continue on internal witness review, abstraction-gap analysis, explicit transition proposals,
mismatch regression handling, toolchain reproducibility, and external-review preparation.

## Mandatory stop point

Independent cryptography review becomes mandatory before:

- accepting or freezing baseline or T1 outcome oracles;
- freezing the experiment population, fault distribution, scenario exclusions, or formal property set;
- freezing the formal/Python projection or claiming refinement or implementation equivalence;
- treating the current formal outcome population as complete;
- adding and accepting transition semantics for `DIVERGED`, `AVAILABLE_UNSAFE`, or `LOCKED`;
- treating bounded non-reachability as impossibility;
- freezing retry budgets, candidate lifetimes, passive intervals, model constants, or other parameters;
- selecting T1 as the final treatment;
- mapping the abstract model to a concrete cryptographic protocol or implementation;
- interpreting formal or simulation output as post-compromise-security evidence;
- claiming CCSDS/SDLS conformance, flight-software correctness, or operational-spacecraft behavior;
- using Phase 08/09/10/11/12, NOS3/cFS, or formal-model output as publication evidence; or
- manuscript submission or any external security claim.

At that point, development must pause until the review record is complete and all corrections are
revalidated.

## Provisional Phase 12 decisions

- The three captured adverse reachability properties are intentionally false testing properties.
- Their expected TLC counterexamples are witnesses, not discovered safety defects.
- Every captured witness is replayed through Python under the Phase 11 16-field projection.
- The formal `receipt` field maps to retained activation evidence during post-activation expiry.
- A future mismatch remains `MISMATCH_REQUIRES_REVIEW`; it is not automatically reconciled.
- `DIVERGED`, `AVAILABLE_UNSAFE`, and `LOCKED` have zero current transition assignments.
- Their current bounded absence is an abstraction-coverage gap, not evidence that they are impossible.
- No projection, transition set, property, bound, treatment parameter, or interpretation is frozen.

## Phase 12 artifacts

- `src/ttc_recovery/formal_adverse_validation.py`
- `spec/phase-12-adverse-outcome-witnesses.json`
- `experiments/scripts/run_phase12_adverse_validation.py`
- `experiments/scripts/validate_phase12_adverse_outcomes.py`
- `tests/test_formal_adverse_validation.py`
- `tests/test_phase12_spec.py`
- `formal/tla/adverse/IndeterminateWitness.cfg`
- `formal/tla/adverse/SecureDegradedWitness.cfg`
- `formal/tla/adverse/ExpiredWitness.cfg`
- `formal/tla/adverse/DivergedAbsence.cfg`
- `formal/tla/adverse/AvailableUnsafeAbsence.cfg`
- `formal/tla/adverse/LockedAbsence.cfg`
- `formal/tla/T1Recovery.tla`
- `docs/phase-12-adverse-outcome-witnesses.md`
- `.github/workflows/python-tests.yml`

## Next internal work

- run the complete Phase 12 local gate and preserve an external evidence bundle;
- inspect all 323 formal/Python comparison rows and raw adverse witness traces;
- prepare explicit abstraction proposals for the three currently absent outcomes without adopting them;
- identify which proposals require cryptography, protocol, or space-systems review;
- add reviewer-facing witness and abstraction-gap summaries; and
- prepare the independent-review package before any transition, property, projection, parameter, or claim freeze.

## Deferred

- completed independent cryptography review
- completed space-systems review
- frozen baseline and T1 oracles
- frozen formal/Python projection or implementation-equivalence argument
- frozen formal outcome population or transition semantics
- frozen experiment population, parameters, thresholds, and statistical analysis plan
- frozen and independently reviewed formal property set
- publication-grade formal evidence
- concrete cryptographic implementation
- CCSDS/SDLS conformance testing
- NOS3/cFS integration
- pilot experiment
- frozen full experiment protocol
- journal manuscript results
