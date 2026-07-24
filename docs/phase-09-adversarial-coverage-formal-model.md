# Phase 09 adversarial coverage and formal-model preparation

## Purpose

Phase 09 expands deterministic adversarial coverage over the provisional T1 controller and prepares a bounded formal-model scaffold. It does not freeze the scenario population, formal property set, treatment parameters, or security claims.

## Explicit coverage suite

The suite contains 24 hand-authored schedules. Together they cover:

- all supported fault kinds: drop, delay, duplicate, reorder, contact closure, endpoint restart, stale counter, and stale replay;
- all protocol phases: prepare, response, commit, confirmation, test command, and status telemetry;
- retry-budget minus-one, equality, and plus-one boundaries;
- candidate-lifetime equality and plus-one boundaries;
- spacecraft-ahead recovery without a hidden peer-state oracle;
- recovery-authority epoch-floor selection;
- multi-fault combinations.

The explicit catalog is regression evidence, not a statistical sample.

## Bounded reachability

Each schedule is executed through the Phase 07 experiment runner. The Phase 09 report records:

- schedule ID and SHA-256 digest;
- schedule length and any unreachable fault actions;
- state trace;
- final outcome and alignment;
- security and availability states;
- inferred final endpoint modes;
- command, telemetry, rejection, retry, and contact-window evidence.

For each abstract state and outcome, the report retains the shortest known witness schedule. Equal-length witnesses are ordered deterministically by schedule digest and scenario ID.

A state or outcome not reached by the current suite is labeled:

```text
NOT_REACHED_WITHIN_PROVISIONAL_BOUND
```

That label does not mean impossible.

## Invariant traceability

Thirteen provisional invariant mappings connect:

1. the machine-readable invariant identifier;
2. an implementation guard or transition;
3. an existing unit test;
4. an explicit Phase 09 witness schedule; and
5. a formal-property identifier.

The mapping is intended to expose unsupported or weakly supported properties before any property set is frozen.

## Formal scaffold

`formal/tla/T1Recovery.tla` describes an abstract recovery-control model with:

- ground and spacecraft modes;
- endpoint epochs and previous epochs;
- a pending candidate and activation receipt;
- prepare, candidate selection, commit, confirmation, command, status, verification, retry, and expiry transitions;
- bounded attempts and one spacecraft activation;
- explicit success, indeterminate, secure-degraded, and expired outcomes.

`formal/tla/MC.cfg` declares the provisional model constants and safety invariants.

The repository validates the presence and consistency of the scaffold, but Phase 09 does not yet claim that TLC or another formal checker has established the properties. Any future counterexample or no-counterexample result remains internal diagnostic evidence until the review gate is satisfied.

## Outputs

The Phase 09 runner writes:

- `phase09-coverage-reachability.json`;
- `phase09-coverage-results.csv`;
- `phase09-reachability.csv`;
- `phase09-invariant-traceability.csv`;
- `phase09-derived-bundle.sha256`.

## Claim boundary

Phase 09 does not establish:

- security of a concrete cryptographic construction;
- post-compromise security of a deployed protocol;
- CCSDS or SDLS conformance;
- flight-software correctness;
- RF behavior or operational-spacecraft behavior;
- completeness of the formal property set;
- impossibility of any state or outcome not reached within the current bound.

Independent review becomes mandatory before freezing formal properties, mapping the model to a concrete protocol, selecting final parameters or treatment, using model-checking output as publication evidence, or making any external security claim.
