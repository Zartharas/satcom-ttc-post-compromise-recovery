# Phase 14 Independent Review Package

## Status

`READY_FOR_OUTREACH_NOT_REVIEWED`

This package prepares the repository for independent review. It does not constitute reviewer outreach,
acceptance, approval, oracle freeze, or permission to use the current outputs as publication evidence.

The review target must be recorded as the exact commit SHA on
`phase-14/independent-review-package` at the time outreach is sent. Issue #3 remains the reviewer-tracking
record. Its completion boxes stay unchecked until the corresponding evidence exists.

## Purpose

The mandatory review scope is the Phase 04/05 source-to-model mapping and the 21 baseline scenario oracles.
The extended diagnostic scope covers the Phase 10-13 formal abstraction, trace projection, adverse witnesses,
outcome expansion, and claim boundaries.

No new transition semantics are introduced in Phase 14.

## Reviewer qualification and scope

The primary reviewer should demonstrate experience in at least two of the expertise areas listed in issue #3.
Authors of either primary source construction may clarify their work, but a source author cannot alone satisfy
the independent-review gate.

The reviewer must state which scope they cover:

- baseline cryptography and source-to-model mapping;
- scenario-oracle review;
- formal-model and projection diagnostics; and
- research-governance and claims review.

A reviewer may accept the mandatory baseline scope while declining the formal-diagnostic scope. Any uncovered
scope requires a second qualified reviewer before that scope can be accepted.

## Required review order

1. Read the two primary source papers directly. The repository source notes are navigation aids only.
2. Review the Phase 04 gate and the Phase 14 claims matrix.
3. Review the B1 and B2 source-to-model decisions against the simulator and deterministic tests.
4. Decide every one of the 21 baseline scenario oracles.
5. Review the governance findings, including the retrospective Phase 6-13 exception.
6. Review the formal-model and Python-projection diagnostics only within their declared abstract scope.
7. Complete the Phase 14 response template without deleting unresolved items.
8. Link every correction to a commit and complete revalidation evidence.

## Governance findings that must be answered

### GOV-01 — response-template coverage mismatch

The Phase 04 gate contains 16 required questions. The Phase 05 response template contains 15 and omits the
endpoint-knowledge question now identified as `B1-R5`. The Phase 14 response template restores the missing
question.

### GOV-02 — retrospective T1 work

The Phase 04 gate says T1 work is blocked pending review, while Phases 6-13 proceeded as
`PROVISIONAL_INTERNAL_REVIEW_ONLY`. The reviewer must state whether retrospective review is acceptable and
which later phases must be repeated after any baseline correction.

### GOV-03 — meaning of locked

The baseline decision says the semantics are corrected and locked for abstract implementation, while the
oracle candidate remains `PENDING_INDEPENDENT_REVIEW`. Phase 14 treats locked as an internal implementation
decision only, not independent approval or oracle freeze.

### GOV-04 — review-target commit drift

Earlier handoff records point to older commits. Outreach must identify the exact Phase 14 commit reviewed, and
the signed response must repeat that SHA.

## Decision rules

Every review question and scenario oracle requires:

- `ACCEPT`, `ACCEPT WITH CORRECTION`, or `REJECT`;
- `HIGH`, `MEDIUM`, or `LOW` confidence;
- a brief rationale;
- a source section, page, theorem, algorithm, or figure when source-grounding is relevant; and
- required repository changes, when applicable.

No unresolved `REJECT` may remain. Every `ACCEPT WITH CORRECTION` requires a linked corrective commit and
revalidation record.

## Claims rules

The machine-readable source is `spec/phase-14-independent-review-package.json`. The reviewer-facing matrix is
`governance/phase-14-claims-traceability.csv`.

Until review is complete:

- baseline semantic and oracle statements remain pending independent review;
- TLA+ statements use bounded execution wording only;
- formal/Python agreement remains `MATCH_WITHIN_DECLARED_ABSTRACTION`;
- Phase 13 remains opt-in and diagnostic-only; and
- model completeness, implementation equivalence, cryptographic security, causal validity, operational
  spacecraft applicability, and publication-evidence claims remain `NOT_PERMITTED`.

## Evidence files

Use `governance/phase-14-evidence-index.csv` as the review index. All repository paths are pinned by the exact
review-target commit. Source papers must be obtained from their publishers or authors and checked directly.

The central files are:

- `governance/phase-04-independent-review-gate.md`
- `docs/baseline-semantics-decision.md`
- `spec/baseline-semantics.json`
- `spec/baseline-oracle-freeze-candidate.json`
- `tests/scenarios/baseline-test-catalog.json`
- `src/ttc_recovery/simulator.py`
- `tests/test_simulator.py`
- `spec/phase-10-formal-model-execution.json`
- `spec/phase-11-formal-python-cross-validation.json`
- `spec/phase-12-adverse-outcome-witnesses.json`
- `spec/phase-13-abstraction-gap-outcomes.json`
- `formal/tla/T1Recovery.tla`
- `formal/tla/T1RecoveryOutcomeExpansion.tla`

## Reproduction

```bash
PYTHONWARNINGS="error::ResourceWarning" PYTHONPATH=src \
python3 -m unittest discover -s tests -p "test_*.py" -v

python3 experiments/scripts/validate_review_handoff.py
python3 experiments/scripts/validate_phase10_formal_execution.py
python3 experiments/scripts/validate_phase11_cross_validation.py
python3 experiments/scripts/validate_phase12_adverse_outcomes.py
python3 experiments/scripts/validate_phase13_outcome_expansion.py
python3 experiments/scripts/validate_phase14_review_package.py
python3 experiments/scripts/validate_repository_manifest.py

python3 experiments/scripts/validate_review_handoff.py --markdown
```

Formal evidence reproduction remains documented in the Phase 10-13 files. Reviewers need not rerun TLC unless
they cover the formal-diagnostic scope, but any accepted formal correction requires full Phase 10-13
revalidation.

## Completion gate

The package may move from ready-for-outreach to reviewed only after:

1. reviewer identity, expertise, affiliation or independent status, conflict statement, date, and exact SHA are
   recorded;
2. all 24 review questions and all 21 oracles have decisions;
3. every source-grounding decision includes a locator;
4. all corrections are linked and revalidated;
5. the reviewer states whether the baselines are suitable for comparison;
6. the reviewer states whether the oracle candidate may be frozen;
7. retrospective revalidation scope is recorded; and
8. uncovered formal-diagnostic scope is assigned to another qualified reviewer.

Until then, the package status remains `READY_FOR_OUTREACH_NOT_REVIEWED`.
