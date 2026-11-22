"""Round-9 output-only manuscript fixes (external-reviewer comments MC1-MC8 and minors).

Applied after review_fixes.apply_review_fixes. Edits the generated manuscript only; Part I source files
are untouched. Every anchor must match exactly once or the build stops.
"""
import re

from review_fixes import _rep, _span


def _all(text, old, new, expect):
    n = text.count(old)
    if n != expect:
        raise SystemExit(f"review_fixes_r9 expected {expect} of {old[:50]!r}, found {n}")
    return text.replace(old, new)


STUDY_F = """### 5.11 Study F: baselines under step-level faults (post hoc)

Study F is a later, post hoc, descriptive run, planned under tag `study-f-plan-v1` and not part of the frozen Part I. It applies step-level faults to B0, B1 (local and deferred activation) and B2 from the Part I start state, at transmission budget 1 (each message sent once) and budget 3 (up to three transmissions of a lost message, an assumption favorable to the baselines). A cell is a flow, step, fault kind and number of consecutive transmissions lost; a message is delivered when fewer transmissions are lost than the budget, so the loss result follows from the engine's rule. The grid has 116 cells (58 per budget); 44 undefined combinations are not run. B0 and B1 under local activation end at activation with no verification step, so verification-loss cells exist only for B1 with deferred activation and for B2. At budget 1 every single-loss cell ended without success; at budget 3 every cell with one or two consecutive losses succeeded (Supplementary Table S7).

"""

STUDY_G = """### 5.12 Study G: T1 with verification retransmission (post hoc)

Study G is a post hoc, exploratory run by the same author with an AI assistant, not registered; its protocol was hashed beforehand. It repeats the Study F loss grid for T1 with the test-command and status-telemetry steps given three transmissions, as for the baselines, (86 cells, 43 per arm). With the larger budget the four canonical `INDETERMINATE` cells and the four cells with two lost transmissions end in `SUCCESS`; with three consecutive losses they stay `INDETERMINATE`. At equal budget, T1's success versus non-success split agrees with every mapped Study F baseline row (no mismatches). Under loss at equal retransmission, therefore, nothing separates T1 from B2, or from B0 with retransmission and the outcome vocabulary. The CSV reproduced byte for byte in a second environment.

"""

SEC8 = """## 8. Threats to Validity and Limitations

The experiment was deliberately scoped as a bounded, synthetic, software-only study. It gains deterministic replay, exact fault placement and reproducible state inspection, and gives up inference about concrete cryptographic protocols and operational spacecraft. The table lists each threat, what it limits, and where the paper addresses it; Part II's threats follow in Section 8.10.

**Table 2. Threats to validity, their effect on the claims, and where each is addressed.**

| Threat | Effect on the claims | Where addressed |
|---|---|---|
| Construct (outcome and state labels) | Alignment, security, availability, verification and outcome are model variables, not flight measurements. The legacy `SECURE_DEGRADED` label is not evidence of security, and `SUCCESS` is defined inside the model, not as secrecy, authentication or mission readiness. Availability is a function of the outcome label in the retained runs. | Component states reported beside the composite outcome; raw evidence retained (Sections 3.6, 6.2, Table S1). |
| Internal (simulator and runs) | The simulator is deterministic and omits timing, concurrency and storage effects. Plan and schedules were committed before the single retained run from a clean commit. Study C left 114 of 191 scheduled actions unreached, so it is not a fault-conditioned success experiment. A later defect would need a labelled correction run. | Study B gives cell-level coverage; Study C is descriptive (Section 6.3). |
| Conclusion (denominators and statistics) | No inferential statistics. Study A has four matched families; Study C is a fixed 100-schedule set and Study D a fixed 12-schedule set, so 5/12 and 11/12 are set-specific and "no lifetime effect" holds only for this set, where the lifetime is read at one check. | Fixed-set counts only; no intervals, optimal budget or reliability claim. |
| Baseline mapping | B0, B1 and B2 are project-defined abstractions that do not implement or inherit their source constructions or proofs. No independent cryptography review was done. B0 and B1 under local activation have no verification step. | Described as abstractions; no equivalence or independence claimed. |
| External (no real system) | No RF link, spacecraft, flight computer, cFS/NOS3, hardware security module or key-management infrastructure. Contacts and restarts are modeled events, so there is no claim of flight readiness, CCSDS/SDLS conformance, timing or link-budget behavior. | Findings are mechanism-oriented patterns to test at higher fidelity. |
| Cryptographic | Cryptography is abstract (no ML-KEM, Triple-KEM, concrete ratchet or SDLS stack). Candidate keys are labels and the recovery authority is never compromised, so nothing here establishes confidentiality, authenticity, forward secrecy or post-compromise security. `SECURE_PROVISIONAL` and `UNSAFE` are model classifications. | Assumptions are inputs, not results. |
| Formal model | The TLA+ evidence uses a declared projection, selected witnesses and zero mismatches, with no refinement proof. `DIVERGED`, `AVAILABLE_UNSAFE` and `LOCKED` became reachable only through added diagnostic transitions, so non-reachability is not impossibility. | Supporting consistency evidence only. |
| Reproducibility | Results tie to an exact commit, plan hash, serialized schedules and a retained bundle with a verified 16-file checksum manifest. Platform metadata may differ across environments, and the raw bundle is not rewritten. | Section 9; derived tables trace to the retained run. |
| Ethical and legal scope | Synthetic and software-only: no transmission, RF interference, real credentials, third-party spacecraft or human-subject data. This limits ecological validity. | Presented as controlled research, not penetration testing or flight validation. |

"""


