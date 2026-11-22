# TLA+ tools digest check (post hoc, 2026-11-21)

The tla2tools.jar of the TLA+ v1.7.4 release was downloaded from the official GitHub release asset and hashed.

- SHA-1 `bee4a54f3ee3d4afc347c3240ec2d9e93b075104`. The release page lists this value for the asset (it lists no SHA-256).
- SHA-256 `936a262061c914694dfd669a543be24573c45d5aa0ff20a8b96b23d01e050e88`, identical to the value recorded in `docs/phase-10-formal-model-execution.md`.

This closes the open note that the jar digest had not been compared with the publisher's. It checks only that the recorded jar is the published one; it does not re-run TLC.
