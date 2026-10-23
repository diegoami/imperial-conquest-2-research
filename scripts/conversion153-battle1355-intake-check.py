#!/usr/bin/env python3
"""Read-only consolidation checks for conquest #153/#154. Never runs a game/.NET.

--conquest CHECKOUT --broad-artifacts DIR --private-artifacts DIR --out NEW.json
Private owner inputs/traces are read only by the reviewed audit and entry checks;
only the existing public aggregate, booleans and public packet digests are emitted.
"""
import argparse
import hashlib
import json
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

BROAD = "83d52d2bad99ad8e3870f498cd7d939e0354f482"
BATTLE = "12ae80280609d8d40ec3eca942a7a893af3e5161"
BASE = "runs/experiments/data/"
BP, TP = "run-exp-sav-conversion-broad153", "run-exp-battle1355"


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def load(path):
    return json.loads(path.read_text())


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    for key in ["conquest", "broad-artifacts", "private-artifacts", "out"]:
        ap.add_argument("--" + key, type=Path, required=True)
    a = ap.parse_args()
    require(not a.out.exists(), "Output exists")

    def git(*args):
        return subprocess.check_output(["git", "-C", str(a.conquest), *args])

    def execute(argv, private=False):
        p = subprocess.run(list(map(str, argv)), capture_output=True, text=True)
        require(p.returncode == 0, "Private audit failed; no public result emitted" if private else p.stderr or p.stdout)

    with tempfile.TemporaryDirectory(prefix="ic2-research153-1355-") as tmp:
        root = Path(tmp)
        for packet, pin in [(BP, BROAD), (TP, BATTLE)]:
            names = git("ls-tree", "-r", "--name-only", pin, BASE + packet).decode().splitlines()
            if packet == BP:
                names += [BASE + "run-exp-sav-conversion-roundtrip/compare.py", "state/sav.py",
                          "scripts/sav_export_policy_check.py", "scripts/sav_atlas_coverage.py", "scripts/sav_atlas_invariants.py"]
            for name in names:
                p = root / name
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_bytes(git("show", f"{pin}:{name}"))
        art = root / "artifacts"
        art.mkdir()
        (art / BP).symlink_to(a.broad_artifacts.resolve(), target_is_directory=True)
        (art / TP).mkdir()
        (art / TP / "private-v1").symlink_to(a.private_artifacts.resolve(), target_is_directory=True)
        bp, tp = root / BASE / BP, root / BASE / TP
        execute([sys.executable, bp / "compare.py", "research-comparison.json"])
        execute([sys.executable, bp / "coverage.py", "research-comparison.json", "research-coverage.csv"])
        execute([sys.executable, bp / "validate.py", "research-comparison.json", "research-validation.json"])
        equal = {}
        for old, new in [("comparison-final.json", "research-comparison.json"),
                         ("coverage-final.csv", "research-coverage.csv"), ("validation-final.json", "research-validation.json")]:
            raw = (bp / new).read_bytes()
            require(raw == (bp / old).read_bytes(), "Whole final record differs: " + old)
            equal[old] = dict(identical=True, sha256=sha(raw))
        audit = load(bp / "research-validation.json")
        rows = load(bp / "research-comparison.json")
        archives = []
        for mf in sorted(bp.glob("batch-*-manifest.json")):
            m = load(mf)
            with tarfile.open(a.broad_artifacts / m["archive"]) as tar:
                members = tar.getmembers()
                expected = {x["file"]: x for x in m["files"]}
                require(len(members) == len(expected) and {x.name for x in members} == set(expected), "Tar inventory differs")
                for member in members:
                    require(member.isfile() and Path(member.name).suffix.lower() in {".sav", ".json", ".png"}, "Unexpected tar member")
                    e = expected[member.name]
                    require(member.size == e["bytes"] and sha(tar.extractfile(member).read()) == e["sha256"], "Tar member differs")
            archives.append(dict(name=m["archive"], members=len(members), sha256=m["sha256"]))
        policy_count = 0
        runtime_counts = {}
        for row in rows:
            if not row["export_success"]:
                continue
            name = row["case"]["name"]
            selected = [load(path) for path in sorted(bp.glob("live-" + name + "-v*.json"))]
            selected = [r for r in selected if r.get("complete")][-1]
            require(selected["input_unchanged"], "Measured original input changed")
            require(sha((a.broad_artifacts / "exports-v1" / (name + ".SAV")).read_bytes()) == selected["input_sha256"], "Input receipt hash differs")
            runtime_counts[selected["exe"]] = runtime_counts.get(selected["exe"], 0) + 1
            version = "v2" if (bp / ("return-" + name + "-v2.json")).exists() else "v1"
            returned = a.broad_artifacts / Path(row["original_files"]["reopen"]["file"]).parent
            targets = [a.broad_artifacts / "exports-v1" / (name + ".SAV"),
                       returned / ("REEXPORT-v2.SAV" if version == "v2" else "REEXPORT.SAV")]
            for target in targets:
                out = bp / f"research-policy-{policy_count}.json"
                execute([sys.executable, root / "scripts/sav_export_policy_check.py", target, "--out", out])
                require(load(out)["accepted"], "Fresh policy refusal")
                policy_count += 1
        require(policy_count == 154, "Expected 154 policy passes")
        require(runtime_counts == {"Imperial Conquest 2.exe": 68, "Imperial Conquest 2 fast rollingsave seed.exe": 9}, "Runtime counts differ")
        build = load(bp / "build-source-pin-v1.json")
        for item in build["compile_substitutions"]:
            raw = (a.broad_artifacts / "build-overlay" / Path(item["path"]).name).read_bytes()
            require(sha(raw) == item["sha256"], "Compile overlay digest differs")
            require(hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest() == item["git_blob"], "Compile overlay blob differs")

        execute([sys.executable, tp / "audit_private.py", "research-safe-audit.json"], private=True)
        safe_raw = (tp / "research-safe-audit.json").read_bytes()
        require(safe_raw == (tp / "public-safe-audit-v2.json").read_bytes(), "Sanitized audit differs")
        p = a.private_artifacts
        ready = load(p / "original-end-flow-v3/battle-ready.json")
        matched = load(p / "matched-original-v1/matched-initial.json")
        entry, state = ready["battle_entry"], matched["state"]
        require(entry["half_round"] == state["Counter"] == 2 and entry["x2"] == state["SideToMove"] == 0, "Entry phase differs")
        require(ready["rng_at_battle_entry"] == matched["RandSeed"] and entry["grid"] == state["Grid"], "Entry RNG/grid differs")
        keys = {"X": "x", "Y": "y", "Origin": "merc", "Troops": "troops", "Quality": "quality",
                "Morale": "morale", "Moves": "state", "Shots": "ammo", "Target": "target", "Name": "name"}
        require(len(entry["slots"]) == len(state["Slots"]) == 40, "Entry slot count")
        for original, native in zip(entry["slots"], state["Slots"]):
            require(all(original[v] == native[k] for k, v in keys.items()), "Controlled entry slot differs")
            require(original["type"] == ["li", "hi", "ar", "lc", "hc"][native["Type"]], "Controlled entry type differs")
        actual = load(p / "native-battle-v1/native-initial-tactical-state.json")["Battle"]
        for key in ["Troops", "Type", "Quality", "Moves", "Shots"]:
            require([x[key] for x in actual["Slots"]] == [x[key] for x in state["Slots"]], "Natural entry field differs")
        frames = load(p / "native-battle-v1/native-general-output.json")["frames"]
        require(len(frames) == 1194, "Actual frame count differs")
        result = load(p / "original-end-flow-v3/result.json")
        require(not result["complete"] and "after_battle" not in result, "Unexpected completed original save claim")
        receipt = dict(broad_source=BROAD, battle_source=BATTLE,
                       checker_sha256=sha(Path(__file__).read_bytes()),
                       broad_records=equal, broad_audit=audit, tar_archives=archives,
                       fresh_policy_passes=policy_count, compile_overlay_blobs_verified=2,
                       selected_original_runtime_counts=runtime_counts, all77_original_inputs_preserved=True,
                       battle_safe_audit_sha256=sha(safe_raw), battle_safe_audit=load(tp / "research-safe-audit.json"),
                       controlled_original_entry_all40slots_grid_rng_phase_equal=True,
                       natural_entry_troops_type_quality_moves_ammo_equal=True,
                       actual_native_frame_count=1194, original_postbattle_save_captured=False,
                       limitations=["Read-only artifact/source checks; no new game/.NET/Wine execution",
                                    "No native Windows/owner-twelve-save/exhaustive parity acceptance",
                                    "No exact original instruction/cause/fix or separate model review",
                                    "Owner hashes/paths/full states/traces deliberately excluded",
                                    "Drive remote copies not downloaded"])
        with a.out.open("x") as f:
            json.dump(receipt, f, indent=2)
            f.write("\n")
    print("PASS: exact broad comparison/coverage/audit, 154 policy passes, exact safe battle audit and private entry checks")


if __name__ == "__main__":
    main()
