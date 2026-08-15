# Changelog

## Unreleased — hands-on paper retained results and repository refresh

- Integrated Sections 1-10 into a single submission-facing manuscript with the working final title, abstract, and keywords.
- Inserted Table 1 and the full 40-row deterministic Table 2 from tracked retained-run CSV sources.
- Added a standard-library vector renderer and publication-facing SVGs for the recovery architecture, Study C outcomes, and Study D sensitivity grid.
- Applied integration-only de-duplication by removing the redundant Discussion claim-boundary tail and Threats-to-Validity summary tail from the assembled manuscript while preserving their component source drafts.
- Added manuscript-wide numerical lineage, citation resolution, overclaim, duplicate-paragraph, and dissertation-style wording checks.
- Completed submission-stage related-work review against current CCSDS/NIST sources and primary
  TT&C key-management, SDLS key-update, space key-establishment, and SpaceSec testbed literature.
- Added evidence-linked manuscript drafts for Introduction, Background/Related Work, System/Threat
  Model, Recovery Designs, Experimental Method, Reproducibility, and Conclusion; Sections 1-10 now
  all have working drafts.
- Narrowed novelty positioning to operational post-compromise TT&C resynchronization behavior and
  explicitly avoided universal first/superiority claims.
- Added bibliography entries for Bader 2024, Dowling et al. 2025, AegisSat 2025, and the SpaceSec
  2025 testbed-fidelity work.
- Corrected current-facing simulator-architecture text that still described independent review and
  formal modeling as future/open work; historical phase artifacts remain unchanged.
- Refocused active development on the hands-on research paper rather than additional governance
  phases.
- Committed the outcome-blind final experiment plan at `cfb730a8191d37863e9e419823686b3c3afe18a2`.
- Committed the plan-bound final runner at `c630fb4f65ad78211fd3ffb0391000d7ed3629b1`.
- Executed retained run `20260814T022506Z-gc630fb4` once from a clean exact commit.
- Verified the retained bundle SHA-256
  `b3b8c55a9e522ffe3f7898d7b786583e46a4dc3db0aba9d3947fd6ebdaeecaa1`
  and all 16 internal checksum-manifest entries.
- Retained Study A (13 member rows), Study B (40 deterministic schedules), Study C (100 fixed
  schedules), and Study D (108 sensitivity executions).
- Added manuscript-facing result summaries and a post-execution Study C runtime-reachability
  audit without replacing or rerunning the retained experiment.
- Refreshed current-facing README/status/paper/reference/navigation files while preserving
  historical phase artifacts and their original status language.
- Added active paper-branch push CI and final-plan `--validate-only` checking.
- Retained all cryptographic, flight, conformance, causal, and real-world-prevalence claim
  boundaries; no independent cryptography review was completed.
- Closed the optional independent-review tracker after confirming it carried no external review
  evidence and was not required for manuscript completion.
- Added manuscript drafts for Results, Discussion, and Threats to Validity grounded in the retained
  final experiment.

## Unreleased — Phase 15 D4 review and freeze readiness

- Added the separate outcome-blind WP15-D4R review package pinned to validated D4 target `34d63a5` and repaired the preflight defect recorded as RIT-019.
- Completed FR-01 through FR-16 with `PASS` without viewing projected values, raw family outcomes, aggregates, rates, or rankings.
- Recorded the explicit internal `ACCEPT` decision at commit `307f685389d799fb5b22d481763bd171393085db`; the record explicitly does not claim independent validation.
- Recorded successful exact-decision-commit CI in runs `30942565654` and `30942565653`, making the reviewed D4 planning-object freeze effective.
- Reconciled the tracked effective-freeze state at commit `771730bd0cd0401a2098c6e3fdd9b85e0727c4ff`; exact-head runs `30955849832` and `30955849545` also completed successfully.
- Froze only the exact reviewed observation cutoffs, treatment-within-family analysis-unit denominators, member registry, and allowed planning-display registry.
- Kept the publication analysis plan unfrozen and kept family-value display, rates, pooled aggregation, inference, superiority, causal interpretation, cryptographic claims, independent-validation claims, and publication evidence closed.
- Kept Issue #3 open for the separate external baseline-review gate; the internal D4 review does not satisfy that independent-review requirement.

## Unreleased — Phase 14 independent review package

- Added a reviewer-facing package with status `READY_FOR_OUTREACH_NOT_REVIEWED`.
- Added an integrated response template covering all 24 review questions and all 21 baseline scenario oracles.
- Restored the omitted B1 endpoint-knowledge question as `B1-R5` without rewriting the historical Phase 05
  response template.
- Added a 20-entry claims traceability matrix with explicit qualifiers, evidence paths, reviewer questions, and
  prohibited overstatements.
- Added a 21-entry evidence index pinned by the exact review-target commit.
- Added four open governance findings covering response-template mismatch, retrospective Phase 6-13 work,
  implementation-lock versus independent-approval ambiguity, and review-target commit drift.
- Separated mandatory baseline cryptography review from the optional or separately staffed formal-diagnostic
  scope.
- Added a second-reviewer requirement when the primary reviewer does not cover formal methods or another
  declared scope.
- Added automated checks that issue #3 remains open, the baseline oracle candidate remains pending, no reviewer
  approval is fabricated, and all hard claim boundaries remain `NOT_PERMITTED`.
- Added Phase 14 unit tests, standalone validation, and CI integration.
- Added no protocol transition, formal property, fault behavior, treatment parameter, or security claim.

## Unreleased — Phase 13 abstraction-gap outcome expansion

