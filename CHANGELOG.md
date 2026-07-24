# Changelog

## Unreleased — Phase 09 adversarial coverage and formal-model preparation

- Added 24 explicit adversarial recovery schedules covering every supported fault kind and protocol
  phase.
- Added retry-budget minus-one, equality, and plus-one schedules, including explicit accounting for
  fault actions beyond a reduced execution bound.
- Added candidate-lifetime equality and plus-one boundary schedules.
- Added spacecraft-ahead, authority-epoch-floor, restart, replay, stale-counter, evidence-loss, and
  multi-fault schedules.
- Added bounded state and outcome reachability reports with deterministic shortest known witnesses.
- Added `NOT_REACHED_WITHIN_PROVISIONAL_BOUND` language so bounded non-reachability is not converted
  into an impossibility claim.
- Added 13 invariant mappings connecting machine-readable requirements, implementation guards, unit
  tests, explicit schedules, and formal-property identifiers.
- Added a provisional TLA+ recovery-control module and model-check configuration.
- Added JSON/CSV coverage, reachability, and traceability output with a SHA-256 manifest.
- Added Phase 09 tests, a standalone validator, and a full CI coverage smoke test.
- Kept the scenario population, formal property set, model bounds, parameters, and all security or
  publication claims provisional and unfrozen.

## Unreleased — Phase 08 provisional analysis

- Added read-only verification for preserved Phase 07 evidence bundles using relative-path SHA-256
  manifests.
- Added field-level JSON/CSV consistency checks before analysis.
- Added per-schedule fault, phase, and event-derived diagnostic annotations while marking diagnostic
  labels descriptive rather than causal.
- Added overall, outcome, fault-kind, fault-phase, fault-count, security, and availability summaries.
- Added explicit denominators, overlapping-group declarations, and low-count warnings.
- Added coverage auditing for missing or weakly represented fault classes and phases.
- Added trace checks for schedule hashes, seeds, fault counts, event ordering, retry accounting, and
  outcome-field consistency.
- Added adverse-case extraction for all non-success records.
- Added fixed-schedule sensitivity scaffolding over provisional transmission and candidate-lifetime
  grids, including counts of scheduled fault actions made unreachable by reduced budgets.
- Added a derived JSON/CSV analysis bundle with its own SHA-256 manifest.
- Added Phase 08 tests, a machine-readable specification, a standalone validator, and a full CI
  analysis smoke test.
- Kept all denominators, grids, thresholds, statistical methods, interpretations, and security claims
  provisional and unfrozen.

## Unreleased — Phase 07 seeded fault schedules and metrics

- Added deterministic seeded fault-schedule generation with canonical JSON serialization.
- Added SHA-256 schedule identity so replay depends on the complete serialized schedule, not only
  the seed.
- Added explicit drop, delay, duplicate, reorder, contact-close, endpoint-restart, stale-counter,
  and stale-replay fault actions.
- Added contact-window recovery duration, divergence, degradation, transmission, retry, rejection,
  command, telemetry, and compromise metrics.
- Kept security and availability as separate reported dimensions.
- Added JSON result/event export and flat CSV metric export.
- Added a provisional seed configuration, 14-scenario regression catalog, Phase 07 validator, and
  CI export smoke test.
- Kept all seeds, parameters, distributions, thresholds, analysis rules, and security claims
  provisional and unfrozen.

## Unreleased — Phase 06 provisional T1 design

- Added an abstract bounded-resynchronization controller for T1.
- Added prepare, response, commit, confirmation, command, and status transitions.
- Added forward epoch negotiation that does not use simulator-only peer state.
- Added one bounded pending candidate and one bounded activation receipt.
- Added exact-binding prepare and commit retransmission behavior.
- Added deterministic loss, replay, conflict, authorization, and cache-bound tests.
- Added provisional `SECURE_DEGRADED` handling when confirmation delivery is exhausted after
  spacecraft activation.
- Added explicit external-review stop points before oracle freeze, final experiments, concrete
  cryptography, integration evidence, or manuscript claims.
- Kept all T1 security and outcome claims provisional.

## Unreleased — Phase 05 review handoff

- Added the independent-review response template.
- Added the 21-scenario baseline-oracle freeze candidate.
- Added automated review-handoff consistency validation.
- Added deterministic tests preventing silent oracle drift or unsupported acceptance.
- Extended CI to all pull-request base branches and added handoff validation.

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
- Expanded deterministic baseline unit coverage from 13 to 19 tests.

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
