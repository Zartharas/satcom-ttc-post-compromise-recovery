# Project Status

## Completed

- Phase One related-work and novelty framing
- Phase Two system and threat model
- Phase Three machine-readable abstract design
- repository foundation and automated Python test workflow
- B1 Triple-KEM source-semantic review
- B2 construction selection: Poettering-Roesler URKE-inspired strict baseline
- machine-readable Phase 04 baseline semantics
- adversarial review of B1 activation and B2 compromise scope
- corrected deterministic B1 and B2 fault tests
- Phase 05 independent-review handoff and 21-oracle freeze candidate
- automated handoff validation and stacked-pull-request CI
- provisional Phase 06 T1 bounded-resynchronization controller
- deterministic provisional T1 fault and guard tests
- Phase 07 seeded and explicit fault-schedule framework
- provisional contact-window recovery metrics and JSON/CSV export
- preserved-run checksum and provenance workflow outside the Git repository
- provisional Phase 08 aggregation, trace-audit, and sensitivity analysis layer
- Phase 09 explicit adversarial coverage, bounded reachability, and formal-model scaffold
- Phase 10 command-line SANY/TLC execution and counterexample-capture workflow

## Current phase

Phase 10 executes the provisional formal recovery-control model with a pinned command-line TLA+ toolchain
while the Phase 04/05 independent-review gate remains open.

The Phase 10 layer now provides:

- pinned stable TLA+ command-line tools release `1.7.4`;
- official release SHA-1 verification before execution;
- recorded JAR SHA-256, Java version, platform, commands, worker count, and input hashes;
- a real SANY parse gate;
- a bounded positive TLC model-check gate;
- mandatory `NO_COUNTEREXAMPLE_WITHIN_RECORDED_BOUND` wording;
- an intentional false invariant used only to verify counterexample capture;
- structured JSON serialization of the negative-control trace;
- raw Java, SANY, positive-TLC, and negative-control logs;
- a SHA-256 manifest for every derived Phase 10 output; and
- a separate CI formal job with short-lived evidence artifacts.

The first successful CI execution at the current finite constants recorded:

- SANY: `PARSE_SUCCESS`;
- positive TLC: 50 generated states, 28 distinct states, zero queued states, search depth 10;
- positive status: `NO_COUNTEREXAMPLE_WITHIN_RECORDED_BOUND`;
- negative control: four-state counterexample to `NegativeControlNoActivation`;
- tool: TLA+ command-line tools `1.7.4`;
- Java: Temurin `17.0.19`;
- TLC workers: one; and
- JAR SHA-256: `936a262061c914694dfd669a543be24573c45d5aa0ff20a8b96b23d01e050e88`.

## Review status

- Baseline oracle candidate: `PENDING_INDEPENDENT_REVIEW`
- Independent cryptography review: not yet performed
- T1 treatment status: `PROVISIONAL_INTERNAL_REVIEW_ONLY`
- Phase 07 seed and parameter status: `UNFROZEN`
- Phase 08 denominator and grid status: `UNFROZEN`
- Phase 09 scenario population: `PROVISIONAL_EXPLICIT_REGRESSION_SET`
- Phase 09/10 formal property set: `PROVISIONAL_ONLY`
- Formal model review status: `NOT_INDEPENDENTLY_REVIEWED`
- Phase 10 execution status: `FORMAL_EXECUTION_GATES_PASSED`
- Positive TLC interpretation: `NO_COUNTEREXAMPLE_WITHIN_RECORDED_BOUND`
- Phase 10 publication-evidence status: `NOT_PERMITTED`
- Publication, treatment-effectiveness, causal, or PCS claim status: not permitted

Development may continue on internal counterexample review, bounded configuration expansion, model-to-Python
trace comparison, parser and toolchain reproducibility, and external-review preparation.

## Mandatory stop point

Independent cryptography review becomes mandatory before:

- accepting or freezing baseline or T1 outcome oracles;
- freezing the experiment population, fault distribution, scenario exclusions, or formal property set;
- freezing retry budgets, candidate lifetimes, passive intervals, model constants, or other parameters;
- adopting denominator exclusions, success thresholds, or a statistical analysis plan;
- selecting T1 as the final treatment;
- mapping the abstract model to a concrete cryptographic protocol or implementation;
- treating bounded non-reachability or a clean TLC run as proof;
- interpreting reachability or model-checking output as post-compromise-security evidence;
- claiming CCSDS/SDLS conformance, flight-software correctness, or operational-spacecraft behavior;
- using Phase 08/09/10, NOS3/cFS, or formal-model output as publication evidence; or
- manuscript submission or any external security claim.

At that point, development must pause until the review record is complete and all corrections are
revalidated.

## Provisional Phase 10 decisions

- The stable v1.7.4 command-line release is pinned instead of the newer pre-release.
- The official release checksum is verified before execution; SHA-256 is also recorded in each run.
- CI uses Temurin Java 17 and one TLC worker for reproducible trace ordering and state reporting.
- Terminal deadlocks are disabled in the finite TLC configurations and do not create a liveness claim.
- SANY parse success, positive TLC completion, negative-control capture, and bundle verification are
  separate mandatory gates.
- The positive result is never called proof or formal verification of a concrete protocol.
- `NegativeControlNoActivation` is intentionally false and exists only to verify trace capture.
- The expected negative-control counterexample is not a discovered protocol flaw.
- Generated execution evidence is preserved outside Git or as short-lived CI artifacts.
- No property set, model constant, treatment parameter, or interpretation is frozen.

## Phase 10 artifacts

- `src/ttc_recovery/formal_execution.py`
- `spec/phase-10-formal-model-execution.json`
- `experiments/scripts/run_phase10_formal_execution.py`
- `experiments/scripts/validate_phase10_formal_execution.py`
- `tests/test_formal_execution.py`
- `tests/test_phase10_spec.py`
- `formal/tla/T1Recovery.tla`
- `formal/tla/MC.cfg`
- `formal/tla/NegativeControl.cfg`
- `formal/README.md`
- `docs/phase-10-formal-model-execution.md`
- `.github/workflows/python-tests.yml`

## Next internal work

- run the complete Phase 10 local gate and preserve an external evidence bundle;
- compare the four-state negative-control trace with the intended model transitions;
- add model-to-Python trace correspondence without claiming refinement proof;
- run additional finite constant configurations as explicitly separate records;
- capture any unexpected counterexample without reclassifying it before analysis;
- identify properties and abstractions requiring cryptography or space-systems review; and
- prepare the independent-review package before any property or claim freeze.

## Deferred

- completed independent cryptography review
- completed space-systems review
- frozen baseline and T1 oracles
- frozen experiment population, parameters, thresholds, and statistical analysis plan
- frozen and independently reviewed formal property set
- publication-grade formal evidence
- concrete cryptographic implementation
- CCSDS/SDLS conformance testing
- NOS3/cFS integration
- pilot experiment
- frozen full experiment protocol
- journal manuscript results
