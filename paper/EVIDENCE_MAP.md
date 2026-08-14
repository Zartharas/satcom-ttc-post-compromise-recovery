# Paper Evidence Map

## Purpose

Map manuscript content to the smallest relevant evidence source so historical governance does
not dominate the paper and every result remains traceable.

| Manuscript content | Primary evidence | Current state |
|---|---|---|
| System/threat model | `spec/system-model.json`, `spec/security-invariants.json`, architecture/threat docs | Ready |
| B0/B1/B2 design | baseline decision/spec/catalog and primary source notes | Ready internally; independent review open |
| T1 design | T1 design docs/spec/controller | Ready |
| Fault model/metrics | `src/ttc_recovery/fault_metrics.py` and final plan | Ready |
| Matched comparison boundary | D2 matrix/documentation | Ready |
| Matched population | D3 config/runner/validator | Ready |
| Predeclared cutoffs/units | D4 plan + decision/review records | Frozen exact objects |
| Final plan | `experiments/configs/paper-final-experiment.json` | Committed before outcome execution |
| Final runner | `experiments/scripts/run_paper_final_experiment.py` | Committed/validated |
| Final execution identity | retained run `20260814T022506Z-gc630fb4` | Completed; 16/16 bundle files verified |
| Matched outcomes | `paper/tables/table-1-matched-family-outcomes.csv` | Retained/analyzed |
| Deterministic T1 outcomes | `paper/tables/table-2-deterministic-t1.csv` | Retained/analyzed |
| Study B grouped interpretation | `paper/tables/study-b-fault-response-summary.csv` | Derived from retained run |
| Study C outcome population | `paper/tables/study-c-outcome-summary.csv` | Retained/analyzed |
| Study C reachability limitation | `paper/tables/study-c-execution-coverage-audit.csv` | Post-execution diagnostic audit |
| Sensitivity | `paper/tables/study-d-sensitivity-summary.csv` | Retained/analyzed |
| Figure 2 source | `paper/figures/figure-2-outcome-distribution-source.csv` | Retained source data |
| Figure 3 source | `paper/figures/figure-3-sensitivity-source.csv` | Retained source data |
| Formal assurance | `formal/`, Phase 10-13 artifacts | Supporting bounded evidence |
| Independent-review statement | Issue #3 + Phase 14 package | Open |
| Reproducibility | final config, execution commit, retained manifest, bundle SHA-256 | Ready; public release pending |

## Evidence hierarchy

1. Retained final experiment outputs and tracked derivatives for Results.
2. Predeclared/frozen contracts for Methods and comparison boundaries.
3. Executable source/tests/validators for implementation and reproducibility.
4. Formal evidence for bounded assurance statements.
5. Historical trackers only for provenance or review-status limitations.

Do not use tracker status text as a substitute for retained experiment output.

## Required limitations

The manuscript must state:

- synthetic software-only experiment;
- abstract cryptographic operations;
- baseline source-to-model mapping not independently approved until Issue #3 closes;
- finite/bounded formal models;
- non-equivalent cross-treatment timing/retry semantics;
- no CCSDS/SDLS conformance;
- no RF/flight/operational-spacecraft validation;
- generated schedules do not estimate real-world fault prevalence;
- Study C schedule definitions and runtime-applied fault coverage differ because later-attempt
  actions may be unreachable; and
- no strong PCS, causal-superiority, or universal treatment-ranking claim.

## Manuscript-number rule

Every final number, count, percentage, or plotted value must map to tracked table/figure source
data or the immutable retained bundle and an exact derivation command/script. Manual
transcription without lineage is not acceptable.
