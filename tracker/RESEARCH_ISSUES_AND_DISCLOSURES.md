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
| RIT-017 | REPRODUCIBILITY | HIGH | FIXED | 15 | The qualified-family population lacked predeclared observation cutoffs, denominator membership, allowed-display boundaries, and post-observation revision controls. | D4 and D4R passed local validation; FR-01 through FR-16 passed; the formal decision is `ACCEPT`; and decision-commit runs `30942565654` and `30942565653` succeeded for exact commit `307f685`. The reviewed cutoffs, analysis-unit denominators, member registry, and planning displays are freeze-effective. |
| RIT-018 | DEFECT | HIGH | FIXED | 15 | The initial D4 configuration widened four family `expected_allowed_fields` lists beyond the authoritative D2 matrix. | D4 was corrected at `968af687`; exact field parity remained enforced; local regression passed; and both required pull-request CI workflows succeeded for review-package commit `d321f92`. |
| RIT-019 | REPRODUCIBILITY | HIGH | FIXED | 15 | The initial separate D4 freeze-review preflight continued after repository-manifest failure, and the ignored review packet labeled review-package HEAD `40edf80` as the candidate instead of validated D4 checkpoint `34d63a5`. | The flawed packet was preserved and invalidated; the corrected packet separated target `34d63a5` from package `d321f92`; three outcome-blind review rounds passed; failed automation attempts and recoveries were retained; and CI runs `30938748822` and `30938748747` completed successfully. |

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

RIT-017 and RIT-018 passed local validation. The separate D4R review completed all 16 questions with `PASS`, the formal decision is `ACCEPT`, and exact decision commit `307f685` passed both required workflows. Local and CI evidence confirmed that:

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

D4 engineering validation alone did not freeze the candidate. The separate explicit `ACCEPT` decision and successful exact decision-commit CI now freeze only the reviewed planning objects. Comparative display and all analytical or publication claims remain separately gated.

## WP15-D4 freeze-review preflight defect

The first separate freeze-review attempt was stopped before any
family-level substantive decision. Two issues were observed:

- repository manifest validation failed after the seven D4R package
  files were added, but a later unconditional shell `echo` printed
  a misleading PASS marker; and
- the ignored packet used current review-package HEAD `40edf80` as
  `candidate_commit`, although the machine-readable D4R contract
  identifies validated D4 checkpoint `34d63a5` as the review target.

The first packet remains preserved with a separate invalidation
record. No comparative values were viewed, no family review began,
and every freeze, comparison, inference, and publication gate
remains closed.

## WP15-D4R review and CI closure

The corrected separate review completed all 16 questions with `PASS`. Review-package commit `d321f92` passed both required pull-request workflows:

- `Phase 15 treatment comparability` — run `30938748822`, `success`;
- `Python and formal-model tests` — run `30938748747`, `success`.

The formal decision is `ACCEPT`. Exact decision commit `307f685389d799fb5b22d481763bd171393085db` passed both required workflows:

- `Phase 15 treatment comparability` — run `30942565654`, `success`;
- `Python and formal-model tests` — run `30942565653`, `success`.

Freeze effectiveness is now true for the exact reviewed cutoffs, analysis-unit denominators, member registry, and allowed planning displays. No comparative values were viewed, and all analytical and publication gates remain closed.

## WP15-D4F freeze-effectiveness closure

The explicit decision record is bound to exact decision commit `307f685389d799fb5b22d481763bd171393085db`. Both required pull-request workflows completed successfully for that SHA. The effective freeze covers only:

- the four exact reviewed observation cutoffs;
- the 12 treatment-within-family analysis-unit denominator identities;
- the 13-member traceability registry; and
- the allowed planning-display registry.

The publication analysis plan is not frozen. Member-value display, family comparison, rates, pooled aggregation, inference, ranking, causal interpretation, cryptographic claims, independent validation, and publication evidence remain prohibited.

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

- [x] Pull the D4 field-contract correction.
- [x] Parse the D4 contract and rerun its focused tests.
- [x] Run D2, D3, D3B, D4, and Phase 15 validators.
- [x] Generate one disposable outcome-blind D4 candidate bundle.
- [x] Audit 4 families, 13 rows, 12 units, 4 cutoffs, and closed gates.
- [x] Verify that projected values cannot alter the D4 identity contract.
- [x] Verify the D4 four-file manifest.
- [x] Run the complete 236-test regression suite.
- [x] Refresh and validate the 185-entry tracked-file manifest.
- [x] Commit the D4 closeout status and manifest.
- [x] Run review-package and decision-commit CI under draft PR #13 authorization.
- [x] Conduct the separate D4 freeze review before any family-value display.
- [x] Record the effective freeze for the exact reviewed planning objects.
- [ ] Keep Issue #3 and publication boundaries accurate.
- [ ] Keep sensitive security candidates outside the public repository.
