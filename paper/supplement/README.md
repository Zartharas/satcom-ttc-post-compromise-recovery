# Supplementary materials for TAES peer review

**Status: complete source-locked tables available; not yet a publisher-ready supplementary submission package.**

These two tables are part of the existing **frozen synthetic** study. They are not independent spacecraft, flight, RF, cryptographic or software-in-the-loop validation. Submit them together with the regular manuscript for review, as required by the [TAES author instructions](https://ieee-aess.org/publications/transactions-aes/author-information).

| Item | Contents | Authoritative immutable source | Integrity/rebuild command |
|---|---|---|---|
| [Supplementary Table S0](SUPPLEMENTARY_TABLE_S0.md) | All 13 Study A member rows, original seven fields and family-authorized evidence JSON; 12 analysis units (CF-02's two B1 policy traces count as one) | `paper/tables/table-1-matched-family-outcomes.csv` | `python3 paper/supplement/build_table_s0.py --check` |
| [Supplementary Table S1](SUPPLEMENTARY_TABLE_S1.md) | All 40 Study B deterministic schedules and original ten fields; 1 control, 31 canonical cells, 8 retry-exhaustion cases | `paper/tables/table-2-deterministic-t1.csv` | `python3 paper/supplement/build_table_s1.py --check` |

For the complete code provenance, execution plan and retained-bundle identity, see `paper/manuscript/reproducibility.md`. The large original raw bundle is retained externally and **has not been publicly deposited or assigned a persistent DOI**. These tables do not replace that raw archive.

**Important outcome semantics:** `SECURE_DEGRADED` is a historical simulator enum; for adverse cases the authoritative `security_state=UNSAFE` must be retained. Study C's 74 successful schedules do not establish 74% success under applied faults; the observed execution coverage is a separate caveat in the manuscript.

## Pre-submission checklist (not yet approved)

- [x] Main manuscript explicitly refers to both S0 and S1.
- [x] S0/S1 generated and checked against frozen original source CSVs, with no row removal.
- [ ] Produce separate, legible, paginated reviewer PDF(s) or editor-accepted supplemental format; inspect all tables.
- [ ] Provide any necessary code/data access without disclosing private credentials, restricted mission data, or raw bundles before a separate rights review.
- [ ] Confirm supplementary upload and viewer accessibility in the TAES submission portal.
- [ ] Confirm text and table reuse rights and complete availability statement.

The journal's instructions request supplementary files for peer review, not merely references to a public GitHub repository. No publisher upload, archival DOI, or permission clearance is implied by this README.
