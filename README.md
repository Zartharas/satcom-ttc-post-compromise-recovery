# SATCOM TT&C Post-Compromise Recovery

Hands-on experimental cybersecurity research on restoring trusted satellite telemetry,
tracking, and command (TT&C) communications after operational-key compromise and
ground-space security-state divergence.

## Research objective

Evaluate, within a bounded synthetic software model, how abstract recovery baselines and a
bounded resynchronization treatment behave under matched recovery conditions and controlled
communication faults.

No operational satellites, live TT&C systems, RF links, or flight software are used.

## Current research questions

1. **Matched recovery behavior:** How do B0, B1, B2, and T1 differ in terminal security,
   availability, alignment, and verification outcomes under defensibly matched conditions?
2. **T1 fault robustness:** How does T1 behave under loss, delay, duplication, reordering,
   contact interruption, endpoint restart, stale counter, and replay faults?
3. **T1 sensitivity:** How sensitive is T1 behavior to retry budget and candidate-retention
   lifetime?
4. **Assurance:** Where do bounded TLA+ witnesses and Python executions agree or differ under
   the declared projection?

## Implemented platform

- **B0:** SDLS EP-style symmetric over-the-air rekeying abstraction.
- **B1:** Triple-KEM/PQNoise-inspired key-update abstraction with explicit activation variants.
- **B2:** strict stateful/ratcheted key-evolution abstraction.
- **T1:** bounded, replay-resistant resynchronization controller.
- Deterministic baseline/T1 scenario catalogs.
- Seeded and explicit fault injection with structured recovery metrics.
- Conservative matched-family comparability rules.
- Reproducible capture, lineage, checksum, and manifest tooling.
- Bounded TLA+ execution and Python/formal cross-validation.

## Paper-completion state

The engineering and reproducibility foundation is substantially complete. Active work is now:

- final experiment design and retained execution;
- results analysis;
- manuscript preparation; and
- reproducible research release.

The exact WP15-D4 reviewed observation cutoffs, treatment-within-family analysis units, member
registry, and allowed planning-display registry remain frozen and are not modified by the paper
restructuring branch.

The final publication analysis plan and final dataset are not yet frozen or executed.
Independent cryptography review remains open as a parallel validation activity. Until it is
complete, the repository does not claim independent approval of the baseline mappings or
cryptographic/post-compromise security.

See:

- `PROJECT_STATUS.md`
- `paper/RESEARCH_COMPLETION_MAP.md`
- `paper/EXPERIMENT_EXECUTION_PLAN.md`
- `paper/EVIDENCE_MAP.md`
- `paper/manuscript/outline.md`

## Quick validation

```bash
PYTHONWARNINGS="error::ResourceWarning" PYTHONPATH=src \
python3 -m unittest discover -s tests -p "test_*.py" -v

python3 experiments/scripts/validate_repository_manifest.py
python3 experiments/scripts/validate_phase15_protocol.py
python3 experiments/scripts/validate_phase15_treatment_comparability.py
python3 experiments/scripts/validate_phase15_matched_family_population.py
python3 experiments/scripts/validate_phase15_family_descriptive_plan.py
```

## Claim boundaries

This repository does not claim flight readiness, CCSDS/SDLS conformance, cryptographic proof,
strong PCS, protection after trust-anchor compromise, availability against indefinite
suppression, causal superiority, or applicability to every satellite mission.

Cross-treatment conclusions must remain inside explicitly matched families and allowed fields.
T1 latency, retries, and transmissions are analyzed as T1 behavior unless an equivalent
cross-treatment measurement basis is established.
