import os
import unittest
from study_e import guard

ROOT = os.environ.get("TTC_REPO_ROOT")


class FrozenGuard(unittest.TestCase):
    @unittest.skipUnless(ROOT, "set TTC_REPO_ROOT to the TT&C repository checkout (mounted read-only)")
    def test_frozen_study_a_to_d_files_match_manifest(self):
        checked, bad, _missing = guard.check(ROOT)
        self.assertGreater(checked, 0)
        self.assertEqual(bad, [])

    def test_guard_detects_a_modified_file(self):
        import hashlib, tempfile
        with tempfile.TemporaryDirectory() as d:
            os.makedirs(os.path.join(d, "results"))
            os.makedirs(os.path.join(d, "artifacts/manifests"))
            fp = os.path.join(d, "results/x.csv")
            with open(fp, "w") as fh:
                fh.write("a\n")
            h = hashlib.sha256(b"a\n").hexdigest()
            with open(os.path.join(d, guard.MANIFEST), "w") as fh:
                fh.write(f"{h}  results/x.csv\n")
            self.assertEqual(guard.check(d)[1], [])
            with open(fp, "w") as fh:
                fh.write("b\n")
            self.assertEqual(guard.check(d)[1], ["results/x.csv"])


if __name__ == "__main__":
    unittest.main()
