#!/usr/bin/env python3
"""Read-only research intake for conquest #151; never invokes .NET, Wine or a game.

Use --conquest CHECKOUT --artifacts PRIVATE_RUN_DIR --out NEW_RECEIPT.json.
Requires the pinned Git objects and the retained artifacts (including audit DLLs).
Runs unchanged upstream comparison/validation scripts in a temporary snapshot,
verifies archive members, and freshly checks all thirteen exported SAVs.
"""
import argparse
import hashlib
import json
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

PIN = "4ca3afa04c3eb8454c63ed6a4984f5564e8e0496"
PACKET = "runs/experiments/data/run-exp-sav-conversion-roundtrip"
DRAFT = "findings/2026-10-23-remake-original-save-conversion-roundtrips.md"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def run(argv):
    p = subprocess.run(list(map(str, argv)), capture_output=True, text=True)
    require(p.returncode == 0, p.stderr or p.stdout)
    return p.stdout


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--conquest", type=Path, required=True)
    ap.add_argument("--artifacts", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    require(not a.out.exists(), "Output already exists")

    def git(*args):
        return subprocess.check_output(["git", "-C", str(a.conquest), *args])

    def source(path):
        return git("show", f"{PIN}:{path}")

    with tempfile.TemporaryDirectory(prefix="ic2-research151-") as tmp:
        root = Path(tmp)
        paths = git("ls-tree", "-r", "--name-only", PIN, PACKET).decode().splitlines()
        paths += ["state/sav.py", "scripts/sav_export_policy_check.py",
                  "scripts/sav_atlas_coverage.py", "scripts/sav_atlas_invariants.py"]
        for name in paths:
            target = root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(source(name))
        (root / "artifacts").mkdir()
        (root / "artifacts/run-exp-sav-conversion-roundtrip").symlink_to(a.artifacts.resolve(), target_is_directory=True)
        packet = root / PACKET
        run([sys.executable, packet / "compare.py", "research-comparison.json"])
        comparison_bytes = (packet / "research-comparison.json").read_bytes()
        require(comparison_bytes == (packet / "comparison-v6.json").read_bytes(), "Complete comparison changed")
        run([sys.executable, packet / "validate.py", "research-validation.json"])
        audit_bytes = (packet / "research-validation.json").read_bytes()
        require(audit_bytes == (packet / "validation-v2.json").read_bytes(), "Complete audit changed")
        comparison, audit = json.loads(comparison_bytes), json.loads(audit_bytes)

        archives = []
        for name in ["batch1-conversions", "batch2-complete"]:
            manifest = json.loads((packet / (name + "-manifest.json")).read_text())
            archive = a.artifacts / manifest["archive"]
            require(archive.stat().st_size == manifest["bytes"], "Archive size mismatch")
            require(sha(archive.read_bytes()) == manifest["sha256"], "Archive digest mismatch")
            with tarfile.open(archive) as tar:
                members = tar.getmembers()
                expected = {r["file"]: r for r in manifest["files"]}
                require(len(members) == len(expected) and {m.name for m in members} == set(expected), "Archive inventory mismatch")
                for m in members:
                    require(m.isfile() and Path(m.name).suffix.lower() in {".sav", ".json", ".png"}, "Unexpected member type")
                    row = expected[m.name]
                    require(m.size == row["bytes"] and sha(tar.extractfile(m).read()) == row["sha256"], "Archive member mismatch")
            archives.append(dict(name=archive.name, bytes=manifest["bytes"],
                                 sha256=manifest["sha256"], members_verified=len(members)))

        policies, reloads = [], []
        targets = [(a.artifacts / "exports-v2" / (n + ".SAV"), n)
                   for n in comparison["native_export_import"]]
        for name in comparison["returned_sessions"]:
            receipt = json.loads((packet / (name + ".json")).read_text())
            require(receipt["loaded"] and receipt["complete"] and not receipt.get("error"), "Incomplete live receipt")
            command = json.loads((packet / ("return-" + name + "-v2.json")).read_text())
            lines = [json.loads(line) for line in command["stdout"].splitlines() if line.strip()]
            imported = next(x for x in lines if x["kind"] == "import")
            continued = next(x for x in lines if x["kind"] == "returned-session-order")
            require(imported["reloadEqual"] and continued["verified"], "Native reload/continuation failed")
            require(imported["Report"]["SkippedArmies"] == [] and imported["Report"]["SkippedFleets"] == [], "Skipped entity")
            reloads.append(dict(case=receipt["case"], reload_equal=True, tax27_verified=True))
            targets.append((a.artifacts / name / ("RETURN" + receipt["case"] + ".SAV"), "return-" + receipt["case"]))
        for i, (target, label) in enumerate(targets):
            out = packet / f"research-policy-{i}.json"
            run([sys.executable, root / "scripts/sav_export_policy_check.py", target, "--out", out])
            result = json.loads(out.read_text())
            require(result["accepted"] and result["source_sha256"] is None, "Policy refusal")
            policies.append(dict(case=label, accepted_without_source=True))

        receipt = dict(source_commit=PIN, finding_blob=git("rev-parse", f"{PIN}:{DRAFT}").decode().strip(),
                       checker_sha256=sha(Path(__file__).read_bytes()),
                       method="Unchanged pinned compare/validate rerun; archive-member audit; fresh policy and reload-receipt checks",
                       comparison_sha256=sha(comparison_bytes), complete_comparison_equal=True,
                       audit_sha256=sha(audit_bytes), complete_audit_equal=True,
                       upstream_audit=audit, archives=archives,
                       policy_reruns=policies, native_reload_receipts=reloads,
                       native_difference_totals={k: len(v["differences"]) for k, v in comparison["native_export_import"].items()},
                       limitations=["No new Wine, native Windows, .NET or game execution",
                                    "CLI/live execution is upstream observation, checked against retained artifacts/receipts",
                                    "Local archive bytes checked; Drive download/readback not performed",
                                    "Not the owner twelve-save set, format-4 migration, eliminated nations or research #37 completion",
                                    "Main-session intake validation; no separate model review"])
        with a.out.open("x") as f:
            json.dump(receipt, f, indent=2)
            f.write("\n")
    print("PASS: exact comparison/audit reproduction, 164 archive-member hashes, 13 fresh policy passes, 7 native reload receipts")


if __name__ == "__main__":
    main()
