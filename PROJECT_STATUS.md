# Project Status

## Completed

- Phase One related-work and novelty framing
- Phase Two system and threat model
- Phase Three machine-readable abstract design
- repository foundation and automated Python test workflow
- B1 Triple-KEM source-semantic review
- B2 construction selection: Poettering-Roesler URKE-inspired strict baseline
- machine-readable Phase 04 baseline semantics
- adversarial review of B1 activation and B2 compromise scope
- corrected deterministic B1 and B2 fault tests
- Phase 05 independent-review handoff and 21-oracle freeze candidate
- automated handoff validation and stacked-pull-request CI
- provisional Phase 06 T1 bounded-resynchronization controller
- deterministic provisional T1 fault and guard tests
- Phase 07 seeded and explicit fault-schedule framework
- provisional contact-window recovery metrics and JSON/CSV export
- preserved-run checksum and provenance workflow outside the Git repository
- provisional Phase 08 aggregation, trace-audit, and sensitivity analysis layer

## Current phase

Phase 08 performs read-only descriptive analysis over preserved Phase 07 evidence while the Phase
04/05 independent-review gate remains open.

The analysis layer now provides:

- SHA-256 verification of a relative-path Phase 07 evidence manifest;
- field-level agreement checks between the Phase 07 JSON and CSV representations;
- per-schedule fault-kind, fault-phase, and descriptive diagnostic annotations;
- overall, outcome, fault-kind, fault-phase, and fault-count summaries;
- separate security and availability summaries;
- explicit denominator and overlapping-group metadata;
- coverage audits for missing and low-count fault groups;
- trace checks for schedule identity, event ordering, metric counts, and outcome consistency;
- an adverse-case table for all non-success records;
- fixed-schedule sensitivity reruns over provisional transmission and candidate-lifetime grids; and
- a SHA-256 manifest for every derived Phase 08 JSON/CSV output.

## Review status

- Baseline oracle candidate: `PENDING_INDEPENDENT_REVIEW`
- Independent cryptography review: not yet performed
- T1 treatment status: `PROVISIONAL_INTERNAL_REVIEW_ONLY`
- Phase 07 seed and parameter status: `UNFROZEN`
- Phase 07 result status: `PROVISIONAL_INTERNAL_REVIEW_ONLY`
- Phase 08 denominator and grid status: `UNFROZEN`
- Phase 08 analysis scope: `DESCRIPTIVE_AND_SENSITIVITY_SCAFFOLD_ONLY`
- Statistical analysis plan: not defined
- Publication, treatment-effectiveness, causal, or PCS claim status: not permitted

Development may continue on internal trace review, descriptive tables, coverage diagnostics,
fixed-schedule sensitivity scaffolding, plot-ready derived tables, and non-cryptographic analysis
instrumentation.

## Mandatory stop point

Independent cryptography review becomes mandatory before:

- accepting or freezing baseline or T1 outcome oracles;
- freezing the experiment population, seed set, fault distribution, or scenario exclusions;
- freezing retry budgets, candidate lifetimes, passive intervals, or other treatment parameters;
- adopting denominator exclusions, success thresholds, or a statistical analysis plan;
- selecting T1 as the final treatment;
- interpreting simulation output as post-compromise-security or treatment-effectiveness evidence;
- implementing real cryptographic primitives or claiming protocol conformance;
- using NOS3/cFS or Phase 08 results as publication evidence; or
- manuscript submission or any external security claim.

At that point, development must pause until the review record is complete and all corrections are
revalidated.

## Provisional Phase 08 decisions

- The preserved Phase 07 evidence directory is read-only; Phase 08 writes to a separate external
  data directory.
- Source analysis begins only after bundle SHA-256 verification and JSON/CSV consistency checks.
- Every aggregate reports its denominator.
- Fault-kind and fault-phase groups overlap and explicitly declare that membership rule.
- Low-count groups remain visible and are marked `LOW_N_DESCRIPTIVE_ONLY`.
- Diagnostic labels organize recorded events but are marked `DESCRIPTIVE_NOT_CAUSAL`.
- Security and availability remain separate dimensions.
- Sensitivity reruns reuse each exact serialized Phase 07 schedule.
- Reduced budgets record fault actions that become unreachable rather than silently changing the
  schedule definition.
- Success fractions are descriptive proportions, not probability estimates or statistical claims.
- No denominator rule, grid point, threshold, diagnostic label, or interpretation is frozen.

## Phase 08 artifacts

- `src/ttc_recovery/provisional_analysis.py`
- `spec/phase-08-provisional-analysis.json`
- `experiments/configs/phase-08-provisional.json`
- `experiments/scripts/analyze_phase07_results.py`
- `experiments/scripts/validate_phase08_provisional_analysis.py`
- `tests/scenarios/phase-08-provisional-analysis-catalog.json`
- `tests/test_provisional_analysis.py`
- `tests/test_phase08_spec.py`
- `docs/phase-08-provisional-analysis.md`

## Next internal work

- run Phase 08 against the preserved Phase 07 evidence bundle;
- verify the derived Phase 08 checksum manifest;
- inspect every trace anomaly and adverse case;
- review missing and low-count coverage groups before proposing any expanded seed population;
- examine whether sensitivity results reflect parameter effects or unreachable scheduled actions;
- add plot-ready summaries without implying confirmatory statistics;
- identify assumptions requiring cryptographic or space-systems review; and
- prepare—but do not yet claim—formal-model properties.

## Deferred

- completed independent cryptography review
- completed space-systems review
- frozen baseline and T1 oracles
- frozen experiment population, parameters, thresholds, and statistical analysis plan
- confirmatory statistical analysis
- formal model checking results
- real cryptography
- NOS3/cFS integration
- pilot experiment
- frozen full experiment protocol
- journal manuscript results
