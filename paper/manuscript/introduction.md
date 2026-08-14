# 1. Introduction

Telemetry, tracking, and command (TT&C) links form the operational control path between a
spacecraft and its authorized ground segment. Loss of confidence in the cryptographic state of
that path is therefore not merely a confidentiality problem: it can become a control-recovery
problem. CCSDS Space Data Link Security (SDLS) standardizes data-link security processing for
space links, while the SDLS Extended Procedures define auxiliary key-management, security
association, and monitoring/control services [@ccsds_sdls_355_0_b_2;
@ccsds_sdls_ep_355_1_b_1]. These standards provide an important foundation, but operational
recovery after key compromise must also cope with characteristics of space communication:
contact opportunities can be intermittent, bandwidth is constrained, delivery may be disrupted,
and a ground endpoint may not be able to observe spacecraft state continuously.

Recent work has made the post-compromise key-management problem increasingly explicit. Bader
identifies post-compromise security, long-term security, and protection from the beginning of a
contact as central TT&C key-management requirements, and argues that stateful key-evolution
approaches are promising for this environment [@bader_ttc_key_management]. Hülsing, Lange, and
Weber subsequently proposed a KEM-based key-update mechanism that provides fresh SDLS key
material without changing the SDLS traffic-protection protocol
[@hulsing_lange_weber_sdls_key_update]. Broader work on key establishment in space likewise
argues that intermittent connectivity, latency, and long-lived communication relationships make
stateful or continuous key agreement attractive alternatives to repeatedly establishing
Internet-style sessions [@dowling_hale_tian_wimalasiri_space_key].

Those developments address an essential cryptographic question: how can new keying material be
established after compromise? A distinct operational question remains once a key-update
construction is placed into a disrupted TT&C setting: **how do legitimate ground and spacecraft
endpoints regain a mutually trusted operational state when recovery messages, confirmation
evidence, or endpoint state can be lost?** A cryptographic exchange can be secure in its stated
model while an operational integration still faces ambiguity about activation, rollback,
retransmission, stale state, and what evidence is sufficient to declare the spacecraft recovered.
If one endpoint activates a candidate key and the final confirmation is lost, the cryptographic
exchange and the operational state machine no longer answer exactly the same question.

This paper studies that operational recovery layer in a controlled software environment. We use
three project-defined baseline abstractions—an SDLS Extended Procedures-style symmetric rekeying
baseline (B0), a Triple-KEM/PQNoise-inspired update baseline (B1), and a strict ratcheted
key-evolution baseline (B2)—and compare them only where their semantics can be matched
conservatively. We then evaluate a bounded resynchronization treatment (T1) that introduces an
explicit recovery authority, forward epoch negotiation, bounded candidate state, bounded
retransmission, replay/stale-state rejection, asymmetric activation handling, and
post-convergence command/telemetry verification.

The study is intentionally hands-on but safe and reproducible. It uses no operational satellite,
live RF transmission, mission credentials, or flight system. Instead, a deterministic simulator
represents one authoritative ground security domain and one spacecraft security function across
discrete intermittent contact windows. Faults are injected at explicit recovery phases, and the
final experiment was predeclared before outcome inspection. The retained study contains four
matched comparison families, 40 deterministic T1 schedules, a fixed 100-schedule mixed-fault
population, a 3 x 3 sensitivity grid producing 108 executions, and bounded TLA+/Python
cross-validation evidence.

The paper makes four contributions.

1. **A conservative operational comparison framework.** We separate structural metric parity
   from semantic comparability and restrict cross-treatment claims to four qualified matched
   families and family-authorized categorical fields. This prevents contact duration, retry
   counts, or transmission counts from being compared across mechanisms that do not measure them
   equivalently.
2. **A bounded TT&C recovery-control treatment.** T1 models post-compromise resynchronization as
   an explicit control-state transaction around an opaque cryptographic core. Candidate creation,
   activation, confirmation, retries, expiry, replay rejection, and verification evidence are
   represented separately.
3. **Predeclared fault and sensitivity experiments.** The study deterministically exercises every
   semantically implemented T1 fault-kind/phase cell, retains adverse outcomes, characterizes a
   fixed mixed-schedule population, and evaluates bounded retry/candidate-lifetime sensitivity
   without inferential or prevalence claims.
4. **Mechanism-level recovery findings.** The retained results distinguish state convergence from
   verified recovery, show that isolated delivery faults can be absorbed by bounded
   retransmission, and identify endpoint-state loss around activation as a qualitatively different
   failure that additional retries do not repair.

The results do not support a universal superiority claim for T1 over B0, B1, or B2. In the four
defensibly matched families, the treatments produced the same authorized categorical terminal
classifications. T1's distinctive evidence instead comes from the controlled fault studies,
where the experiment can isolate operational mechanisms without pretending that baseline timing
and retry semantics are equivalent.

The scope of the claims is deliberately narrow. Cryptographic operations are abstract; the
project does not implement the complete source constructions or inherit their proofs. No
independent cryptography review of the source-to-model mappings was completed. The experiment
does not establish strong post-compromise security, CCSDS/SDLS conformance, causal superiority,
flight readiness, or real-world satellite fault prevalence. Its contribution is controlled
experimental evidence about recovery-control behavior inside a declared, reproducible TT&C
model.
