# Research Engineering Issues and Responsible Disclosure Tracker

**Branch:** `phase-15/publication-preparation`  
**Last updated:** 2026-08-03  
**Status:** `ACTIVE`

## Purpose

This file tracks defects, research-governance gaps, reproducibility problems, upstream contribution opportunities, and potential security findings discovered during the study.

The objective is to improve the public repository and create a transparent record of engineering maturity. Recognition may result from accepted fixes, upstream pull requests, acknowledged responsible disclosures, reproducible artifacts, or assigned vulnerability identifiers, but none of these outcomes is guaranteed.

## Scope and authorization

Allowed work is limited to:

- this repository and its controlled local test environment;
- dependencies and open-source projects examined under their published contribution and security policies;
- synthetic inputs, bounded formal models, and authorized test systems;
- documentation, reproducibility, validation, and defensive security analysis.

Prohibited work includes:

- testing operational spacecraft, ground stations, RF links, or third-party infrastructure without written authorization;
- transmitting commands or malformed traffic to systems not owned or explicitly authorized;
- accessing private data, credentials, or restricted environments;
- publishing exploit details before coordinated disclosure;
- describing an ordinary software defect as a security vulnerability without validated security impact;
- claiming a CVE, advisory, bounty, or external recognition before it is formally assigned or acknowledged.

## Classification

| Type | Meaning |
|---|---|
| `DEFECT` | Incorrect repository behavior, implementation, test, or documentation |
| `REPRODUCIBILITY` | Missing provenance, non-determinism, manifest failure, or evidence gap |
| `GOVERNANCE` | Consent, disclosure, review, claims, or process-control problem |
| `UPSTREAM_BUG` | Defect in an external open-source dependency or tool |
| `SECURITY_CANDIDATE` | Plausible security impact requiring validation and private triage |
| `SECURITY_CONFIRMED` | Reproduced security impact accepted for coordinated disclosure |
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
| RIT-002 | GOVERNANCE | HIGH | OPEN | 6–15 | Provisional Phases 6–13 proceeded after an earlier gate stated that T1 work was blocked pending review. | Work remains explicitly provisional; reviewer must determine retrospective revalidation scope. |
| RIT-003 | GOVERNANCE | MEDIUM | FIXED_PENDING_VALIDATION | 4–14 | “Corrected and locked” could be misread as independent approval rather than an internal implementation decision. | Phase 14 separates implementation lock, approval, oracle freeze, and publication permission. |
| RIT-004 | REPRODUCIBILITY | MEDIUM | FIXED_PENDING_VALIDATION | 5–14 | Earlier reviewer handoff records referenced older review-target commits. | Exact Phase 14 commit pinning and evidence-index rules added. |
| RIT-005 | REPRODUCIBILITY | LOW | CLOSED | 13 | Initial checksum verification was attempted before the derived bundle had been generated. | Run order corrected; final bundle and run-level manifests verified after generation. |
| RIT-006 | DEFECT | LOW | TRIAGED | 14 | GitHub `/tree/<commit>` link could return or appear to return the repository landing view, confusing reviewers. | Use immutable commit and direct blob links in outreach and documentation. |
| RIT-007 | GOVERNANCE | HIGH | FIXED_PENDING_VALIDATION | 14 | Prospective reviewer names were published in an outreach-planning issue before consent. | Names removed; Issue #3 now prohibits implying participation or publishing identity without permission. |
| RIT-008 | GOVERNANCE | HIGH | OPEN | 14–15 | AI assistance was not clearly disclosed in the initial external-review request. | Future outreach and publication materials require context-appropriate AI-use disclosure; exact venue policy still to be selected. |
| RIT-009 | ENHANCEMENT | MEDIUM | FIXED_PENDING_VALIDATION | 15 | Project lacked a consolidated publication-readiness tracker. | Phase 15 tracker added and updated with protocol, parity, pilot, and publication gates; CI validation remains pending. |
| RIT-010 | ENHANCEMENT | MEDIUM | FIXED_PENDING_VALIDATION | 15 | Project lacked a consolidated engineering issue and disclosure register. | This file establishes the register and responsible-disclosure workflow; final branch validation remains pending. |
| RIT-011 | REPRODUCIBILITY | HIGH | OPEN | 15 | B0, B1, and B2 have deterministic scenario tests but do not emit contact-window, retry, event-log, and provenance fields equivalent to the T1 seeded pipeline. | Comparative publication execution is blocked until baseline metric/capture parity is implemented or a narrower comparison is justified before aggregate results are viewed. |
| RIT-012 | REPRODUCIBILITY | HIGH | OPEN | 15 | The existing seeded runner writes result JSON and metrics CSV but does not yet create the complete Phase 15 run directory, metadata record, logs, exclusions, or layered checksum manifests. | Implement a dedicated pilot capture wrapper before Gate P1 and before retaining a pilot as valid pipeline evidence. |

