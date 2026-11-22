# Study E data-deposit plan (DRAFT for author decision; not legal advice)
Follows the content-class licensing already used in the Study 8E repository (code MIT; original documentation and author-generated data CC BY 4.0; third-party data under its own terms).

| Item | Class | Proposed treatment |
|---|---|---|
| study_e code, tests, tools | original software | MIT |
| Pre-registration, anchor report text, paper | original documentation | CC BY 4.0 |
| Study E result tables (exchange outcomes) | author-generated data | CC BY 4.0 |
| anchors_report.json / SatNOGS window statistics (durations, gaps, per-pair rows) | derived from SatNOGS API data | Conservatively CC BY-SA 4.0, kept in its own file with attribution to SatNOGS Network; separate from the CC BY 4.0 files |
| Raw SatNOGS trace (476 rows) | third-party data | NOT redeposited; reference by Study 8E freeze record, SHA-256 6f80a44f...a8e, and the public API query recipe |
| Raw Starlink ping files | third-party data (CC BY 4.0, Zenodo 14987305) | NOT redeposited; cite DOI and hashes; aggregate statistics only |
| Published-range numbers (CosmicDancePro, WetLinks, NPS thesis) | cited facts | cite only, no figures or tables copied |

Reasoning: share-alike attaches to adapted material, and whether aggregate statistics are "adapted" is not clear-cut; the conservative route is to license the SatNOGS-derived file CC BY-SA 4.0 and keep it separate so the share-alike does not spread to the rest. This avoids redistributing raw third-party data, while the hashes keep the anchors verifiable.
Open: confirm with a librarian or the venue's data policy if the venue requires raw data; a lawyer's view is the only authoritative answer on share-alike scope.
