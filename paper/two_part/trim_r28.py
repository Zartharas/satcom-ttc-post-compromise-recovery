"""Round 28 page-budget trims (author asked: fewer pages only if no loss of context).
Each pair removes wording that repeats another section; numbers and findings are unchanged.
Applied in build_two_part_manuscript.py after apply_restructure; each old string must match once."""
TRIMS = [
  # main-text-only trims (the supplement S10 keeps this detail)
 (" Our observations neither establish the need for that concept nor test conformance.", ""),
 (", and it is not rewritten when manuscript summaries change.", "."),
 (", and the plan-bound runner supports `--validate-only` to check the archived plan and schedule contracts without running outcomes.", "."),
 (" The repository holds the simulator, plan, validation and derivation tools, result sources and formal models.", ""),
 # Introduction
 (" Operational recovery must also cope with intermittent contact, constrained bandwidth and a ground endpoint that cannot observe spacecraft state continuously.", ""),
 ("; the study represents these consequences only as model outcome labels and does not measure them.", "; the study represents these only as model outcome labels."),
 (" No operational satellite, live RF transmission, mission credential or flight system is used.", ""),
 ("T1 attempts the test-command and status-telemetry steps once by design, and B0 and B1 under local activation model no such steps; when Study G (Section 5.5) gives T1 the same three transmissions, one or two lost steps no longer leave it `INDETERMINATE`, so this finding is a consequence of that design choice.",
  "This follows from T1's single attempt at the test-command and status-telemetry steps (B0 and B1 under local activation model none); with the same three transmissions (Study G, Section 5.5), one or two lost steps no longer leave T1 `INDETERMINATE`."),
 ("Every Part I run starts from one seeded divergence with both keys marked compromised. In seven of the ten unsafe deterministic schedules (ten of 40; Supplementary Tables S1 and S4) no new key was activated at either endpoint, so the compromised key simply stayed active; in the other three (a ground restart at CONFIRM and two exhaustions at CONFIRM) the spacecraft had already activated the new key and the ground had not, which locks the ground out of command.",
  "Of the ten unsafe deterministic schedules (ten of 40; Supplementary Tables S1 and S4), seven activated no new key at either endpoint, so the compromised key stayed active, and three left the ground locked out (Section 6.2)."),
 ("The results do not support a universal superiority claim for T1 over B0, B1 or B2, and several Part I findings are rules of the model: lost verification evidence yields `INDETERMINATE`, a restart destroys volatile pending state, and the Study D threshold follows from fault multiplicity in a designed set (Table S2). The experiment does not establish strong post-compromise security, CCSDS/SDLS conformance, flight readiness or real-world fault prevalence, and no independent review of the source-to-model mappings was completed (Section 8). Part I and Part II are different models and no quantitative result is transferred between them; Part II's loss values are stress parameters, not measurements of a TT&C uplink.",
  "The results do not support a universal superiority claim for T1, and several Part I findings are rules of the model: lost verification evidence yields `INDETERMINATE`, a restart destroys volatile pending state, and the Study D threshold follows from fault multiplicity in a designed set (Table S2). They do not establish post-compromise security, CCSDS/SDLS conformance, flight readiness or real-world fault prevalence (Section 8). Part I and Part II are different models, and no quantitative result is transferred between them."),
 # 2.3
 (" Non-equivalent mechanisms are compared conservatively, with no pooled score and no universal priority claim.", ""),
 ("Our simulator has lower hardware and environmental fidelity by design, with no RF propagation, orbital physics, power behavior or flight computer. Its strength is control-state observability and determinism:",
  "Our simulator has no RF propagation, orbital physics, power behavior or flight computer; its strength is control-state observability and determinism:"),
 # 3.3
 (" No adaptive adversary is evaluated; one able to force a restart or exhaust the retry budget is the realistic threat these schedules stand in for.", " No adaptive adversary is evaluated."),
 # 5.3
 ("The 31 cells are `DROP`, `DELAY` and `CONTACT_CLOSE` across six phases each; `DUPLICATE` and `REORDER` across the four message-bearing phases; `ENDPOINT_RESTART` of the spacecraft at COMMIT and of the ground at CONFIRM; `STALE_COUNTER` at PREPARE; and `STALE_REPLAY` at COMMIT and CONFIRM.",
  "The 31 cells (fault kind by phase) are listed in Supplementary Table S1."),
 # 6.1
 ("In CF-01, passive operational-key compromise followed by fresh recovery material, B0, B1, B2 and T1 all ended `SUCCESS` with synchronized state, `AVAILABLE` availability and `SECURE_PROVISIONAL` security, and the active key was not marked compromised at the observation cutoff. CF-02, the no-fault case, gave the same result for B0, B2, T1 and both B1 policy traces, with complete verification evidence; the two B1 traces are alternative policies, not replications, and are not double-counted. In CF-05, post-convergence loss of status telemetry, B2 and T1 produced the same classification: `INDETERMINATE`, synchronized state, `DEGRADED` availability, `NOT_ESTABLISHED` security state and incomplete telemetry and verification. The protocol had converged, but success was withheld because the required evidence was incomplete. In CF-06, stale replay after successful advancement, B2 and T1 ended `SUCCESS` with one replay and one replay rejection, a sanity check that rejection did not disturb completion.",
  "In CF-01 (passive operational-key compromise followed by fresh recovery material) and CF-02 (no fault), B0, B1, B2 and T1 all ended `SUCCESS` with synchronized state, `AVAILABLE` availability and `SECURE_PROVISIONAL` security; the two B1 policy traces in CF-02 are alternatives, not replications, and are not double-counted. In CF-05, post-convergence loss of status telemetry, B2 and T1 both ended `INDETERMINATE` (synchronized, `DEGRADED`, `NOT_ESTABLISHED`): the protocol had converged, but success was withheld because the required evidence was incomplete. In CF-06, stale replay after successful advancement, B2 and T1 ended `SUCCESS` with one replay and one replay rejection."),
 (" CF-02 contains two B1 policy traces for traceability; they constitute one B1 analysis unit rather than two independent replications.", ""),
 # 7.1
 ("T1 gives its verification steps one attempt each by design, so a lost step stays `INDETERMINATE` by rule, and B0 and B1 under local activation model no such step; in Study F a baseline that models a status step absorbs the same loss with retransmission. Part I therefore shows what the harness and vocabulary expose, not that T1's verification design is better.",
  "This follows from T1's single-attempt design (Section 1, item 1), so Part I shows what the harness and vocabulary expose, not that T1's verification design is better."),
 # 7.2
 ("it destroyed the pending state needed to complete the transaction, and retries cannot reconstruct state the endpoint no longer holds.", "retries cannot reconstruct state the endpoint no longer holds."),
 ("Activation boundaries create asymmetric failures. Exhaustion before or at COMMIT left the ground side ahead (`EXPIRED`, `UNSAFE`, `UNAVAILABLE`); exhaustion at CONFIRM left the spacecraft ahead in a degraded, unsafe asymmetric state. Once one endpoint has advanced,",
  "Activation boundaries create asymmetric failures (Section 6.2): once one endpoint has advanced,"),
 # 7.3
 ("A simple synthetic success proportion for Study C would mislead: only 77 of 191 scheduled actions were reached, 43 schedules applied no fault, and seven of the 31 referenced cells were not exercised at runtime. The run stays valid; the audit reveals a generator property, namely that a scheduled later-attempt fault need not occur. The post hoc split in Section 6.3 is descriptive, not predeclared and not a success rate, so Study C",
  "A synthetic success proportion for Study C would mislead: only 77 of 191 scheduled actions were reached, 43 schedules applied no fault, and seven of the 31 referenced cells were not exercised, because a scheduled later-attempt fault need not occur. The post hoc split in Section 6.3 is descriptive, not a success rate, so Study C"),
 (" Three outcomes became reachable only when diagnostic transitions were added, so reachability depends on which transitions the abstraction contains.", ""),
 # 8
 ("Table 2 lists each threat, what it limits and where the paper addresses it; reproducibility is covered in Section 9 and a closing paragraph covers Part II.",
  "Table 2 lists each threat, what it limits and where it is addressed; Section 9 covers reproducibility."),
 ("the key ring reverted on process restart, the security-association table survived only in the optional file-save build as a snapshot at the next accepted frame, and a stop command issued before restart was lost. Key-state reversion was observed by direct mutation of key state; command-driven key load and activation were not exercised (source reading only), nor were processor or power resets and CCSDS behavior, so the three levels are not validated.",
  "the key ring reverted on process restart, and the security-association table survived only in the optional file-save build. Key-state reversion was observed by direct mutation of key state; command-driven key load and activation, processor or power resets and CCSDS behavior were not exercised (source reading only), so the three levels are not validated."),
]

