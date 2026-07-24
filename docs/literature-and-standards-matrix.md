# Literature and Standards Matrix

| Source family | Established contribution | Remaining question used by this paper |
|---|---|---|
| CCSDS SDLS | Link-layer traffic protection | Does not alone define complete post-compromise recovery |
| CCSDS Extended Procedures | Key, SA, OTAR, monitoring, and lifecycle procedures | Divergent-state recovery remains insufficiently specified |
| SpaceSec 2024 TT&C key-management analysis | Identifies PCS and synchronization trade-off | How to retain healing while recovering after state loss |
| Triple-KEM/PQNoise key update | KEM-based update with confirmation and optional long-term update | Interrupted, missing, reordered, or partial completion behavior |
| QUIC-MLS | Asynchronous PCS for disconnected QUIC environments | SDLS TT&C command restoration and SA resynchronization |
| NIST FIPS 203 and SP 800-227 | ML-KEM standard and KEM guidance | No TT&C recovery policy or state-restoration procedure |
| Prior dissertation | Practitioner motivation | Controlled quantitative validation of one proposition |

## Provisional novelty statement

To our knowledge, prior work has not experimentally evaluated a bounded, replay-resistant
resynchronization mechanism for SDLS-protected satellite TT&C following compromise-induced
ground-space key-state divergence while jointly measuring attacker exclusion, permanent
lockout, command restoration, and recovery overhead under missed contacts, message faults,
and stale-state restoration.
