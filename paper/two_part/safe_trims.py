"""Output-only prose trims for the two-part review build.

Each trim replaces the span between two anchors in the generated manuscript text. Part I's files are never
edited. Every anchor must occur exactly once, and no number, citation key or code identifier may be lost.
"""

from __future__ import annotations

import re

CONTRIB_1_2 = (
    "1. **A conservative operational comparison framework.** We separate structural metric parity from "
    "semantic comparability and restrict cross-treatment claims to four qualified matched families and "
    "family-authorized categorical fields, so contact duration, retry counts or transmission counts are never "
    "compared across mechanisms that do not measure them equivalently.\n"
    "2. **A bounded TT&C recovery-control treatment.** T1 models resynchronization as an explicit control-state "
    "transaction around an opaque cryptographic core, with candidate creation, activation, confirmation, "
    "retries, expiry, replay rejection and verification evidence represented separately.\n"
)

RELATED_22_25 = """### 2.2 KEM-based SDLS key update

Hülsing, Lange, and Weber propose a standalone key-update mechanism for SDLS based on PQNoise and KEMs that produces fresh key material while leaving SDLS traffic protection untouched, with cryptographic analysis in its stated model and required key confirmation [@hulsing_lange_weber_sdls_key_update]. This motivates B1. The source does not define the simulator's operational questions: when a security association becomes active, whether activation waits for a post-handshake status message, how rollback works after one-sided activation, or what telemetry shows operational recovery. B1 therefore separates source-supported cryptographic completion from project-defined activation policies. The primary mapping activates each endpoint when it locally completes the three-message exchange; an enhanced variant adds authenticated status gating. Neither policy is attributed to the source paper. NIST FIPS 203 standardizes ML-KEM and NIST SP 800-227 gives KEM recommendations [@nist_fips203; @nist_sp800_227], but neither defines a TT&C recovery state machine, so the simulator treats candidate cryptographic values as opaque references and does not implement or validate ML-KEM.

### 2.3 Stateful and continuous key agreement

Ratcheted key exchange keeps evolving state so that new key material replaces earlier state. Poettering and Rösler formalize this and analyze security under state exposure [@poettering_roesler_bidirectional_rke; @poettering_roesler_async_rke]. B2 uses the unidirectional pattern as an operational abstraction, with ground as sender and spacecraft as receiver, and keeps no skipped-state cache, rollback state or recovery checkpoint, so one-sided evolution and state-loss boundaries stay observable. Dowling, Hale, Tian, and Wimalasiri analyze key establishment across space networking architectures and argue that high latency, intermittent availability and long-lived relationships can favor continuous or stateful key agreement, noting that maintaining state does not inherently preclude recovery from state loss [@dowling_hale_tian_wimalasiri_space_key]. That is the problem this paper isolates: the control problem that appears when the ground and spacecraft copies of such state are no longer safely aligned. T1 is not a replacement cryptographic construction. It is a bounded resynchronization layer around an assumed authenticated recovery-control core.

### 2.4 Satellite cybersecurity testbeds

Satellite cybersecurity research is moving toward controlled experimental platforms. AegisSat combines a physical CubeSat with an environment emulator and attack manager [@idan_aegissat]. Castanon Remy et al. propose a seven-attribute fidelity framework for space cybersecurity testbeds [@castanon_remy_space_testbed]. Our simulator has lower hardware and environmental fidelity by design: it has no RF propagation, orbital physics, power behavior or flight computer. Its strength is control-state observability and determinism, since endpoint epoch, candidate, receipt, replay decision, fault application and terminal classification replay exactly. The approaches are complementary: high-fidelity testbeds can later test whether these mechanisms survive concrete flight software, transport, storage, timing and link behavior.

### 2.5 Positioning of this study

The closest literature covers standards for TT&C protection and key management, requirements analyses for post-compromise key management, key-update and continuous-key-agreement designs, and satellite cybersecurity testbeds. These establish that post-compromise key renewal matters and that stateful mechanisms can suit disrupted links. This study focuses on **post-compromise operational resynchronization**. Its variables are ground and spacecraft alignment, candidate activation, evidence completeness, replay and stale rejection, endpoint restart, bounded retransmission, and terminal security and availability classification, not primitive performance. Non-equivalent mechanisms are compared conservatively, with no pooled score. We make no universal priority claim. The contribution is a reproducible, predeclared experimental treatment of the gap between establishing fresh keying material and showing that legitimate TT&C control has returned to a mutually trusted operational state.

"""

