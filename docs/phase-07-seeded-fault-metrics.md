# Phase 07 Seeded Fault Scheduling and Recovery Metrics

## Status

`PROVISIONAL_INTERNAL_REVIEW_ONLY`

Phase 07 is an internal experiment-development layer over the provisional T1 controller. It does not freeze experiment parameters, select the final treatment, implement cryptographic primitives, establish CCSDS or SDLS conformance, or support an external post-compromise-security claim.

## Purpose

The phase makes fault experiments reproducible and auditable by separating three artifacts:

1. The integer seed used to generate a candidate schedule.
2. The fully serialized ordered fault schedule.
3. The SHA-256 identity of that serialized schedule.

The serialized schedule, not the seed alone, is the authoritative replay artifact. This prevents changes in generator implementation from silently changing the meaning of a previously reported seed.

## Fault model

The experiment layer currently supports:

- `DROP`
- `DELAY`
- `DUPLICATE`
- `REORDER`
- `CONTACT_CLOSE`
- `ENDPOINT_RESTART`
- `STALE_COUNTER`
- `STALE_REPLAY`

Faults can target recovery prepare, response, commit, confirmation, test-command, or status-telemetry phases. Explicit regression schedules are used for stable fault-class tests. Seeded schedules are used for repeatable exploratory combinations.

## Contact-window time

Duration is measured in discrete contact windows. No wall-clock interpretation is implied. A delay or contact closure advances the modeled contact counter and records whether the endpoints were divergent or degraded during that interval.

## Metrics

The result record reports security and availability separately. It includes:

- outcome and endpoint alignment;
- provisional security state;
- availability state;
- recovery duration in contact windows;
- divergent and degraded contact windows;
- total message transmissions and retry overhead;
- fault counts by type;
- protocol rejection counts;
- replay and stale-state rejection counts;
- test-command acceptance;
- telemetry-evidence completion;
- verification completion; and
- active-key compromise status in the abstract model.

No composite score is calculated.

## Result files

The runner writes:

- a JSON record containing configuration, full schedules, metrics, and event logs; and
- a flat CSV metric table for statistical and graphical analysis.

Default provisional paths are:

- `results/raw/phase-07-seeded-results.json`
- `results/processed/phase-07-seeded-metrics.csv`

Generated results are not committed as frozen evidence during this phase.

## Reproduction

Run the provisional seed set:

```bash
PYTHONPATH=src python3 experiments/scripts/run_seeded_fault_experiments.py
```

Use alternate output paths:

```bash
PYTHONPATH=src python3 experiments/scripts/run_seeded_fault_experiments.py \
  --json-output /tmp/phase07-results.json \
  --csv-output /tmp/phase07-metrics.csv
```

Validate the design package:

```bash
python3 experiments/scripts/validate_phase07_seeded_metrics.py
```

## Unfrozen parameters

The seed set, retry budget, candidate lifetime, initial epoch relationship, authority epoch floor, fault-count limit, fault selection, delay duration, contact model, passive interval, success thresholds, and statistical plan remain provisional.

## Mandatory review boundary

Independent cryptography review becomes mandatory before any experiment parameter or seed set is frozen, before T1 is selected as the final treatment, before results are interpreted as post-compromise-security evidence, before concrete cryptography or conformance work, before NOS3/cFS evidence is used for publication, and before manuscript submission or any external security claim.
