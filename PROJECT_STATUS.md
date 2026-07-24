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

## Current phase

Phase 09 expands deterministic adversarial coverage and prepares a provisional formal model while the
Phase 04/05 independent-review gate remains open.

The Phase 09 layer now provides:

- 24 explicit adversarial schedules;
- coverage of every supported fault kind and every modeled protocol phase;
- retry-budget minus-one, equality, and plus-one boundaries;
- candidate-lifetime equality and plus-one boundaries;
- spacecraft-ahead and authority-epoch-floor recovery cases;
- multi-fault, restart, replay, stale-counter, and evidence-loss schedules;
- bounded reachability reports for six abstract states and seven outcomes;
- deterministic shortest known witness schedules;
- explicit `NOT_REACHED_WITHIN_PROVISIONAL_BOUND` labels for unreached states or outcomes;
- 13 invariant-to-implementation/test/schedule/formal-property mappings;
- a provisional TLA+ recovery-control module and model-check configuration; and
- JSON/CSV output with a SHA-256 derived bundle manifest.

## Review status

- Baseline oracle candidate: `PENDING_INDEPENDENT_REVIEW`
- Independent cryptography review: not yet performed
- T1 treatment status: `PROVISIONAL_INTERNAL_REVIEW_ONLY`
- Phase 07 seed and parameter status: `UNFROZEN`
- Phase 08 denominator and grid status: `UNFROZEN`
- Phase 09 scenario population: `PROVISIONAL_EXPLICIT_REGRESSION_SET`
- Phase 09 formal property set: `PROVISIONAL_ONLY`
- Formal model status: `SCAFFOLD_NOT_FORMALLY_REVIEWED`
- Model-checking result status: no publication evidence permitted
- Publication, treatment-effectiveness, causal, or PCS claim status: not permitted

Development may continue on internal schedule expansion, bounded reachability, invariant traceability,
formal-model refinement, syntax/tooling checks, and counterexample capture.

## Mandatory stop point

Independent cryptography review becomes mandatory before:

- accepting or freezing baseline or T1 outcome oracles;
- freezing the experiment population, fault distribution, scenario exclusions, or formal property set;
- freezing retry budgets, candidate lifetimes, passive intervals, or other treatment parameters;
- adopting denominator exclusions, success thresholds, or a statistical analysis plan;
- selecting T1 as the final treatment;
- mapping the abstract model to a concrete cryptographic protocol or implementation;
- interpreting reachability or model-checking output as post-compromise-security evidence;
- claiming CCSDS/SDLS conformance, flight-software correctness, or operational-spacecraft behavior;
- using Phase 08/09, NOS3/cFS, or formal-model output as publication evidence; or
- manuscript submission or any external security claim.

At that point, development must pause until the review record is complete and all corrections are
revalidated.

## Provisional Phase 09 decisions

- Explicit schedules are regression witnesses, not a statistical sample.
- Schedule SHA-256 identity and scenario ID are retained for every witness.
- The shortest known witness is selected by schedule length, then digest, then scenario ID.
- Fault actions beyond a configured retry budget remain recorded as unreachable schedule actions.
- An unreached state or outcome is not called impossible.
- Invariant traceability exposes the implementation guard, unit test, explicit witness, and formal
  property identifier.
- The TLA+ module models recovery-control state only.
- The TLA+ scaffold does not inherit or provide a cryptographic proof.
- The current repository validates scaffold consistency but does not yet claim a successful TLC or
  equivalent model-checking result.
- No scenario set, property set, bound, parameter, or interpretation is frozen.

## Phase 09 artifacts

- `src/ttc_recovery/formal_coverage.py`
- `spec/phase-09-adversarial-coverage-formal-model.json`
- `experiments/scripts/run_phase09_coverage.py`
- `experiments/scripts/validate_phase09_formal_coverage.py`
- `tests/scenarios/phase-09-adversarial-coverage-catalog.json`
- `tests/test_formal_coverage.py`
- `tests/test_phase09_spec.py`
- `formal/tla/T1Recovery.tla`
- `formal/tla/MC.cfg`
- `formal/README.md`
- `docs/phase-09-adversarial-coverage-formal-model.md`

## Next internal work

- run the complete Phase 09 local and CI gate;
- preserve a Phase 09 output bundle outside the Git repository;
- inspect every reached and bounded-unreached state and outcome;
- review shortest witnesses for accidental abstraction artifacts;
- run a real TLA+ parser/model checker when tooling is available, while keeping results internal;
- capture and classify any counterexamples;
- identify properties that require cryptographic or space-systems review; and
- prepare the external review package before any property or claim freeze.

## Deferred

- completed independent cryptography review
- completed space-systems review
- frozen baseline and T1 oracles
- frozen experiment population, parameters, thresholds, and statistical analysis plan
- frozen and independently reviewed formal property set
- publication-grade formal model checking results
- real cryptography
- NOS3/cFS integration
- pilot experiment
- frozen full experiment protocol
- journal manuscript results
