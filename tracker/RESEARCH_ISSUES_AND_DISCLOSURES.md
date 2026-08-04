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
| RIT-011 | REPRODUCIBILITY | HIGH | FIXED_PENDING_VALIDATION | 15 | B0/B1/B2 lacked shared T1 metrics and equivalent capture artifacts. | D1 passed local validation with 199 tests, 21 retained scenarios, JSON/CSV checks, immutable capture, and manifests. CI pending. |
| RIT-012 | REPRODUCIBILITY | HIGH | FIXED_PENDING_VALIDATION | 15 | Seeded execution lacked a complete immutable Phase 15 run directory. | Wrapper passed local D1 validation for raw, analysis, governance, logs, and layered manifests. CI pending. |
| RIT-013 | REPRODUCIBILITY | HIGH | FIXED_PENDING_VALIDATION | 15 | Shared fields did not identify semantically comparable baseline/T1 cases. | D2 passed local validation with eight conservative families, 36 unique dispositions, restricted fields, and no pooled catalog percentages. CI pending. |
| RIT-014 | REPRODUCIBILITY | HIGH | FIXED_PENDING_VALIDATION | 15 | A semantic matrix did not provide an executable qualified-family population with controlled analysis units and denominators. | D3 passed local validation with four qualified families, 13 member rows, 12 analysis units, strict projections, and an internal derived manifest. D3B integration validation and CI remain pending. |
| RIT-015 | DEFECT | LOW | FIXED_PENDING_VALIDATION | 15 | A D2 test searched for a noncontiguous phrase despite a correct matrix rule. | Assertion corrected; focused and complete local suites passed. CI pending. |
| RIT-016 | REPRODUCIBILITY | HIGH | FIXED_PENDING_VALIDATION | 15 | Standalone D3 outputs were not retained with exact D2/D3 inputs inside the immutable pilot bundle. | D3B now retains D2/D3 contracts and both catalogs, gates D3 on T1/baseline success, validates output semantics, records metadata schema 0.2.0, and adds a protected derived layer. Integrated local smoke and CI remain pending. |

## WP15-D3B evidence paths

- `spec/phase-15-d3b-capture-integration.json`
- `docs/phase-15-d3b-capture-integration.md`
- `experiments/scripts/run_phase15_pilot_capture.py`
- `experiments/scripts/validate_phase15_d3b_capture_integration.py`
- `tests/test_phase15_capture.py`
- `tests/test_phase15_protocol.py`
- `.github/workflows/phase15-comparability.yml`

## D3B acceptance conditions

RIT-016 cannot close merely because D3 files appear in a directory. Closure requires evidence that:

- the exact D2 matrix, D3 configuration, baseline catalog, and T1 catalog are retained;
- retained source and captured SHA-256 values match;
- D3 executes only after successful T1 and baseline stages;
- incomplete, tampered, or semantically relaxed D3 output fails closed;
- 4 families, 13 member rows, 12 analysis units, and 13 source executions are preserved;
- family coverage remains complete;
- success-rate denominators remain undefined;
- aggregation, inference, superiority, and publication gates remain closed;
- D3 internal, run-level derived, raw, analysis, and complete-bundle manifests verify; and
- local and CI validation pass at exact commits.

## Reproducibility rules

A parity or comparability issue is not closed because files share column names.

Closure requires evidence appropriate to the issue:

- metric-field parity requires identical declared fields and successful JSON/CSV generation;
- capture parity requires provenance, logs, exclusion/rerun handling, and checksums;
- scenario parity requires matched inputs or predeclared exceptions;
- semantic parity requires compatible meanings, not only compatible types;
- executable comparability requires predeclared family membership and observation controls;
- immutable integration requires retained inputs, metadata, fail-closed validation, and layered manifests; and
- publication readiness requires a frozen population and analysis plan before aggregate interpretation.

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

- [ ] Pull and validate the D3B checkpoint.
- [ ] Run focused capture and protocol tests.
- [ ] Run D2, D3, D3B, and Phase 15 validators.
- [ ] Run the complete regression suite.
- [ ] Execute one clean disposable integrated capture.
- [ ] Audit retained-input hashes, metadata, D3 counts, claim gates, and manifests.
- [ ] Refresh the tracked-file manifest only after D3B passes.
- [ ] Run CI after draft-PR authorization.
- [ ] Keep Issue #3 and publication boundaries accurate.
- [ ] Keep sensitive security candidates outside the public repository.