TRIMS += [
 # 7.4 / 2.1 / 2.3 duplicates of the Recovery SA description
 ("CCSDS 350.5-G-2 already recommends a separate last-resort Recovery SA with isolated recovery context and non-volatile onboard storage (Sections 3.5.1.2 and 4.5.6) [@ccsds_sdls_rationale_350_5_g_2]. The COMMIT and CONFIRM", "The COMMIT and CONFIRM"),
 ("Whether a Recovery SA implementation would mitigate it is untested.", "Whether the CCSDS Recovery SA (Section 2.1) would mitigate it is untested."),
 ("stresses long mission lifetimes, limited contact time and possible ground-side key compromise, and concludes", "and concludes"),
 ("We adopt the same motivation but do not re-evaluate SDLS conformance or prove a post-compromise-security property; we model what happens operationally when legitimate endpoints must re-establish a common trusted state while delivery and state faults occur.",
  "We adopt the same motivation but neither re-evaluate SDLS conformance nor prove post-compromise security; we model what happens operationally when legitimate endpoints must re-establish a common trusted state under delivery and state faults."),
 ("; its authors did not evaluate contact windows, delay or flight hardware, the setting examined here.", "; its authors did not evaluate contact windows, delay or flight hardware."),
 # 6.3 / 5.2 / Table 1 note
 (" These values describe the fixed synthetic population and are not estimates of mission reliability or real-world fault prevalence.", ""),
 ("; deterministic Study B, where each canonical cell was explicitly reached, is the stronger coverage evidence", ""),
 (" Study A executes these families unchanged from the frozen plan and shows member outcomes side by side.", ""),
 # Section 9
 ("The execution wrapper verified the branch head, clean tracked tree, protected input hashes, repository manifest, plan contract and full regression suite before the final result boundary.",
  "The execution wrapper verified the clean tracked tree, input hashes, manifest, plan contract and regression suite before the final result boundary."),
 # 7.4 item 5 and Conclusion
 ("which needs to know whether the state is trusted, whether verification succeeded and whether the evidence explains the transition.", "so mission logic knows whether the state is trusted and whether verification succeeded."),
 (" The fixed 100-schedule population is descriptive only, because many later-attempt faults were never reached at runtime, so its 74 successful schedules are not a fault-conditioned success rate. Bounded TLA+/Python comparisons agree on selected traces over the declared abstraction but do not establish refinement, cryptographic security or completeness of the model.",
  " The fixed 100-schedule population is descriptive only, and its 74 successful schedules are not a fault-conditioned success rate."),
]

