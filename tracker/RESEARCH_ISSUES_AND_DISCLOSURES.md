# Research Engineering Issues and Responsible Disclosure Tracker

**Branch:** `phase-15/publication-preparation`  
**Last updated:** 2026-08-04  
**Status:** `ACTIVE`

## Purpose

This file tracks defects, research-governance gaps, reproducibility problems, upstream contribution opportunities, and potential security findings discovered during the study.

The objective is to improve the public repository and maintain a transparent engineering record. Recognition may result from accepted fixes, upstream pull requests, acknowledged responsible disclosures, reproducible artifacts, or assigned vulnerability identifiers, but none is guaranteed.

## Scope and authorization

Allowed work is limited to:

- this repository and its controlled local test environment;
- dependencies and open-source projects examined under published contribution and security policies;
- synthetic inputs, bounded formal models, and authorized test systems;
- documentation, reproducibility, validation, and defensive security analysis.

Prohibited work includes:

- testing operational spacecraft, ground stations, RF links, or third-party infrastructure without written authorization;
- transmitting commands or malformed traffic to systems not owned or explicitly authorized;
- accessing private data, credentials, or restricted environments;
- publishing exploit details before coordinated disclosure;
- describing an ordinary software defect as a security vulnerability without validated impact; and
- claiming a CVE, advisory, bounty, or external recognition before formal assignment or acknowledgment.

## Classification

| Type | Meaning |
|---|---|
| `DEFECT` | Incorrect repository behavior, implementation, test, or documentation |
| `REPRODUCIBILITY` | Missing provenance, non-determinism, manifest failure, evidence gap, or noncomparable measurement |
| `GOVERNANCE` | Consent, disclosure, review, claims, or process-control problem |
| `UPSTREAM_BUG` | Defect in an external open-source dependency or tool |
| `SECURITY_CANDIDATE` | Plausible security impact requiring validation and private triage |
| `SECURITY_CONFIRMED` | Reproduced impact accepted for coordinated disclosure |
| `ENHANCEMENT` | Improvement that is not a defect |
| `FALSE_POSITIVE` | Investigated concern with no reproducible issue |

## Severity

| Severity | Meaning |
|---|---|
| `CRITICAL` | Credible immediate risk of severe compromise in an authorized system |
| `HIGH` | Major security, data-integrity, or scientific-validity impact |
| `MEDIUM` | Material defect with bounded impact or reliable workaround |
| `LOW` | Minor defect, documentation gap, or usability issue |
| `INFO` | Observation, hardening opportunity, or process improvement |

## Status workflow

`NEW` → `TRIAGED` → `REPRODUCED` → `FIX_IN_PROGRESS` → `FIXED_PENDING_VALIDATION` → `CLOSED`

Security candidates may instead follow:

`NEW_PRIVATE` → `TRIAGED_PRIVATE` → `REPRODUCED_PRIVATE` → `VENDOR_NOTIFIED` → `COORDINATED_REMEDIATION` → `DISCLOSED` → `CLOSED`

Do not place undisclosed vulnerability details, proof-of-concept exploit code, credentials, or sensitive vendor communications in this public file.

## Current issue register

