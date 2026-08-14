# 8. Threats to Validity and Limitations

The experiment was deliberately scoped as a bounded, synthetic, software-only study. This design
enabled deterministic replay, outcome-blind predeclaration, exact fault placement, and
reproducible state inspection, but it also limits what can be inferred about concrete
cryptographic protocols and operational spacecraft.

## 8.1 Construct validity

The principal constructs are alignment, security state, availability state, verification state,
and terminal outcome. These are explicit model variables rather than direct measurements of a
flight system.

The most important naming limitation is the historical `SECURE_DEGRADED` outcome enum. In the
retained restart and confirmation-exhaustion cases, the independent `security_state` field is
`UNSAFE`. The manuscript therefore treats the enum as a reproducibility label and interprets
security from the separate security-state dimension. A reader should not infer cryptographic
security from the enum name.

Similarly, `SUCCESS` is defined operationally inside the model and requires the modeled
post-recovery evidence. It is not equivalent to proof of cryptographic secrecy, authentication
security, or mission readiness.

Mitigation comes from reporting the component state dimensions alongside the composite outcome
and from preserving raw scenario-level evidence rather than relying on a single score.

## 8.2 Internal validity

The simulator is deterministic for a fixed configuration and serialized schedule, which improves
reproducibility but does not represent all timing, concurrency, storage, or implementation effects
of a deployed system.

The final plan, schedules, and analysis boundaries were committed before the retained final
outcomes were executed. The retained run was executed once from a clean exact commit, and the
bundle plus internal checksum manifest were preserved. This reduces the risk of outcome-driven
parameter or denominator changes.

Study C revealed a specific internal-validity limitation in the schedule generator: a scheduled
later-attempt fault may never become reachable because the transaction can complete or terminate
before that attempt. The 100 schedules contained 191 planned actions, but only 77 were applied;
43 schedules applied no fault action, and runtime execution covered 24 of 31 scheduled
fault-kind/phase cells. The manuscript therefore does not interpret Study C as a fault-conditioned
success experiment. Deterministic Study B is used for explicit fault-cell coverage.

The implementation and experiment boundary were regression-tested before execution, but testing
cannot exclude all software defects. Any later-discovered defect would require a separately
identified correction run rather than silent replacement of the retained data.

## 8.3 Conclusion validity

The study does not use inferential statistics to claim treatment effects. Study A contains only
four qualified matched families and deliberately restricts comparison to fields with defensible
semantic equivalence. B1 activation-policy variants are not counted as independent replications.

Study C's denominator of 100 is a fixed synthetic schedule population rather than a probability
sample from satellite operations. Study D uses 12 deliberately selected challenge schedules per
parameter cell. Its 5/12 and 11/12 verification-completion counts therefore describe that fixed
challenge set and do not establish confidence intervals, real-world probabilities, or a universal
optimal retry budget.

The absence of a change across candidate lifetimes two through four contacts should likewise be
read as "no observed effect in this challenge set," not as evidence that candidate lifetime is
generally irrelevant.

## 8.4 Baseline-mapping validity

B0, B1, and B2 are operational abstractions used for controlled comparison. B1 is motivated by
the Hülsing-Lange-Weber SDLS key-update construction, and B2 is motivated by ratcheted
key-exchange state-evolution work. The simulator does not implement those source constructions
and does not inherit their security proofs.

The source-to-model mappings were internally reviewed and regression-tested, but no independent
cryptography review was completed before manuscript analysis. The paper therefore must describe
the baselines as project-defined abstractions and must not claim independent approval,
cryptographic equivalence, or inherited post-compromise-security guarantees.

This limitation is partly mitigated by explicit source notes, separation between source claims
and simulator-added activation/telemetry semantics, conservative matched-family selection, and
journal peer review. A later independent specialist review could strengthen the mapping, but it
is not treated as evidence already obtained.

## 8.5 External validity

