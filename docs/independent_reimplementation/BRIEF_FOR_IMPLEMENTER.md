# Brief for an independent implementer (draft prepared 2026-11-22; not sent to anyone)

Purpose: an independent, blind check that the written specification of the Part I T1 exchange determines the Study B outcomes. The AI-agent re-implementation (docs/study_g/AI_REIMPLEMENTATION_REPORT_2026-11-21.md) was not independent and not blind; this replaces it only if a human does it from the spec alone.

## Give the implementer (specification only)
paper/manuscript/{system-threat-model,recovery-designs,experimental-method}.md, spec/{system-model,t1-requirements,t1-provisional-design,transition-guards,security-invariants}.json (an allowlist, not spec/*.json: phase-09 to phase-14, phase-15-* and baseline-* spec files describe witnesses, outcomes or the review package and must be withheld), docs/phase-15-data-dictionary.md, docs/phase-15-experiment-protocol.md, docs/t1-provisional-design.md.
## Withhold
paper/manuscript/{results,discussion,introduction,conclusion,manuscript}.md and the abstract, paper/tables, results/, src/, tests/, experiments/, study_*/, formal/ and every results figure. Before handing over, the author should grep the given files for result numbers (e.g. "25", "SUCCESS", "INDETERMINATE", "EXPIRED") and redact any aggregate; the earlier attempt leaked through manuscript prose.

## Task
Implement the T1 exchange (ground and spacecraft state machines, channel with the fault kinds in experimental-method.md) and generate the Study B schedule set from the written rule. For each schedule output one CSV row with the header
`schedule_id,schedule_class,fault_kind_or_control,phase_or_control,outcome,alignment,security_state,availability_state,verification_complete,rejection_evidence`
where `rejection_evidence` is a JSON object with keys rejection_count, replay_rejection_count, stale_state_rejection_count (same shape as paper/tables/table-2-deterministic-t1.csv, which the implementer must not see).
Rules: work alone; do not read src/ or run the repository code; write down every point where the spec forced a choice (an assumption log, one line each: question, options, choice, why); do not ask the author for clarifications (ask only about logistics), because a gap in the spec is itself a result.
## Freeze protocol
Before sending outputs: freeze code, CSV and assumption log; record `shasum -a 256` of each and the date/time; send only the hashes first, then the files. The author compares afterwards and does not feed the comparison back for a second attempt unless it is labelled a second round.

## Author-side comparison (run by you, after receiving the frozen CSV)
    python3 docs/independent_reimplementation/compare_study_b.py <implementer.csv>
Reports agreement per field over the 40 schedules (and the 31 canonical cells), lists every disagreeing schedule, and separates the five primary fields (outcome, alignment, security_state, availability_state, verification_complete) from the rejection triple.
Acceptance (proposed, yours to change): all five primary fields agree on all 40 schedules, or every disagreement is traced to a spec ambiguity the implementer logged.

## Known ambiguities the AI run found (do not tell the implementer; check whether they independently hit them)
Duplicate/stale-replay counter attribution; whether a rejection stops retries; STATUS opportunity after a lost TEST; restart semantics; Study B parameters (initial epochs 2/1, floor 0, budget 3, lifetime 3) not stated for Study B itself; delay length.
Fixing these in the spec before handover would give a cleaner test, but editing frozen Part I documents needs your separate approval; a new addendum file that the implementer also gets is an alternative.

## Cost and consent
Their time; any payment, authorship or acknowledgement terms are yours to decide. Share nothing restricted; all listed files are the repository's own text.