SECTION_9 = """## 9. Reproducibility and Artifact Availability

The numerical results trace to an exact code version, a predeclared plan, serialized schedules, retained raw outputs and derived table and figure sources.

### 9.1 Versioned execution identity

The final retained study used:

- plan commit: `cfb730a8191d37863e9e419823686b3c3afe18a2`;
- plan SHA-256:
  `3570834a70c76e020dada459e036786f690698125fe1d9e171e9f945748a1012`;
- execution/runner commit:
  `c630fb4f65ad78211fd3ffb0391000d7ed3629b1`; and
- retained run identifier: `20260814T022506Z-gc630fb4`.

The execution wrapper verified the branch head, clean tracked tree, protected input hashes, repository manifest, plan contract and full regression suite before the final result boundary.

### 9.2 Retained bundle

The retained final bundle has external SHA-256:

```text
b3b8c55a9e522ffe3f7898d7b786583e46a4dc3db0aba9d3947fd6ebdaeecaa1
```

Its internal 16-file checksum manifest verified completely. It holds the final plan input, raw Study A, B, C, and D outputs, processed tables and summaries, figure-source CSVs, execution metadata, and command and runner logs. It is not rewritten when manuscript summaries change.

### 9.3 Derivatives and validation

Derived sources are tracked under `paper/tables/` and `paper/figures/`, and `experiments/scripts/summarize_paper_final_results.py` verifies the run identity and checksum manifest before deriving them. At the final execution boundary 256 repository tests passed, and the plan-bound runner supports `--validate-only` to check the committed plan and schedule contracts without running outcomes. Manuscript-only commits rerun the same checks in CI.

### 9.4 Availability

The repository contains the simulator, final plan, validation and derivation tools, tracked result sources, bounded formal models and the evidence map. The raw bundle stays outside Git history, is identified by the run ID and SHA-256 above, and has not been deposited in a public archive or given a persistent identifier, so a full raw-output audit needs access to it; the author can make it available on reasonable request. Reproducing the results validates the software model, schedules, analysis pipeline and bounded formal evidence, not the cryptographic security of B0 to B2 or T1, and not flight applicability.

"""

CONCLUSION = """## 10. Conclusion

Post-compromise TT&C recovery needs more than fresh key material. Ground and spacecraft endpoints must also agree on which state is operational, survive disrupted delivery without accepting stale or replayed control material, and produce enough evidence to justify resuming trusted command operations.

In a bounded, reproducible software model, T1 matched the abstract baselines' categorical outcomes in the four families where comparison could be defended, so no superiority claim is made. The deterministic study gave the clearest mechanism-level evidence. Isolated loss and contact closure were absorbed within the retry budget, and delayed, duplicated, reordered, stale-counter and stale-replay cases completed while invalid material was rejected. Lost post-convergence evidence left the controller synchronized but `INDETERMINATE`. Endpoint restart around COMMIT or CONFIRM destroyed or separated pending or activated state and produced unsafe asymmetric outcomes. Raising the transmission budget from two to three repaired the repeated omission and contact challenges in that fixed set, a fourth opportunity added no observed benefit, and none of them repaired the COMMIT-stage restart failure. Retransmission can recover missing messages; it cannot reconstruct protocol state that no longer exists. The fixed 100-schedule population is descriptive only: many later-attempt faults were never reached at runtime, so its 74 successful schedules are not a fault-conditioned success rate. Bounded TLA+/Python comparisons agree on selected traces over the declared abstraction but do not establish refinement, cryptographic security, or completeness of the model.

Part II extended the question to the activation exchange. In an exact model, resumable verification (an assumption outside the standards) cleared indeterminate outcomes that plain retries could not, and recovery reached the declared 0.95 level in 83-90% of multi-attempt configurations with divergence, not almost always, in the model, not on a real link.

The design implication is architectural: separate candidate state from operational state, bind recovery to monotonic authority and evidence, make activation and confirmation rules explicit, retain enough protected state to survive restart or support authenticated re-initiation, and keep security, availability, alignment and verification distinct when deciding whether normal TT&C control may resume.

Future work should instantiate the recovery-control layer with concrete reviewed cryptographic mechanisms, anchor the exchange model to measured link loss and contact data, obtain an independent review of the exchange abstraction, integrate the logic with representative flight and ground software such as cFS/NOS3, and test it under realistic link behavior. The present contribution is a reproducible experimental foundation for one narrow question: how trusted TT&C state is restored without converting key update into lockout or false confidence after compromise.

"""


