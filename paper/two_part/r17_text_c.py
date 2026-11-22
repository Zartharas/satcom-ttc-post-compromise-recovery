"""Round 17 output-only prose (Sections 8-10 and Part II)."""

THREATS_HEAD = r"""## 8. Threats to Validity and Limitations

The experiment was deliberately scoped as a bounded, synthetic, software-only study. It gains deterministic replay, exact fault placement and reproducible state inspection, and gives up inference about concrete cryptographic protocols and operational spacecraft. Table 2 lists each threat, what it limits and where the paper addresses it; reproducibility is covered in Section 9 and a closing paragraph covers Part II.

**Table 2. Threats to validity, their effect on the claims, and where each is addressed.**

| Threat | Effect on the claims | Where addressed |
|---|---|---|
| Construct (outcome and state labels) | Alignment, security, availability, verification and outcome are model variables, not flight measurements. `SECURE_DEGRADED` is not evidence of security, `SUCCESS` is defined inside the model, and availability is a function of the outcome label in the retained runs. | Components reported beside the composite outcome; raw evidence retained (Sections 3.4, 6.2, Table S1). |
| Internal (simulator and runs) | The simulator is deterministic and omits timing, concurrency and storage effects. Plan and schedules were archived before the single retained run. Study C left 114 of 191 scheduled actions unreached, so it is not a fault-conditioned success experiment. | Study B gives cell-level coverage; Study C is descriptive (Section 6.3). |
| Conclusion (denominators and statistics) | No inferential statistics. Study A has four matched families; Study C is a fixed 100-schedule set and Study D a fixed 12-schedule set, so 5/12 and 11/12 are set-specific and "no lifetime effect" holds only for this set, where the lifetime is read at one check. | Fixed-set counts only; no intervals, optimal budget or reliability claim. |
| Baseline mapping | B0, B1 and B2 are project-defined abstractions that do not implement or inherit their source constructions or proofs. No independent cryptography review was done. B0 and B1 under local activation have no verification step. | Described as abstractions; no equivalence or independence claimed. |
| External (no real system) | No RF link, spacecraft, flight computer, cFS/NOS3, hardware security module or key-management infrastructure. Contacts and restarts are modeled events, so there is no claim of flight readiness, CCSDS/SDLS conformance, timing or link-budget behavior. | Mechanism-oriented patterns to test at higher fidelity. |
| Cryptographic | Cryptography is abstract (no ML-KEM, Triple-KEM, concrete ratchet or SDLS stack). Candidate keys are labels and the recovery authority is never compromised, so nothing here establishes confidentiality, authenticity, forward secrecy or post-compromise security. | Assumptions are inputs, not results. |
| Formal model | The TLA+ evidence uses a declared projection, selected witnesses and zero mismatches, with no refinement proof. `DIVERGED`, `AVAILABLE_UNSAFE` and `LOCKED` became reachable only through added diagnostic transitions, so non-reachability is not impossibility. | Supporting consistency evidence only. |
| Ethical and legal scope | Synthetic and software-only: no transmission, RF interference, real credentials, third-party spacecraft or human-subject data. | Controlled research, not penetration testing or flight validation. |

"""

REPRO = r"""## 9. Reproducibility and Artifact Availability

The numerical results trace to an exact code version, a predeclared plan, serialized schedules, retained raw outputs and derived table and figure sources. The final study used the archived inputs below, shortened to 12 hexadecimal characters (Supplementary Table S9 gives the full values): plan identifier `cfb730a8191d`, plan SHA-256 `3570834a70c7`, runner identifier `c630fb4f65ad` and retained run identifier `20260814T022506Z-gc630fb4`. The execution wrapper verified the branch head, clean tracked tree, protected input hashes, repository manifest, plan contract and full regression suite before the final result boundary.

The retained bundle has the external SHA-256 below, and its internal 16-file checksum manifest verified completely. It holds the final plan input, raw Study A to D outputs, processed tables and summaries, figure-source CSVs, execution metadata and logs, and it is not rewritten when manuscript summaries change.

```text
b3b8c55a9e522ffe3f7898d7b786583e46a4dc3db0aba9d3947fd6ebdaeecaa1
```

Derived sources are tracked under `paper/tables/` and `paper/figures/`, and `experiments/scripts/summarize_paper_final_results.py` verifies the run identity and checksum manifest before deriving them. At the final execution boundary 256 repository tests passed, and the plan-bound runner supports `--validate-only` to check the archived plan and schedule contracts without running outcomes. The repository holds the simulator, plan, validation and derivation tools, result sources and formal models. The raw bundle stays outside the repository's version history, is identified by the run ID and SHA-256 above, and has not been deposited in a public archive or given a persistent identifier, so a full raw-output audit needs access to it; the author can make it available on reasonable request.

The Part II code, tests, TLA+ specifications, frozen pre-registration, analysis-script amendment and confirmatory results are in the project repository [@study_e_repository]. The freeze is recorded by permanent, dated labels that note the author's approval of 2026-11-19. The two frozen versions (pre-registration and analysis script) and the Study F plan are identified in Supplementary Table S9, and the results table carries a SHA-256 checksum for checking a reproduction. The arithmetic is deterministic; the checksum was recomputed in a second software environment, and the test suite has 99 tests. A SatNOGS-derived summary would carry the CC BY-SA 4.0 licence of its source. Reproducing the results validates the software model, schedules, analysis pipeline and bounded formal evidence, not the cryptographic security of B0 to B2 or T1, link behavior or flight applicability.

"""

