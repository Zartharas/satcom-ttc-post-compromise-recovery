# Research Engineering Issues and Responsible Disclosure Tracker

**Branch:** `phase-15/publication-preparation`  
**Last updated:** 2026-08-04  
**Status:** `ACTIVE`

## Purpose

This register tracks implementation defects, scientific-validity gaps, reproducibility problems, governance issues, upstream opportunities, and potential security findings. It separates observed evidence from inference and prevents ordinary software defects from being overstated as vulnerabilities.

## Scope and authorization

Allowed work is limited to this repository, synthetic inputs, bounded formal models, controlled local execution, documented open-source contribution paths, and authorized systems.

Prohibited work includes testing operational spacecraft, ground stations, RF links, or third-party infrastructure without written authorization; accessing private data or credentials; publishing exploit details before coordinated disclosure; or claiming external recognition before formal acknowledgment.

## Classification

| Type | Meaning |
|---|---|
| `DEFECT` | Incorrect implementation, test, or documentation behavior |
| `REPRODUCIBILITY` | Missing provenance, determinism, checksum, or comparable-measurement control |
| `GOVERNANCE` | Consent, disclosure, review, claim, or process problem |
| `UPSTREAM_BUG` | Reproduced defect in an external dependency or tool |
| `SECURITY_CANDIDATE` | Plausible security impact requiring private validation |
| `SECURITY_CONFIRMED` | Reproduced security impact accepted for coordinated disclosure |
| `ENHANCEMENT` | Improvement that is not a defect |
| `FALSE_POSITIVE` | Investigated concern with no reproducible issue |

## Status workflow

`NEW` → `TRIAGED` → `REPRODUCED` → `FIX_IN_PROGRESS` → `FIXED_PENDING_VALIDATION` → `CLOSED`

Security candidates use a private coordinated-disclosure workflow.

## Current issue register