def _span(text: str, start: str, end: str, new: str) -> str:
    if text.count(start) != 1 or text.count(end) != 1:
        raise SystemExit(f"safe-trim anchor not found exactly once: {start[:40]!r} / {end[:40]!r}")
    a, b = text.index(start), text.index(end)
    if b <= a:
        raise SystemExit(f"safe-trim anchors out of order: {start[:40]!r}")
    return text[:a] + new + text[b:]


def apply_safe_trims(text: str) -> str:
    text = _span(text, "1. **A conservative operational comparison framework.**", "3. **Fault-response findings.**", CONTRIB_1_2)
    text = _span(text, "### 2.2 KEM-based SDLS key update", "## 3. System and Threat Model", RELATED_22_25)
    text = _span(text, "## 9. Reproducibility and Artifact Availability", "### 9.7 Part II artifacts", SECTION_9)
    text = text.replace("### 9.7 Part II artifacts", "### 9.5 Part II artifacts", 1)
    if text.count("identified in Section 9.7") != 1:
        raise SystemExit("Section 9.7 cross-reference not found exactly once")
    text = text.replace("identified in Section 9.7", "identified in Section 9.5", 1)
    text = _span(text, "## 10. Conclusion", "## Acknowledgment", CONCLUSION)
    text = apply_section_7_and_prior_art(text)
    for key in ("ccsds_sdls_355_0_b_2", "hulsing_lange_weber_sdls_key_update", "nist_fips203", "nist_sp800_227",
                "poettering_roesler_bidirectional_rke", "poettering_roesler_async_rke",
                "dowling_hale_tian_wimalasiri_space_key", "idan_aegissat", "castanon_remy_space_testbed"):
        if "@" + key not in text:
            raise SystemExit("citation lost by a trim: " + key)
    return text


BADER_SENTENCE_OLD = "requirement. It identifies stateful authenticated key agreement or ratcheted key evolution as a\npromising direction."
BADER_SENTENCE_NEW = (
    "requirement. It identifies stateful authenticated key agreement or ratcheted key evolution as a\n"
    "promising direction, and it notes that strong post-compromise security seems to imply that endpoints that "
    "fall out of sync cannot re-establish communication, leaving open whether a solution can offer both "
    "[@bader_ttc_key_management]."
)
HULSING_SENTENCE_OLD = "Hülsing, Lange, and Weber propose a standalone key-update mechanism for SDLS based on PQNoise and KEMs that produces fresh key material while leaving SDLS traffic protection untouched, with cryptographic analysis in its stated model and required key confirmation [@hulsing_lange_weber_sdls_key_update]."
HULSING_SENTENCE_NEW = HULSING_SENTENCE_OLD + (
    " The authors note that the exchange cannot reorder or re-request lost or out-of-order packets, so it must assume an "
    "attack and drop the connection unless the fragmentation layer provides those functions "
    "[@hulsing_lange_weber_sdls_key_update]."
)

