# Line-ending note for Study G result hashes

The CSV writer produced CRLF line endings. `run_manifest.json` and `docs/study_g/STUDY_G_RESULTS.md` record the SHA-256 of the file as written (CRLF):

fe7e36e8388e9b1b5fc8169b3601545b9dabdb3192337793fc475f2f51833b00

This repository normalises text files to LF (`.gitattributes`: `* text=auto eol=lf`), so a fresh checkout of `study_g_out/*/study_g_results.csv` has the LF hash:

a5756dbce9793ff18d129cdabbdbfea13437dfe7b2821d391082ca270bf69c76

Both are the same table. The Linux and device-VM runs agree under either convention. To compare against the recorded hash from a checkout, convert the LF file to CRLF first (`sed 's/$/\r/' file | sha256sum`; verified to give the CRLF hash for the committed file). The same normalisation applies to the other CSV files committed in this change.
