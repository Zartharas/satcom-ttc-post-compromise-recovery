# Phase 04 Independent Cryptography Review Gate

## Status

**Open.** Phase 04 implementation and automated validation are complete. PR #1 remains in
draft until an independent reviewer evaluates the source-to-model mapping and the baseline
outcome oracles.

## Review objective

Determine whether the abstract B1 and B2 semantics are fair, source-grounded comparison
baselines for the TT&C recovery study without importing unmodeled recovery assistance or
claiming cryptographic properties that the simulator cannot establish.

## Materials under review

The reviewer should examine, at minimum:

- `docs/baseline-semantics-decision.md`
- `spec/baseline-semantics.json`
- `spec/security-invariants.json`
- `spec/transition-guards.json`
- `tests/scenarios/baseline-test-catalog.json`
- `src/ttc_recovery/simulator.py`
- `tests/test_simulator.py`
- `references/source-notes/triple-kem.md`
- `references/source-notes/poettering-roesler-urke.md`

The source papers named in the two source notes should be consulted directly. Repository
source notes are navigation aids, not substitutes for the papers.

## Required review questions

### B1: Triple-KEM integration

1. Is `ACTIVATE_ON_LOCAL_COMPLETION` the fairest minimum-assumption operational baseline when
   the cited three-message exchange does not define an SDLS activation acknowledgment?
2. Does loss of `KEM_CONFIRM` correctly produce ground-ahead operational divergence under that
   policy?
3. Is `DEFER_UNTIL_AUTHENTICATED_STATUS` clearly separated as an enhanced four-message
   integration rather than attributed to Triple-KEM?
4. Are status-loss and confirmation-loss outcomes assigned consistently for the enhanced
   integration?
5. Does any B1 test rely on information unavailable to the modeled endpoint?

### B2: URKE-inspired strict baseline

1. Is the ground-sender and spacecraft-receiver role mapping faithful enough for the stated
   ground-to-space recovery experiment?
2. Is sender-on-send evolution with immediate prior-state deletion a defensible strict
   recoverability lower bound?
3. Are `TRAFFIC_KEY`, `SENDER_STATE`, `RECEIVER_STATE`, and `BOTH_ENDPOINT_STATES` sufficiently
   distinct compromise scopes?
4. Is passive sender-state exposure treated consistently with the source model?
5. Is receiver-state exposure conservatively classified when it permits future-key tracing?
6. Does the active sender-state impersonation path model an attacker-known divergent receiver
   branch without overstating a source-paper theorem?
7. Are dropped update, replay, stale restore, and lost status outcomes mutually consistent?

### Claim boundaries

1. Do repository statements clearly distinguish deterministic model behavior from cryptographic
   proof?
2. Are all PCS references qualified by compromise scope, attacker behavior, and fresh-entropy
   assumptions?
3. Is any result labeled `SUCCESS` where the abstraction should instead return
   `AVAILABLE_UNSAFE` or `INDETERMINATE`?
4. Does any baseline receive recovery behavior that is unavailable in its explicitly modeled
   message flow?

## Required reviewer response

For each review question, record:

- `ACCEPT`, `ACCEPT WITH CORRECTION`, or `REJECT`
- a brief rationale
- the supporting source section, page, theorem, algorithm, or figure
- required repository changes, when applicable
- confidence: `HIGH`, `MEDIUM`, or `LOW`

The reviewer should also provide:

- name and relevant expertise
- affiliation or independent status
- conflict-of-interest statement
- review date
- repository branch and commit SHA reviewed

## Acceptance criteria

Phase 04 may leave draft status only when:

1. all 19 deterministic tests pass on supported CI versions;
2. all machine-readable specifications parse successfully;
3. the tracked-file manifest verifies;
4. no unresolved `REJECT` decision remains;
5. every `ACCEPT WITH CORRECTION` item has a linked commit and revalidation evidence;
6. the reviewer confirms that B1 and B2 are suitable comparison baselines for this study;
7. baseline scenario outcomes are frozen in the test catalog.

A review can approve the abstract mapping without approving the simulator as a cryptographic
implementation. No such implementation claim is requested.

## Baseline-oracle freeze

After acceptance, record the following in the pull request:

- approved commit SHA;
- reviewer identity and date;
- final B1 activation policies;
- final B2 compromise scopes;
- final outcome for every scenario ID;
- CI run identifier;
- manifest verification result.

After the freeze, changes to baseline message flow, compromise scope, state-transition timing,
or expected outcomes require a new review entry. Editorial changes and additional tests that do
not alter an existing oracle may proceed with normal pull-request review.

## Reproduction commands

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -p "test_*.py" -v

python3 - <<'PY'
from pathlib import Path
import json

for name in [
    "spec/baseline-semantics.json",
    "spec/security-invariants.json",
    "spec/system-model.json",
    "spec/t1-requirements.json",
    "spec/transition-guards.json",
    "tests/scenarios/baseline-test-catalog.json",
]:
    json.loads(Path(name).read_text(encoding="utf-8"))
    print(f"OK: {name}")
PY

shasum -a 256 -c artifacts/manifests/repository-v0.1.1.sha256
```

## Gate consequence

T1 design and implementation remain blocked until this review is accepted and the baseline
oracles are frozen.
