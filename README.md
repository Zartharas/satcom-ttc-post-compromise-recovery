# SATCOM TT&C Post-Compromise Recovery

Research repository for an experimental cybersecurity journal article on restoring trusted
satellite telemetry, tracking, and command (TT&C) communications after cryptographic key
compromise and ground-space security-state divergence.

## Working research question

> Under TT&C key compromise and ground-space state divergence, which recovery approach
> most reliably restores authenticated communication while excluding compromised key
> states and avoiding permanent lockout?

## Current status

Version 0.1.1 contains the Phase One novelty framing, Phase Two system and threat model,
machine-readable specifications, B0-B2 baseline scenarios, a deterministic simulator scaffold,
and placeholders for experiments, results, integrations, manuscript work, references,
governance, and releases.

## Baselines

- **B0:** SDLS EP-style symmetric over-the-air rekeying
- **B1:** Triple-KEM/PQNoise-style key update with key confirmation
- **B2:** strict stateful authenticated or ratcheted key-evolution family

## Proposed treatment

- **T1:** bounded, replay-resistant resynchronization controller

T1 remains requirements-only. This repository does not implement a novel cryptographic
primitive or claim formal post-compromise security.

## Quick start

```bash
PYTHONPATH=src python -m unittest -v
PYTHONPATH=src python src/ttc_recovery/simulator.py
```

## Repository map

- `docs/` — research and architecture documentation
- `spec/` — machine-readable model and requirements
- `src/` — simulator source
- `tests/` — test code and scenario catalog
- `experiments/` — reproducible experiment configurations
- `results/` — generated outputs
- `integrations/` — later NOS3 and cFS integration
- `paper/` — manuscript, figures, tables, and submission materials
- `references/` — bibliography and source-review notes
- `governance/` — legal, ethical, data, and disclosure controls
- `artifacts/` — versioned releases and integrity manifests

## Non-claims

This repository does not claim flight readiness, CCSDS conformance, formal strong
post-compromise security, protection after onboard trust-anchor compromise, availability
against indefinite message suppression, or applicability to every satellite mission.
