# Phase 10 — Formal Model Execution and Counterexample Capture

## Purpose

Phase 10 moves the provisional TLA+ recovery-control model from source-only validation to an actual
command-line SANY and TLC workflow. The phase records the exact finite configuration, toolchain,
execution logs, state-space summary, and an intentional negative-control counterexample.

## Execution gates

A Phase 10 run passes only when all of the following are true:

1. SANY parses `formal/tla/T1Recovery.tla` successfully.
2. TLC completes `formal/tla/MC.cfg` without finding a counterexample inside the recorded finite model.
3. TLC finds the intentionally induced `NegativeControlNoActivation` violation under
   `formal/tla/NegativeControl.cfg`.
4. The generated JSON and log files match `phase10-derived-bundle.sha256`.

The positive TLC result is labeled `NO_COUNTEREXAMPLE_WITHIN_RECORDED_BOUND`. That wording is mandatory.

## Toolchain pin

The automated workflow downloads `tla2tools.jar` from the official TLA+ v1.7.4 release and verifies the
release page's published SHA-1 before execution. The output bundle additionally records the downloaded
JAR's SHA-256, Java version, platform, commands, worker count, and all model input hashes.

CI uses Temurin Java 17 and one TLC worker. One worker reduces run-to-run variation in trace ordering and
state-space reporting. It is not a performance configuration.

The first successful CI execution recorded:

- TLA+ command-line tools `1.7.4`;
- Temurin Java `17.0.19`;
- JAR SHA-256 `936a262061c914694dfd669a543be24573c45d5aa0ff20a8b96b23d01e050e88`;
- SANY status `PARSE_SUCCESS`;
- 50 generated states;
- 28 distinct states;
- zero states left on the queue;
- complete-state-graph search depth 10;
- positive status `NO_COUNTEREXAMPLE_WITHIN_RECORDED_BOUND`; and
- a four-state expected negative-control counterexample.

These numbers describe one exact finite configuration and execution environment. They are not performance
benchmarks, probability estimates, or proof results.

## Positive model configuration

The recorded finite constants are:

- `MaxAttempts = 3`
- `InitialGroundEpoch = 2`
- `InitialSpaceEpoch = 1`
- `MaxEpoch = 6`

The positive configuration checks:

- type correctness;
- epoch monotonicity;
- candidate state cannot represent verified authority;
- bounded attempts and activation count;
- no rollback below the initial epochs;
- at most one spacecraft activation;
- success requires convergence, command acceptance, status evidence, and verification;
- secure degradation cannot be success; and
- status loss after convergence is not divergence.

These properties are provisional and incomplete until independent review.

## Negative control

`NegativeControlNoActivation == activationCount = 0` is intentionally false because the model permits a
spacecraft activation. TLC is expected to produce a counterexample reaching `activationCount = 1`.

The recorded four-state trace follows the abstract sequence `Init → Prepare → SelectCandidate → Commit`.
The negative-control trace validates the capture pipeline. It must never be presented as a newly found
protocol weakness, treatment failure, or security result.

## Derived outputs

A successful run writes:

- `phase10-formal-execution.json`
- `phase10-negative-control-counterexample.json`
- `phase10-java-version.log`
- `phase10-sany.log`
- `phase10-tlc-positive.log`
- `phase10-tlc-negative-control.log`
- `phase10-derived-bundle.sha256`

Generated TLC metadata directories are execution scratch data and are excluded from the derived manifest.
The complete external run directory can be preserved outside Git with an additional provenance file and
portable run manifest.

## Interpretation boundary

Phase 10 does not establish:

- proof of post-compromise security;
- correctness of a concrete cryptographic construction;
- CCSDS or SDLS conformance;
- flight-software, network, RF, or spacecraft behavior;
- unbounded liveness;
- completeness of the formal property set; or
- publication-ready formal evidence.

Independent review remains mandatory before the formal property set is frozen, the abstraction is mapped
to a concrete protocol, parameters or treatment are selected, or model-checking output is used in a paper
or external security claim.