| ID | Type | Severity | Status | Phase | Summary | Current disposition |
|---|---|---|---|---|---|---|
| RIT-001 | GOVERNANCE | MEDIUM | FIXED_PENDING_VALIDATION | 4–14 | Historical Phase 05 response template omitted endpoint-knowledge question `B1-R5`. | Phase 14 restores the question without rewriting historical evidence; external disposition remains pending. |
| RIT-002 | GOVERNANCE | HIGH | OPEN | 6–15 | Provisional Phases 6–13 proceeded after an earlier gate stated T1 was blocked pending review. | Work remains provisional; a future reviewer must determine retrospective revalidation scope. |
| RIT-003 | GOVERNANCE | MEDIUM | FIXED_PENDING_VALIDATION | 4–14 | “Corrected and locked” could be misread as independent approval. | Phase 14 separates implementation lock, approval, oracle freeze, and publication permission. |
| RIT-004 | REPRODUCIBILITY | MEDIUM | FIXED_PENDING_VALIDATION | 5–14 | Earlier handoff records referenced older review-target commits. | Exact Phase 14 commit pinning and evidence-index rules added. |
| RIT-005 | REPRODUCIBILITY | LOW | CLOSED | 13 | Checksum verification was initially attempted before the derived bundle existed. | Execution order corrected and final manifests verified. |
| RIT-006 | DEFECT | LOW | TRIAGED | 14 | A GitHub `/tree/<commit>` link may appear as a landing view and confuse reviewers. | Use immutable commit and direct blob links. |
| RIT-007 | GOVERNANCE | HIGH | FIXED_PENDING_VALIDATION | 14 | Prospective reviewer names were published before consent. | Names removed; Issue #3 now prohibits implied participation or public identity without permission. |
| RIT-008 | GOVERNANCE | HIGH | OPEN | 14–15 | AI assistance was not clearly disclosed in the initial review request. | Future outreach and publication materials require context-appropriate disclosure after venue selection. |
| RIT-009 | ENHANCEMENT | MEDIUM | FIXED_PENDING_VALIDATION | 15 | Project lacked a consolidated publication-readiness tracker. | Tracker now covers protocol, parity, comparability, capture, manuscript, and claim gates. |
| RIT-010 | ENHANCEMENT | MEDIUM | FIXED_PENDING_VALIDATION | 15 | Project lacked a consolidated issue/disclosure register. | This register establishes the workflow; final branch validation remains pending. |
| RIT-011 | REPRODUCIBILITY | HIGH | FIXED_PENDING_CI | 15 | B0/B1/B2 lacked shared T1 metrics and equivalent capture artifacts. | D1 passed local validation with 199 tests, 21 retained scenarios, JSON/CSV checks, immutable capture, and manifests. CI pending. |
| RIT-012 | REPRODUCIBILITY | HIGH | FIXED_PENDING_CI | 15 | Seeded execution lacked a complete immutable Phase 15 run directory. | Wrapper passed local D1 validation for raw, analysis, governance, logs, and layered manifests. CI pending. |
| RIT-013 | REPRODUCIBILITY | HIGH | FIXED_PENDING_CI | 15 | Shared fields did not identify semantically comparable baseline/T1 cases. | D2 passed local validation with eight conservative families, 36 unique dispositions, restricted fields, and no pooled catalog percentages. CI pending. |
| RIT-014 | REPRODUCIBILITY | HIGH | FIXED_PENDING_CI | 15 | A semantic matrix did not provide an executable qualified-family population with controlled analysis units and denominators. | D3 passed local validation with four qualified families, 13 member rows, 12 analysis units, strict projections, and an internal derived manifest. CI pending. |
| RIT-015 | DEFECT | LOW | FIXED_PENDING_CI | 15 | A D2 test searched for a noncontiguous phrase despite a correct matrix rule. | Assertion corrected; focused and complete local suites passed. CI pending. |
| RIT-016 | REPRODUCIBILITY | HIGH | FIXED_PENDING_CI | 15 | Standalone D3 outputs were not retained with exact D2/D3 inputs inside the immutable pilot bundle. | D3B passed integrated local validation with retained D2/D3 contracts and catalogs, metadata schema 0.2.0, fail-closed semantic checks, and four verified manifest layers. CI pending. |
| RIT-017 | REPRODUCIBILITY | HIGH | FIXED_PENDING_VALIDATION | 15 | The qualified-family population lacked predeclared observation cutoffs, denominator membership, allowed-display boundaries, and post-observation revision controls. | D4 implements an outcome-blind freeze candidate for 4 families, 13 member rows, 12 treatment-within-family units, and 4 explicit cutoffs. Local validation, CI, and a separate freeze decision remain pending. |
| RIT-018 | DEFECT | HIGH | FIXED_PENDING_VALIDATION | 15 | The initial D4 configuration widened four family `expected_allowed_fields` lists beyond the authoritative D2 matrix. | D4 was corrected at `968af687` to use the exact D2 field membership and order. The strict builder correctly prevented output generation; focused, full-suite, bundle, and manifest revalidation remain pending. |

## WP15-D4 evidence paths

- `experiments/configs/phase-15-family-descriptive-plan.json`
- `docs/phase-15-d4-family-descriptive-analysis-plan.md`
- `src/ttc_recovery/family_descriptive_plan.py`
- `experiments/scripts/run_phase15_family_descriptive_plan.py`
- `experiments/scripts/validate_phase15_family_descriptive_plan.py`
- `tests/test_phase15_family_descriptive_plan.py`
- `tracker/WP15_D4_FREEZE_CANDIDATE_TRACKER.md`
- `.github/workflows/phase15-comparability.yml`

## WP15-D4 defect record

The first local D4 execution failed before producing a bundle with:

```text
ValueError: Allowed-field order drifted for CF-01
```

The failure exposed an over-broad D4 configuration rather than a D2 matrix defect. The initial D4 lists added fields that the authoritative D2 families did not authorize:

- CF-01 added `verification_complete`;
- CF-02 added `command_accepted` and `telemetry_complete`;
- CF-05 added `fault_count`; and
- CF-06 added `security_state`.

