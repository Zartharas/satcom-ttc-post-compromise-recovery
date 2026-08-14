# SATCOM TT&C Post-Compromise Recovery

Hands-on experimental cybersecurity research on restoring trusted satellite telemetry,
tracking, and command (TT&C) communications after operational-key compromise and
ground-space security-state divergence.

## Research objective

Evaluate, within a bounded synthetic software model, how abstract recovery baselines and a
bounded resynchronization treatment behave under matched recovery conditions and controlled
communication/state faults.

No operational satellites, live TT&C systems, RF links, or flight software are used.

## Research questions

1. **Matched recovery behavior:** Under defensibly matched conditions, how do B0, B1, B2, and
   T1 compare in terminal security, availability, alignment, and verification classifications?
2. **T1 fault robustness:** How does T1 behave under controlled loss, delay, duplication,
   reordering, contact interruption, endpoint restart, stale counter, and replay faults?
3. **T1 sensitivity:** How does T1 behavior change across bounded retry budgets and
   candidate-retention lifetimes?
4. **Assurance:** Where do bounded TLA+ witnesses and Python executions agree or differ under
   the declared abstraction/projection?

## Current paper state

The final experiment plan was predeclared before outcome inspection and is preserved in
`experiments/configs/paper-final-experiment.json`.

The retained final experiment was executed once from:

- execution commit: `c630fb4f65ad78211fd3ffb0391000d7ed3629b1`;
- plan commit: `cfb730a8191d37863e9e419823686b3c3afe18a2`;
- plan SHA-256: `3570834a70c76e020dada459e036786f690698125fe1d9e171e9f945748a1012`;
- retained run: `20260814T022506Z-gc630fb4`;
- retained bundle SHA-256:
  `b3b8c55a9e522ffe3f7898d7b786583e46a4dc3db0aba9d3947fd6ebdaeecaa1`.

The retained bundle's 16-file checksum manifest verified completely. Result analysis is now
active manuscript evidence. No independent cryptography review was completed; the manuscript
retains `independent_validation=false` and treats the source-to-model mappings as project-defined
abstractions rather than independently approved cryptographic mappings.

See `paper/RESULTS_SUMMARY.md` for the post-execution findings and interpretation boundaries.

## Findings at a glance

- The four defensibly matched treatment families showed categorical parity on their
  pre-authorized fields; the retained data do not support a T1 superiority claim over the
  abstract baselines.
- Across 31 deterministic T1 fault-kind/phase cells, 25 terminated `SUCCESS`, four
  `INDETERMINATE`, one `EXPIRED`, and one `SECURE_DEGRADED`.
- Missing post-convergence command/status evidence was conservatively classified
  `INDETERMINATE` rather than `SUCCESS`.
- Endpoint restart around activation/confirmation was the clearest observed T1 failure boundary.
- In the fixed 12-schedule sensitivity challenge set, three transmission opportunities produced
  11/12 verified completions versus 5/12 with two; a fourth opportunity added no observed
  benefit in that set.
- The fixed 100-schedule mixed panel is secondary descriptive evidence. Its schedule definitions
  covered all 31 valid cells, but only 24 cells were reached at runtime; therefore its 74
  successful schedules are not reported as a “74% success rate under faults.”

## Implemented research platform

- **B0:** SDLS EP-style symmetric over-the-air rekeying abstraction.
- **B1:** Triple-KEM/PQNoise-inspired key-update abstraction with explicit activation variants.
- **B2:** strict stateful/ratcheted key-evolution abstraction.
- **T1:** bounded, replay-resistant resynchronization controller.
- Deterministic baseline/T1 scenario catalogs.
- Seeded and explicit fault injection with structured recovery metrics.
- Conservative matched-family comparability rules.
- Reproducible capture, lineage, checksum, and manifest tooling.
- Bounded TLA+ execution and Python/formal cross-validation.

## Evidence navigation

- `PROJECT_STATUS.md` — current project state and remaining work.
- `paper/RESULTS_SUMMARY.md` — retained-run findings and limitations.
- `paper/EVIDENCE_MAP.md` — manuscript-to-evidence mapping.
- `paper/EXPERIMENT_EXECUTION_PLAN.md` — intentionally preserved pre-run plan.
- `paper/RESEARCH_COMPLETION_MAP.md` — work completed versus remaining.
- `paper/manuscript/outline.md` — current manuscript structure.
- `paper/tables/` and `paper/figures/` — tracked, reproducible result-source data.

Generated raw final outputs remain ignored by Git; the immutable retained bundle is identified
by the run and SHA-256 above.

## Historical provenance policy

Phase-numbered documents, specifications, governance records, trackers, and historical
experiment configs are preserved as versioned evidence. They may contain statuses such as
`PROVISIONAL`, `CANDIDATE_NOT_FROZEN`, or `NOT_YET_AUTHORIZED` that were correct when those
artifacts were created. They are not rewritten after the fact to look current.

Current project state is defined by this README, `PROJECT_STATUS.md`, and the `paper/` workspace.

## Quick validation

```bash
PYTHONWARNINGS="error::ResourceWarning" PYTHONPATH=src \
python3 -m unittest discover -s tests -p "test_*.py" -v

python3 experiments/scripts/validate_repository_manifest.py

PYTHONWARNINGS="error::ResourceWarning" PYTHONPATH=src \
python3 experiments/scripts/run_paper_final_experiment.py --validate-only
```

## Claim boundaries

This repository does not claim flight readiness, CCSDS/SDLS conformance, cryptographic proof,
strong post-compromise security, protection after trust-anchor compromise, availability against
indefinite suppression, causal superiority, real-world fault prevalence, or applicability to
every satellite mission.

Cross-treatment conclusions remain inside explicitly matched families and allowed fields.
T1-specific duration, retry, and transmission metrics are not treated as equivalent
cross-treatment measurements.