## New issue template

Copy the block below for every new item.

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
4. Determine whether the impact is functional, scientific, security-related, or only cosmetic.
5. Check authorization before testing beyond this repository.
6. Search the upstream project's existing issues and security policy before reporting.
7. Avoid duplicate public reports for a suspected security issue.
8. Keep sensitive details private until the maintainer confirms a disclosure path.
9. Add a regression test before calling a code defect fixed.
10. Record the exact validating commit and CI run.

## Upstream contribution path

An issue may become a public upstream contribution when:

- the defect is reproduced against the upstream project's supported version;
- the report contains a minimal reproducer;
- no secrets, private data, or unauthorized system details are included;
- the proposed fix is narrowly scoped;
- tests demonstrate the failure before and success after the fix;
- contributor guidance and licensing requirements are followed;
- the report does not exaggerate security impact.

Useful public outcomes include:

- accepted issue report;
- merged documentation correction;
- merged regression test;
- merged bug fix;
- maintainer acknowledgment;
- release-note credit.

These outcomes may support a résumé or research-impact narrative, but they must be described factually.

## Responsible security-disclosure path

### Step 1 — Private validation

- Confirm the behavior in an authorized environment.
- Record affected versions and prerequisites.
- Determine whether confidentiality, integrity, availability, authentication, authorization, or isolation is affected.
- Rule out configuration error and expected behavior.
- Create the smallest non-destructive reproducer.

### Step 2 — Find the disclosure channel

Prefer, in order:

1. the repository `SECURITY.md`;
2. the vendor security portal;
3. the maintainer's published security email;
4. a relevant CNA or coordination body when the vendor is unresponsive.

Do not open a public GitHub issue for an undisclosed vulnerability unless the project's policy explicitly instructs that approach.

### Step 3 — Submit a precise report

Include:

- affected product and version;
- environment and prerequisites;
- clear impact;
- reproduction steps;
- minimal evidence;
- suggested remediation when known;
- disclosure timeline request;
- preferred credit name and identifier.

### Step 4 — Coordinate

- Allow reasonable remediation time.
- Retest the vendor's fix.
- Do not pressure the vendor for a CVE.
- Do not publicly claim severity or exploitation beyond reproduced evidence.
- Preserve the vendor's acknowledgment and final advisory.

### Step 5 — Record public recognition accurately

Only after publication may this tracker record:

- advisory identifier;
- CVE identifier assigned by a CNA;
- vendor acknowledgment;
- release containing the fix;
- credited researcher name;
- public disclosure date.

## Security-candidate decision test

A suspected issue should remain `SECURITY_CANDIDATE` unless all of the following are answered:

- What protected security property is violated?
- Which attacker capability is required?
- Which supported version is affected?
- Is the behavior reproducible?
- Does it cross a trust boundary?
- Is the impact more than a crash in a local test harness?
- Is the test authorized?
- Is there a private disclosure route?

If these questions cannot be answered, classify the item as `DEFECT`, `REPRODUCIBILITY`, `ENHANCEMENT`, or `FALSE_POSITIVE` instead.

## Research-paper use

Issue-tracker data may support the paper only when:

- the issue is relevant to the research method or validity;
- the record is complete and reproducible;
- disclosure restrictions permit publication;
- the manuscript distinguishes internal defects from external vulnerabilities;
- counts are not inflated by duplicates or cosmetic observations;
- unresolved security details are omitted or generalized;
- contributions are described without implying endorsement.

## Immediate actions

- [ ] Link every current issue to evidence or a repository commit.
- [ ] Implement baseline metric/capture parity for RIT-011.
- [ ] Implement the dedicated pilot capture wrapper for RIT-012.
- [ ] Add labels or GitHub issues only when public disclosure is appropriate.
- [ ] Review upstream dependencies for published contribution and security policies.
- [ ] Add regression tests for all code defects fixed during Phase 15.
- [ ] Keep sensitive security candidates outside the public repository.
- [ ] Review this register before every publication-candidate experiment run.
