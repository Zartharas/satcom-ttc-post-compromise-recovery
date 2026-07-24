import csv
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from ttc_recovery.fault_metrics import (
    ExperimentPhase,
    FaultAction,
    FaultKind,
    SeededExperimentConfig,
    run_seeded_experiment,
    write_results,
)
from ttc_recovery.provisional_analysis import (
    adverse_cases,
    aggregate_results,
    annotate_results,
    build_analysis,
    coverage_audit,
    load_phase07_results,
    run_sensitivity_scaffold,
    sha256_file,
    trace_anomalies,
    verify_checksum_manifest,
    verify_metrics_csv,
    write_analysis_outputs,
)


class ProvisionalAnalysisTests(unittest.TestCase):
    def setUp(self):
        self.results = [
            self._run(8001, []),
            self._run(
                8002,
                [
                    FaultAction(
                        ExperimentPhase.STATUS_TELEMETRY,
                        1,
                        FaultKind.DROP,
                        target="ground",
                    )
                ],
            ),
            self._run(
                8003,
                [
                    FaultAction(
                        ExperimentPhase.CONFIRM,
                        attempt,
                        FaultKind.DROP,
                        target="ground",
                    )
                    for attempt in (1, 2, 3)
                ],
            ),
            self._run(
                8004,
                [
                    FaultAction(
                        ExperimentPhase.PREPARE,
                        attempt,
                        FaultKind.DROP,
                        target="spacecraft",
                    )
                    for attempt in (1, 2, 3)
                ],
            ),
            self._run(
                8005,
                [
                    FaultAction(
                        ExperimentPhase.COMMIT,
                        1,
                        FaultKind.DUPLICATE,
                        target="spacecraft",
                    )
                ],
            ),
            self._run(
                8006,
                [
                    FaultAction(
                        ExperimentPhase.RESPONSE,
                        1,
                        FaultKind.DELAY,
                        target="ground",
                        contacts=2,
                    )
                ],
            ),
            self._run(
                8007,
                [
                    FaultAction(
                        ExperimentPhase.COMMIT,
                        1,
                        FaultKind.ENDPOINT_RESTART,
                        target="spacecraft",
                    )
                ],
            ),
            self._run(
                8008,
                [
                    FaultAction(
                        ExperimentPhase.COMMIT,
                        1,
                        FaultKind.STALE_REPLAY,
                        target="spacecraft",
                    )
                ],
            ),
        ]
        self.payload = {
            "schema_version": "0.1.0",
            "status": "PROVISIONAL_INTERNAL_REVIEW_ONLY",
            "result_count": len(self.results),
            "results": [result.to_dict() for result in self.results],
        }

    @staticmethod
    def _run(seed, schedule):
        return run_seeded_experiment(
            SeededExperimentConfig(
                seed=seed,
                ground_epoch=2,
                spacecraft_epoch=1,
                max_transmissions=3,
                candidate_lifetime_contacts=3,
                max_faults=4,
                compromise_active_keys=True,
            ),
            schedule=schedule,
        )

    def test_bundle_and_metrics_csv_verify(self):
        with tempfile.TemporaryDirectory() as directory:
            bundle = Path(directory)
            json_path = bundle / "phase07-results.json"
            csv_path = bundle / "phase07-metrics.csv"
            write_results(self.results, json_path, csv_path)
            provenance = bundle / "run-provenance.txt"
            provenance.write_text("claim_status=PROVISIONAL_INTERNAL_REVIEW_ONLY\n")
            manifest = bundle / "phase07-run-bundle.sha256"
            manifest.write_text(
                "\n".join(
                    f"{sha256_file(path)}  {path.name}"
                    for path in (json_path, csv_path, provenance)
                )
                + "\n",
                encoding="utf-8",
            )

            verified = verify_checksum_manifest(bundle)
            loaded = load_phase07_results(json_path)
            csv_verified = verify_metrics_csv(loaded["results"], csv_path)

            self.assertEqual(verified["verified_file_count"], 3)
            self.assertTrue(csv_verified["json_csv_consistent"])
            self.assertEqual(csv_verified["row_count"], len(self.results))

    def test_checksum_verification_detects_tampering(self):
        with tempfile.TemporaryDirectory() as directory:
            bundle = Path(directory)
            target = bundle / "phase07-results.json"
            target.write_text("original\n", encoding="utf-8")
            digest = sha256_file(target)
            (bundle / "phase07-run-bundle.sha256").write_text(
                f"{digest}  {target.name}\n", encoding="utf-8"
            )
            target.write_text("tampered\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                verify_checksum_manifest(bundle)

    def test_json_csv_mismatch_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            csv_path = Path(directory) / "metrics.csv"
            write_results(
                self.results,
                Path(directory) / "results.json",
                csv_path,
            )
            with csv_path.open("r", encoding="utf-8", newline="") as handle:
                rows = list(csv.DictReader(handle))
            rows[0]["outcome"] = "DIVERGED"
            with csv_path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
                writer.writeheader()
                writer.writerows(rows)
            with self.assertRaises(ValueError):
                verify_metrics_csv(self.payload["results"], csv_path)

    def test_annotations_keep_diagnostic_labels_descriptive(self):
        annotated = annotate_results(self.payload["results"])
        labels = {int(row["seed"]): row["diagnostic_label"] for row in annotated}
        self.assertEqual(labels[8001], "VERIFIED_RECOVERY")
        self.assertEqual(labels[8002], "STATUS_TELEMETRY_LOSS")
        self.assertEqual(labels[8003], "CONFIRMATION_PATH_EXHAUSTION")
        self.assertEqual(labels[8004], "PRE_ACTIVATION_DELIVERY_EXHAUSTION")
        self.assertTrue(
            all(row["diagnostic_status"] == "DESCRIPTIVE_NOT_CAUSAL" for row in annotated)
        )

    def test_valid_records_have_no_trace_anomalies(self):
        self.assertEqual(trace_anomalies(self.payload["results"]), [])

    def test_trace_audit_detects_schedule_hash_tampering(self):
        tampered = json.loads(json.dumps(self.payload["results"]))
        tampered[0]["metrics"]["schedule_sha256"] = "0" * 64
        codes = {row["code"] for row in trace_anomalies(tampered)}
        self.assertIn("SCHEDULE_HASH_MISMATCH", codes)

    def test_aggregates_declare_overlapping_denominators(self):
        annotated = annotate_results(self.payload["results"])
        aggregates = aggregate_results(annotated, min_group_size=3)
        drop_row = next(
            row
            for row in aggregates["by_fault_kind"]
            if row["group_value"] == "DROP"
        )
        overall = aggregates["overall"][0]
        self.assertTrue(drop_row["overlapping_groups"])
        self.assertEqual(drop_row["membership"], "schedule contains fault kind")
        self.assertFalse(overall["overlapping_groups"])
        self.assertEqual(overall["n"], len(self.results))

    def test_coverage_audit_flags_missing_and_low_n_groups(self):
        rows = coverage_audit(
            self.payload["results"],
            required_faults=["DROP", "REORDER"],
            required_phases=["RECOVERY_PREPARE", "TEST_COMMAND"],
            min_group_size=3,
        )
        status = {(row["dimension"], row["value"]): row["status"] for row in rows}
        self.assertEqual(status[("fault_kind", "REORDER")], "MISSING")
        self.assertEqual(status[("fault_phase", "TEST_COMMAND")], "MISSING")
        self.assertEqual(status[("fault_phase", "RECOVERY_PREPARE")], "LOW_N")

    def test_adverse_case_table_excludes_success(self):
        annotated = annotate_results(self.payload["results"])
        rows = adverse_cases(annotated)
        self.assertTrue(rows)
        self.assertTrue(all(row["outcome"] != "SUCCESS" for row in rows))
        self.assertTrue(any(row["outcome"] == "SECURE_DEGRADED" for row in rows))

    def test_sensitivity_reuses_fixed_schedules(self):
        rows, summary = run_sensitivity_scaffold(
            self.payload["results"],
            max_transmissions_values=[2, 3],
            candidate_lifetime_values=[2, 3],
        )
        self.assertEqual(len(rows), len(self.results) * 4)
        self.assertEqual(len(summary), 4)
        source_hashes = {
            result.metrics.schedule_sha256 for result in self.results
        }
        self.assertEqual(
            {row["source_schedule_sha256"] for row in rows}, source_hashes
        )
        self.assertTrue(
            all(row["status"] == "PROVISIONAL_SENSITIVITY_SCAFFOLD" for row in rows)
        )

    def test_analysis_outputs_are_complete_and_checksummed(self):
        analysis = build_analysis(
            self.payload,
            source_json_sha256="a" * 64,
            min_group_size=3,
            required_faults=[kind.value for kind in FaultKind],
            required_phases=[phase.value for phase in ExperimentPhase],
            max_transmissions_values=[2, 3],
            candidate_lifetime_values=[2, 3],
        )
        with tempfile.TemporaryDirectory() as directory:
            paths = write_analysis_outputs(analysis, Path(directory))
            self.assertEqual(len(paths), 14)
            self.assertTrue(Path(paths["analysis_json"]).is_file())
            manifest = Path(paths["checksum_manifest"])
            lines = manifest.read_text(encoding="utf-8").splitlines()
            self.assertEqual(len(lines), 13)
            for line in lines:
                expected, name = line.split(maxsplit=1)
                self.assertEqual(
                    hashlib.sha256((Path(directory) / name).read_bytes()).hexdigest(),
                    expected,
                )


if __name__ == "__main__":
    unittest.main()