def apply_round9_fixes(text):
    t = text

    t = _rep(
        t,
        "so `UNSAFE` records that a compromised key is still active at the end of the run, not an observed exploit.",
        "so `UNSAFE` records only that the ground's active key is still the seeded compromised key at the end of the run, not an observed exploit and not an exposure at the spacecraft. No adaptive adversary strategy is evaluated; an adversary able to force a restart or exhaust the retry budget is the realistic threat these schedules stand in for. Every Part I run starts from one seeded divergence (ground epoch 2, spacecraft epoch 1, both keys marked compromised) and models a single recovery transaction with no re-initiation.",
    )
    t = _rep(
        t,
        "This design avoids a hidden simulator oracle in which ground code directly reads the spacecraft's active epoch.",
        "This design avoids a hidden simulator oracle in which ground code directly reads the spacecraft's active epoch. In the Part I start state (ground epoch 2, spacecraft epoch 1, authority floor 0) the ground proposes max(2, 0) + 1 = 3 and the spacecraft selects max(3, 1 + 1) = 3; a spacecraft already at epoch 4 would select max(3, 5) = 5. The floor only raises the ground's proposal, and the spacecraft's own epoch always wins through the maximum.",
    )
    t = _rep(
        t,
        "Non-equivalent mechanisms are compared conservatively, with no pooled score.",
        "Several T1 constructs are standard commit-protocol ideas: a candidate isolated until activation resembles a prepared state, the activation receipt a commit record, and persisted pending state a participant log [@gray_notes_1978; @skeen_nonblocking_1981]. What differs here is a channel that is not always on, asymmetric trust, and a compromised key still active during recovery. Non-equivalent mechanisms are compared conservatively, with no pooled score.",
    )
    t = _rep(
        t,
        "activated, and then tested through modeled command and telemetry evidence.",
        "activated, and then tested through modeled command and telemetry evidence. In the simulator, however, B0 ends at activation: its test and status steps are not modeled, so no verification evidence can be lost for B0 (the same holds for B1 under local-completion activation). Verification loss is modeled only for B1 with deferred activation, B2 and T1.",
    )
    t = _rep(
        t,
        "they constitute one B1 analysis unit rather than two independent replications.*",
        "they constitute one B1 analysis unit rather than two independent replications. For B0, and for B1 under local activation, the \"Verification complete\" cue is the simulator default for a flow that ends at activation, not an observed test and status exchange, so CF-02 parity on verification holds by default for them.*",
    )
    t = _rep(
        t,
        "Thus, within this matched family, replay rejection did not prevent successful completion.",
        "This is a sanity check: replay rejection did not disturb successful completion.",
    )
    t = _rep(
        t,
        "The restart destroyed pending protocol state needed to complete the transition.",
        "The restart destroyed pending protocol state needed to complete the transition. In this model a restart clears an endpoint's pending state and activation receipt but keeps its monotonic counter and replay record, so a retried PREPARE is rejected as non-monotonic; this persistence split is an assumption, and a different one could change the outcome.",
    )
    t = _rep(
        t,
        "this case is not evidence of a cryptographically secure degraded state.",
        "this case is not evidence of a cryptographically secure degraded state. The spacecraft had already moved to the new key while the restarted ground still held the old one, so this is a loss of ground command authority, not a compromised key left active at the spacecraft.",
    )
    t = _rep(
        t,
        "The complete 40-row deterministic fault-coverage matrix",
        "Counting by end state, seven of the ten unsafe Study B schedules (the COMMIT-stage spacecraft restart and six exhaustions at PREPARE, RESPONSE or COMMIT) ended with no new key activated at either endpoint, so the seeded compromised key simply stayed active; the other three left the spacecraft ahead and the ground locked out. The model records contacts only as abstract slots: 17 of the 21 unsafe runs in Studies B and C ended within the first contact, so contact-counted exposure is 0 for them and no exposure-time metric is reported for Part I (post hoc reanalysis in the repository).\n\nThe complete 40-row deterministic fault-coverage matrix",
    )
    t = _rep(
        t,
        "provides the stronger fault-coverage evidence.",
        "provides the stronger fault-coverage evidence. A post hoc split of the retained event log shows that all 43 schedules with no applied fault ended in `SUCCESS`, while the 57 with at least one applied fault ended in 31 `SUCCESS`, 15 `INDETERMINATE`, six `SECURE_DEGRADED` and five `EXPIRED`; the split is descriptive, was not predeclared, and is not a success rate. The 11 unsafe schedules are six spacecraft-ahead and five with the starting divergence unresolved.",
    )
    t = _rep(
        t,
        "A post hoc split of the retained event log shows that all 43 schedules without an applied fault ended in `SUCCESS`, while the 57 with at least one applied fault ended in 31 `SUCCESS`, 15 `INDETERMINATE`, six `SECURE_DEGRADED` and five `EXPIRED`; the split is descriptive, was not predeclared, and is not a success rate.",
        "The post hoc split in Section 6.3 is descriptive, was not predeclared, and is not a success rate.",
    )
    t = _rep(
        t,
        "so a lost step stays `INDETERMINATE` by rule; in Study F a baseline with retransmission absorbs the same loss.",
        "so a lost step stays `INDETERMINATE` by rule, and B0 and B1 under local activation model no such step; in Study F a baseline that models a status step absorbs the same loss with retransmission. Part I therefore shows what the harness and vocabulary expose, not that T1's verification design is better. What remains distinct about T1 is its recovery authority, epoch floor, candidate isolation and activation receipt; Study G (Section 5.12) gave T1 the same retransmission and found no difference in the success partition under loss, so no resilience claim beyond B0 with retransmission is made.",
    )
    t = _rep(
        t,
        "even though every prior message was legitimate.",
        "even though every prior message was legitimate. Only the CONFIRM-stage cases create a new asymmetry (the ground locked out); the earlier cases leave the starting divergence in place.",
    )
    t = _rep(
        t,
        "the enum label is not evidence that the terminal state is secure.",
        "the enum label is not evidence that the terminal state is secure. In the retained runs availability is a function of the outcome label, so the two fields carry the same information there; they stay separate because they need not coincide in general.",
    )
    t = _rep(
        t,
        "a baseline absorbs a lost status message that T1 leaves indeterminate by rule.",
        "a baseline that models a status step absorbs a lost status message that T1 leaves indeterminate by rule.",
    )
    t = _rep(
        t,
        "the state spaces are finite, and no refinement relation is proven.",
        "the state spaces are finite, and no refinement relation is proven. The TLA+ model has no key, compromise, adversary, restart or replay variables, so it checks control-flow structure only.",
    )
    t = _all(t, "T1 fault robustness", "T1 fault handling", 2)

    # Section 5.11 (Study F) before Results.
    t = _rep(t, "## 6. Results", STUDY_F + STUDY_G + "## 6. Results")

    # Section 8 as a table.
    t = _span(t, "## 8. Threats to Validity and Limitations", "### 8.9 Ethical, legal, and safety scope", SEC8)
    # The span consumed the old 8.9 heading; drop its body up to 8.10.
    tail_start = t.find("### 8.10 Part II validity")
    sec8_end = t.find("\n\n", t.find("| Ethical and legal scope")) + 2
    t = t[:sec8_end] + t[tail_start:]

    t = _span(
        t,
        "![Figure 3. Verification-complete executions across the Study D parameter grid.",
        "Candidate lifetime produced no observed change over the tested range.*",
        "Verification completed in 5 of the 12 fixed challenge schedules at a transmission budget of 2 and in 11 of 12 at budgets 3 and 4, at every candidate lifetime of 2, 3 and 4 contacts.",
    )

    # Part II.
    t = _rep(t, "**Table 2. Study E hypotheses and outcomes", "**Table 3. Study E hypotheses and outcomes")
    t = _rep(
        t,
        "were frozen before any confirmatory run in a version-controlled repository, with the frozen versions identified in Section 9.5.",
        "were declared by the author before any confirmatory run in a version-controlled repository (author-frozen, not registered with an external registry), with the frozen versions identified in Section 9.5.",
    )
    t = _rep(
        t,
        "baseline loss up to 2\\% and storm-time uplink loss of up to 60\\% at one site for limited periods (a figure caption; the source abstract says a 60\\% increase) [@basak_cosmicdancepro]",
        "baseline loss up to 2\\% and storm-time increases in uplink loss at some sites [@basak_cosmicdancepro]",
    )
    t = _rep(
        t,
        "stress points beyond clear-sky broadband loss; their upper end is comparable to the worst broadband uplink loss reported during the 2024 solar storms and is not measured TT\\&C loss.",
        "stress points beyond clear-sky broadband loss; $p$ is a free parameter and no value of it is a measured TT\\&C loss.",
    )
    t = _rep(
        t,
        "| H-E4: divergence almost always recoverable under a static Recovery SA | Median recovery fraction is about 1,",
        "| H-E4: divergence almost always recoverable under a static Recovery SA | Partly supported at the declared 0.95 level: the median recovery fraction is about 1,",
    )
    t = _rep(
        t,
        "Bursty loss can help or hurt, so a single independent-loss figure is not a safe planning assumption.",
        "Bursty loss can help or hurt, so a single independent-loss figure is not a safe planning assumption. An exploratory exposure measure (not pre-registered; frozen model and R0 parameters; horizon capped at 20 contacts) gives the expected contacts until the Recovery-association fallback restores authority after a divergence: with $K=4$ and a detection delay of one contact it rises from 2.2 contacts at $p=0.05$ to 4.0 at $p=0.5$, and each extra contact of detection delay adds one contact (8.0 at $p=0.5$ with delay 5), so in the model detection delay moves exposure more than a tenfold increase in loss. Not every hypothesis could fail unseen: journal invariance in H-E2c holds by design, H-E5 was declared with a pass rule that one witness per direction satisfies, and a test grid run before the confirmatory run already showed witnesses against H-E2b. The outcomes of H-E2a, H-E3 and H-E4 were least determined in advance by the declared rules.",
    )
    t = _rep(
        t,
        "the checksum was reproduced in a second environment by the same author,",
        "the checksum was recomputed in a second software environment and an AI agent re-implemented Study B from the specification (same 40 outcomes), not an independent party,",
    )
    t = _rep(
        t,
        "The two parts use different models, and no quantitative result is transferred between them. Part I has no Recovery SA fallback; Part II models one (H-E4).",
        "Part I has no Recovery SA fallback; Part II models one (H-E4). No quantitative result is transferred between the parts. Against the 40 scripted Part I schedules, Part II agrees only partly (`study_e_reconcile`); 18 have no counterpart.",
    )
    # Display-only relabel of the raw SECURE_DEGRADED enum (frozen data and supplement tables keep it).
    keep = ("raw", "historical", "legacy", "predates", "enum")
    out_lines = []
    for ln in t.split("\n"):
        if "SECURE_DEGRADED" in ln and not any(k in ln for k in keep):
            ln = ln.replace("`SECURE_DEGRADED`", "`LOCKOUT`")
        out_lines.append(ln)
    t = "\n".join(out_lines)
    t = _rep(
        t,
        "The historical raw label `SECURE_DEGRADED` is retained for reproducibility but",
        "The historical raw label `SECURE_DEGRADED` is retained in the data for reproducibility, shown here as `LOCKOUT`, but",
    )
    t = _rep(t, ' Recovery for intermittent TT&C needs both message-validity protections and explicit recovery-state management.', '')
    t = _rep(t, ' The retained run stays valid: the population was predeclared and executed correctly, and the audit reveals a property of the generator, since scheduling a later-attempt fault does not force it to occur.', ' The run stays valid; the audit reveals a generator property: a scheduled later-attempt fault need not occur.')
    t = _rep(t, ' Study C is secondary evidence about the outcome distribution of a fixed synthetic population, while deterministic Study B gives the controlled cell-level evidence.', ' Study C is secondary evidence; deterministic Study B gives the controlled cell-level evidence.')
    t = _rep(t, ' Whether an implementation using CCSDS Recovery SA would encounter or mitigate such a hazard remains untested.', ' Whether a Recovery SA implementation would meet or mitigate it is untested.')
    t = _rep(t, ' Finally, recovery policy should expose security and availability separately to mission decision logic, which needs to know whether the state is trusted, whether command and telemetry verification succeeded, and whether enough evidence was retained to explain the transition.', ' Finally, recovery policy should expose security and availability separately to mission decision logic, which needs to know whether the state is trusted, whether verification succeeded, and whether the evidence explains the transition.')
    t = _rep(t, ' Study C looked capable of yielding a simple synthetic success proportion, but the post-execution reachability audit shows that reading would mislead.', ' A simple synthetic success proportion would mislead, as the post-execution reachability audit shows.')
    t = _rep(t, ': the duplicate, stale, and reordered cases completed because invalid material was rejected without discarding valid progress.', '.')
    t = _rep(t, ' Replay resistance alone is still not a complete recovery story.', ' Replay resistance alone is not a complete recovery story.')
    t = _rep(t, 'Our observations do not establish the need for that concept or test its conformance. Rather, the', 'Our observations neither establish the need for that concept nor test conformance. The')
    t = _rep(t, ', a sanity boundary showing that the controller does not obtain its fault-handling story from obviously different classifications in the simplest matched cases.', '.')
    t = _rep(t, ', since losing that evidence leaves the implementation synchronized but unable to justify a success classification.', '; without it a synchronized implementation cannot justify success.')
    t = _rep(t, ' The dominant adverse cases were missing evidence, exhausted delivery opportunities, and destroyed endpoint state, not successful replays.', ' The dominant adverse cases were missing evidence, exhausted delivery, and destroyed state, not successful replays.')
    t = _rep(t, "so a single independent-loss figure is not a safe planning assumption.", "so a single independent-loss figure is not a safe planning assumption (Supplementary Figure S8 maps outcome regions over p and K for one slice).")
    t = _rep(
        t,
        "The falsified hypotheses describe the model's rules and should not be transferred to Part I or to real links.",
        "A software-only check (`docs/f1_f4_software_only`; NASA CryptoLib commit 329f895 run, cFE and PSP read only) found persistence differing by state class and build option: the key ring reverted on process restart, the security-association table survived only in the optional file-save build as a snapshot at the next accepted frame, and a stop command issued before restart was lost. Command-driven key activation, processor or power resets, and CCSDS-specified behavior were not exercised, so the volatile, commit and journal levels are not validated. The falsified hypotheses describe the model's rules and should not be transferred to Part I or to real links.",
    )
    t = _rep(t, 'Satellite cybersecurity research is moving toward controlled experimental platforms. ', '')
    t = _rep(t, 'are the natural basis for the follow-up testing this paper does not perform.', 'are the natural basis for follow-up testing; this paper reports only a software-only source check (Section 8.10).')
    t = _rep(t, ' The approaches are complementary: high-fidelity testbeds can later test whether these mechanisms survive concrete flight software, transport, storage, timing and link behavior.', ' High-fidelity testbeds can later test whether the mechanisms survive concrete flight software and links.')
    t = _rep(t, ' These establish that post-compromise key renewal matters and that stateful mechanisms can suit disrupted links.', '')
    t = _rep(t, 'A software-only check (`docs/f1_f4_software_only`; NASA CryptoLib commit 329f895 run, cFE and PSP read only) found persistence differing by state class and build option:', 'A software-only check (`docs/f1_f4_software_only`; CryptoLib commits 329f895 and NOS3-pinned b46879c run, cFE and PSP read only) found persistence differing by state class and build option:')
    t = _rep(t, ' Command-driven key activation, processor or power resets, and CCSDS-specified behavior were not exercised, so the volatile, commit and journal levels are not validated.', ' Command-driven key load and activation also reverted on restart; processor or power resets and CCSDS behavior were not exercised, so the three levels are not validated.')
    return t
