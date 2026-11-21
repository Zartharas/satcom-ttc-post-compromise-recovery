import re

ADDED_KEYS = ("cohn_gordon_pcs_2016", "alwen_double_ratchet_2019", "nasa_cryptolib", "nasa_nos3")


def _rep(text, old, new):
    pat = r"\s+".join(re.escape(w) for w in old.split())
    found = re.findall(pat, text)
    if len(found) != 1:
        raise SystemExit(f"review_fixes anchor count {len(found)} for: {old[:70]}")
    return re.sub(pat, lambda m: new, text, count=1)


def apply_review_fixes(text):
    t = text
    t = _rep(
        t,
        "services needed to operate an SDLS implementation [@ccsds_sdls_ep_355_1_b_1].",
        "services needed to operate an SDLS implementation [@ccsds_sdls_ep_355_1_b_1]. "
        "They include Set and Read ARSN commands and key inventory and verification services, "
        "which help resynchronize anti-replay state but require an operating security association "
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
    return t
