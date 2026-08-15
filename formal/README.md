# Bounded Formal-Model Evidence

The files in `formal/tla/` describe abstract recovery-control state machines used as bounded
model-consistency evidence for the current paper.

The preserved baseline module models:

- ground and spacecraft recovery modes;
- forward epoch selection;
- one pending candidate and one activation receipt;
- prepare, candidate selection, commit, confirmation, command, status, verification, retry, and expiry transitions;
- bounded attempts and one spacecraft activation; and
- explicit `SUCCESS`, `INDETERMINATE`, `SECURE_DEGRADED`, and `EXPIRED` outcomes.

The formal files do not model or prove:

- a concrete cryptographic primitive;
- CCSDS or SDLS conformance;
- packet or wire encoding;
- flight-software behavior;
- RF behavior or an operational spacecraft; or
- post-compromise security for a concrete protocol.

## Phase 10 toolchain

Phase 10 executes the model with the command-line TLA+ tools rather than relying only on source inspection.

- Stable release: `1.7.4`
- Asset: `tla2tools.jar`
- Official published SHA-1: `bee4a54f3ee3d4afc347c3240ec2d9e93b075104`
- CI Java: Temurin 17
- TLC workers: `1`

`MC.cfg` checks the recorded Phase 10 positive invariant set. A clean run is reported only as
`NO_COUNTEREXAMPLE_WITHIN_RECORDED_BOUND`.

`NegativeControl.cfg` checks the intentionally false `NegativeControlNoActivation` property. Its sole
purpose is to demonstrate that the execution pipeline captures a TLC counterexample and serializes the
trace. That expected counterexample is not a discovered defect in the recovery treatment.

Terminal states are expected in this finite state machine, so the finite configurations explicitly set
`CHECK_DEADLOCK FALSE`. This prevents normal terminal completion from being mislabeled as a model error;
it does not create a liveness claim.

## Phase 11 trace cross-validation

`SuccessWitness.cfg` checks the intentionally false `ReachabilityWitnessNoSuccess` property. It exists only
to obtain the shortest bounded trace reaching `SUCCESS`.

The emitted formal trace is normalized and replayed through the Python T1 controller under a declared
macro-step mapping. A clean comparison is labeled `MATCH_WITHIN_DECLARED_ABSTRACTION`; it is not called a
refinement proof or an implementation-equivalence result. A mismatch is labeled
`MISMATCH_REQUIRES_REVIEW` and must not be silently reconciled.

The bound configurations in `formal/tla/bounds/` vary one finite constant at a time. They are diagnostic
configurations, not selected treatment parameters. Every clean run retains the wording
`NO_COUNTEREXAMPLE_WITHIN_RECORDED_BOUND`.

## Phase 12 adverse-outcome witnesses

The configurations in `formal/tla/adverse/` use testing-only reachability properties.

Expected witnesses are captured for:

- `INDETERMINATE` after status loss;
- `SECURE_DEGRADED` after spacecraft activation followed by confirmation-budget exhaustion; and
- `EXPIRED` after retry exhaustion before activation.

Each trace is replayed through Python under the same 16-field projection used in Phase 11. The formal
`receipt` field is explicitly mapped as retained activation evidence during post-activation terminal
cleanup, because the Python controller may clear its live receipt object.

Separate checks for `DIVERGED`, `AVAILABLE_UNSAFE`, and `LOCKED` are expected to complete without a witness
in the preserved baseline. Those outcomes have zero assignments in `T1Recovery.tla`, so their Phase 12
diagnosis is `ABSENT_FROM_CURRENT_TRANSITION_ASSIGNMENTS`. Their status remains
`NOT_REACHED_WITHIN_RECORDED_BOUND`; they are not described as impossible.

## Phase 13 opt-in outcome expansion

`T1Recovery.tla` remains the preserved baseline for the Phase 10–12 results. Phase 13 enforces its exact
SHA-256 and reproduces the recorded 50-generated / 28-distinct / depth-10 absence state space.

`T1RecoveryOutcomeExpansion.tla` is a separate opt-in diagnostic module. It extends the baseline with the
expansion-only variable `gapCause` and one explicit transition path for each previously absent outcome:

- `DIVERGED` through confirmation loss followed by unilateral ground activation;
- `AVAILABLE_UNSAFE` through an explicitly adversary-known candidate that is activated and verified; and
- `LOCKED` through sender advancement after explicit prior sender-state deletion.

The configurations in `formal/tla/expansion/` use testing-only false reachability properties to obtain one
bounded witness for each path. Each trace is compared against a Python simulator projection and is also
checked against an existing canonical B1/B2 scenario with the same final outcome.

The source-level assignment audit must continue to show:

```text
T1Recovery.tla:                 0 assignments for each expanded outcome
T1RecoveryOutcomeExpansion.tla: 1 explicit assignment for each expanded outcome
```

The expansion is labeled `EXPANDED_OUTCOME_POPULATION_DIAGNOSTIC_ONLY`. It does not replace the baseline,
and `gapCause` is a provisional diagnostic classification rather than an accepted causal model.

## Evidence boundary

Phases 10 through 13 record SANY output, TLC output, finite constants, state counts, depth, tool and Java
versions, input hashes, expected testing-only witness traces, comparison records, absence or assignment
diagnostics, baseline-regression evidence, and SHA-256 manifests.

The results are not described as formal proof, cryptographic verification, implementation equivalence,
formal-model completeness, causal validation, or proof of post-compromise security. Capturing one explicit
path for each expanded outcome does not establish that the outcome population, cause vocabulary,
transition relation, or witness set is complete, realistic, necessary, sufficient, or exhaustive.

Model-checking and trace-comparison output is used in the current manuscript only as bounded supporting
consistency evidence. It has not been independently validated and does not establish correctness of the
abstraction, property set, projection, transition relation, cause vocabulary, or mapping to any concrete
treatment.

Any state, outcome, or behavior not observed in a recorded finite model must remain labeled
`NOT_REACHED_WITHIN_RECORDED_BOUND` or `NOT_REACHED_WITHIN_PROVISIONAL_BOUND`, never impossible.
