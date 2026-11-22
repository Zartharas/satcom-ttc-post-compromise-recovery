# Pre-registration v3 draft: changes to carry from v2 (NOT FROZEN)
- Model = v0.3.0-dev: single-attempt core + GE channel option + multi-attempt run over H contacts (rules in MULTI_ATTEMPT_RULES.md).
- Outcome key (outcome, end_contact, attempts); primary endpoints: P(SUCCESS), P(fallback required), P(INDETERMINATE), expected attempts, expected contacts to success.
- H-E2a (revised): SUCCESS non-decreasing in B, K, L, H; non-increasing in p. Divergence is reported, not assumed monotone.
- H-E3 (new): with EXPIRED_OLD-only retry, increasing H beyond L changes SUCCESS by less than the INDETERMINATE mass (retry cannot address INDETERMINATE); resumable verification is the lever.
- H-E2b/H-E2c unchanged from v2.
- Sensitivity: retry_on includes INDETERMINATE; bursty channel (GE) with stationary loss matched to the i.i.d. grid.
- Validation: exact == enumeration (exact rational) incl. multi-attempt and GE; closed forms (total loss, one-contact geometric); MC within 4.5 SE; mutants killed; TLC support check; frozen-record guard.
- Grid size and parameter values: to be fixed by the author before freeze.
