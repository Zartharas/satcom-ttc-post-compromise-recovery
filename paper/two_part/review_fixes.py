import re

ADDED_KEYS = ("cohn_gordon_pcs_2016", "alwen_double_ratchet_2019", "nasa_cryptolib", "nasa_nos3")


def _rep(text, old, new):
    pat = r"\s+".join(re.escape(w) for w in old.split())
    found = re.findall(pat, text)
    if len(found) != 1:
        raise SystemExit(f"review_fixes anchor count {len(found)} for: {old[:70]}")
    return re.sub(pat, lambda m: new, text, count=1)


def _span(text, start, end, new):
    i = text.find(start)
    j = text.find(end, i + 1) if i >= 0 else -1
    if i < 0 or j < 0 or text.count(start) != 1:
        raise SystemExit(f"review_fixes span anchors not found uniquely: {start[:50]}")
    return text[:i] + new + text[j + len(end):]


CONTRIB = (
    "The paper reports four findings, obtained with a conservative comparison framework and a bounded "
    "recovery-control treatment (T1) that serve as the experimental apparatus.\n\n"
    "1. **Convergence is not verified recovery.** In four of 31 single-fault cells the endpoints converged "
    "but the controller lacked command or telemetry evidence, so the outcome was `INDETERMINATE`. Recording alignment, "
    "security state, availability and verification evidence separately exposes states a single success flag hides, "
    "such as a `SECURE_DEGRADED` label with an `UNSAFE` security state.\n"
    "2. **Retransmission absorbs omission, not destroyed state.** Single drops and contact closures were recovered "
    "within the retry budget. An endpoint restart at COMMIT or CONFIRM, and exhausted retries, left a compromised key "
    "active (two of 31 cells and all eight retry-exhaustion schedules). Extra retries cannot rebuild state an endpoint "
    "no longer holds, so pending state needs protected persistence or an authenticated re-initiation path. This follows from the model's rules "
    "and is untested outside the model. Exhaustion before the spacecraft activates leaves the starting divergence "
    "unresolved, whereas exhaustion at CONFIRM leaves the spacecraft ahead.\n"
    "3. **Parity is a boundary, not a result.** Four matched families gave the same authorized categorical outcomes for "
    "the treatments present, but two inject no fault and two hold only B2 and T1, so they cannot discriminate. A later "
    "descriptive run (Study F) found that retransmission alone lets baselines absorb isolated loss. The fixed 100-schedule "
    "mixed population is descriptive and carries no reliability claim.\n"
    "4. **The activation exchange can be analyzed exactly.** In a pre-specified parametric study, hypotheses, grid and "
    "policy set were frozen before the confirmatory run, which was computed exactly and reproduced in a second environment. "
    "Some hypotheses were supported and others falsified or only partly supported; the falsifications are model-rule "
    "effects, not link behavior.\n\n"
)

SCOPE = (
    "The claims are deliberately bounded. Cryptographic operations are abstract, no independent review of the "
    "source-to-model mappings was completed, and the experiment does not establish strong post-compromise security, "
    "CCSDS/SDLS conformance, causal superiority, flight readiness, or real-world fault prevalence. Several Part I findings "
    "are rules of the model: lost verification evidence yields `INDETERMINATE`, a restart destroys volatile pending state, "
    "and the Study D threshold follows from fault multiplicity in a designed set (Table S2). Study F (Supplementary Table S7) "
    "put B0-B2 through step-level faults and found that, with up to three transmissions, every cell with one or two losses "
    "succeeded. Ten of the 40 deterministic schedules end unsafe (Tables S4 and S5). Part II's loss values are stress "
    "parameters, not measurements of a TT&C uplink, and its exchange has not been independently reviewed."
)


