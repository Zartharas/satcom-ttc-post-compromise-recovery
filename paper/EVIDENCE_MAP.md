# Paper Evidence Map

## Purpose

Map manuscript content to the smallest relevant repository evidence so historical governance
does not dominate the paper.

| Manuscript content | Primary evidence | State |
|---|---|---|
| System/threat model | `spec/system-model.json`, `spec/security-invariants.json`, architecture docs | Ready |
| B0/B1/B2 design | baseline decision/spec/catalog | Ready internally; external review open |
| T1 design | T1 design docs/spec/controller | Ready |
| Fault model/metrics | `src/ttc_recovery/fault_metrics.py`, Phase 07 artifacts | Ready |
| Matched comparison | D2 matrix/documentation | Ready |
| Matched population | D3 config/runner/validator | Ready |
| Predeclared cutoffs/units | D4 plan + decision/review records | Frozen exact objects |
| Capture/provenance | Phase 15 capture controls/wrapper/manifests | Ready |
| Formal assurance | `formal/`, Phase 10-13 artifacts | Supporting evidence ready |
| Matched outcomes | Final Study A bundle | Pending |
| Deterministic fault coverage | Final Study B bundle | Pending |
| Mixed-fault robustness | Final Study C bundle | Pending |
| Sensitivity | Final Study D bundle | Pending |
| Tables/figures | `paper/tables/`, `paper/figures/` + source data | Pending |
| Review limitation | Issue #3 + Phase 14 package | Open |
| Reproducibility statement | final config/commit/manifests/release | Pending |

## Evidence hierarchy

1. Final retained experiment outputs for Results.
2. Frozen/predeclared contracts for Methods and comparison boundaries.
3. Executable source/tests/validators for implementation/reproducibility.
4. Formal evidence for bounded assurance statements.
5. Historical trackers only for provenance or review-status limitations.

Do not use tracker status text as a substitute for experiment output.

## Required limitations

The manuscript must state:

- synthetic software-only experiment;
- abstract cryptographic operations;
- baseline source-to-model mapping not independently approved until Issue #3 closes;
- finite/bounded formal models;
- non-equivalent cross-treatment timing/retry semantics;
- no CCSDS/SDLS conformance;
- no RF/flight/operational-spacecraft validation;
- generated faults do not estimate real-world prevalence; and
- no strong PCS or causal-superiority claim.

## Manuscript-number rule

Every final number, count, percentage, or plotted value must map to retained table/figure source
data and an exact generation script/command. Manual transcription without lineage is not
acceptable.
