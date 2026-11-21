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
    for key in ("ccsds_sdls_355_0_b_2", "hulsing_lange_weber_sdls_key_update", "nist_fips203", "nist_sp800_227",
                "poettering_roesler_bidirectional_rke", "poettering_roesler_async_rke",
                "dowling_hale_tian_wimalasiri_space_key", "idan_aegissat", "castanon_remy_space_testbed"):
        if "@" + key not in text:
            raise SystemExit("citation lost by a trim: " + key)
    return text