import re as _re

def drop_fig2(text):
    """Move the Study C bar chart (counts are already in the text) to the supplement as Figure S11."""
    new, n = _re.subn(r"!\[Figure 2\..*?\]\(\.\./figures_ieee/fig2\.pdf\)\n\n\*Figure 2\..*?\*\n?", "", text, flags=_re.S)
    assert n == 1, "fig2 block not found"
    assert text.count("(Figure 2)") == 1
    return new.replace("(Figure 2)", "(Supplementary Figure S11)")

TRIMS += [
 ("`SECURE_DEGRADED` is not evidence of security, `SUCCESS` is defined inside the model, and availability is a function of the outcome label in the retained runs.", "`SECURE_DEGRADED` is not evidence of security, and availability is a function of the outcome label in the retained runs."),
 (" Plan and schedules were archived before the single retained run.", ""),
 ("Candidate keys are labels and the recovery authority is never compromised, so nothing here establishes confidentiality, authenticity, forward secrecy or post-compromise security.", "Candidate keys are labels and the recovery authority is never compromised, so nothing here establishes confidentiality, authenticity or post-compromise security."),
 (" Non-equivalent", " Non-equivalent"),
]
TRIMS.append((" No quantitative result is transferred between the parts.", ""))
TRIMS += [
 (" Ground and spacecraft endpoints must also agree on which state is operational, survive disrupted delivery without accepting stale or replayed control material, and produce enough evidence to justify resuming trusted command operations.", " Ground and spacecraft must also agree on which state is operational, survive disrupted delivery without accepting stale or replayed control material, and produce evidence that justifies resuming trusted command operations."),
 ("A separate post-execution audit compared scheduled actions with runtime `fault_applied` events and did not alter the retained population. ", "A post-execution audit compared scheduled actions with runtime `fault_applied` events without altering the retained population. "),
 ("The retained bundle has the external SHA-256 below, and its internal 16-file checksum manifest verified completely.", "The retained bundle has the external SHA-256 below, and its 16-file checksum manifest verified."),
]
TRIMS += [
 (" These describe only the fixed challenge set, not cross-treatment performance.", ""),
 (" It is designed to expose parameter sensitivity, not to estimate fault probability.", ""),
 ("plan fixed and archived before the run (2026-08-14 UTC);", "plan fixed and archived before the run;"),
]
TRIMS = [x for x in TRIMS if x[0] != x[1]]

