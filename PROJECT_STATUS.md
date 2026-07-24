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
- Phase 11 formal/Python trace cross-validation and finite bound panel

## Current phase

Phase 11 compares an actual TLC success witness with the Python T1 controller under a declared abstract
projection and records a small finite bound panel while the Phase 04/05 independent-review gate remains open.

The Phase 11 layer now provides:

- testing-only `ReachabilityWitnessNoSuccess` reachability property;
- an eight-state shortest bounded path from initialization through successful verification;
- normalization of TLC state assignments and transition labels;
- Python replay of the same declared macro-step sequence;
- comparison of 16 abstract fields at every witness step;
- explicit `MATCH_WITHIN_DECLARED_ABSTRACTION` and `MISMATCH_REQUIRES_REVIEW` statuses;
- no silent reconciliation of formal/Python differences;
- five finite TLC configurations covering lower/higher retry and epoch bounds plus the exact baseline;
- mandatory reproduction of the Phase 10 baseline state counts;
- JSON, CSV, raw logs, and SHA-256 derived output; and
- a real Java/TLC CI gate with a short-lived evidence artifact.

The first successful Phase 11 CI execution recorded:

- SANY: `PARSE_SUCCESS`;
- success witness: eight states and the action sequence `Init`, `Prepare`, `SelectCandidate`, `Commit`,
  `Confirm`, `AcceptCommand`, `ReceiveStatus`, `Verify`;
- witness state-space summary: 28 generated states, 21 distinct states, depth 8;
- formal/Python comparison: 136 matched rows, zero mismatches;
- comparison status: `MATCH_WITHIN_DECLARED_ABSTRACTION`;
- attempts 1: 18 generated states, 12 distinct states, depth 8;
- baseline attempts 3 / epoch ceiling 6: 50 generated states, 28 distinct states, depth 10;
- attempts 5: 82 generated states, 44 distinct states, depth 12;
- epoch ceiling 4: 50 generated states, 28 distinct states, depth 10;
- epoch ceiling 8: 50 generated states, 28 distinct states, depth 10; and
- every positive bound case: `NO_COUNTEREXAMPLE_WITHIN_RECORDED_BOUND`.

## Review status

- Baseline oracle candidate: `PENDING_INDEPENDENT_REVIEW`
- Independent cryptography review: not yet performed
- T1 treatment status: `PROVISIONAL_INTERNAL_REVIEW_ONLY`
- Phase 07 seed and parameter status: `UNFROZEN`
- Phase 08 denominator and grid status: `UNFROZEN`
- Phase 09 scenario population: `PROVISIONAL_EXPLICIT_REGRESSION_SET`
- Phase 09/10/11 formal property set: `PROVISIONAL_ONLY`
- Formal model review status: `NOT_INDEPENDENTLY_REVIEWED`
- Phase 10 execution status: `FORMAL_EXECUTION_GATES_PASSED`
- Phase 11 trace status: `MATCH_WITHIN_DECLARED_ABSTRACTION`
- Phase 11 implementation-equivalence claim: `NOT_PERMITTED`
- Phase 11 bound and parameter status: `UNFROZEN`
- Positive TLC interpretation: `NO_COUNTEREXAMPLE_WITHIN_RECORDED_BOUND`
- Phase 11 publication-evidence status: `NOT_PERMITTED`
- Publication, treatment-effectiveness, causal, or PCS claim status: not permitted

Development may continue on internal trace inspection, additional explicitly bounded configurations,
projection review, mismatch regression handling, toolchain reproducibility, and external-review preparation.

## Mandatory stop point

Independent cryptography review becomes mandatory before:

- accepting or freezing baseline or T1 outcome oracles;
- freezing the experiment population, fault distribution, scenario exclusions, or formal property set;
- freezing the formal/Python projection or claiming refinement or implementation equivalence;
- freezing retry budgets, candidate lifetimes, passive intervals, model constants, or other parameters;
- adopting denominator exclusions, success thresholds, or a statistical analysis plan;
- selecting T1 as the final treatment;
- mapping the abstract model to a concrete cryptographic protocol or implementation;
- treating bounded non-reachability, a clean TLC run, or trace agreement as proof;
- interpreting formal or simulation output as post-compromise-security evidence;
- claiming CCSDS/SDLS conformance, flight-software correctness, or operational-spacecraft behavior;
- using Phase 08/09/10/11, NOS3/cFS, or formal-model output as publication evidence; or
- manuscript submission or any external security claim.

At that point, development must pause until the review record is complete and all corrections are
revalidated.

## Provisional Phase 11 decisions

- `ReachabilityWitnessNoSuccess` is intentionally false and exists only to capture a shortest bounded
  success path.
- The expected success-witness violation is not a defect or failed protocol property.
- `SelectCandidate` maps to Python prepare acceptance plus response acceptance.
- `AcceptCommand` and `ReceiveStatus` are projected evidence substeps before the Python verification call.
- Trace agreement is limited to the 16 declared abstract fields and eight recorded macro-steps.
- A future mismatch is preserved and classified; it is not automatically repaired.
- The five-case bound panel is diagnostic and does not select parameters.
- The larger retry bound exposes additional retry states in this finite model.
- The unchanged epoch-ceiling counts reflect this initial condition and single-recovery abstraction only.
- No projection, bound, property, treatment parameter, or interpretation is frozen.

## Phase 11 artifacts

- `src/ttc_recovery/formal_cross_validation.py`
- `spec/phase-11-formal-python-cross-validation.json`
- `experiments/scripts/run_phase11_cross_validation.py`
- `experiments/scripts/validate_phase11_cross_validation.py`
- `tests/test_formal_cross_validation.py`
- `tests/test_phase11_spec.py`
- `formal/tla/SuccessWitness.cfg`
- `formal/tla/bounds/Attempts1.cfg`
- `formal/tla/bounds/Attempts5.cfg`
- `formal/tla/bounds/Epoch4.cfg`
- `formal/tla/bounds/Epoch8.cfg`
- `formal/tla/T1Recovery.tla`
- `formal/README.md`
- `docs/phase-11-formal-python-cross-validation.md`
- `.github/workflows/python-tests.yml`

## Next internal work

- run the complete Phase 11 local gate and preserve an external evidence bundle;
- inspect every formal/Python comparison row and the raw eight-state witness;
- confirm bound-panel counts on the local pinned toolchain;
- add explicit mismatch fixtures and reviewer-facing trace summaries;
- identify projection assumptions requiring cryptography or space-systems review;
- decide whether another bounded panel is useful before external review; and
- prepare the independent-review package before any projection, property, parameter, or claim freeze.

## Deferred

- completed independent cryptography review
- completed space-systems review
- frozen baseline and T1 oracles
- frozen formal/Python projection or implementation-equivalence argument
- frozen experiment population, parameters, thresholds, and statistical analysis plan
- frozen and independently reviewed formal property set
- publication-grade formal evidence
- concrete cryptographic implementation
- CCSDS/SDLS conformance testing
- NOS3/cFS integration
- pilot experiment
- frozen full experiment protocol
- journal manuscript results
