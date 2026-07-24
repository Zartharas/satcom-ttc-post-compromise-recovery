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

## Current phase

Phase 07 develops reproducible internal experiments over the provisional T1 controller while the
Phase 04/05 independent-review gate remains open.

The experiment layer now models:

- seeded schedules generated through a recorded deterministic PRNG seed;
- canonical serialized schedules with SHA-256 identity;
- explicit `DROP`, `DELAY`, `DUPLICATE`, `REORDER`, `CONTACT_CLOSE`,
  `ENDPOINT_RESTART`, `STALE_COUNTER`, and `STALE_REPLAY` actions;
- adversarial combinations across prepare, response, commit, confirmation, test-command, and
  status-telemetry phases;
- duration measured in discrete contact windows;
- message, retry, rejection, divergence, degradation, command, telemetry, and compromise metrics;
- separate security and availability classifications; and
- JSON event/result records plus flat CSV metric output.

## Review status

- Baseline oracle candidate: `PENDING_INDEPENDENT_REVIEW`
- Independent cryptography review: not yet performed
- T1 treatment status: `PROVISIONAL_INTERNAL_REVIEW_ONLY`
- Phase 07 parameter status: `UNFROZEN`
- Phase 07 result status: `PROVISIONAL_INTERNAL_REVIEW_ONLY`
- Publication or PCS claim status: not permitted

Development may continue on internal red-team tests, seeded simulation scaffolding, metric sanity
checks, and non-cryptographic instrumentation.

## Mandatory stop point

Independent cryptography review becomes mandatory before:

- accepting or freezing baseline or T1 outcome oracles;
- freezing any experiment parameter, seed set, distribution, threshold, or statistical plan;
- selecting the final T1 treatment;
- freezing the full experiment protocol;
- interpreting simulation output as post-compromise-security evidence;
- implementing real cryptographic primitives or claiming protocol conformance;
- using NOS3/cFS results as publication evidence; or
- manuscript submission or any external security claim.

At that point, development must pause until the review record is complete and all corrections are
revalidated.

## Provisional Phase 07 decisions

- A seed is only a generator input; the serialized fault schedule and its SHA-256 digest are the
  authoritative replay artifacts.
- Seeded exploration and explicit regression schedules are kept separate.
- Contact duration is measured in modeled contact windows, not wall-clock time.
- Security and availability are reported separately and are not collapsed into a composite score.
- `SUCCESS` requires convergence, fresh command acceptance, complete status evidence, and an active
  key not marked compromised in the abstract model.
- Endpoint convergence with incomplete evidence remains `INDETERMINATE`.
- Spacecraft-only activation after bounded confirmation failure remains provisionally
  `SECURE_DEGRADED` while an authorized recovery path is still modeled.
- No seed, retry budget, candidate lifetime, fault distribution, passive interval, threshold, or
  aggregation rule is frozen.

## Phase 07 artifacts

- `src/ttc_recovery/fault_metrics.py`
- `spec/phase-07-seeded-fault-metrics.json`
- `experiments/configs/phase-07-provisional.json`
- `experiments/scripts/run_seeded_fault_experiments.py`
- `experiments/scripts/validate_phase07_seeded_metrics.py`
- `tests/scenarios/phase-07-seeded-fault-catalog.json`
- `tests/test_fault_metrics.py`
- `tests/test_phase07_spec.py`
- `docs/phase-07-seeded-fault-metrics.md`

## Next internal work

- run the full local and CI test matrix;
- inspect seeded schedules for accidental bias or unreachable fault combinations;
- add aggregation and visualization scaffolding without freezing analysis rules;
- perform a state-machine red-team review of restart, contact-lifetime, and replay semantics;
- identify assumptions requiring cryptographic or space-systems review; and
- prepare—but do not yet claim—formal-model properties.

## Deferred

- completed independent cryptography review
- completed space-systems review
- frozen baseline and T1 oracles
- frozen experiment parameters and statistical analysis plan
- formal model checking results
- real cryptography
- NOS3/cFS integration
- pilot experiment
- frozen full experiment protocol
- journal manuscript results
