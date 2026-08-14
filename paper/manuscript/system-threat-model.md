# 3. System and Threat Model

## 3.1 System boundary

The model contains one authoritative ground security domain and one spacecraft security
function communicating across discrete intermittent TT&C contact windows. The principal entities
are the ground endpoint, spacecraft endpoint, recovery authority, communication link, adversary,
and append-only evidence service.

The traffic classes are telecommand, telemetry, key-management traffic, and recovery-control
traffic. The contact model does not assume a reliable transport. Delivery opportunities are
represented explicitly so that loss, delay, contact closure, and bounded retries can change the
recovery path.

The topology is intentionally narrower than a constellation or multi-ground-station mission.
This restriction makes endpoint-state relationships and recovery causality observable without
introducing routing, federation, or multi-authority effects that the current experiment is not
designed to test.

## 3.2 Endpoint state

Each endpoint maintains an active epoch, active security-association identifier, active key
reference, bounded pending recovery state, bounded replay state, monotonic state, and records of
compromised/retired key references. Cryptographic values are opaque identifiers carrying model
metadata; they are not outputs of a concrete cryptographic implementation.

The pending recovery object contains one recovery identifier, proposed/selected epoch, treatment,
phase, candidate key reference, contact-based lifetime, transcript reference, authority
identifier, and monotonic recovery-authority counter. At most one pending candidate is permitted
per endpoint.

The spacecraft may additionally retain one bounded activation receipt. Its purpose is narrow: if
an exact COMMIT is retransmitted after the spacecraft has already activated the candidate, the
receipt permits re-emission of the corresponding confirmation without a second activation.

Endpoint modes distinguish `NORMAL`, `SUSPECTED`, `RECOVERING`, `CANDIDATE`,
`ACTIVATED_UNVERIFIED`, `VERIFIED`, `EXPIRED`, and `LOCKED` states. Joint alignment is
classified as synchronized, ground ahead, spacecraft ahead, divergent, recovering, verified, or
locked according to the declared model state.

## 3.3 Recovery authority

T1 assumes a recovery authority whose trust is independent of the compromised operational
traffic key. The authority maintains a monotonic counter and an epoch floor that survive ordinary
endpoint rollback in the model.

The ground proposes:

```text
max(ground active epoch, recovery-authority epoch floor) + 1
```

and the spacecraft selects:

```text
max(proposed epoch, spacecraft active epoch + 1)
```

The spacecraft returns the selected epoch in the recovery response. This design avoids a hidden
simulator oracle in which ground code directly reads the spacecraft's active epoch.

The experiment does not prove that a real recovery authority can maintain these properties.
Credential protection, counter durability, and trust-anchor engineering are assumptions that a
concrete implementation would need to justify.

## 3.4 Adversary capabilities

The modeled adversary may learn operational traffic keys; obtain modeled ground protocol state;
observe, inject, replay, delay, duplicate, reorder, or suppress recovery-related messages;
exploit delivery interruption to create asymmetric endpoint advancement; present stale recovery
state or stale counters/replays; and induce modeled endpoint restart at selected recovery
boundaries.

The retained final T1 fault model exercises `DROP`, `DELAY`, `DUPLICATE`, `REORDER`,
`CONTACT_CLOSE`, `ENDPOINT_RESTART`, `STALE_COUNTER`, and `STALE_REPLAY` at phases where
the implementation gives those faults behavioral meaning.

The experiment does not assume that the adversary is permanently passive after compromise. It
does assume that successful recovery requires at least one bounded opportunity in which the
adversary cannot suppress or alter every legitimate recovery message. This is consistent with the
general observation that recovery cannot be guaranteed against indefinite denial
[@bader_ttc_key_management].

## 3.5 Trusted assumptions

The current model trusts the onboard security function outside the modeled operational-key/state
exposure; the independent recovery trust anchor; protected monotonic recovery-authority state;
restored known-good ground software; adequate fresh entropy for a future concrete cryptographic
core; the deterministic experiment orchestrator and evidence store; and the selected
cryptographic primitives under their external assumptions.

These assumptions are explicit because violating them changes the recovery problem. In
particular, compromise of the independent recovery authority or onboard root of trust is not
treated as an ordinary T1 recovery case.

## 3.6 Security, availability, and verification dimensions

The experiment does not reduce recovery to a single Boolean. It separately records endpoint
alignment, security-state classification, availability-state classification, verification
completeness, and a terminal outcome enum.

This separation prevents synchronized state from automatically being interpreted as trusted
mission recovery. `SUCCESS` requires synchronized forward state, acceptance of a fresh
post-recovery command, authenticated status telemetry, rejection of compromised/stale material,
and evidence that the modeled recovery transaction completed.

`INDETERMINATE` is used when the endpoints have converged but required command/status evidence
is missing. `EXPIRED` represents bounded recovery that cannot complete before its modeled
opportunity ends. The historical raw label `SECURE_DEGRADED` is retained for reproducibility but
must be interpreted together with the independent security-state field; in retained adverse
restart/exhaustion cases, that field is `UNSAFE`.

## 3.7 Out-of-scope threats

The model excludes onboard recovery-trust-anchor compromise, compromise of the independent
recovery authority, physical spacecraft capture, cryptographic primitive breaks, side-channel
attacks, indefinite denial of service, live RF interference/jamming, multi-spacecraft federation,
and arbitrary compromise of the experiment evidence service.

The study also does not model concrete flight-software storage, radiation effects, hardware reset
semantics, link budgets, clock drift, or mission-specific command logic. These are external
validity boundaries rather than implicit assumptions of correctness.
