# Provisional formal-model execution

The files in `formal/tla/` describe an abstract recovery-control state machine for internal review.

They model:

- ground and spacecraft recovery modes;
- forward epoch selection;
- one pending candidate and one activation receipt;
- prepare, candidate selection, commit, confirmation, command, status, verification, retry, and expiry transitions;
- bounded attempts and one spacecraft activation;
- explicit `SUCCESS`, `INDETERMINATE`, `SECURE_DEGRADED`, and `EXPIRED` outcomes.

They do not model or prove:

- a concrete cryptographic primitive;
- CCSDS or SDLS conformance;
- packet or wire encoding;
- flight-software behavior;
- RF behavior or an operational spacecraft;
- post-compromise security for a concrete protocol.

## Phase 10 toolchain

Phase 10 executes the model with the command-line TLA+ tools rather than relying only on source inspection.

- Stable release: `1.7.4`
- Asset: `tla2tools.jar`
- Official published SHA-1: `bee4a54f3ee3d4afc347c3240ec2d9e93b075104`
- CI Java: Temurin 17
- TLC workers: `1`

`MC.cfg` checks the provisional positive invariant set. A clean run is reported only as
`NO_COUNTEREXAMPLE_WITHIN_RECORDED_BOUND`.

`NegativeControl.cfg` checks the intentionally false `NegativeControlNoActivation` property. Its sole
purpose is to demonstrate that the execution pipeline captures a TLC counterexample and serializes the
trace. That expected counterexample is not a discovered defect in the recovery treatment.

Terminal states are expected in this finite state machine, so both configurations explicitly set
`CHECK_DEADLOCK FALSE`. This prevents normal terminal completion from being mislabeled as a model error;
it does not create a liveness claim.

## Evidence boundary

Phase 10 records SANY output, TLC output, finite constants, state counts, depth, tool and Java versions,
input hashes, the expected negative-control trace, and a SHA-256 manifest for the derived bundle.

The positive result is not described as formal proof, cryptographic verification, or proof of
post-compromise security. Model-checking output remains internal diagnostic evidence until independent
review accepts the abstraction, property set, and mapping to any concrete treatment.

Any state, outcome, or behavior not observed in the recorded finite model must remain labeled
`NOT_REACHED_WITHIN_PROVISIONAL_BOUND`, never impossible.
