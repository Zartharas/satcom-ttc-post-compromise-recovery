# study_g (EXPLORATORY, post hoc, same-author, AI-implemented, not third-party pre-registered)
Study G reruns Study F's step-level loss grid on T1 with a verification retransmission budget of 3
(T1_V3) beside Part I behaviour (T1_V1). Protocol: docs/study_g/STUDY_G_PROTOCOL.md. Adds files only;
nothing under src/, tests/, results/, paper/, study_e/ or study_f/ is edited.

- t1_retry.py: wrapper (subclass of the Part I runner; only `_pre_delivery` overridden).
- run_grid.py: grid definition, hashes, runner. `PYTHONPATH=src:. python3 -m study_g.run_grid --out OUT`
  (refuses to run if the protocol footer hashes do not match).
- tests: `PYTHONPATH=src:. python3 -m unittest discover -s study_g/tests -p 'test_*.py' -t .`
