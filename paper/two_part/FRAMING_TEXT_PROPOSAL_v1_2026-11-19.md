# Framing text proposal v1 (abstract, introduction, conclusion) for the two-part paper

Status: PROPOSAL for the author. Nothing here is applied to the repo. Part I wording (Studies A-D, frozen) is left exactly as it is; every change below is an addition or a clearly marked edit. Numbers come from CONFIRMATORY_FINDINGS_v1 (tags study-e-prereg-v1, study-e-analysis-script-v1).

Author decisions needed are marked **[AUTHOR]**.

---

## 1. Abstract

Keep the existing abstract unchanged, then append:

> A second study (Part II) models the key-activation and verification exchange itself as a six-message abstraction and computes outcome probabilities exactly over 7,680 exchange configurations (message loss, contact slots, transmission budget, candidate lifetime, restart probability, persistence level, activation mode) and 207,360 multi-attempt configurations. Its hypotheses were frozen in the repository before the confirmatory run. Within the model, plain retries could not clear all indeterminate outcomes whereas resumable verification, an assumption outside the standards, could; and bursty loss changed outcomes relative to independent loss at equal average loss, in both directions. Several expected monotonicities failed: success was not monotone in loss or slot count when restarts occur and state is not journaled, durable persistence sometimes raised ground-ahead divergence, and volatile-state divergence did not always grow with restart probability. Recovery from divergence reached the declared 0.95 threshold in 83-90% of multi-attempt configurations with divergence, not almost always. These are properties of the abstraction, not measured link behavior; loss values are stress parameters, not measured TT&C uplink loss.

Length: about 165 words added to a 250-word abstract, so about 415 words. This exceeds the repository's 250-word rule (see 1b) and may exceed the journal limit; 1b is the condensed alternative.

### 1b. Constraint found in the repository: the abstract is locked at exactly 250 words

`.github/workflows/taes-s1-publication-hygiene.yml` asserts `len(ABSTRACT.split()) == 250`, and `build_integrated_manuscript.py` also enforces 200-300 words. The append in section 1 would give about 415 words and fail both checks. If the 250-word rule is kept for the two-part paper, use this combined abstract instead (exactly 250 words by `split()`). It replaces, not extends, the Part I abstract, so it is a decision for you. This is v2: you chose to keep the sentence that the mixed-schedule counts (74 successes; 77 of 191 scheduled faults reached) are descriptive, not reliability estimates. To fit it, the v1 sentence on a fourth transmission and candidate lifetimes was dropped; the Part I detail on lifetimes is therefore not in the abstract. **[AUTHOR]** Read the wording through before it is used.

> Fresh key establishment does not by itself restore trusted satellite telemetry, tracking, and command operation after compromise when intermittent contact, message loss, and endpoint state loss leave ground and spacecraft in different recovery states. Part I studies this problem in a deterministic software model with three baseline abstractions and a bounded resynchronization controller: four matched families, 40 controller schedules, a 100-schedule mixed-fault population, a 3 x 3 sensitivity grid, and bounded TLA+/Python comparisons. The matched families showed categorical parity, not superiority. Of 31 fault cells, 25 succeeded, four were indeterminate, one expired, and one produced an unsafe spacecraft-ahead state. Retries absorbed single drops but not lost verification evidence or destroyed endpoint state; raising the transmission budget from two to three increased verification-complete executions from 5/12 to 11/12. The mixed population produced 74 successes, but only 77 of 191 scheduled faults were reached, so those counts are descriptive, not reliability estimates. Part II computes a six-message activation-and-verification exchange exactly over 7,680 configurations and 207,360 multi-attempt configurations, with hypotheses frozen in the repository beforehand. Plain retries could not clear indeterminate outcomes, whereas resumable verification, an assumption outside the standards, could; bursty loss changed outcomes in both directions; several expected monotonicities failed, and recovery reached the declared 0.95 level in 83-90% of configurations with divergence, rather than almost always. These are properties of the abstraction, not measured link behavior, and loss values are stress parameters. Neither part claims CCSDS conformance. The results support separating candidate state, activation, verification evidence, and persistent recovery state.

Devil's advocate on this text:
- "Frozen in the repository" is accurate (annotated git tags, pushed) but is not an independent timestamp such as OSF. The text therefore says "in the repository", not "pre-registered with a registry". Keep that wording unless you register it externally.
- "Resumable verification" is described as an assumption in the text so a reader cannot take it for a CCSDS feature.
- The 83-90% range covers two retry policies (89.8% and 83.2%); stating one number alone would overstate.

---

## 2. Introduction

### 2a. Insert before "The paper makes four contributions."

