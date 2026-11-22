"""Frozen-record guard: verify that frozen Study A-D files still match the repository SHA-256 manifest."""
import hashlib
import os

FROZEN_PREFIXES = ("results/", "paper/tables/", "experiments/")
MANIFEST = "artifacts/manifests/repository-v0.1.1.sha256"


def check(root, prefixes=FROZEN_PREFIXES):
    """Returns (checked, mismatches, missing)."""
    checked, bad, missing = 0, [], []
    mp = os.path.join(root, MANIFEST)
    if not os.path.isfile(mp):
        raise FileNotFoundError(
            "TTC_REPO_ROOT=%r is not the TT&C repository checkout: manifest %s not found. "
            "Set it to the real path (quote it if it contains spaces); unset it to skip the guard." % (root, MANIFEST))
    with open(os.path.join(root, MANIFEST), encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line.strip():
                continue
            digest, _, path = line.partition("  ")
            path = path.strip().lstrip("*")
            if not path.startswith(prefixes):
                continue
            fp = os.path.join(root, path)
            if not os.path.isfile(fp):
                missing.append(path)
                continue
            with open(fp, "rb") as fh:
                h = hashlib.sha256(fh.read()).hexdigest()
            checked += 1
            if h != digest.strip():
                bad.append(path)
    return checked, bad, missing
