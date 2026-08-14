# Manuscript Outline — Hands-On TT&C Post-Compromise Recovery Study

## 1. Introduction
- TT&C security problem: key compromise plus ground-space state divergence.
- Gap between cryptographic key update and operational resynchronization/availability.
- Safe controlled software experiment.
- Contributions: baseline mappings, T1, fault experiments, matched comparison, bounded assurance.

## 2. Background and Related Work
### 2.1 Satellite TT&C security-state recovery
### 2.2 B0 SDLS-style rekeying abstraction
### 2.3 B1 Triple-KEM/PQNoise-inspired update
### 2.4 B2 URKE-inspired state evolution
### 2.5 Post-compromise recovery gap

State that source proofs are not inherited by the simulator.

## 3. System and Threat Model
### 3.1 Ground and spacecraft endpoints
### 3.2 Operational key state and recovery authority
### 3.3 Compromise scopes
### 3.4 Ground-space divergence
### 3.5 Attacker capabilities and bounded passive interval
### 3.6 Excluded threat classes

## 4. Recovery Designs
### 4.1 B0
### 4.2 B1 activation variants
### 4.3 B2 strict state evolution
### 4.4 T1 bounded resynchronization
### 4.5 Outcome/security/availability classifications

Planned Figure 1: experimental architecture and evidence flow.

## 5. Experimental Method
### 5.1 Research questions
- RQ1 matched recovery behavior.
- RQ2 T1 fault robustness.
- RQ3 T1 sensitivity.
- RQ4 bounded formal/Python agreement.

### 5.2 Reproducibility and capture
- exact commit/config;
- serialized schedules;
- raw/derived outputs;
- checksums/manifests;
- exclusion/rerun policy.

### 5.3 Study A — matched treatment families
- CF-01, CF-02, CF-05, CF-06;
- 13 member rows / 12 analysis units;
- frozen D4 cutoffs/denominators;
- allowed categorical fields;
- no pooled cross-family scoring.

### 5.4 Study B — deterministic T1 fault coverage
- valid fault-kind/phase cells;
- canonical and boundary-attempt schedules;
- trace and terminal-state evidence.

### 5.5 Study C — fixed mixed-fault T1 panel
- 100 predeclared seeds;
- explicit generator distribution;
- schedule checksums;
- descriptive interpretation.

### 5.6 Study D — sensitivity
- max transmissions 2/3/4;
- candidate lifetime 2/3/4;
- fixed 12-schedule panel.

### 5.7 Formal assurance
- bounded TLA+;
- negative/adverse witnesses;
- Python/formal projection;
- abstraction limits.

## 6. Results
### 6.1 Matched-family categorical outcomes
Planned Table 1.

### 6.2 Deterministic T1 fault coverage
Planned Table 2.

### 6.3 Mixed-fault robustness
Planned Figure 2.

### 6.4 Sensitivity
Planned Figure 3.

### 6.5 Representative adverse traces
Select only after full retained-population analysis.

### 6.6 Formal/Python assurance summary
Keep bounded and diagnostic; detailed evidence can move to supplement.

## 7. Discussion
### 7.1 Mechanisms explaining recovery/failure
### 7.2 Security-availability trade-offs
### 7.3 Last-message/evidence-retention effects
### 7.4 Replay/stale-state handling
### 7.5 Where T1 helps and where it fails/degrades
### 7.6 Mission-aware TT&C implications

Avoid universal superiority, causal, cryptographic-proof, or prevalence claims.

## 8. Threats to Validity and Limitations
### 8.1 Construct validity
### 8.2 Simulator/internal validity
### 8.3 External validity / no flight or RF validation
### 8.4 Independent-review status
### 8.5 Non-equivalent cross-treatment timing/retry semantics
### 8.6 Generated fault-population limitations
### 8.7 Formal-model bounds/projection limits

## 9. Reproducibility and Artifact Availability
- code/version;
- final configs/schedules;
- checksums/manifests;
- analysis scripts;
- table/figure source data;
- archive/release.

## 10. Conclusion
- answer RQ1-RQ4 within the declared model;
- summarize reproducible findings;
- state limitations;
- place concrete crypto/NOS3/cFS/RF work in future research.
