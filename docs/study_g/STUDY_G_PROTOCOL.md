# Study G protocol: does T1 still differ from "B0 plus retransmission plus the outcome vocabulary" when verification steps are retransmitted?

## Status and labelling (read first)
- EXPLORATORY and POST HOC. The question was raised by an external reviewer (MC2) after Study F was run and read. It is not a confirmatory test.
- Same-author. The protocol, the code and the analysis are produced inside the author's own project.
- AI-implemented. The wrapper, grid, tests and this protocol were written by an AI coding assistant (Claude) in a scratch copy of branch study-e-freeze-candidate at d52ae92, then handed to the author.
- NOT pre-registered with any third party. "Written before the run" here means only that this file was fixed, hashed (footer) and committed to the scratch copy before the Study G grid was executed. The author, not the assistant, decides whether to commit and tag it.
- Honest sequencing note: the wrapper and grid code were written before this protocol, and the predictions below were derived by reading the frozen code (t1_controller.py, fault_metrics.py) and the existing Study F CSV, not by running the Study G grid. No Study G grid result had been produced when this file was fixed. The unit tests were run after this file was fixed.
- No inferential statistics, no pooling with Part I, no superiority claim. Part I (Studies A-D), Study E and Study F are frozen and are not edited.

## Question
Part I gives T1's TEST_COMMAND and STATUS_TELEMETRY steps one attempt each (verify_recovery is single-attempt by design), while T1's four recovery messages get up to 3 transmissions. Study F's budget-3 baselines absorb the same single or double loss. The manuscript line "converged is not verified recovery" is therefore partly a design artifact of the retransmission asymmetry. Study G asks: if T1's verification steps get the same budget-3 retransmission policy as the Study F baselines, what, if anything, still separates T1 from "B0 (or B2) plus retransmission plus the outcome vocabulary"?