- Preserved `formal/tla/T1Recovery.tla` byte-for-byte as the Phase 12 baseline and enforced its recorded
  SHA-256 in code, tests, and the machine-readable Phase 13 contract.
- Reproduced the baseline 50-generated / 28-distinct / depth-10 state space for `DIVERGED`,
  `AVAILABLE_UNSAFE`, and `LOCKED` absence checks.
- Added separate opt-in `T1RecoveryOutcomeExpansion.tla` diagnostic modeling with the expansion-only
  `gapCause` state variable.
- Added explicit confirmation-loss, adversary-known-candidate, and prior-sender-state-deletion paths.
- Captured four-, seven-, and five-state testing-only witnesses for `DIVERGED`, `AVAILABLE_UNSAFE`, and
  `LOCKED`, respectively.
- Compared the three expansion traces over the existing 16-field projection and recorded 272/272 matched
  rows with zero mismatches.
- Added independent canonical Python checks using the existing B1 confirmation-loss, B2 receiver-state
  exposure, and B2 dropped-update semantics.
- Added assignment auditing that records zero assignments in the baseline and exactly one explicit
  assignment per outcome in the opt-in expansion.
- Added JSON witness records, comparison and audit CSV files, raw Java/SANY/TLC logs, and a SHA-256 derived
  manifest.
- Added Phase 13 tests, specification, validator, runner, documentation, and a real Java/TLC CI gate.
- Kept the expansion, causes, transition paths, projection, model-completeness interpretation, and
  publication claims provisional and unfrozen.

## Unreleased — Phase 12 adverse-outcome witnesses

- Added six testing-only outcome reachability properties and separate TLC configurations.
- Captured bounded witnesses for `INDETERMINATE`, `SECURE_DEGRADED`, and `EXPIRED`.
- Replayed each adverse witness through the Python T1 controller under the Phase 11 16-field projection.
- Added explicit retained-receipt-evidence mapping for post-activation terminal cleanup.
- Recorded 119/119 matched rows for `INDETERMINATE`, 119/119 for `SECURE_DEGRADED`, and 85/85 for
  `EXPIRED`, with zero mismatches.
- Added bounded absence checks for `DIVERGED`, `AVAILABLE_UNSAFE`, and `LOCKED`.
- Added source-level transition-assignment auditing and the diagnosis
  `ABSENT_FROM_CURRENT_TRANSITION_ASSIGNMENTS`.
- Kept every absent outcome labeled `NOT_REACHED_WITHIN_RECORDED_BOUND`, never impossible.
- Added JSON witness records, comparison CSV files, an unreached-outcome diagnostic CSV, raw SANY/TLC logs,
  and a SHA-256 derived manifest.
- Added Phase 12 tests, specification, validator, runner, documentation, and a real Java/TLC CI gate.
- Kept the model, outcome population, projection, properties, transition semantics, interpretation, and
  publication claims provisional and unfrozen.

## Unreleased — Phase 11 formal/Python trace cross-validation

- Added the testing-only `ReachabilityWitnessNoSuccess` invariant and a separate success-witness TLC
  configuration.
- Captured the shortest bounded eight-state path from initialization through successful verification.
- Added TLA+ scalar and transition-label normalization for TLC traces.
- Added Python T1 controller replay under an explicit macro-step and evidence mapping.
- Compared 16 abstract fields at every witness step and retained per-field CSV evidence.
- Added `MATCH_WITHIN_DECLARED_ABSTRACTION` and `MISMATCH_REQUIRES_REVIEW` statuses without claiming
  refinement proof or implementation equivalence.
- Added a five-case finite bound panel for lower/higher retry and epoch bounds plus exact Phase 10 baseline
  reproduction.
- Recorded the first successful comparison: 136 matched rows, zero mismatches, and exact reproduction of
  the 50-generated / 28-distinct / depth-10 baseline.
- Recorded the provisional bound panel: attempts 1 produced 18/12/depth 8; attempts 5 produced
  82/44/depth 12; epoch ceilings 4 and 8 retained the baseline counts under the current initial condition.
- Added JSON, CSV, raw SANY/TLC logs, and a SHA-256 derived manifest.
- Added Phase 11 tests, specification, validator, runner, documentation, and a real Java/TLC CI gate.
- Kept the projection, properties, bounds, parameters, interpretation, and publication claims provisional
  and unfrozen.

## Unreleased — Phase 10 formal model execution

- Pinned the stable TLA+ command-line tools release `1.7.4` and verified the official published JAR
  checksum before execution.
- Added a real SANY parse gate and a bounded positive TLC model-check gate.
- Added mandatory `NO_COUNTEREXAMPLE_WITHIN_RECORDED_BOUND` wording for clean finite TLC runs.
- Added the intentionally false `NegativeControlNoActivation` property and separate TLC configuration
  to prove the counterexample-capture pipeline is working.
- Added structured negative-control trace serialization and retained raw SANY/TLC logs.
- Added tool, Java, platform, command, worker-count, input-hash, state-count, and search-depth metadata.
- Added a SHA-256 manifest for all derived Phase 10 execution files.
- Added a separate Java/TLC CI job and short-lived formal-execution artifacts.
- Added Phase 10 parser tests, specification tests, a machine-readable contract, validator, runner, and
  documentation.
- Recorded the first successful finite CI run: 50 generated states, 28 distinct states, depth 10, no
  positive counterexample within the recorded bound, and a four-state expected negative-control trace.
- Kept the model, properties, constants, treatment mapping, interpretation, and publication claims
  provisional and unfrozen.

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