SECTION_7_START = "## 7. Discussion"
SECTION_7_END = "### 7.8 Implications for mission-aware TT&C recovery"
SECTION_7_A = """## 7. Discussion

The retained experiment shifts the paper's central contribution away from a treatment-ranking claim and toward an operational question: what prevents a key-recovery mechanism from becoming a trusted TT&C recovery mechanism when communication is intermittent and endpoint state can diverge? Several common communication faults are recoverable with a bounded transaction, but state convergence is not the same as verified operational recovery, and retransmission cannot compensate for lost endpoint protocol state.

### 7.1 Convergence is not the same as verified recovery

The clearest recurring pattern separates synchronization from evidence of recovery completion. In deterministic Study B, loss of the test-command or status-telemetry opportunity left both endpoints synchronized, yet the terminal result was `INDETERMINATE` rather than `SUCCESS`. The same principle appears in matched family CF-05, where B2 and T1 both converged but lacked the required telemetry and verification evidence.

This is intentionally conservative. A procedure that changes key state but cannot show that trusted command and telemetry operations work afterward should not be treated as operationally recovered, because legitimate state advancement can still leave an unusable control path. The result supports separating at least three properties: key-state transition, endpoint synchronization, and mission-facing verification. Making these explicit, instead of collapsing them into one success flag, is the design lesson; the simulator does not establish cryptographic security.

### 7.2 Bounded retransmission handles omission but not state destruction

Single `DROP` and `CONTACT_CLOSE` faults during the four recovery-message phases were recovered within the configured retry budget. The sensitivity experiment further showed that a third transmission opportunity changed six challenge cases from non-success to verified success, whereas a fourth produced no additional observed benefit. Three transmissions are not globally optimal; bounded retransmission absorbs a class of omission and contact failures, with a benefit that depends on the challenge set.

The persistent spacecraft-restart failure marks the boundary. A restart at COMMIT destroyed the pending protocol state needed to complete the transaction, and additional retries cannot reconstruct state the endpoint no longer retains. Recoverable transport interruption and recoverability of protocol state are separate design problems: pending state may need protected persistence across restart, or the protocol may need an authenticated re-initiation path that abandons the interrupted transaction without leaving the endpoints asymmetric.

### 7.3 Activation boundaries create asymmetric failure modes

Exhaustion before or at COMMIT left the ground side ahead and produced `EXPIRED`, `UNSAFE`, and `UNAVAILABLE`. Exhaustion at CONFIRM left the spacecraft side ahead and produced a degraded, unsafe asymmetric state. The difference reflects where each endpoint commits the candidate state: once one endpoint has advanced, losing the evidence or final message the other needs can create an asymmetric terminal condition even though every prior message was legitimate.

This also bears on the B1 mapping. The source construction motivates key-update and confirmation semantics, but the question of when a recovered key becomes operational is an integration decision, not a theorem inherited from the cryptographic source [@hulsing_lange_weber_sdls_key_update]. Any operational mapping to SDLS-style systems should document the activation policy explicitly [@ccsds_sdls_355_0_b_2; @ccsds_sdls_ep_355_1_b_1].

### 7.4 Security and availability must remain separate

The raw enum `SECURE_DEGRADED` predates the final experiment and should be read cautiously. In the retained restart and confirmation-exhaustion cases the independent `security_state` field is `UNSAFE`, so the enum label is not evidence that the terminal state is secure. Availability, alignment, and security classification are different dimensions: a synchronized system can lack verification evidence, an available system can be unsafe, and an asymmetric system can stay partly operational while failing the recovery security objective. The diagnostic expansion of the formal model made the same point by constructing an `AVAILABLE_UNSAFE` path in which availability and convergence coexist with candidate exposure. It does not show that such a path is likely in practice, but it shows why a single composite success metric would hide important state distinctions.

### 7.5 Replay and stale-state rejection are necessary but not sufficient

The deterministic replay, stale-counter, duplicate, and reordering cases were all rejected without blocking completion, so malformed, stale, or duplicate material does not silently replace the accepted transaction. Replay resistance alone is still not a complete recovery story. The dominant adverse cases were missing evidence, exhausted delivery opportunities, and destroyed endpoint state, not successful replays. Recovery for intermittent TT&C needs both message-validity protections and explicit recovery-state management. The B2 abstraction likewise separates traffic-key exposure from sender and receiver state exposure, following ratcheted key-exchange work [@poettering_roesler_bidirectional_rke; @poettering_roesler_async_rke], without inheriting its proofs.

### 7.6 Matched-family parity is a boundary, not a negative result

Study A found categorical parity, not treatment superiority, and the comparability work excluded families whose fields or semantics were not equivalent enough for a defensible cross-treatment claim. Within the four retained families, T1 reached the same authorized terminal classifications as the corresponding abstract baselines, a sanity boundary showing that the controller does not obtain its fault-handling story from obviously different classifications in the simplest matched cases.

Studies B and D instead document T1's mechanisms alone and show no advantage over any baseline: Study F (Supplementary Table S7) found that, with retransmission, a baseline absorbs a lost status message that T1 leaves indeterminate by rule.

### 7.7 The mixed-schedule panel is descriptive, not a reliability estimate

Study C looked capable of yielding a simple synthetic success proportion, but the post-execution reachability audit shows that reading would mislead. Only 77 of 191 scheduled actions were reached, 43 schedules applied no fault action, and seven of the 31 referenced fault-kind and phase cells were not exercised at runtime. The retained run stays valid: the population was predeclared and executed correctly, and the audit reveals a property of the generator, since scheduling a later-attempt fault does not force it to occur. Study C is secondary evidence about the outcome distribution of a fixed synthetic population, while deterministic Study B gives the controlled cell-level evidence.

"""
SECTION_7_B = """### 7.8 Implications for mission-aware TT&C recovery

Five design implications follow from the bounded evidence. First, a recovery transaction should keep **candidate state** distinct from **operational state**, and candidates should not authorize ordinary command traffic before the defined activation condition holds. Second, activation should be paired with authenticated evidence that survives intermittent contact, since losing that evidence leaves the implementation synchronized but unable to justify a success classification. Third, message identifiers, epoch and counter checks, and exact transaction binding support idempotent recovery: the duplicate, stale, and reordered cases completed because invalid material was rejected without discarding valid progress. Fourth, restart behavior belongs in the protocol design, not the transport layer. If pending state is volatile, a reset near activation can create an unsafe asymmetric state, so durable protected state or authenticated transaction restart is a more relevant mitigation than more retries. Finally, recovery policy should expose security and availability separately to mission decision logic, which needs to know whether the state is trusted, whether command and telemetry verification succeeded, and whether enough evidence was retained to explain the transition.

"""
SECTION_7_9 = """### 7.9 Role of the formal evidence

The bounded TLA+ work gives a second encoding of the control-state view and makes adverse outcome paths explicit. The zero-mismatch projection results for the selected success and adverse witnesses show consistency between those bounded traces and the Python model over the declared fields. The evidence stays supporting: the macro-step mapping is project-defined, the state spaces are finite, and no refinement relation is proven. The diagnostic expansion also shows that outcome reachability depends on which transitions the abstraction contains, since three outcomes absent from the original model became reachable only when explicit diagnostic transitions were added. The formal results demonstrate transparency and internal consistency of the modeled control logic, not cryptographic or flight-system correctness.

"""


def apply_section_7_and_prior_art(text: str) -> str:
    if text.count(BADER_SENTENCE_OLD) != 1:
        raise SystemExit("Bader anchor not found exactly once")
    text = text.replace(BADER_SENTENCE_OLD, BADER_SENTENCE_NEW, 1)
    if text.count(HULSING_SENTENCE_OLD) != 1:
        raise SystemExit("Hulsing anchor not found exactly once")
    text = text.replace(HULSING_SENTENCE_OLD, HULSING_SENTENCE_NEW, 1)
    text = _span(text, SECTION_7_START, SECTION_7_END, SECTION_7_A)
    text = _span(text, SECTION_7_END, "CCSDS 350.5-G-2 already recommends", SECTION_7_B)
    text = _span(text, "### 7.9 Role of the formal evidence", "### 7.10 Part II and the Part I mechanisms", SECTION_7_9)
    for must in ("77 of 191", "43 schedules", "seven of the 31", "six challenge cases", "Study F (Supplementary Table S7)"):
        if must not in text:
            raise SystemExit("Section 7 trim lost a required fact: " + must)
    return text
