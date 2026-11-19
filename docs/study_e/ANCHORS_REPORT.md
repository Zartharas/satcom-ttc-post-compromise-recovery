# Study E anchor report (descriptive; DRAFT; no pre-registered analysis executed)

## Inspection order (read this first)
The Starlink ping summary statistics were inspected BEFORE this report's fitting rule was written, so they cannot be presented as blind. The SatNOGS timing summaries were computed by this tool for the first time; Study 8E's own results (frozen separately) used the same trace, so the author is not blind to its timing behaviour either. The Gilbert-Elliott cases below are therefore a stated sensitivity rule with stress-test values, not parameters fitted to these files.

## 1. SatNOGS POP-002 trace (from Study 8E, re-materialized and hash-verified)
Label: SCHEDULED downlink observation windows; not contacts, not loss, not uplink.
Rows 476, pairs 20, overlaps excluded 0. Source file SHA-256 6f80a44fa6cfa63a70df49de3ba447de3d59efe0632208180f26552f37b46a8e (equals the Study 8E freeze record).

| | n | min | p25 | median | p75 | p90 | max | mean |
|---|---|---|---|---|---|---|---|---|
| window duration (s) | 476 | 180 | 209 | 277 | 406 | 466 | 771 | 314 |
| gap between windows (s) | 456 | 30 | 38046 | 46507 | 85558 | 169550 | 683981 | 76784 |

First-page records only (latest 25 per pair, June 2026 window): not representative, not a full history.

## 2. Starlink ping bursts (Zenodo 10.5281/zenodo.14987305, CC BY 4.0)
Label: consumer LEO BROADBAND (Starlink) ICMP ping bursts; not TT&C, not telemetry, 10 s cadence.

- usable bursts 91580; blank rows excluded 74 (unknown content, never counted as loss)
- packets sent 915800, lost 19777, mean loss 2.160%
- bursts with any loss 8.79%; bursts losing all packets 520
- P(lossy | previous burst lossy) = 0.137; P(lossy | previous ok) = 0.078 (adjacent = spacing <= 15 s and no blank row between)
- lossy run lengths (bursts: count) {'1': 6360, '2': 716, '3': 56, '4': 19, '5': 2, '7': 1}; mean 1.126, max 7
- 10 packets per 10 s: cannot resolve packet-level sojourns or a 15 s handover cycle
- file hashes: {"checked": true, "files": 12, "matches_local_record": true, "limit": "hashes were recorded locally at download; not compared with Zenodo checksums"}

## 3. Modeled pass durations (circular orbit, Earth rotation ignored; MODELED, not measured)

| altitude km | min elev deg | max pass s | mean pass s | slots@30s max/mean | slots@60s max/mean |
|---|---|---|---|---|---|
| 400 | 5 | 474.5 | 373.8 | 15 / 12 | 7 / 6 |
| 400 | 10 | 372.6 | 293.2 | 12 / 9 | 6 / 4 |
| 400 | 20 | 242.0 | 190.2 | 8 / 6 | 4 / 3 |
| 550 | 5 | 589.6 | 465.1 | 19 / 15 | 9 / 7 |
| 550 | 10 | 476.9 | 375.6 | 15 / 12 | 7 / 6 |
| 550 | 20 | 322.2 | 253.4 | 10 / 8 | 5 / 4 |
| 800 | 5 | 764.2 | 604.3 | 25 / 20 | 12 / 10 |
| 800 | 10 | 637.1 | 502.7 | 21 / 16 | 10 / 8 |
| 800 | 20 | 450.2 | 354.4 | 15 / 11 | 7 / 5 |
| 1200 | 5 | 1022.1 | 811.2 | 34 / 27 | 17 / 13 |
| 1200 | 10 | 876.0 | 693.2 | 29 / 23 | 14 / 11 |
| 1200 | 20 | 646.7 | 510.0 | 21 / 16 | 10 / 8 |

Mean assumes closest-approach angle uniform on [0, visibility half-angle] (a convention). The candidate K grid [2, 3, 4, 6] is therefore conservative relative to full geometric passes; K is a count of message slots usable for this exchange, which may be far fewer than geometric slots (command windows, scheduling, contention).

## 4. Matched-stationary Gilbert-Elliott sensitivity cases (pre-specified rule, not a fit)
Good state never loses, bad state always loses, mean bad sojourn m slots, stationary loss equal to the i.i.d. grid value. Invalid combinations (a > 1) are reported as such.

| p stationary | m | a (good->bad) | b (bad->good) |
|---|---|---|---|
| 1/20 | 2 | 1/38 | 1/2 |
| 1/20 | 4 | 1/76 | 1/4 |
| 1/10 | 2 | 1/18 | 1/2 |
| 1/10 | 4 | 1/36 | 1/4 |
| 1/5 | 2 | 1/8 | 1/2 |
| 1/5 | 4 | 1/16 | 1/4 |
| 3/10 | 2 | 3/14 | 1/2 |
| 3/10 | 4 | 3/28 | 1/4 |
| 1/2 | 2 | 1/2 | 1/2 |
| 1/2 | 4 | 1/4 | 1/4 |

## 5. What these anchors do and do not support
- SatNOGS windows: scheduled observation windows by volunteer downlink stations. They bracket plausible window lengths and show uneven scheduling; they say nothing about loss, command uplink or contact gaps.
- Starlink bursts: one consumer broadband link; low average loss with occasional total-loss bursts and mild burst-to-burst persistence at 10 s resolution. Not spacecraft TT&C.
- Pass table: geometry only; real contacts are shorter (masks, terrain, scheduling).
- None of these is a measured TT&C uplink dataset. The paper must call the study parametric, anchored to downlink proxies and published ranges.
