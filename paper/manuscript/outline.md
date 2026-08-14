# Manuscript Outline — Hands-On TT&C Post-Compromise Recovery Study

## 1. Introduction

- TT&C security problem: operational-key compromise plus ground-space state divergence.
- Gap between cryptographic key update and operational resynchronization/verification.
- Safe, controlled software experiment.
- Contributions: conservative baseline mappings, T1 controller, deterministic/mixed fault
  experiments, matched-family analysis, sensitivity analysis, and bounded assurance evidence.

## 2. Background and Related Work

### 2.1 Satellite TT&C security-state recovery
### 2.2 B0 SDLS-style rekeying abstraction
### 2.3 B1 Triple-KEM/PQNoise-inspired update
### 2.4 B2 URKE-inspired state evolution
### 2.5 Post-compromise recovery and operational-resynchronization gap

State explicitly that source constructions/proofs are not inherited by the simulator.

## 3. System and Threat Model

### 3.1 Ground and spacecraft endpoints
### 3.2 Operational key state and recovery authority
### 3.3 Compromise scopes
### 3.4 Ground-space divergence
### 3.5 Attacker capabilities and bounded recovery opportunity
### 3.6 Excluded threat classes

## 4. Recovery Designs

### 4.1 B0
### 4.2 B1 activation variants
### 4.3 B2 strict state evolution
### 4.4 T1 bounded resynchronization
### 4.5 Outcome/security/availability classifications

Figure 1: experimental architecture and evidence flow.

## 5. Experimental Method

### 5.1 Research questions
- RQ1 matched recovery behavior.
- RQ2 T1 fault robustness.
- RQ3 T1 sensitivity.
- RQ4 bounded formal/Python agreement.

### 5.2 Predeclaration, reproducibility, and capture
- plan commit `cfb730a8191d37863e9e419823686b3c3afe18a2`;
- execution commit `c630fb4f65ad78211fd3ffb0391000d7ed3629b1`;
- serialized schedules and SHA-256 identities;
- immutable raw/derived bundle;
- exclusion/rerun policy;
- retained run `20260814T022506Z-gc630fb4`.

### 5.3 Study A — matched treatment families
- CF-01, CF-02, CF-05, CF-06;
- 13 member rows / 12 analysis units;
- frozen D4 cutoffs/denominators;
- family-authorized categorical fields;
- no pooled cross-family scoring.

### 5.4 Study B — deterministic T1 fault coverage
- 31 canonical valid fault-kind/phase cells;
- no-fault control;
- eight retry-exhaustion boundary schedules;
- 40 total deterministic schedules.

### 5.5 Study C — fixed mixed-schedule T1 population
- seeds 10001–10100;
- 100 predeclared serialized schedules;
- descriptive interpretation only;
- runtime-reachability audit disclosed separately.

### 5.6 Study D — sensitivity
- max transmissions 2/3/4;
- candidate lifetime 2/3/4;
- fixed 12-schedule challenge set;
- 108 total executions.

### 5.7 Formal assurance
- bounded TLA+;
- negative/adverse witnesses;
- Python/formal projection;
- finite-abstraction limitations.

## 6. Results

### 6.1 Matched-family categorical parity — Table 1
- CF-01: B0/B1/B2/T1 all SUCCESS/SYNC/AVAILABLE/SECURE_PROVISIONAL.
- CF-02: all four analysis units SUCCESS/SYNC/AVAILABLE/SECURE_PROVISIONAL with verification
  complete.
- CF-05: B2/T1 both INDETERMINATE/SYNC/DEGRADED after status evidence loss.
- CF-06: B2/T1 both SUCCESS/SYNC/AVAILABLE with replay rejection.
- Conclusion: no categorical-superiority claim.

### 6.2 Deterministic T1 fault behavior — Table 2
- canonical cells: 25 SUCCESS, 4 INDETERMINATE, 1 EXPIRED, 1 SECURE_DEGRADED;
- isolated recovery-phase loss/closure recovered within retry budget;
- post-convergence evidence loss remained INDETERMINATE;
- duplicate/reorder/stale inputs rejected without blocking recovery;
- endpoint restart exposed the clearest failure/degradation boundary;
- retry-exhaustion panel: 6 EXPIRED, 2 SECURE_DEGRADED.

### 6.3 Fixed mixed-schedule characterization — Figure 2
- 74 SUCCESS, 15 INDETERMINATE, 6 SECURE_DEGRADED, 5 EXPIRED;
- reachability audit: 77/191 scheduled actions applied, 43/100 schedules with zero applied
  actions, 24/31 scheduled cells exercised at runtime;
- do not call 74/100 a success rate “under faults.”

### 6.4 Retry/retention sensitivity — Figure 3
- max transmissions 2: 5/12 verified;
- max transmissions 3: 11/12;
- max transmissions 4: 11/12;
- candidate lifetime 2–4 showed no observed effect in this challenge set;
- persistent COMMIT-stage spacecraft restart was not repaired by retries.

### 6.5 Representative adverse traces
- verification evidence loss -> INDETERMINATE while synchronized;
- COMMIT-stage spacecraft restart -> EXPIRED / ground ahead / unsafe;
- CONFIRM-stage restart or exhaustion -> spacecraft ahead / degraded with unsafe security state.

### 6.6 Formal/Python assurance summary
Keep bounded and diagnostic; detailed evidence moves to supplement.

## 7. Discussion

### 7.1 Recovery versus verification evidence
### 7.2 Bounded retransmission and the value of a third transmission opportunity
### 7.3 Endpoint-state persistence as a recovery boundary
### 7.4 Security/availability separation and `SECURE_DEGRADED` terminology
### 7.5 Replay/stale-state rejection
### 7.6 Why matched-family parity is not treatment superiority
### 7.7 Mission-aware TT&C design implications

Avoid universal superiority, causal, cryptographic-proof, or prevalence claims.

## 8. Threats to Validity and Limitations

### 8.1 Construct validity
### 8.2 Simulator/internal validity
### 8.3 External validity / no flight or RF validation
### 8.4 Independent-review status
### 8.5 Non-equivalent cross-treatment timing/retry semantics
### 8.6 Study C scheduled-versus-runtime-applied fault reachability
### 8.7 Fixed challenge-set sensitivity limits
### 8.8 Formal-model bounds/projection limits

## 9. Reproducibility and Artifact Availability

- code/version and execution commit;
- final config/schedules;
- retained bundle SHA-256 and internal manifest;
- derivation script;
- tracked table/figure source data;
- archive/release location when published.

## 10. Conclusion

- answer RQ1-RQ4 within the declared synthetic model;
- emphasize deterministic operational fault findings and state-persistence boundary;
- state limitations explicitly;
- place concrete cryptography, NOS3/cFS, RF, and operational validation in follow-on work.
