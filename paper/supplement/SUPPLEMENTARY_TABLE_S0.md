# Supplementary Table S0 — Full matched-family Study A authorized evidence

Source: `paper/tables/table-1-matched-family-outcomes.csv` (frozen study).

Source SHA-256: `ef29a216b3de050a219e83a0e78c68e3f2f207160418bdafe0a3424a3b94a140`.

Population: 4 qualified families, 13 member rows, 12 treatment-within-family analysis units.
CF-02's B1-01 and B1-05 rows are alternative activation-policy traces in **one B1 analysis unit**, not independent replications.
All seven source fields and complete original evidence JSON are retained in source order.
The security labels are synthetic/provisional classifications, not independently verified cryptographic-security claims.

| family_id | treatment_or_policy_variant | source_id | outcome | alignment_class | availability_state | family_specific_authorized_evidence |
|---|---|---|---|---|---|---|
| CF-01 | B0 | B0-02 | SUCCESS | SYNC | AVAILABLE | {"active_key_compromised":false,"security_state":"SECURE_PROVISIONAL"} |
| CF-01 | B1 | B1-02 | SUCCESS | SYNC | AVAILABLE | {"active_key_compromised":false,"security_state":"SECURE_PROVISIONAL"} |
| CF-01 | B2 | B2-02 | SUCCESS | SYNC | AVAILABLE | {"active_key_compromised":false,"security_state":"SECURE_PROVISIONAL"} |
| CF-01 | T1 | T1-15 | SUCCESS | SYNC | AVAILABLE | {"active_key_compromised":false,"security_state":"SECURE_PROVISIONAL"} |
| CF-02 | B0 | B0-01 | SUCCESS | SYNC | AVAILABLE | {"security_state":"SECURE_PROVISIONAL","verification_complete":true} |
| CF-02 | B1 / B1-01 | B1-01 | SUCCESS | SYNC | AVAILABLE | {"security_state":"SECURE_PROVISIONAL","verification_complete":true} |
| CF-02 | B1 / B1-05 | B1-05 | SUCCESS | SYNC | AVAILABLE | {"security_state":"SECURE_PROVISIONAL","verification_complete":true} |
| CF-02 | B2 | B2-01 | SUCCESS | SYNC | AVAILABLE | {"security_state":"SECURE_PROVISIONAL","verification_complete":true} |
| CF-02 | T1 | T1-01 | SUCCESS | SYNC | AVAILABLE | {"security_state":"SECURE_PROVISIONAL","verification_complete":true} |
| CF-05 | B2 | B2-08 | INDETERMINATE | SYNC | DEGRADED | {"drop_count":1,"security_state":"NOT_ESTABLISHED","telemetry_complete":false,"verification_complete":false} |
| CF-05 | T1 | T1-09 | INDETERMINATE | SYNC | DEGRADED | {"drop_count":1,"security_state":"NOT_ESTABLISHED","telemetry_complete":false,"verification_complete":false} |
| CF-06 | B2 | B2-10 | SUCCESS | SYNC | AVAILABLE | {"rejection_count":1,"replay_count":1,"replay_rejection_count":1} |
| CF-06 | T1 | T1-13 | SUCCESS | SYNC | AVAILABLE | {"rejection_count":1,"replay_count":1,"replay_rejection_count":1} |
