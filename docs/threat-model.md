# Threat Model

## Protected system

One authoritative ground security domain communicates with one spacecraft security function
over intermittent TT&C contact windows.

## Adversary capabilities

The modeled adversary may obtain operational keys and ground protocol state; observe, inject,
replay, delay, duplicate, reorder, or suppress messages; cause asymmetric endpoint advancement;
and restore the ground endpoint from a stale snapshot.

## Trusted components

The initial model trusts the onboard security function, protected monotonic state, independent
recovery trust anchor, restored known-good ground software, adequate entropy, experiment
orchestrator, evidence store, and selected cryptographic primitives under accepted assumptions.

## Recovery assumption

A strong recovery claim requires at least one bounded opportunity during which the adversary
cannot alter or suppress every legitimate recovery message.

## Out of scope

Onboard trust-anchor compromise, primitive breaks, physical spacecraft capture, side-channel
attacks, indefinite denial of service, live RF interference, multiple spacecraft, and compromise
of the independent recovery authority.
