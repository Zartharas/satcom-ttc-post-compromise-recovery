TLC reachability cross-check (support only, not probabilities). Needs tla2tools.jar (TLA+ Tools v1.7.4 as used; SHA-256 936a2620...0e88; NOT compared to the publisher's digest).
  java -cp tla2tools.jar tlc2.TLC -deadlock -dump states.dump TtcRecovery.tla
  python3 -I cmp.py states.dump /path/to/study_e   # compares with exact DP support at p=1/3, r=1/4
Independence is limited: same author and same model understanding as the Python code.
