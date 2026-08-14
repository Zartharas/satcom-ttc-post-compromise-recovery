# 2. Background and Related Work

## 2.1 TT&C security and SDLS

CCSDS SDLS defines data-link security processing that can be used with CCSDS telemetry,
telecommand, and Advanced Orbiting Systems links to provide authentication and/or
confidentiality at the data-link layer [@ccsds_sdls_355_0_b_2]. The SDLS Extended Procedures
provide auxiliary key-management, security-association management, and monitoring/control
services needed to operate an SDLS implementation [@ccsds_sdls_ep_355_1_b_1]. The associated
2024 Green Books document the concept and rationale for both the base protocol and Extended
Procedures [@ccsds_sdls_rationale_350_5_g_2; @ccsds_sdls_ep_rationale_350_11_g_1].

The operational context matters for key management. TT&C communication may be available only
during ground-contact windows, and the first usable frame of a contact can be operationally
important. Bader formalizes this as an all-frame protection requirement and emphasizes that
satellite key-management concepts must account for long mission lifetimes, limited contact time,
and the possibility of ground-side key compromise [@bader_ttc_key_management]. That work
concludes that SDLS is suitable for traffic protection when configured appropriately but that
the SDLS Extended Procedures do not by themselves satisfy the stated post-compromise-security
requirement. It identifies stateful authenticated key agreement or ratcheted key evolution as a
promising direction.

Our work adopts the same general motivation but asks a different question. We do not attempt to
re-evaluate SDLS conformance or prove a cryptographic post-compromise-security property. Instead,
we model what happens operationally when legitimate endpoints must re-establish a common trusted
state after compromise and delivery/state faults occur during the transition.

## 2.2 KEM-based SDLS key update

Hülsing, Lange, and Weber propose a standalone key-update/establishment mechanism for SDLS based
on PQNoise and KEMs [@hulsing_lange_weber_sdls_key_update]. Their construction is designed to
produce fresh key material for SDLS while leaving the SDLS traffic-protection protocol itself
untouched. The paper provides cryptographic security analysis in its stated model and requires
key confirmation.

This construction motivates B1. However, the source does not define the simulator's operational
questions: exactly when an SDLS security association becomes active, whether activation should
wait for a post-handshake status message, how rollback should work after one-sided activation, or
what telemetry evidence constitutes operational recovery. B1 therefore separates source-supported
cryptographic completion from project-defined activation policies. The primary mapping activates
each endpoint when that endpoint locally completes the three-message exchange; an enhanced
comparison variant adds authenticated status gating. Neither policy is attributed to the source
paper.

NIST FIPS 203 standardizes ML-KEM, and NIST SP 800-227 provides general recommendations for KEM
use [@nist_fips203; @nist_sp800_227]. These publications establish current KEM terminology and
implementation guidance, but they do not define a TT&C recovery state machine. Our simulator
therefore treats candidate cryptographic values as opaque references rather than claiming to
implement or validate ML-KEM.

## 2.3 Stateful and continuous key agreement

Ratcheted key exchange maintains evolving protocol state so that new key material can replace
earlier state. Poettering and Rösler's ratcheted-key-exchange work formalizes sender/receiver
state evolution and analyzes security under state exposure
[@poettering_roesler_bidirectional_rke; @poettering_roesler_async_rke]. B2 uses the
unidirectional state-evolution pattern as an operational abstraction with ground as sender and
spacecraft as receiver. The strict model deliberately retains no skipped-state cache, rollback
state, or recovery checkpoint so that one-sided evolution and state-loss boundaries remain
observable.

More recent space-specific work by Dowling, Hale, Tian, and Wimalasiri analyzes key establishment
across space networking architectures and argues that high latency, intermittent availability,
and long-lived communication relationships can favor continuous/stateful key agreement over
repeated session establishment [@dowling_hale_tian_wimalasiri_space_key]. Their work considers
how continuous key agreement, including MLS-style approaches, could fit DTN or IP-oriented space
protocol stacks and notes that maintaining state does not inherently preclude recovery from state
loss.

That observation is directly adjacent to our focus. Continuous key agreement addresses how
fresh key state may evolve over time; this paper experimentally isolates the control problem that
appears when the legitimate ground and spacecraft copies of that state are no longer safely
aligned. T1 is not proposed as a replacement cryptographic construction. It is a bounded
operational resynchronization layer around an assumed authenticated recovery-control core.

## 2.4 Satellite cybersecurity testbeds

Satellite cybersecurity research has increasingly moved from conceptual threat analysis toward
controlled experimental platforms. AegisSat combines a physical Earth-based CubeSat with an
environment emulator, attack manager, telemetry collection, and repeated attack experiments
[@idan_aegissat]. Castanon Remy et al. propose a seven-attribute fidelity framework for space
cybersecurity testbeds and demonstrate it with a concrete space/ground/link/user-segment testbed
[@castanon_remy_space_testbed]. These efforts emphasize the value of explicit system models,
threat models, reproducible data collection, and safe experimentation.

Our simulator has lower hardware and environmental fidelity than those platforms by design. It
does not emulate RF propagation, orbital physics, power behavior, or a flight computer. Its
strength is instead **control-state observability and determinism**: endpoint epoch, candidate,
receipt, replay decision, fault application, and terminal classification can be replayed exactly.
This makes the platform suitable for isolating recovery-state transitions that would be harder to
attribute in a more physically realistic testbed.

The approaches are complementary. High-fidelity testbeds can later evaluate whether the
control-state mechanisms observed here survive concrete flight software, transport, storage,
timing, and link behavior. The current study first establishes a reproducible mechanism-level
baseline.

## 2.5 Positioning of this study

The closest literature falls into four groups: standards for TT&C traffic protection and
management; requirements analyses for post-compromise TT&C key management; cryptographic
key-update or continuous-key-agreement designs; and general satellite cybersecurity testbeds.
These works establish that post-compromise key renewal is important and that stateful mechanisms
can be appropriate for disrupted space links.

The present study focuses more narrowly on **post-compromise operational resynchronization**. Its
experimental variables are not cryptographic primitive performance but ground/space alignment,
candidate activation, evidence completeness, replay/stale rejection, endpoint restart, bounded
retransmission, and terminal security/availability classification. The comparison design also
treats non-equivalent mechanisms conservatively rather than deriving a pooled treatment score.

Accordingly, we do not make a universal priority claim. The contribution is a reproducible,
predeclared experimental treatment of a specific gap between establishing fresh keying material
and demonstrating that legitimate TT&C control has returned to a mutually trusted operational
state.
