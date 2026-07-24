# Provisional formal-model scaffold

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

`T1Recovery.tla` and `MC.cfg` are a provisional scaffold. Phase 09 validates their declared variables, actions, and property names, but the repository does not yet claim an independently reviewed or complete formalization.

Any TLC or other model-checker output produced before the external review gate is internal diagnostic evidence only. An unreached state or outcome must be reported as `NOT_REACHED_WITHIN_PROVISIONAL_BOUND`, not as impossible.