def apply_review_fixes(text):
    t = text
    t = _rep(
        t,
        "services needed to operate an SDLS implementation [@ccsds_sdls_ep_355_1_b_1].",
        "services needed to operate an SDLS implementation [@ccsds_sdls_ep_355_1_b_1]. "
        "Set and Read ARSN commands help resynchronize anti-replay state, and key verification and "
        "key inventory let the Initiator check key state, but all of them need an operating security "
        "association, and the text does not present them as recovery from a failed activation "
        "[@ccsds_sdls_ep_355_1_b_1].",
    )
    pair = "[@poettering_roesler_bidirectional_rke; @poettering_roesler_async_rke]"
    if pair not in t:
        raise SystemExit("review_fixes: Poettering pair missing")
    t = t.replace(pair, "[@poettering_roesler_bidirectional_rke]")
    t = _rep(
        t,
        "Ratcheted key exchange keeps evolving state so that new key material replaces earlier state.",
        "Post-compromise security was formalized by Cohn-Gordon, Cremers, and Garratt "
        "[@cohn_gordon_pcs_2016], and Alwen, Coretti, and Dodis analyze the Double Ratchet, "
        "including immediate decryption of later messages after message loss "
        "[@alwen_double_ratchet_2019]. This paper tests neither property; it studies the operational "
        "recovery around them. Ratcheted key exchange keeps evolving state so that new key material "
        "replaces earlier state.",
    )
    t = _rep(
        t,
        "Castanon Remy et al. propose a seven-attribute fidelity framework for space cybersecurity testbeds [@castanon_remy_space_testbed].",
        "Castanon Remy et al. propose a seven-attribute fidelity framework for space cybersecurity testbeds [@castanon_remy_space_testbed]. "
        "NASA's open-source CryptoLib SDLS implementation [@nasa_cryptolib] and the NOS3 simulation framework [@nasa_nos3] "
        "are the natural basis for the follow-up testing this paper does not perform.",
    )
    t = _rep(
        t,
        "These establish that post-compromise key renewal matters and that stateful mechanisms can suit disrupted links.",
        "These establish that post-compromise key renewal matters and that stateful mechanisms can suit disrupted links. "
        "The nearest work, SDLS-DR [@ledin_sdls_dr_risc2026], persists ratchet state at commit points and adds a Recovery association; "
        "its authors did not evaluate contact windows, delay or flight hardware, the setting examined here.",
    )
    t = _rep(
        t,
        "is the design lesson; the simulator does not establish cryptographic security.",
        "is the design lesson; the simulator does not establish cryptographic security. "
        "T1 gives its test-command and status-telemetry steps one attempt each by design, so a lost step stays "
        "`INDETERMINATE` by rule; in Study F a baseline with retransmission absorbs the same loss.",
    )
    t = _rep(
        t,
        "does not force it to occur.",
        "does not force it to occur. A post hoc split of the retained event log shows that all 43 schedules "
        "without an applied fault ended in `SUCCESS`, while the 57 with at least one applied fault ended in "
        "31 `SUCCESS`, 15 `INDETERMINATE`, six `SECURE_DEGRADED` and five `EXPIRED`; the split is descriptive, "
        "was not predeclared, and is not a success rate.",
    )
    t = _rep(
        t,
        "The evidence stays supporting: the macro-step mapping is project-defined,",
        "The evidence stays supporting: both encodings are by the same author, only seven selected single-path traces "
        "were compared, the macro-step mapping is project-defined,",
    )
    t = _rep(
        t,
        "The frozen versions are identified by two permanent labels in that repository",
        "The freeze is recorded by annotated tags that note the author's approval of 2026-11-19; the pre-registration "
        "document itself still carries its freeze-candidate header. The frozen versions are identified by two permanent "
        "labels in that repository",
    )
    t = _rep(
        t,
        "terminated `EXPIRED` with the ground side ahead (`G_AHEAD`),",
        "terminated `EXPIRED` with the ground side ahead (`G_AHEAD`, the unresolved starting divergence, since the ground had not yet activated),",
    )
    t = _rep(t, "A restart at `RECOVERY_CONFIRM` produced", "A ground restart at `RECOVERY_CONFIRM` produced")
    t = _rep(
        t,
        "`RECOVERY_COMMIT` produced `EXPIRED`, `G_AHEAD`, `UNSAFE`, and `UNAVAILABLE`.",
        "`RECOVERY_COMMIT` produced `EXPIRED`, `G_AHEAD`, `UNSAFE`, and `UNAVAILABLE`; `G_AHEAD` is again the unresolved starting divergence.",
    )
    t = _rep(
        t,
        "recovery cannot be guaranteed against indefinite denial [@bader_ttc_key_management].",
        "recovery cannot be guaranteed against indefinite denial [@bader_ttc_key_management]. "
        "The fault schedules inject transport and state faults only; no schedule has the adversary use a compromised key "
        "to issue accepted commands, so `UNSAFE` records that a compromised key is still active at the end of the run, "
        "not an observed exploit.",
    )
    t = _rep(
        t,
        "`ENDPOINT_RESTART` at COMMIT and CONFIRM;",
        "`ENDPOINT_RESTART` of the spacecraft at COMMIT and of the ground at CONFIRM;",
    )
    t = _span(t, "The paper makes four contributions.", "the falsifications are reported as model-rule effects, not link behavior.", CONTRIB.rstrip("\n"))
    t = _span(t, "The scope of the claims is deliberately narrow.", "its exchange has not been independently reviewed.", SCOPE)
    t = _rep(
        t,
        "problem. CCSDS CCSDS_PLACEHOLDER",
        "problem.",
    ) if False else t
    t = _rep(
        t,
        "control-recovery problem. CCSDS Space Data Link Security",
        "control-recovery problem. If recovery stalls or ends asymmetric, operators may be unable to command the spacecraft, "
        "may command on state it has not confirmed, or may leave a compromised key active; the study represents these "
        "consequences only as model outcome labels and does not measure them. CCSDS Space Data Link Security",
    )
    t = _rep(
        t,
        "CCSDS 354.0-M-1 excludes session-key recovery procedures;",
        "CCSDS 354.0-M-1 places recovery procedures for session-key protection and onboard crypto units outside its scope;",
    )
    t = _rep(
        t,
        "The final study addresses four research questions.",
        "The final study addresses four research questions, which decompose the question in Section 1 into baseline matching, "
        "behavior under faults, sensitivity to retry and retention limits, and formal consistency.",
    )
    t = _span(
        t,
        "The results do not support a universal superiority claim for T1 over B0, B1, or B2.",
        "baseline timing\nand retry semantics are equivalent.",
        "The results do not support a universal superiority claim for T1 over B0, B1, or B2; its distinctive evidence comes from "
        "the controlled fault studies, which isolate operational mechanisms without pretending that baseline timing and retry "
        "semantics are equivalent.",
    )
    t = _span(
        t,
        "Recent work has made the post-compromise key-management problem increasingly explicit.",
        "Internet-style sessions [@dowling_hale_tian_wimalasiri_space_key].",
        "Recent work has made the post-compromise key-management problem explicit. Bader identifies post-compromise security, "
        "long-term security, and protection from the beginning of a contact as central TT&C key-management requirements "
        "[@bader_ttc_key_management]. Hülsing, Lange, and Weber proposed a KEM-based key update that provides fresh SDLS key "
        "material without changing SDLS traffic protection [@hulsing_lange_weber_sdls_key_update], and Dowling et al. argue that "
        "intermittent connectivity and long-lived relationships favor stateful or continuous key agreement "
        "[@dowling_hale_tian_wimalasiri_space_key].",
    )
    t = _span(
        t,
        "The study is intentionally hands-on but safe and reproducible.",
        "was predeclared before outcome inspection.",
        "The study uses no operational satellite, live RF transmission, mission credentials, or flight system. A deterministic "
        "simulator represents one authoritative ground security domain and one spacecraft security function across discrete "
        "intermittent contact windows, with faults injected at explicit recovery phases; the final experiment was predeclared "
        "before outcome inspection.",
    )
    return t