> Part I (Sections 3-9) studies the recovery-control exchange in a deterministic fault-injection model. Part II asks a complementary, parametric question: when message loss, spacecraft restarts and short contact windows disrupt the key-activation and verification exchange, how often does the exchange finish, diverge or stall, and how much do persistence, retry and resumability choices change that? CCSDS 355.1-B-1 specifies key activation and key verification as separate procedures, with no recovery procedure found in its text; CCSDS 354.0-M-1 places recovery procedures for master-key-protected procedures outside its scope; and SDLS-DR, a ratcheted extension, does not evaluate contact windows, handover, delay, Doppler or flight hardware [@ccsds_sdls_ep_355_1_b_1; @ccsds_key_mgmt_354_0_m_1; @ledin_sdls_dr_risc2026].

### 2b. Change "four contributions" to "five" and add item 5

> 5. **A pre-specified parametric study of the activation exchange.** Hypotheses, grid and analysis rules were frozen before the confirmatory run, which was computed exactly and reproduced in a second environment. Some hypotheses were supported and others were falsified or only partly supported in the model; the falsifications are reported as model-rule effects, not link behavior.

### 2c. Append to the final scope paragraph ("The scope of the claims is deliberately narrow ...")

> Part II is a parametric model study: its loss values are stress parameters rather than measurements of a TT&C uplink, its six-message exchange has not been independently reviewed, and its recovery-association and resumption parameters are assumptions.

**[AUTHOR]** The scope paragraph says "No independent cryptography review ... was completed". That sentence stays true for Part II. The statement about independent review of the six-message abstraction is a fact only you can confirm.

---

## 3. Conclusion

### 3a. Insert after the TLA+/Python paragraph ("Bounded TLA+/Python comparisons ...")

> Part II extended the question to the activation exchange itself. In an exact model of a six-message abstraction, plain retries could not remove the mass of indeterminate outcomes, while resumable verification could, provided the remaining messages are idempotent, which is an assumption and not a standard feature. Bursty loss changed outcomes relative to independent loss at the same average rate, in both directions. Several expected regularities did not hold: success was not monotone in loss or slot count when restarts occur and state is not journaled; durable persistence sometimes raised ground-ahead divergence; and volatile-state divergence did not always grow with restart probability. The recovery fraction reached the declared 0.95 level in 83-90% of multi-attempt configurations with divergence rather than almost always. These failures arise from the abstraction's rules, in which durable progress can carry more attempts into the window where ground has activated and the spacecraft has not, and they should not be read as behavior of a real link.

### 3b. Replace the first sentence of the final paragraph

Current: "Future work should instantiate the recovery-control layer with concrete reviewed cryptographic mechanisms, evaluate protected persistent-state strategies across endpoint restart, integrate ..."

Proposed: "Future work should instantiate the recovery-control layer with concrete reviewed cryptographic mechanisms, anchor the exchange model to measured TT&C link loss and contact data, obtain an independent review of the exchange abstraction, integrate ..."

Reason: Part II examined persistence levels at the abstract level, so "evaluate protected persistent-state strategies" is partly done; the open gap is now measurement and independent review. **[AUTHOR]** Confirm this reading.

---

## 4. Risks to check before applying
1. Part I is frozen. These edits add framing only; none changes a Part I result. The generated `manuscript.md`, the section files in `paper/manuscript/`, the builder, `references/bibliography.bib` and the TAES workflows are all checksum-locked by `artifacts/manifests/repository-v0.1.1.sha256`, and CI regenerates `manuscript.md` byte-for-byte. Applying these edits to them therefore needs your decision to change those locks; until then the material lives in `paper/two_part/` and a separate builder would read Part I read-only.
2. The abstract and intro now make claims about hypotheses that were falsified. That is deliberate: omitting them would be selective reporting. Do not soften them in review.
3. "Reproduced in a second environment" means the same table digest was recomputed in a Linux container, on a different Python version, by the same assistant that built the code. It is not an external replication, so the text avoids the word "independently".

---

## 5. Title and Sections 7-9 (added 2026-11-19, implemented in the builder)

- **Title (author chose):** "Post-Compromise Satellite TT&C Resynchronization Under Intermittent Links: Fault-Injection and Parametric Studies". The builder's `--title` option overrides it.
- **7.10 Part II and the Part I mechanisms:** links Part I's state-destruction and convergence-versus-verified-recovery findings to Part II's persistence levels and INDETERMINATE outcome; states that no quantitative result is transferred between the two models.
- **8.10 Part II validity:** construct (unreviewed abstraction, stress parameters), external (proxy anchors, not blind), conclusion (repository-only freeze, post-freeze runner amendment, H-E2c operationalization) and same-author reproduction.
- **9.7 Part II artifacts:** code, tests, TLA+, pre-registration and results at the two tags; exact arithmetic; digest reproduced in a second environment; public data deposit planned but not made.
- **Abstract:** v3 spells out "T1" (IEEE abstract guidance asks for self-contained text without undefined abbreviations) and stays at exactly 250 words. The TAES page I found did not state an abstract limit; IEEE-wide guidance found says 150-250 words.
