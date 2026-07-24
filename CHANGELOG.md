# Changelog

## Unreleased — Phase 04

- Locked B1 Triple-KEM completion semantics separately from operational SDLS activation.
- Changed default B1 final-confirmation loss from automatic divergence to an expired attempt
  with the previous epoch still active.
- Added unilateral B1 activation as an explicit negative-control policy.
- Selected the Poettering-Roesler URKE pattern for the strict B2 baseline.
- Corrected B2 ordering so the ground sender evolves on send and the spacecraft receiver
  evolves on accepted receipt.
- Separated lost status telemetry from cryptographic synchronization.
- Added stale-restore and replay behavior for B2.
- Expanded deterministic unit coverage from 8 to 13 tests.

## 0.1.0 — 2026-07-22

- Created machine-readable Phase Three specification.
- Corrected B1 classification.
- Added B0-B2 test catalog.
- Added requirements-only T1 boundary.
- Added deterministic simulator scaffold and sanity tests.
