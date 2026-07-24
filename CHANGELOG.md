# Changelog

## Unreleased — Phase 04 semantic hardening

- Made B1 local-completion activation the primary minimum-assumption baseline.
- Removed simulator-wide bilateral-delivery knowledge from B1 activation.
- Reclassified authenticated-status gating as an explicit four-message enhanced variant.
- Added B1 status-loss behavior and showed that the enhanced variant retains last-message
  uncertainty.
- Added explicit B2 compromise scopes for traffic key, sender state, receiver state, and both
  endpoint states.
- Renamed the B2 traffic-key test so it no longer implies generic state-compromise recovery.
- Added passive sender-state, receiver-state tracing, both-state tracing, and active sender
  impersonation tests.
- Expanded deterministic unit coverage from 13 to 19 tests.

## Unreleased — Phase 04 initial mapping

- Locked B1 Triple-KEM completion semantics separately from operational SDLS activation.
- Selected the Poettering-Roesler URKE pattern for the strict B2 baseline.
- Corrected B2 ordering so the ground sender evolves on send and the spacecraft receiver evolves
  on accepted receipt.
- Separated lost status telemetry from cryptographic synchronization.
- Added stale-restore and replay behavior for B2.

## 0.1.0 — 2026-07-22

- Created machine-readable Phase Three specification.
- Corrected B1 classification.
- Added B0-B2 test catalog.
- Added requirements-only T1 boundary.
- Added deterministic simulator scaffold and sanity tests.