| ID | Type | Severity | Status | Phase | Summary | Current disposition |
|---|---|---|---|---|---|---|
| RIT-001 | GOVERNANCE | MEDIUM | FIXED_PENDING_VALIDATION | 4–14 | Historical Phase 05 response template omitted the B1 endpoint-knowledge question later identified as `B1-R5`. | Phase 14 restores the question without rewriting historical evidence; external disposition remains pending. |
| RIT-002 | GOVERNANCE | HIGH | OPEN | 6–15 | Provisional Phases 6–13 proceeded after an earlier gate stated that T1 work was blocked pending review. | Work remains explicitly provisional; a future reviewer must determine retrospective revalidation scope. |
| RIT-003 | GOVERNANCE | MEDIUM | FIXED_PENDING_VALIDATION | 4–14 | “Corrected and locked” could be misread as independent approval rather than an internal implementation decision. | Phase 14 separates implementation lock, approval, oracle freeze, and publication permission. |
| RIT-004 | REPRODUCIBILITY | MEDIUM | FIXED_PENDING_VALIDATION | 5–14 | Earlier reviewer handoff records referenced older review-target commits. | Exact Phase 14 commit pinning and evidence-index rules added. |
| RIT-005 | REPRODUCIBILITY | LOW | CLOSED | 13 | Checksum verification was initially attempted before the derived bundle existed. | Run order corrected; final bundle and run-level manifests verified after generation. |
| RIT-006 | DEFECT | LOW | TRIAGED | 14 | A GitHub `/tree/<commit>` link could appear as a repository landing view and confuse reviewers. | Use immutable commit and direct blob links in outreach and documentation. |
| RIT-007 | GOVERNANCE | HIGH | FIXED_PENDING_VALIDATION | 14 | Prospective reviewer names were published in an outreach-planning issue before consent. | Names removed; Issue #3 now prohibits implying participation or publishing identity without permission. |
| RIT-008 | GOVERNANCE | HIGH | OPEN | 14–15 | AI assistance was not clearly disclosed in the initial external-review request. | Future outreach and publication materials require context-appropriate AI-use disclosure; the venue policy remains to be selected. |
| RIT-009 | ENHANCEMENT | MEDIUM | FIXED_PENDING_VALIDATION | 15 | Project lacked a consolidated publication-readiness tracker. | Tracker now covers protocol, parity, comparability, pilot, manuscript, and publication gates; branch validation remains pending. |
| RIT-010 | ENHANCEMENT | MEDIUM | FIXED_PENDING_VALIDATION | 15 | Project lacked a consolidated engineering issue and disclosure register. | This file establishes the register and disclosure workflow; final branch validation remains pending. |
| RIT-011 | REPRODUCIBILITY | HIGH | FIXED_PENDING_VALIDATION | 15 | B0, B1, and B2 did not emit the shared T1 metric fields or equivalent capture artifacts. | WP15-D1 passed local validation with 199 tests, 21 retained catalog cases, JSON/CSV checks, extended capture, and manifests. CI remains pending. |
| RIT-012 | REPRODUCIBILITY | HIGH | FIXED_PENDING_VALIDATION | 15 | The seeded runner did not create a complete immutable Phase 15 run directory. | The wrapper passed local end-to-end validation for T1, baseline adapter, analysis, metadata, logs, governance records, and layered manifests. CI remains pending. |
| RIT-013 | REPRODUCIBILITY | HIGH | FIXED_PENDING_VALIDATION | 15 | Shared metric fields did not define which baseline and T1 cases were semantically comparable. | WP15-D2 passed local validation with 207 tests, eight families, 36 unique catalog dispositions, prohibited pooled percentages, and a 169-entry manifest. CI remains pending. |
| RIT-014 | REPRODUCIBILITY | HIGH | FIX_IN_PROGRESS | 15 | A semantic matrix does not itself create an executable matched treatment population with controlled projection and denominators. | WP15-D3 now implements four qualified families, 13 member rows, 12 treatment-family analysis units, exact T1 recipes, member-level projections, coverage denominators, and derived checksums. Standalone validation and later immutable-bundle integration remain pending. |
| RIT-015 | DEFECT | LOW | FIXED_PENDING_VALIDATION | 15 | The WP15-D2 population-rule test searched for a phrase that was not present contiguously even though the matrix rule itself was correct. | The assertion now checks the exact population rule; 8 focused and 207 complete tests passed locally. CI remains pending. |

## WP15-D1 evidence paths

- `src/ttc_recovery/baseline_metrics.py`
- `experiments/configs/phase-15-baseline-parity.json`
- `experiments/scripts/run_phase15_baseline_parity.py`
- `experiments/scripts/run_phase15_pilot_capture.py`
- `tests/test_baseline_metrics.py`
- `tests/test_phase15_baseline_runner.py`
- `docs/phase-15-baseline-metric-parity.md`
- `docs/phase-15-data-dictionary.md`
- `governance/phase-15-data-capture-controls.md`

## WP15-D2 evidence paths

- `spec/phase-15-treatment-comparability-matrix.json`
- `docs/phase-15-treatment-comparability.md`
- `src/ttc_recovery/treatment_comparability.py`
- `experiments/scripts/validate_phase15_treatment_comparability.py`
- `tests/test_phase15_treatment_comparability.py`
- `.github/workflows/phase15-comparability.yml`

## WP15-D3 evidence paths

- `experiments/configs/phase-15-matched-family-population.json`
- `docs/phase-15-matched-family-population.md`
- `src/ttc_recovery/matched_family_population.py`
- `experiments/scripts/run_phase15_matched_family_population.py`
- `experiments/scripts/validate_phase15_matched_family_population.py`
- `tests/test_phase15_matched_family_population.py`
- `.github/workflows/phase15-comparability.yml`

## New issue template

