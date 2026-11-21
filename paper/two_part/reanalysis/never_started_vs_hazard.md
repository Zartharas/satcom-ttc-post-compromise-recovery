# Never-started versus new-hazard split (read-only reanalysis of retained raw JSON)

## study_b: 40 schedules, 10 UNSAFE

- no_rotation_at_either_endpoint_never_activated: 5
- no_rotation_recovery_never_reached_spacecraft: 2
- spacecraft_rotated_ground_locked_out: 3

  - ('no_rotation_at_either_endpoint_never_activated', 'EXPIRED', 'G_AHEAD'): 5
  - ('no_rotation_recovery_never_reached_spacecraft', 'EXPIRED', 'G_AHEAD'): 2
  - ('spacecraft_rotated_ground_locked_out', 'SECURE_DEGRADED', 'S_AHEAD'): 3

## study_c: 100 schedules, 11 UNSAFE

- no_rotation_at_either_endpoint_never_activated: 5
- spacecraft_rotated_ground_locked_out: 6

  - ('no_rotation_at_either_endpoint_never_activated', 'EXPIRED', 'G_AHEAD'): 5
  - ('spacecraft_rotated_ground_locked_out', 'SECURE_DEGRADED', 'S_AHEAD'): 6