II1_POS = r"""### II.1 Model

Positioning. Beyond Section 1, the Recovery security association of CCSDS 350.5-G-2 (Sections 3.5.1.2 and 4.5.6) supplies a last-resort association, not an exchange for resynchronizing the two ends [@ccsds_sdls_rationale_350_5_g_2]. CCSDS 355.1-B-1 has the Initiator activate before signaling the Recipient (Section 3.2.3.2) and defines no handling of a lost signal in the text read [@ccsds_sdls_ep_355_1_b_1]. SDLS-DR persists ratchet state at commit points and recovers from disorderly state loss over a Recovery association, but did not evaluate contact windows, ground-station handover, range-dependent delay, Doppler or flight hardware [@ledin_sdls_dr_risc2026]. Over-the-air rekeying proposals such as E-Laun treat loss only qualitatively in the text read [@duc_elaun_2025], and a recent preprint models post-quantum key-update transport under loss, contact time and COP-1 retransmission, but not endpoint restart or state divergence [@kim_seo_2026]. The activation exchange also resembles the atomic-commit problem, where two parties must change state together over an unreliable channel and neither can be certain the other has done so [@gray_notes_1978; @skeen_nonblocking_1981]. Study E examines these gaps at the level of an abstract exchange only.

"""

II3_HEAD = r"""### II.3 Pre-registration and results

Hypotheses H-E1 to H-E5, the grid and the policy set were declared by the author before any confirmatory run in a version-controlled repository (author-frozen, not registered with an external registry); Section 9 and Supplementary Table S9 identify the frozen versions. The confirmatory runner was added afterwards under a disclosed amendment, implements only the frozen hypotheses, and operationalizations of ambiguous wording were declared before the run. A small test grid run before the confirmatory run had revealed witnesses against H-E2b, and the hypothesis was not changed. Starlink statistics were inspected before the Gilbert-Elliott rule was written, so the anchors are not blind. An erratum records that the frozen text cited only the baseline loss from the storm-analysis paper. Table 3 gives the outcomes over the full grid.

"""

II4 = r"""### II.4 Interpretation and limitations

Retrying expired attempts adds little because the dominant failure is an exchange that ends indeterminate, and resumable verification closes most of that gap, as an assumption outside the standards. The falsified hypotheses show that more durable persistence and more reliable links do not compose monotonically: durable persistence preserves progress that non-durable schemes reset, so under tight budgets more attempts end with ground activated and the spacecraft not, and extra slots can lower success when restarts strike mid-exchange. These are consequences of the model's rules, not claims about real links, and some, such as the restart invariance of journaled persistence, hold by design; the exact computation measures their extent. Bursty loss can help or hurt, so a single independent-loss figure is not a safe planning assumption (Supplementary Figure S8 maps outcome regions over p and K for one slice). An exploratory exposure measure (not pre-registered; frozen model and R0 parameters; horizon capped at 20 contacts) gives the expected contacts until the Recovery-association fallback restores authority after a divergence: with $K=4$ and a detection delay of one contact it rises from 2.2 contacts at $p=0.05$ to 4.0 at $p=0.5$, and each extra contact of detection delay adds one contact (8.0 at $p=0.5$ with delay 5), so in the model detection delay moves exposure more than a tenfold increase in loss. Not every hypothesis could fail unseen: journal invariance in H-E2c holds by design, H-E5 was declared with a pass rule that one witness per direction satisfies, and H-E2b already had witnesses in a test grid; H-E2a, H-E3 and H-E4 were least determined in advance.

Limitations specific to Study E: the six-message abstraction is not flight software and has not been independently reviewed by a second person; parameters are anchored to proxies, none a measured TT\&C uplink; the Gilbert-Elliott channel is an uncalibrated sensitivity probe; Recovery-association and resume-policy parameters are assumptions; skipped-key desynchronization is not coupled to the exchange; the TLA+ check is same-author and omits the resume policy and the Gilbert-Elliott channel; and SatNOGS records are first-page only and not representative.

"""

CONCL = r"""## 10. Conclusion

Post-compromise TT&C recovery needs more than fresh key material. Ground and spacecraft endpoints must also agree on which state is operational, survive disrupted delivery without accepting stale or replayed control material, and produce enough evidence to justify resuming trusted command operations.

In a bounded, reproducible software model, T1 matched the abstract baselines' categorical outcomes in the four families where comparison could be defended, so no superiority claim is made. The deterministic study gave the clearest mechanism-level evidence. Isolated loss and contact closure were absorbed within the retry budget, and delayed, duplicated, reordered, stale-counter and stale-replay cases completed while invalid material was rejected. Lost post-convergence evidence left the controller synchronized but `INDETERMINATE`, and endpoint restart around COMMIT or CONFIRM destroyed or separated pending or activated state and produced unsafe asymmetric outcomes. Raising the transmission budget from two to three repaired the repeated omission and contact challenges in that fixed set, a fourth opportunity added no observed benefit, and none repaired the COMMIT-stage restart failure: retransmission can recover missing messages, not protocol state that no longer exists. Studies F and G found that, at equal retransmission, T1's success partition under loss matches the baselines'. The fixed 100-schedule population is descriptive only, because many later-attempt faults were never reached at runtime, so its 74 successful schedules are not a fault-conditioned success rate. Bounded TLA+/Python comparisons agree on selected traces over the declared abstraction but do not establish refinement, cryptographic security or completeness of the model.

"""
