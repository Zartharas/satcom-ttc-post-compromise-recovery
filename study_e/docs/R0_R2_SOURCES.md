# Source basis for R0 (Recovery-SA re-bootstrap) and R2 (ratchet skipped-key cache) and EP activation (v0.3.1-dev)
Read from full texts downloaded by the author (2026-11-19). Paraphrased, not quoted. Section numbers as in the downloaded copies; re-check against the final published versions before citing.

## CCSDS 355.1-B-1 (SDLS Extended Procedures, Blue Book, Feb 2020)
- 3.2.3.2 Key Activation: precondition both ends hold the same keys in pre-activation state; the Initiator transitions its keys to Active FIRST, then sends a Key Activation Command; the Recipient activates on receipt. There is no acknowledgement inside the procedure, so an Initiator-ahead window exists by construction. -> supports the model's ground-ahead divergence class (A3). Which side is "ground" in a given mission is mission-specific.
- 3.2.3.5 Key Verification: separate procedure, five steps (challenge creation, signalling, response computation, response signalling, response verification), performed after both ends hold Active keys. The six-message exchange in the model is a PROJECT ABSTRACTION of activation plus verification, not an EP message set.
- The standard contains no recovery-SA or resynchronisation-after-loss procedure text (searched: recovery, lost, desynchron, resync: none).

## CCSDS 350.5-G-2 (SDLS Summary of Concept and Rationale, Green Book, Jan 2024)
- 3.5.1.2 and 4.5.6: a Recovery SA is a last-resort SA at both ends, not for regular operations, whose on-board keys should not be erasable, reloadable or revocable, so telecommanding can be restored when regular SAs are unavailable. (The earlier assumption table cited 350.11-G-1 3.3.4.1 for this; the text found is in 350.5-G-2, corrected.)

## CCSDS 354.0-M-1 (Symmetric Key Management, Magenta Book / Recommended Practice, Dec 2023, 39 pages) - read in full text
- The document exists and is the correct reference number (an earlier search could not find it).
- 4.3.1 Key Activation: same three steps as EP (Initiator activates, signals Key IDs, Recipient activates); the text uses the spacecraft as the Recipient whose previously uploaded session keys are activated. So the ground-side Initiator is ahead by construction (ground-ahead window).
- 3.1.2: the specification of procedures for protecting session keys and authenticating onboard crypto units 'includes recovery procedures' as OUTSIDE its scope. Master keys may serve as recovery keys and may have a longer operational lifetime if justified by the mission threat and risk assessment. -> evidence that recovery/resynchronisation after failed activation is an acknowledged specification gap, not just something SDLS-DR leaves open.
- Keys can also be activated as part of another procedure (e.g. OTAR), and an optional Suspended state exists.

## SDLS-DR (Ledin, Iacovazzi, Raza; IEEE RISC 2026, accepted version)
- State is persisted at each commit point (the pseudocode persists after each encrypt and after each verified decrypt); an orderly reboot resumes without desynchronisation. -> the model's `commit` persistence level.
- Disorderly state loss: recovery proceeds over the Recovery association; the ground detects sustained authentication failure, re-provisions a fresh root key and identity keypair, and the bootstrap stage repeats. The paper gives no message count, detection threshold or timing. -> R0 parameters (n_msgs, detect delay) are MODEL PARAMETERS, not source values.
- Received frames that need skipped keys go to a skipped-key cache; the cache is bounded; an adversary advertising large indices can exhaust it. Frame processing derives on a copy and commits only after the tag verifies; a rejected frame leaves live state untouched. -> R2 `cmax` is a MODEL PARAMETER; the paper does not fix it.
- Stated limitations: no evaluation of contact windows, ground-station handover, range-dependent delay or Doppler, and no flight-hardware evaluation. -> the gap Study E addresses (abstract level only; no claim about their testbed beyond what they state).

## Cremers, Medinger, Naska (IEEE S&P 2025; full version): impossibility results for PCS
- Protocols that must be resilient to certain state loss cannot achieve full conversation PCS. -> frames the Recovery-SA trade-off (static state = guaranteed path, no PCS on that association). Messaging model; transfer to SDLS is an argument, not a theorem.