## Intervention: the retransmission wrapper
- study_g/t1_retry.py defines T1VerificationRetryRunner, a subclass of the Part I experiment runner (ttc_recovery.fault_metrics._ExperimentRunner). It overrides only _pre_delivery. For TEST_COMMAND and STATUS_TELEMETRY, at the single call the Part I runner makes (attempt 1), it makes up to verification_budget transmissions (attempts 1..budget of the same step), stopping at the first delivered one, and returns delivered or dropped to the unmodified runner. Fault actions are looked up per attempt exactly as in Part I. T1Session.verify_recovery is unmodified and still called once with the resulting drop flags.
- No file under src/ is edited. Retransmitting the test command and re-requesting status are assumed safe and idempotent (assumption A-retx-T1, the analogue of Study F's A-retx).
- verification_budget 1 must reproduce Part I exactly (unit test). Recovery-message steps keep Part I's budget of 3 (max_transmissions) in both arms.

## Grid (reused from Study F where it applies)
- Initial state: Study F's T1_BASE, i.e. Part I defaults: ground epoch 2, spacecraft epoch 1, current keys attacker-known (compromise_active_keys=True), max_transmissions 3, candidate_lifetime_contacts 3, seed 0.
- Arms: T1_V1 (verification budget 1 = Part I behaviour) and T1_V3 (verification budget 3 = Study F's budget 3).
- Fault kinds reused from Study F: DROP and CONTACT_CLOSE (loss kinds, assumption A-seq), REORDER, ENDPOINT_RESTART. Loss counts 1, 2, 3 consecutive lost transmissions of the step (attempts 1..n). Budgets 1 and 3.
- T1 steps: RECOVERY_PREPARE, RECOVERY_RESPONSE, RECOVERY_COMMIT, RECOVERY_CONFIRM, TEST_COMMAND, STATUS_TELEMETRY.
- Cells per arm: 1 control + 6 steps x 2 loss kinds x 3 loss counts (36) + REORDER at the four recovery steps (4) + ENDPOINT_RESTART at COMMIT (spacecraft) and CONFIRM (ground) (2) = 43; 86 cells in all. Cell id format: T1|step|kind|c<lost>|V<budget>.
- Not in the grid, not tested: DELAY, DUPLICATE, STALE_COUNTER, STALE_REPLAY (Study F recorded these as NOT_DEFINED for baselines; they stay out), and Study F's native B2 faults (stale ground restore, replayed update), which have no T1 counterpart in this grid.
- Role mapping (an analogy by role, not an equivalence; stored in the grid definition and hashed): PREPARE and RESPONSE map to B0 OTAR_UPLOAD, B1 KEM_INIT_RESPONSE (both policies) and B2 RATCHET_UPDATE; COMMIT and CONFIRM map to B1 KEM_CONFIRM (both policies); TEST_COMMAND and STATUS_TELEMETRY map to B1_DEFERRED AUTHENTICATED_STATUS and B2 STATUS_TELEMETRY. REORDER maps to B1 KEM_INIT_RESPONSE REORDER; ENDPOINT_RESTART maps to B1 KEM_CONFIRM ENDPOINT_RESTART. Study F rows are read from study_f_out/mac/study_f_results.csv, not recomputed, except the exposure column (below).

## Outcome fields (one row per cell)
outcome, alignment, security_state, availability_state, verification_complete, command_accepted, telemetry_complete, total_transmissions, divergent_contact_windows, active_key_compromised, spacecraft_on_compromised_key and ground_on_compromised_key (exposure at end: whether each endpoint's active key is still an attacker-known key). Exposure for the Study F baselines is computed by re-executing Study F's step functions on the same inputs, after checking that the re-execution reproduces every Study F outcome, alignment and security_state row; if it does not, exposure for baselines is reported as unavailable.

## Denominator and reporting rules
All 86 Study G cells are reported; none is excluded after the run. Counts are of cells in a designed grid, not of probabilities, and carry no sampling interpretation. Unfavourable results are reported. A cell-level comparison is shown for T1_V1, T1_V3 and the Study F B0, B1_LOCAL, B1_DEFERRED, B2 rows at budgets 1 and 3.

## Hypotheses (stated as predictions that can fail)
- P1. At TEST_COMMAND and STATUS_TELEMETRY, with DROP or CONTACT_CLOSE and 1 or 2 lost transmissions, T1_V3 ends SUCCESS, SYNC(3), verification_complete true, SECURE_PROVISIONAL. That is 8 cells; the four Part I canonical INDETERMINATE cells (one loss per step and kind) are among them. Failure of this would mean the wrapper or the verification logic does not absorb loss.
- P2. With 3 lost transmissions at those two steps, T1_V3 ends INDETERMINATE, SYNC(3), NOT_ESTABLISHED, verification_complete false (4 cells), the same classification as T1_V1 and as Study F's B2 STATUS_TELEMETRY c3 R3 row.
- P3. T1_V1 ends INDETERMINATE in all 12 verification-step loss cells (lost 1, 2 or 3), reproducing Part I.
- P4. For the 24 recovery-step loss cells and the REORDER and ENDPOINT_RESTART cells, T1_V1 and T1_V3 rows are identical in every field (the wrapper does not touch them).
- P5. In the recovery steps, 1 or 2 lost transmissions end SUCCESS; 3 lost end EXPIRED at PREPARE, RESPONSE and COMMIT and SECURE_DEGRADED at CONFIRM (spacecraft activated, ground never confirmed). ENDPOINT_RESTART at COMMIT ends EXPIRED (G_AHEAD) and at CONFIRM ends SECURE_DEGRADED (S_AHEAD). Any miss is a finding, reported as such.
- P6. For each mapped (T1 step, baseline step) pair and each loss count 1, 2, 3, T1_V3 and the budget-3 baseline row agree on SUCCESS versus not-SUCCESS (success for 1 or 2 lost, not-success for 3). If true, the loss grid at equal retransmission shows no difference in the success partition between T1 and the baselines.
- P7. Where outcomes still differ between T1_V3 and the matched budget-3 baseline row, the difference is in the outcome label or alignment (for example SECURE_DEGRADED versus DIVERGED, EXPIRED versus LOCKED), not in whether recovery succeeded. If a success/not-success difference appears, it is reported as a remaining distinction.
- P8 (exposure). T1 INDETERMINATE cells have spacecraft_on_compromised_key false (keys rotated, only verification missing), while every non-SUCCESS, non-INDETERMINATE T1 cell and every non-SUCCESS baseline cell has the spacecraft or ground still on a compromised key. If INDETERMINATE cells show exposure, say so.
- Overall expectation, stated so that it can be wrong: at budget 3, nothing in this grid distinguishes T1 from "B2 (or B0) plus retransmission plus the outcome vocabulary" in the SUCCESS/not-SUCCESS partition; the remaining differences are the label vocabulary and the verification requirement itself (B0 and B1_LOCAL in the frozen abstraction have no separate verification step and are scored verification_complete on delivery).

## Not covered
Active attackers beyond Part I scopes, cryptographic properties, timing, retry-count comparison across treatments, fault kinds outside the grid, pooled scores. Baselines are the frozen abstractions, not the published protocols.

## Run procedure
1. Fix and hash this file (footer). 2. Run unit tests. 3. Run study_g/run_grid.py once; it refuses to run if the footer hashes do not match. 4. Keep all outcomes. 5. Deviations are recorded in a separate file, never by editing this protocol. 6. The author, not the assistant, commits and tags.

Hash convention: protocol hash = SHA-256 of this file's bytes up to (not including) the footer marker line; grid hash = SHA-256 of the canonical JSON of the grid definition (config, ordered cell ids, role map), produced by study_g.run_grid.grid_sha256().

<!-- STUDY_G_FOOTER -->
protocol_body_sha256: 74d6d7683fded82bf794ead5fdb08d5216141aba135801f280bd74c9a1303606
grid_sha256: 757b768a97864e0edc0f453c64cb9bb54aaedf7361b402048998def61c2cb26e
base_commit: d52ae92 (branch study-e-freeze-candidate); not tagged
