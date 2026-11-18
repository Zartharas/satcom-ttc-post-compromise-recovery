# Branch 2 continuity handoff: post-compromise satellite TT&C recovery / IEEE TAES

**Captured:** 2026-11-18, America/Chicago. **Purpose:** durable cross-chat state for the next research/development session. **Status:** development and reviewer preparation in progress; NOT submission approved. The author authorized development and publication-readiness work, not unreviewed data release, scientific result replacement, publisher submission or unsafe system experiments.

## Read this first

1. [Master tracking issue #29](https://github.com/Zartharas/satcom-ttc-post-compromise-recovery/issues/29) (this project's action ledger).
2. `PROJECT_STATUS.md`, `paper/manuscript/manuscript.md`, `paper/manuscript/build_integrated_manuscript.py`, `paper/manuscript/reproducibility.md`.
3. `paper/submission/TAES_INTEGRITY_AND_DISCLOSURE_AUDIT_2026-11-18.md`, `paper/supplement/README.md`, `paper/submission/check_taes_citations_and_supplements.py`.
4. Compare the independent, still-unmerged work in [PR #26](https://github.com/Zartharas/satcom-ttc-post-compromise-recovery/pull/26), [PR #27](https://github.com/Zartharas/satcom-ttc-post-compromise-recovery/pull/27), [PR #28](https://github.com/Zartharas/satcom-ttc-post-compromise-recovery/pull/28).
5. F1-F4 hold authority: `paper/extension/ttcsil_integration/INTEGRATED_RECOVERY_GATE_AND_EVIDENCE_CONTRACT_2026-11-17.md`, `paper/extension/TTCSIL_NONOVERLAP_GATE_2026-11-16.md`.

## Verified GitHub checkpoint at handoff

| Object | Confirmed state |
|---|---|
| Primary repo | `Zartharas/satcom-ttc-post-compromise-recovery` (public) |
| Default branch | `main` |
| `main` SHA | `1bda511862f104e82bddcbf95db1ee97702e6c02` |
| Draft PR #26 | `paper/taes-reviewer-pdfs-source-lock-20261118`; head `68a94d8da8842c78baff7eae65a1f06a244a3461`; 2 changed files; no merge |
| Draft PR #27 | `paper/taes-originality-release-holds-20261118`; head `5af63f935745a59de1f9ccb6eefa9c040c2fd17c`; 6 changed files; no merge |
| Draft PR #28 | `paper/taes-p0-prior-art-clarification-20261118`; head `c325d506de14c6c1e2800e2b379bebead6fda5a5`; 4 changed files; no merge |
| Tracking | [Issue #29](https://github.com/Zartharas/satcom-ttc-post-compromise-recovery/issues/29) OPEN |
| Existing CI | Final heads of #26/#27/#28 previously passed their applicable PR workflows; **re-run after any merge/rebase**. Do not treat green CI as scientific or publisher approval. |
| This handoff | Separate, documentation-only draft PR; does not modify existing three PR heads |

Do not interpret a PR marked `mergeable` as a decision to merge. All three PRs branch off the same `main` and modify the repository-wide SHA manifest; **sequential integration requires manifest regeneration and combined CI**, not blind merging. No merge was performed during this handoff.

## Scientific freeze and narrow empirical claims

- Frozen plan commit `cfb730a8191d37863e9e419823686b3c3afe18a2`; plan SHA-256 `3570834a70c76e020dada459e036786f690698125fe1d9f945748a1012`.
- Frozen runner/execution commit `c630fb4f65ad78211fd3ffb0391000d7ed3629b1`; retained run `20260814T022506Z-gc630fb4`.
- Raw retained evidence bundle SHA-256 `b3b8c55a9e522ffe3f7898d7b786583e46a4dc3db0aba9d3947fd6ebdaeecaa1`; retained manifest 16/16 internal integrity. Bundle is not publicly deposited; no DOI. `independent_validation=false` and `publication_evidence=false`.
- **Study A:** four qualified matched families; 13 member rows represent 12 treatment-within-family units because CF-02 B1-01 and B1-05 share one B1 unit; categorical parity, no universal T1 superiority.
- **Study B:** 40 fixed schedules: 1 control, 31 canonical, 8 retry exhaustion. Canonical outcomes 25 SUCCESS, 4 INDETERMINATE, 1 EXPIRED, 1 SECURE_DEGRADED. `SECURE_DEGRADED` is a historic simulator outcome enum; associated `security_state=UNSAFE` must never be laundered into successful security.
- **Study C:** 100 fixed mixed schedules, 74 successes, but only 77 of 191 scheduled fault actions were reached; 43 schedules with zero applied fault. 74 is NOT a success rate under faults.
- **Study D:** 3x3 grid, 108 runs; verification-complete challenge schedules 5/12 at max transmissions 2, 11/12 at 3, 11/12 at 4 across candidate lifetimes 2-4 contacts. No measured operational reliability claim.
- Abstract cryptography, no independent cryptographic review or standards-conformant protected link; NO operational spacecraft, live RF, mission credentials, flight test or independently validated post-compromise security.
- Never rerun, relabel, replace, pool or amend frozen Studies A-D to improve apparent results. Code/docs changes must preserve source fingerprints and test the full derived manuscript.

## TAES publication artifacts and exact scope

**Prior layout-only measurement:** a 19-page `IEEEtran` 10-point/two-column PDF with 250-word abstract, 13 printed references and no logged overfull boxes in the v2 measurement. This is not a publisher-template-authorized full manuscript.

**Uploaded author template:** `IEEE_TAES_templates_latex(1).zip` SHA-256 `35f453d90866185dad95c99f8aff3e455b25e354eed7c8701897900db7215d45`. The Regular Paper subfolder contains `IEEEtaes.cls`, `IEEEtaes.bst`, sample `.tex`, sample PDF. Class SHA-256 `7b3e3d4553f4f871a3e9e3be13c063ea36b21f698a48f6584127b290f86dd7d4`; class says 2022-02-15 V1.1. Uploaded provenance and currency are not independently publisher-certified. It uses `textwidth=41pc`, `columnsep=12pt`, `tablefont=8.25pt`; compare with public TAES approximate 3.45-inch columns / 0.2-inch gap instead of silently overriding the vendor class.

**Already completed isolated evidence:** sample Regular Paper class compiles (seven-page sample, no fatal errors); full-width `table*` fixture containing all 13 Study A member rows and all seven fields, including complete evidence JSON, compiles to two-page specimen with zero overfull LaTeX boxes and ~8.25-point table glyphs. This is a *table-level feasibility proof*, not a complete TT&C manuscript compile. File/ZIP artifacts exist as conversation attachments and may require author reattachment in a new chat; do not assert they are checked into public Git.

**PR #26:** `paper/supplement/render_reviewer_pdfs.py`, source-locked S0/S1 PDF-generation tooling and tracked manifest; S0 13 rows, S1 40 schedules. Draft PDFs and source archive were generated locally and reviewed, but publisher portal accessibility and rights review remain HOLD. Source CSVs and generated Markdown should remain immutable.

**PR #27:** `paper/submission/taes_release_gates.json` with ten HOLD fields, `check_taes_release_gates.py`, `TAES_ORIGINALITY_AND_RELEASE_GATE_2026-11-18.md`, `TAES_TEMPLATE_LAYOUT_FEASIBILITY_2026-11-18.md`, CI integration and SHA manifest. A passing default checker means **holds maintained**, and `--require-ready` fails; it never authorizes submission.

**PR #28:** updates only `background-related-work.md`, generated `manuscript.md`, P0 primary-source adjudication note and SHA manifest. It acknowledges CCSDS Recovery SA prior art, Bader's unresolved cryptographic reestablishment concern and Hülsing/Lange/Weber's explicit lost/out-of-order-fragment handling limitation. Citation reconciliation: 13 unique cited keys in 18 citation-bearing text blocks, 14 BibTeX items; `singh_dissertation` unused and not automatically required. Source-level P0 check does not constitute sentence-by-sentence claim verification.

## Unresolved gates, ranked

1. **P1 merge/readiness integration:** review #26-#28 diffs and conflict-free order; regenerate `artifacts/manifests/repository-v0.1.1.sha256` using `experiments/scripts/validate_repository_manifest.py --write` in a full checked-out repo; run CI/manifest, build-generated-manuscript and supplement checks. Keep PRs draft until reviewed. No publisher release decision follows from CI.
2. **P1 publisher-format proof:** compile the **entire current manuscript**, not only the sample or a Table I fixture, against the supplied/confirmed TAES Regular Paper class with no shell escape; inspect every page, Table I legibility, 3 full-width figures, section flows, tables, reference list, and compare class geometry to official guideline. Verify template authenticity/currentness; DO NOT rewrite the class without independent source authorization.
3. **P1 claim audit:** sentence-level source-to-claim adjudication for all consequential standards, cryptography and empirical claims. The three P0 source groups are *not* a complete audit. Preserve all cited keys and qualify any source-mapping assumptions.
4. **P1 supplements and evidence:** inspect final S0/S1 reviewer PDFs (all rows and JSON), read reviewer README, determine archive and third-party rights and exact controlled-reviewer access. No public raw data/bundle or invented DOI.
5. **AUTHOR-ONLY signoff:** final author name/affiliation/corresponding address/ORCID; substantive AI-generated material inventory and disclosure by section, actual funding/COI/employer IP rights, originality/overlap including any same-manuscript rejection, data availability and consent. These must be author-confirmed privately. Prior separate mission-aware **Paper 2** TAES rejection is **not** a rejection of the present TT&C manuscript.
6. **FINAL publisher decision:** official complete PDF + supplements + portal terms + fees require explicit future user approval. No autonomous submission.
7. **EXTENSION ONLY:** F1-F4 NOS3/cFS integration remains prospective. Controls include exact 48-gitlink software/dependency graph, expected GVCID-to-SPI authorization, independent authenticated TC/TM, cFE message-length bounds, true PID/start-time restart, durable-state proof, dual endpoint logs, independent oracle and negative controls. CVE-2026-79954 / CVE-2026-82480 are source-level risks under review, NOT confirmed exploits in this exact integration. No operational keys, exposed command ports, RF, or experiment campaign.

## Cross-project nonoverlap / related repos (read-only snapshot)

| Repo | `main` SHA at handoff | Keep separate |
|---|---|---|
| [mission-aware-satellite-cyber-recovery](https://github.com/Zartharas/mission-aware-satellite-cyber-recovery) | `7fd87eb1bbfb5ec811bb1f8ec29b4532ac5ff425` | Studies 1-9 decision/evidence; Paper 2 CEAS submitted in technical checks, historical different Paper 2 TAES rejection; P2X PRs #214/#215, source-cited code and cFS fixture overlap boundary; do not import results or alter submitted packages. |
| [verifiable-spacecraft-lifecycle](https://github.com/Zartharas/verifiable-spacecraft-lifecycle) | `f0a26d2edd974827741a53c566b6c79ca2ebdd0b` | S0-S5 software artifact provenance/attestation/rollback; JSSE-D-26-00171 revision 1 prepared for resubmission (status file cites November 22 deadline); do not touch submitted/revision scientific artifacts. |

Cross-repo documentation-only branch PRs link to this checkpoint. No scientific or publisher changes are authorized across repositories by this handoff.

## New-chat operating instruction

Ask the next assistant to: (1) open this file and [Issue #29](https://github.com/Zartharas/satcom-ttc-post-compromise-recovery/issues/29) through GitHub connector, not from memory alone; (2) refresh live repo/PR/CI states; (3) continue publication-readiness development in small reviewable changes with manifest parity and source evidence; (4) preserve frozen science and safety holds; (5) tell the author only which private facts or local source files are truly missing; (6) never claim full TAES template validation, journal approval, external validation, new spacecraft results, active publisher submission or unrelated PR merge without verified evidence.

**Explicit status at handoff: `FROZEN_STUDIES_A_D=UNCHANGED`, `F1_F4_RUNTIME=HOLD`, `TAES_COMPLETE_PUBLISHER_PDF=NOT_BUILT`, `AUTHOR_DECLARATIONS=HOLD`, `PUBLISHER_SUBMISSION_AUTHORIZED=false`.**
