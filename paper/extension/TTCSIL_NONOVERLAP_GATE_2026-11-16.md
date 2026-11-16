# TT&C security-association restart extension — cross-repository non-overlap gate

**Gate ID:** TTCSIL-NONOVERLAP-001  
**Date:** 2026-11-16  
**Status:** DESIGN ONLY; no canonical experiment, new scientific result, paper merge, or publisher action is authorized by this gate.

## Distinct question and scientific boundary

Prospective study `TTCSIL-SA-RST-001` tests whether an **independently instrumented software-in-the-loop ground/spacecraft SA recovery transaction** can avoid false resumption and reach verified commandability across actual application restart at COMMIT/CONFIRM. It measures SA/epoch activation, durable state, acceptance/rejection of fresh and stale commands, and independently observed command/status evidence. It does **not** evaluate mission-aware policy choice, evidence-producer sufficiency, post-quantum object payload feasibility, or software-update artifact assurance.

The existing TT&C Studies A–D are immutable: plan commit `cfb730a8191d37863e9e419823686b3c3afe18a2`, execution `c630fb4f65ad78211fd3ffb0391000d7ed3629b1`, retained run `20260814T022506Z-gc630fb4`, plan SHA-256 `3570834a70c76e020dada459e036786f690698125fe1d9e171e9f945748a1012`, raw-bundle SHA-256 `b3b8c55a9e522ffe3f7898d7b786583e46a4dc3db0aba9d3947fd6ebdaeecaa1`. Do not rerun, relabel, pool, or replace them.

## Cross-project authority at first gate

| Repository | Read-only `main` SHA | Scientific firewall |
|---|---|---|
| [Current TT&C](https://github.com/Zartharas/satcom-ttc-post-compromise-recovery) | `e82a426ec0176059a36ca51b9b491d3c828148d6` | Model-level T1 fault behavior; do not present the prospective implementation as having already validated it |
| [Mission-aware](https://github.com/Zartharas/mission-aware-satellite-cyber-recovery) | `7fd87eb1bbfb5ec811bb1f8ec29b4532ac5ff425` | Exclude Studies 1–7E mission-response selection, evidence qualification, S3X ESA intervals, S6X cFS/Limit Checker artifact tests, and Study 8/8E PQ object/contact-budget endpoints |
| [Mission-aware](https://github.com/Zartharas/mission-aware-satellite-cyber-recovery) | same | Study 8E already uses SatNOGS `POP-002`/`TRACE-002`: 20 traces, 476 source rows, 454 anchors. Do not recycle source observations or claim distinct validation from the same timing/rate estimand |
| [Mission-aware](https://github.com/Zartharas/mission-aware-satellite-cyber-recovery) | same | Studies 5/9 already use CuCD-ID, AegisSat, UNSW-IoTSAT. Study 9 reports 0/8 directly or derivably available operational recovery-decision variables per dataset under its rubric. Never infer TT&C cryptographic/SA truth from attack labels |
| [Verifiable spacecraft lifecycle](https://github.com/Zartharas/verifiable-spacecraft-lifecycle) | `f0a26d2edd974827741a53c566b6c79ca2ebdd0b` | Exclude S0–S5 signing, SBOM, provenance, attestation, rollback, 15-case software artifact matrix and four-target overhead. JSSE revision `JSSE-D-26-00171` remains independent |

## Reuse restrictions

1. Public **upstream cFS/NOS3/CryptoLib software** may be examined and separately version-pinned, subject to licenses and a compatible dependency graph. Prior same-author integrations, frozen source data and analysis code do not establish new external replication or originality.
2. No migration of SatNOGS, ESA v2, CuCD-ID, AegisSat, UNSW-IoTSAT, or any other study's rows into a new TT&C result population. Do not repeat semantic sufficiency, contact feasibility, response selection, or lifecycle assurance under a new label.
3. No copying, pooling, selecting, or republishing results or figures from active/submitted works as new TT&C observations. Cite materially related published work and transparently identify prior submitted same-author work when required.
4. CCSDS 350.5-G-2 §§3.5.1.2 and 4.5.6 already describe **Recovery SAs and segregated non-volatile context**. The extension will not claim to invent recovery SAs, provide a standards-conformant implementation, or prove cryptographic post-compromise security.
5. ECSS-E-ST-70-11C Rev.1 (2025) §§4.2–4.3 provides contingency operability context, not conformance evidence. The aerospace endpoint is verified/restricted return to ordinary TT&C **commandability**.
6. Before outcome execution, refresh all three live repository states and recheck *question, intervention, unit, primary endpoint, artifacts, dataset lineage, and publication status*. If overlap cannot be resolved, STOP.

**Judgment:** Frozen Studies A–D are conditionally separate from the inspected related work. The extension remains **unproven** pending software feasibility, independent oracle, equal-information comparators, and preregistration freeze. The public repository must never receive raw retained bundles or restricted mission/third-party data without separate clearance.