No live RF link, operational satellite, mission control system, flight computer, cFS/NOS3
integration, hardware security module, or production key-management infrastructure was used.
Network contact opportunities and endpoint restarts are modeled events rather than measurements
from an operational mission.

The experiment therefore cannot establish flight readiness, CCSDS/SDLS conformance, timing
behavior on a real spacecraft bus, RF susceptibility, or operational mission reliability. It
also does not address implementation-specific side channels, storage wear, radiation-induced
faults, clock drift, link-budget variation, or vendor-specific key-management behavior.

The current study is best interpreted as mechanism-oriented experimental evidence that identifies
recoverable and non-recoverable control-state patterns worth testing in higher-fidelity
environments. NOS3/cFS integration, concrete cryptography, and RF/operational validation are
follow-on work rather than missing prerequisites for the bounded software study.

## 8.6 Cryptographic validity

Cryptographic operations are abstracted. The experiment does not implement ML-KEM, the complete
Triple-KEM construction, a concrete ratcheted key-exchange protocol, or a production SDLS
cryptographic stack.

Consequently, the results do not establish confidentiality, authenticity, forward secrecy,
post-compromise security, resistance to concrete cryptanalysis, or correct use of a standardized
KEM. The threat model and recovery logic use cryptographic assumptions as inputs; they do not
prove those assumptions.

The distinction is especially important when interpreting `SECURE_PROVISIONAL` and `UNSAFE`:
these are model classifications based on the declared exposure/state rules, not outputs of a
cryptographic proof.

## 8.7 Formal-model validity

The TLA+ evidence is bounded and uses a declared projection from formal variables to Python
controller state. Selected success and adverse witnesses matched the Python projection with zero
recorded mismatches, but this is not a refinement proof or implementation-equivalence result.

The macro-step mapping compresses some Python operations into a formal transition. The finite
model does not contain every implementation state or every environmental behavior. In Phase 12,
`DIVERGED`, `AVAILABLE_UNSAFE`, and `LOCKED` were absent from the original transition
assignments; Phase 13 made them reachable only through an explicit opt-in diagnostic expansion.
This demonstrates that bounded non-reachability depends on abstraction structure and cannot be
interpreted as impossibility.

Formal evidence is therefore used as supporting consistency evidence, not as proof of
cryptographic security, liveness, or completeness.

## 8.8 Reproducibility and artifact validity

The retained experiment is tied to an exact execution commit, exact plan SHA-256, serialized
schedules, a unique run identifier, and an external retained-bundle SHA-256. The bundle's
16-file internal checksum manifest was verified, and manuscript-facing table/figure source data
are derived from that retained run.

This substantially reduces ambiguity about which code and data support the manuscript. It does
not guarantee that future software environments will reproduce byte-identical platform metadata
or timing, but the experiment uses standard-library Python for the principal execution/summary
paths and records the relevant configuration identities.

The raw retained bundle is intentionally not rewritten when manuscript summaries are produced.
Derived tables are traceable back to the preserved run.

## 8.9 Ethical, legal, and safety scope

The study is synthetic and software-only. It does not transmit to satellites, interfere with RF
spectrum, use real mission credentials, access third-party spacecraft, or exercise unauthorized
systems. No new human-subject data are collected for this experiment.

This scope reduces ethical and legal risk and makes the experiment reproducible, but it also
limits ecological validity. The paper therefore presents the work as controlled cybersecurity
research rather than operational penetration testing or flight validation.

## 8.10 Summary of claim boundaries

Within these limitations, the strongest defensible claims are about control-state behavior in
the declared model: conservative verification semantics, bounded recovery from selected
communication faults, rejection of stale/replayed material, sensitivity to retry budget in a
fixed challenge set, and restart/state-persistence failure boundaries.

The study does not establish universal treatment superiority, real-world reliability, causal
effectiveness, cryptographic security, strong post-compromise security, CCSDS/SDLS conformance,
or operational-spacecraft applicability.