# ---- Round 28b: peer-review structure items (author approved "all four in order") ----
TRIMS_B = [
 # (c) soften, and (a) move Study F/G results from Section 5.5 to new Section 6.6
 (" At budget 1 every single-loss cell ended without success; at budget 3 every cell with one or two consecutive losses succeeded (Supplementary Table S7).", ""),
 ("as for the baselines, (86 cells, 43 per arm). With the larger budget the four canonical `INDETERMINATE` cells and the four cells with two lost transmissions end in `SUCCESS`; with three consecutive losses they stay `INDETERMINATE`. At equal budget, T1's success versus non-success split agrees with every mapped Study F baseline row (no mismatches). Under loss at equal retransmission, therefore, nothing separates T1 from B2, or from B0 with retransmission and the outcome vocabulary. The CSV reproduced byte for byte in a second environment.",
  "as for the baselines (86 cells, 43 per arm)."),
 ("\n## 7. Discussion",
  "\n### 6.6 Post hoc studies F and G\n\nStudies F and G (Section 5.5) are post hoc and outside the retained final run. In Study F, at budget 1 every single-loss cell ended without success, and at budget 3 every cell with one or two consecutive losses succeeded (Supplementary Table S7). In Study G, with the larger budget the four canonical `INDETERMINATE` cells and the four cells with two lost transmissions end in `SUCCESS`; with three consecutive losses they stay `INDETERMINATE`. At equal budget, T1's success versus non-success split agrees with every mapped Study F baseline row (no mismatches). Under loss at equal retransmission, therefore, this grid shows no difference between T1 and B2, or B0 with retransmission and the outcome vocabulary. The CSV reproduced byte for byte in a second environment.\n\n## 7. Discussion"),
 ("(Study G, Section 5.5)", "(Study G, Section 6.6)"),
 ("(Study F, Section 5.5)", "(Study F, Section 6.6)"),
 ("Study G (Section 5.5) gave T1", "Study G (Section 6.6) gave T1"),
 # (b) Part II becomes Section 10, Conclusion Section 11
 ("## 10. Conclusion", "## 11. Conclusion"),
 ("## Part II. Study E:", "## 10. Part II. Study E:"),
 ("### II.1 Model", "### 10.1 Model"),
 ("### II.2 Parameter grid and anchors", "### 10.2 Parameter grid and anchors"),
 ("### II.3 Frozen hypotheses and results", "### 10.3 Frozen hypotheses and results"),
 ("### II.4 Interpretation and limitations", "### 10.4 Interpretation and limitations"),
 ("Part II asks a complementary parametric question", "Part II (Section 10) asks a complementary parametric question"),
]

TRIMS_B += [
 ("Studies F and G (Section 5.5) are post hoc and outside the retained final run.", "Studies F and G are post hoc (Section 5.5)."),
 ("In the retained runs availability is a function of the outcome label, so the two fields carry the same information there, but they need not coincide in general: a synchronized system", "In the retained runs availability follows the outcome label, but in general a synchronized system"),
 ("Unfavorable outcomes remain in the dataset, and a later defect would require a separately identified correction run that preserves the original bundle; a rerun is not performed to obtain preferred results.", "Unfavorable outcomes remain in the dataset, and no rerun is performed to obtain preferred results."),
 ("(up to three transmissions of a lost message, an assumption favorable to the baselines)", "(up to three transmissions, an assumption favorable to the baselines)"),
 ("Derived sources are tracked under `paper/tables/` and `paper/figures/`, and `experiments/scripts/summarize_paper_final_results.py` verifies the run identity and checksum manifest before deriving them.", "Derived sources are tracked under `paper/tables/` and `paper/figures/` and are derived only after the run identity and checksum manifest are verified."),
]

TRIMS_B.append(("This section reports the retained final experiment, executed", "Sections 6.1 to 6.5 report the retained final experiment, executed"))

def style_pass(text):
    """One name for the CCSDS Recovery security association throughout the main text."""
    for o, n in [("Recovery-association", "Recovery SA"), ("Recovery association", "Recovery SA")]:
        text = text.replace(o, n)
    return text
