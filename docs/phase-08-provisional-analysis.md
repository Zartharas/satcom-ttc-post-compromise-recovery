# Phase 08 Provisional Analysis

## Status

`PROVISIONAL_INTERNAL_REVIEW_ONLY`

Phase 08 analyzes preserved Phase 07 experiment records. It does not alter the Phase 07 evidence directory, freeze an experiment design, perform confirmatory statistics, or establish post-compromise security.

## Evidence handling

The preferred input is a Phase 07 evidence bundle stored outside the Git repository. The bundle must contain:

- `phase07-results.json`
- `phase07-metrics.csv`
- `phase07-run-bundle.sha256`
- the configuration, scenario catalog, and provenance files referenced by that manifest

When `--bundle-dir` is used, the runner verifies every relative-path SHA-256 entry before loading the results. It then cross-checks every metric field in the CSV against the JSON records.

The source directory is read-only. All derived outputs go to a separate Phase 08 directory.

## Run against a preserved bundle

From the repository root:

```bash
DATA_ROOT="/path/to/satcom-ttc-post-compromise-recovery-data"
PHASE07_RUN="$DATA_ROOT/phase-07/<preserved-run-directory>"
PHASE08_RUN="$DATA_ROOT/phase-08/phase-08-provisional-$(date -u +%Y%m%dT%H%M%SZ)"

mkdir -p "$PHASE08_RUN"

PYTHONPATH=src python3 experiments/scripts/analyze_phase07_results.py \
  --bundle-dir "$PHASE07_RUN" \
  --output-dir "$PHASE08_RUN"
```

The runner records the SHA-256 of the Phase 07 JSON source in the derived analysis JSON. Bundle and CSV verification metadata are also retained.

## Derived outputs

Phase 08 produces:

- `phase08-analysis.json` — complete machine-readable analysis record
- `phase08-annotated-results.csv` — one row per Phase 07 schedule
- `phase08-overall-summary.csv`
- `phase08-outcome-summary.csv`
- `phase08-fault-kind-summary.csv`
- `phase08-fault-phase-summary.csv`
- `phase08-fault-count-summary.csv`
- `phase08-security-availability.csv`
- `phase08-coverage-audit.csv`
- `phase08-trace-anomalies.csv`
- `phase08-adverse-cases.csv`
- `phase08-sensitivity-rows.csv`
- `phase08-sensitivity-summary.csv`
- `phase08-derived-bundle.sha256`

Verify the derived files with:

```bash
(
  cd "$PHASE08_RUN" &&
  shasum -a 256 -c phase08-derived-bundle.sha256
)
```

## Aggregation rules

Every summary reports its denominator `n`.

Outcome and fault-count groups are mutually exclusive. Fault-kind and fault-phase groups overlap because a schedule can contain several kinds and phases. Those summaries explicitly declare overlapping membership and must not be added together as though they partition the source population.

Groups below the provisional minimum size remain visible and are marked `LOW_N_DESCRIPTIVE_ONLY`. They are not silently removed.

The reported success fraction is a descriptive proportion only. It is not a probability estimate, confidence statement, or treatment-effectiveness result.

## Trace audit

Each source record is checked for:

- serialized schedule SHA-256 consistency
- seed consistency between configuration and metrics
- total and per-kind fault-count consistency
- contiguous append-only event sequence numbers
- recovery-duration and retry-overhead consistency
- agreement among outcome, alignment, verification, security, availability, and compromise fields

A clean trace-anomaly file contains a single `NO_ROWS` marker. Any anomaly must be resolved or explicitly dispositioned before using the derived bundle for later analysis.

## Diagnostic labels

Non-success records receive an event-derived diagnostic label, such as status-evidence loss, confirmation-path exhaustion, or pre-activation delivery exhaustion.

These labels are marked `DESCRIPTIVE_NOT_CAUSAL`. They organize recorded traces but do not prove which fault caused an outcome when several faults occur in the same schedule.

## Sensitivity scaffold

The initial grid varies:

- `max_transmissions`: 2, 3, 4
- `candidate_lifetime_contacts`: 2, 3, 4

Every grid point reuses the exact serialized Phase 07 schedule. No new random fault schedule is generated during sensitivity analysis. If a reduced transmission budget makes a scheduled later-attempt fault unreachable, the row records that count explicitly.

The grid is unfrozen. Its outputs are descriptive and cannot be used as an optimization result or final parameter recommendation.

## Mandatory review stop point

Independent review becomes mandatory before:

- freezing the experiment population or seed set
- freezing retry budgets or candidate lifetimes
- adopting denominator exclusions or success thresholds
- defining or freezing the statistical analysis plan
- selecting T1 as the final treatment
- interpreting simulation output as post-compromise-security evidence
- using results as publication evidence or making external security claims
