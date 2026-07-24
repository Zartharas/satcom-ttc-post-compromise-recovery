# Phase 13 — Explicit abstraction-gap outcome modeling

## Purpose

Phase 13 examines the three outcomes that Phase 12 reported as absent from the original TLA+ transition
relation: `DIVERGED`, `AVAILABLE_UNSAFE`, and `LOCKED`.

The phase preserves `formal/tla/T1Recovery.tla` byte-for-byte as the Phase 12 baseline. New paths exist only
in the opt-in module `formal/tla/T1RecoveryOutcomeExpansion.tla`, which extends the baseline with one
expansion-only cause variable and three explicit diagnostic outcome transitions.

This structure prevents an expanded diagnostic model from silently replacing the model whose bounded
absence results were already recorded.

## Preserved baseline

The runner requires the original module to retain SHA-256:

```text
c2a97fa0eb93b7b84a2109be67d673a0199b82e52b8baf67f16d5b137e0da754
```

For each of the three Phase 12 absence configurations, the first successful Phase 13 CI run reproduced:

```text
50 generated states
28 distinct states
0 queued states
search depth 10
NO_COUNTEREXAMPLE_WITHIN_RECORDED_BOUND
0 outcome assignments in T1Recovery.tla
```

The baseline status is therefore `BASELINE_PRESERVED`. This does not convert the Phase 12 bounded absence
result into an impossibility claim.

## Opt-in expansion

The expansion adds `gapCause` with the provisional values:

- `NONE`
- `CONFIRM_LOSS`
- `CANDIDATE_KNOWN`
- `SENDER_STATE_DELETED`

The new outcome paths are:

### DIVERGED

```text
Init
PrepareExpanded
SelectCandidateExpanded
DivergeOnConfirmLoss
```

The ground side activates the candidate after confirmation loss while the spacecraft candidate expires.
The diagnostic path ends with unequal epochs and no terminal lock classification.

The Python replay uses existing simulator endpoint staging, activation, and expiration behavior. Its final
outcome is also checked against the existing B1 local-completion confirmation-loss scenario.

### AVAILABLE_UNSAFE

```text
Init
PrepareExpanded
SelectCandidateExpanded
MarkCandidateKnown
CommitExpanded
ConfirmExpanded
VerifyAvailableUnsafe
```

Both endpoints converge and verification evidence is present, but the candidate is explicitly marked as
known to the adversary. Availability and alignment therefore do not imply the security objective.

The canonical Python check uses the existing B2 receiver-state-exposure scenario.

### LOCKED

```text
Init
PrepareExpanded
SelectCandidateExpanded
MarkSenderStateDeleted
LockAfterSenderAdvance
```

The sender advances after its prior state is explicitly classified as deleted while the receiver remains on
the prior epoch. The path is terminally classified as `LOCKED`, rather than merely divergent.

The canonical Python check uses the existing B2 dropped-update-after-sender-evolution scenario.

## First successful CI result

| Outcome | Witness states | Comparison | Expanded state space |
|---|---:|---:|---:|
| `DIVERGED` | 4 | 68/68 matched | 7 generated, 7 distinct, depth 4 |
| `AVAILABLE_UNSAFE` | 7 | 119/119 matched | 16 generated, 16 distinct, depth 7 |
| `LOCKED` | 5 | 85/85 matched | 10 generated, 10 distinct, depth 5 |

Combined comparison result:

```text
272 comparison rows
272 matched rows
0 mismatches
MATCH_WITHIN_DECLARED_ABSTRACTION
```

For each outcome, the assignment audit records:

```text
baseline assignment count = 0
expanded assignment count = 1
diagnosis = EXPLICITLY_ADDED_IN_OPT_IN_EXPANSION
```

Both the baseline and expanded modules passed SANY parsing. All three expansion configurations produced the
expected testing-only TLC witness, and all three canonical Python baseline checks produced the expected
final outcome.

## Interpretation boundaries

Phase 13 demonstrates only that:

- the Phase 12 model remains unchanged and reproduces its earlier bounded state counts;
- the opt-in expansion contains one explicit path for each previously absent outcome;
- the recorded TLA+ and Python projections agree over the existing 16 fields for those paths; and
- existing B1/B2 simulator semantics independently contain a scenario with the same final outcome.

Phase 13 does not establish:

- completeness of the outcome population, transition relation, cause vocabulary, or witness set;
- realism or likelihood of any expansion path;
- refinement proof or implementation equivalence;
- correctness of the causal labels;
- a concrete cryptographic security property;
- CCSDS or SDLS conformance;
- flight-software, RF, or operational-spacecraft behavior; or
- publication-ready evidence.

The expansion, causes, witnesses, property set, projection, and interpretation all remain provisional and
unfrozen. A future mismatch must be retained as `MISMATCH_REQUIRES_REVIEW` rather than reconciled silently.

## Outputs

The Phase 13 runner produces:

- `phase13-outcome-expansion-validation.json`
- three witness JSON files
- three field-level comparison CSV files
- `phase13-baseline-regression.csv`
- `phase13-expansion-assignment-audit.csv`
- Java and SANY logs
- three baseline TLC logs
- three expanded-witness TLC logs
- `phase13-derived-bundle.sha256`

Generated outputs remain outside Git and require a separate run provenance record before preservation as an
internal evidence bundle.
