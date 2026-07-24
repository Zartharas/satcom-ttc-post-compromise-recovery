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

## Current phase

Phase 06 evaluates internal consistency of a provisional T1 controller while the Phase 04/05
independent-review gate remains open.

The controller models:

- `RECOVERY_PREPARE -> RECOVERY_RESPONSE -> RECOVERY_COMMIT -> RECOVERY_CONFIRM`;
- forward epoch negotiation without simulator-only peer-state knowledge;
- one bounded pending candidate and one bounded activation receipt;
- exact-binding idempotent retransmission;
- command and status verification before `SUCCESS`;
- explicit `EXPIRED`, `INDETERMINATE`, and `SECURE_DEGRADED` failure outcomes.

## Review status

- Baseline oracle candidate: `PENDING_INDEPENDENT_REVIEW`
- Independent cryptography review: not yet performed
- T1 treatment status: `PROVISIONAL_INTERNAL_REVIEW_ONLY`
- Publication or PCS claim status: not permitted

Development may continue on abstract tests, scenarios, metrics, and seeded simulation scaffolding.

## Mandatory stop point

Independent cryptography review becomes mandatory before:

- accepting or freezing baseline/T1 outcome oracles;
- selecting the final T1 treatment and parameter ranges;
- freezing the full experiment protocol;
- interpreting simulation output as post-compromise-security evidence;
- implementing real cryptographic primitives or claiming conformance;
- using NOS3/cFS results as publication evidence;
- manuscript submission or external security claims.

At that point, development must pause until the review record is complete and all corrections are
revalidated.

## Provisional Phase 06 decisions

- T1 uses an established but abstract cryptographic core and adds recovery control only.
- Ground proposes an epoch using ground state and the recovery-authority epoch floor.
- Spacecraft selects the exact target above both its own state and the proposal.
- Candidates cannot authorize normal commands.
- Spacecraft activates on exact commit; ground activates on exact confirmation.
- One bounded activation receipt supports idempotent confirmation recovery.
- Confirmation-budget exhaustion after spacecraft activation is provisionally
  `SECURE_DEGRADED`, not automatically `LOCKED`.
- Success requires convergence, a fresh accepted command, and status telemetry.
- No T1 outcome is externally reviewed or frozen.

## Next internal work

- run the full local and CI test matrix;
- perform a state-machine red-team review;
- add seeded fault schedules and recovery metrics;
- identify which Phase 06 assumptions require cryptographic justification;
- prepare—but do not yet claim—formal-model properties.

## Deferred

- completed independent cryptography review
- completed space-systems review
- frozen baseline and T1 oracles
- formal model checking results
- real cryptography
- NOS3/cFS integration
- pilot experiment
- frozen full experiment protocol
- journal manuscript results