The fix removes those additions and preserves the D2 matrix as the exact source of allowed-field membership and order. The builder remains fail-closed. No D4 output bundle or comparative result was generated before the correction.

## D4 acceptance conditions

RIT-017 and RIT-018 cannot close because corrected files exist. Validation requires evidence that:

- the exact qualified family order remains CF-01, CF-02, CF-05, and CF-06;
- the member registry contains 13 unique rows;
- the candidate denominator registry contains 12 unique treatment-within-family units;
- CF-02 B1-01 and B1-05 remain separate rows under one `CF-02:B1` unit;
- all 4 observation cutoffs are explicit, unique, terminal, and non-adaptive;
- family allowed-field names exactly match the D2 matrix in membership and order;
- projected metric and raw execution values are not read;
- changing projected values cannot change the D4 identity contract;
- the member registry exposes no outcome or projected-value column;
- missing units block a family display rather than shrinking the denominator;
- undeclared units are rejected rather than expanding the denominator;
- success-rate denominators remain undefined;
- comparison, aggregation, inference, superiority, causal, cryptographic, and publication gates remain closed;
- the D4 output manifest covers exactly the four data artifacts and detects tampering; and
- local and CI validation pass at exact commits.

A successful D4 engineering validation does not itself freeze the candidate. Freeze requires a separate explicit decision before any comparative display is viewed.

## Reproducibility rules

A parity or comparability issue is not closed because files share column names.

Closure requires evidence appropriate to the issue:

- metric-field parity requires identical declared fields and successful JSON/CSV generation;
- capture parity requires provenance, logs, exclusion/rerun handling, and checksums;
- scenario parity requires matched inputs or predeclared exceptions;
- semantic parity requires compatible meanings, not only compatible types;
- executable comparability requires predeclared family membership and observation controls;
- immutable integration requires retained inputs, metadata, fail-closed validation, and layered manifests;
- analysis-plan reproducibility requires outcome-blind cutoffs, fixed candidate units, allowed-display rules, and post-observation revision controls; and
- publication readiness requires a separately reviewed and frozen population and analysis plan before comparative interpretation.

## Triage rules

1. Reproduce from a clean state.
2. Preserve raw logs before modifying behavior.
3. Separate facts from hypotheses.
4. Classify impact as functional, scientific, security, governance, or cosmetic.
5. Confirm authorization before testing outside this repository.
6. Add a regression test before calling a code defect fixed.
7. Record exact validating commits and CI runs.
8. Do not close a scientific-validity issue on intention alone.

## Security-candidate decision test

A concern remains a candidate unless the record identifies the protected property, attacker capability, affected supported version, reproducibility, trust-boundary crossing, nontrivial impact, authorization basis, and private disclosure route.

Absent those elements, classify it as a defect, reproducibility issue, enhancement, or false positive.

## New issue template

```text
### RIT-XXX — Short title

- Type:
- Severity:
- Status:
- Date discovered:
- Phase or component:
- Environment:
- Authorization basis:
- Summary:
- Expected behavior:
- Observed behavior:
- Reproduction status:
- Security impact:
- Scientific or publication impact:
- Evidence location:
- Public disclosure safe now: YES / NO
- Fix branch or commit:
- Validation performed:
- Residual risk:
- Closure date:
```

## Immediate actions

- [ ] Pull the D4 field-contract correction.
- [ ] Parse the D4 contract and rerun its focused tests.
- [ ] Run D2, D3, D3B, D4, and Phase 15 validators.
- [ ] Generate one disposable outcome-blind D4 candidate bundle.
- [ ] Audit 4 families, 13 rows, 12 units, 4 cutoffs, and closed gates.
- [ ] Verify that projected values cannot alter the D4 identity contract.
- [ ] Verify the D4 four-file manifest.
- [ ] Run the complete regression suite.
- [ ] Refresh the tracked-file manifest only after D4 passes.
- [ ] Run CI only after draft-PR authorization.
- [ ] Keep Issue #3 and publication boundaries accurate.
- [ ] Keep sensitive security candidates outside the public repository.
