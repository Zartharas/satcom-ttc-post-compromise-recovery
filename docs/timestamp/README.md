# Third-party timestamp: prepared inputs (not executed)

Anchor file: `ANCHOR_2026-11-22.txt` (commit/tree/tar hashes of the three pre-run tags). Reproduce a hash: `git archive --format=tar study-e-prereg-v1 | shasum -a 256`.

## Option A: hash-only (OpenTimestamps). Publishes only a SHA-256 to public calendar servers. Free.
On your Mac, after you decide to do it:
    pip install opentimestamps-client
    ots stamp docs/timestamp/ANCHOR_2026-11-22.txt      # writes ANCHOR_...txt.ots
    # after the Bitcoin attestation confirms (hours), upgrade and verify:
    ots upgrade docs/timestamp/ANCHOR_2026-11-22.txt.ots
    ots verify docs/timestamp/ANCHOR_2026-11-22.txt.ots
Commit the `.ots` proof next to the anchor file. Cannot be undone, but reveals nothing but the hash.

## Option B: Zenodo (GitHub release integration). Publishes the repository contents; a public record cannot be deleted.
Decide first: licence (repo LICENSE is MIT; CITATION.cff says MIT), embargo or not, author metadata (name Aman Kumar Singh; ORCID not found in the repo, yours to supply), and that no restricted material is in the tag. A keyword scan of tracked files (export-controlled, ITAR, proprietary, confidential, CUI, FOUO) hit only policy, threat-model and rules-of-engagement text, not material; please spot-check docs/f1_f4_software_only/ (contains CryptoLib/cFE test output logs under NASA open-source licences) and decide whether to release those.
Zenodo would archive a release, not retroactively the earlier tags; a new tag or release would have a later date.

## What a timestamp proves (state it this way in the paper)
Only that the commits above existed, with these contents, no later than the attestation time. Studies A-D ran before any of this, so a timestamp says nothing about Part I. The tags are annotated but unsigned (tagger is the GitHub noreply identity); signing is optional and does not add third-party time evidence.
