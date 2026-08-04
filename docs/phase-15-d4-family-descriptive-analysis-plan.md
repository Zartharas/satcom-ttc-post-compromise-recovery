# Phase 15 Family-Level Descriptive-Analysis Plan Candidate

## Status

`PREDECLARED_FAMILY_ANALYSIS_PLAN_CANDIDATE_PENDING_VALIDATION_NOT_ANALYSIS_EVIDENCE`

WP15-D4 defines a candidate analysis boundary before any family-level comparative display is authorized. It fixes candidate observation cutoffs, member identity, analysis-unit identity, denominator membership, allowed field names, and revision controls. It does not calculate or present outcomes, counts, rates, percentages, pooled summaries, statistical tests, rankings, or conclusions.

Machine-readable contract:

`experiments/configs/phase-15-family-descriptive-plan.json`

Executable generator:

`experiments/scripts/run_phase15_family_descriptive_plan.py`

## Purpose

D2 identified conservative comparison families. D3 made the qualified-family population executable. D3B retained those inputs and outputs in an immutable bundle. D4 addresses the next reproducibility risk: changing observation boundaries, denominator membership, or display rules after seeing results.

The current output is a **freeze candidate**, not a frozen publication plan. Local and CI validation are still required, and a later explicit authorization is required before any family member values are displayed side by side.

## Outcome-blind generation

The D4 generator validates only:

- family and member identifiers;
- source identifiers and roles;
- analysis-unit identifiers;
- family-authorized field names;
- source-execution SHA-256 values for provenance;
- coverage counts; and
- closed authorization flags.

It does not read:

- `projected_metrics` values;
- raw execution values;
- outcome labels;
- security or availability values;
- fault or rejection values; or
- any value that could influence selection, filtering, cutoff extension, or denominator revision.

A focused mutation test replaces all projected values and requires the complete D4 identity and freeze plan to remain byte-equivalent at the structured-object level.

## Candidate population

| Family | Member rows | Analysis units | Candidate denominator unit |
|---|---:|---:|---|
| CF-01 | 4 | 4 | Treatment within CF-01 |
| CF-02 | 5 | 4 | Treatment within CF-02 |
| CF-05 | 2 | 2 | Treatment within CF-05 |
| CF-06 | 2 | 2 | Treatment within CF-06 |
| **Total** | **13** | **12** | No cross-family denominator |

Member rows are traceability records, not denominator units. CF-02 retains B1-01 and B1-05 as separate policy-variant rows under one `CF-02:B1` analysis unit.

## Candidate observation cutoffs

### CF-01 — Passive operational-key compromise recovery

Cutoff ID: `OC-CF01-TERMINAL-ORACLE`

Stop after the source executor reaches its declared terminal state and the retained internal oracle check completes. No post-terminal message or additional recovery attempt is permitted.

### CF-02 — No-fault state transition

Cutoff ID: `OC-CF02-NO-FAULT-COMPLETION`

Stop after the exact no-fault source transaction reaches its declared terminal state and oracle validation completes. Both B1 variants remain separate rows but share one B1 analysis unit. Neither execution may be extended after its result is known.

### CF-05 — Post-convergence status telemetry loss

Cutoff ID: `OC-CF05-STATUS-OPPORTUNITY`

Stop immediately after the declared post-convergence status-telemetry opportunity is processed and the source terminal classification is recorded. Do not add a replacement telemetry opportunity or extend recovery after status loss.

### CF-06 — Replay after success

Cutoff ID: `OC-CF06-SINGLE-REPLAY`

Stop after successful state advancement and exactly one declared replay attempt is evaluated. The retained rejection and unchanged-state checks must complete. No additional replay, retry, or recovery action is permitted.

## Global observation rules

- Start from the exact retained D3 initial state and execution recipe.
- Retain one deterministic source execution for every declared member row.
- Require the existing internal oracle check before registry admission.
- Do not add contacts, retries, replay attempts, telemetry opportunities, or post-terminal actions after observing a result.
- Do not exclude, merge, relabel, or duplicate a valid member because of its result.
- Technical reruns require a new run record and may not silently replace a valid unfavorable execution.

## Denominator freeze candidate

For each family, the candidate denominator is the exact set of treatment-within-family `analysis_unit_id` values declared before any aggregate display.

Rules:

- missing unit: mark family coverage incomplete and block the family display;
- extra unit: reject the undeclared unit;
- member-row count: traceability only;
- policy variants: do not create independent denominator units;
- success-rate denominator: `NOT_DEFINED`;
- cross-family denominator: `NOT_PERMITTED`;
- aggregate authorization: `false`;
- freeze state: `CANDIDATE_NOT_FROZEN`.

A denominator may not shrink or expand after results are known.

## Candidate display registry

D4 permits generation of planning and identity artifacts only:

- member identity and provenance registry;
- analysis-unit membership registry;
- family observation-cutoff table;
- family allowed-field-name table; and
- family coverage-completeness table.

A future side-by-side member-value table requires separate authorization after D4 validation. D4 itself does not emit that table.

## Prohibited outputs

D4 cannot emit:

- outcome-frequency tables;
- success counts or percentages;
- treatment-level rates;
- pooled family scores;
- cross-family aggregates;
- confidence intervals;
- hypothesis tests;
- effect estimates;
- treatment rankings; or
- superiority, effectiveness, causal, cryptographic-security, or publication conclusions.

## Revision control

Before any future comparative output is viewed, a change requires a new versioned commit, rationale, validator update, and regenerated freeze candidate.

After any comparative output is viewed, a change must be marked post-observation. The superseded plan and outputs must be preserved, a new run must be created, and results cannot be combined unless a later protocol explicitly authorizes a stratified analysis.

Outcome-seeking revision is prohibited.

## Generated artifacts

The runner writes:

- `phase-15-family-descriptive-plan-candidate.json`;
- `phase-15-family-member-registry.csv`;
- `phase-15-family-analysis-units.csv`;
- `phase-15-family-observation-plans.csv`; and
- `phase-15-family-descriptive-plan.sha256`.

The member registry intentionally contains no outcome column and no serialized projected-metric values. The manifest must cover exactly the four data artifacts and must detect missing, altered, or duplicated paths.

## Interpretation boundary

D4 improves reproducibility by predeclaring what would be observed and counted. It does not prove that the treatments are equivalent, fair, secure, effective, operationally representative, or suitable for statistical inference.

Family-specific descriptive comparison remains:

`NOT_YET_AUTHORIZED`

Publication evidence remains:

`false`