```text
### RIT-XXX — Short title

- Type:
- Severity:
- Status:
- Date discovered:
- Phase or component:
- Reporter:
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
- Upstream project or vendor:
- Upstream issue or advisory:
- Fix branch or commit:
- Validation performed:
- Residual risk:
- Closure date:
```

## Triage rules

1. Reproduce the issue from a clean state.
2. Preserve raw logs before modifying the system.
3. Separate observed facts from hypotheses.
4. Determine whether impact is functional, scientific, security-related, or cosmetic.
5. Check authorization before testing beyond this repository.
6. Search the upstream project’s existing issues and security policy before reporting.
7. Avoid duplicate public reports for a suspected security issue.
8. Keep sensitive details private until the maintainer confirms a disclosure path.
9. Add a regression test before calling a code defect fixed.
10. Record the exact validating commit and CI run.

## Reproducibility issue rules

A parity or comparability issue is not closed merely because files share column names.

Closure requires evidence appropriate to the issue:

- metric-field parity requires identical declared shared fields and successful JSON/CSV generation;
- capture parity requires equivalent provenance, logs, exclusion/rerun handling, and checksums;
- scenario parity requires matched inputs or predeclared justified exceptions;
- semantic parity requires compatible measurement meanings, not only compatible types;
- executable comparability requires family-specific execution, exact source traceability, controlled projection, denominator discipline, and immutable capture;
- publication readiness requires a frozen population and analysis plan before aggregate interpretation.

## Upstream contribution path

A public upstream contribution is appropriate when:

- the defect is reproduced against a supported upstream version;
- the report contains a minimal reproducer;
- no secrets, private data, or unauthorized-system details are included;
- the proposed fix is narrowly scoped;
- tests demonstrate failure before and success after the fix;
- contributor and licensing requirements are followed; and
- the report does not exaggerate security impact.

Useful public outcomes include an accepted issue report, merged documentation correction, merged regression test, merged bug fix, maintainer acknowledgment, or release-note credit. Any résumé or research-impact statement must describe the outcome factually.

## Responsible security-disclosure path

### Step 1 — Private validation

- Confirm behavior in an authorized environment.
- Record affected versions and prerequisites.
- Identify the violated confidentiality, integrity, availability, authentication, authorization, or isolation property.
- Rule out configuration error and expected behavior.
- Create the smallest non-destructive reproducer.

### Step 2 — Find the disclosure channel

Prefer:

1. repository `SECURITY.md`;
2. vendor security portal;
3. published maintainer security email; or
4. a relevant CNA or coordination body when the vendor is unresponsive.

Do not open a public GitHub issue for an undisclosed vulnerability unless the project’s policy explicitly requires it.

### Step 3 — Submit and coordinate

Include affected product/version, environment, prerequisites, impact, reproduction steps, minimal evidence, suggested remediation when known, a disclosure-timeline request, and preferred credit name.

Allow reasonable remediation time, retest the fix, and do not pressure the vendor for a CVE. Preserve the final advisory and acknowledgment.

### Step 4 — Record recognition accurately

Only after publication may this tracker record an advisory identifier, CVE assigned by a CNA, vendor acknowledgment, fixed release, credited researcher name, and public disclosure date.

## Security-candidate decision test

A concern remains `SECURITY_CANDIDATE` unless the record answers:

- What protected security property is violated?
- Which attacker capability is required?
- Which supported version is affected?
- Is the behavior reproducible?
- Does it cross a trust boundary?
- Is the impact more than a local test-harness crash?
- Is the test authorized?
- Is there a private disclosure route?

If these cannot be answered, classify the item as `DEFECT`, `REPRODUCIBILITY`, `ENHANCEMENT`, or `FALSE_POSITIVE`.

## Research-paper use

Tracker data may support the paper only when the issue is relevant to validity, the record is reproducible, disclosure restrictions permit publication, internal defects are distinguished from external vulnerabilities, duplicates are removed, and contributions are described without implying endorsement.

## Immediate actions

- [ ] Validate WP15-D3 JSON, focused tests, standalone validator, runner outputs, and derived manifest.
- [ ] Run the complete regression suite after D3 implementation.
- [ ] Refresh the repository manifest only after D3 local validation passes.
- [ ] Integrate the validated D3 artifacts into the immutable Phase 15 pilot bundle.
- [ ] Keep family-specific comparison and all pooled aggregation unauthorized.
- [ ] Run CI for RIT-011 through RIT-015 only after draft-PR authorization.
- [ ] Add public GitHub issues only when disclosure is appropriate.
- [ ] Keep sensitive security candidates outside the public repository.
