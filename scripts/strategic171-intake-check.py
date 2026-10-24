#!/usr/bin/env python3
"""Offline intake of conquest #1388/#171; no original/Wine run or sibling writes.

Use --conquest --artifact-root --work NEW_PRIVATE_DIR --out NEW.json.
Work outputs contain owner-derived RAM diagnostics: keep the directory private.
Requires retained artifacts, .NET and Python3.12 with Unicorn/Capstone.
"""
import argparse
import hashlib
import json
import os
import subprocess
import tarfile
from pathlib import Path

PIN = "363a9069089bd400c6905f3b93975162395031b3"
DP, CP = "runs/experiments/data/", "runs/experiments/"
PILOT, OWNER = "run-exp-strategic-fidelity", "run-exp-seleucid1388"


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def read(p):
    return json.loads(p.read_text())


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    for key in ["conquest", "artifact-root", "work", "out"]:
        ap.add_argument("--" + key, type=Path, required=True)
    a = ap.parse_args()
    os.umask(0o077)
    require(not a.out.exists(), "Output exists")
    a.work.mkdir(mode=0o700, exist_ok=False)
    root = a.work.resolve()
    py, dotnet = "/home/diego/.local/bin/python3.12", "/home/diego/.dotnet/dotnet"

    def git(*args):
        return subprocess.check_output(["git", "-C", str(a.conquest), *args])

    def source(n):
        return git("show", f"{PIN}:{n}")

    def run(label, argv, expected=0):
        p = subprocess.run(list(map(str, argv)), capture_output=True, text=True)
        (root / (label + "-execution.json")).write_text(json.dumps(dict(returncode=p.returncode, stdout=p.stdout, stderr=p.stderr)))
        require(p.returncode == expected, "Offline check failed; inspect private work logs: " + label)
        return p.stdout

    names = []
    for prefix in [DP + PILOT, DP + OWNER, CP + "strategic-fidelity", CP + "seleucid1388", "harness"]:
        names += git("ls-tree", "-r", "--name-only", PIN, prefix).decode().splitlines()
    names += ["state/__init__.py", "state/sav.py", "state/battle_block.py", "patches/ai_hook.py", "tests/test_ai_hook.py"]
    for n in names:
        if n in [DP + OWNER + "/audit-v1.json", DP + PILOT + "/resupply-original-controls-v1.json"]:
            continue
        p = root / n
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(source(n))
    (root / "tests/__init__.py").write_text("")
    local_art = root / "artifacts"
    local_art.mkdir()
    for name in [PILOT, OWNER]:
        dest = local_art / name
        dest.mkdir()
        for p in (a.artifact_root / name).iterdir():
            if p.name.startswith("resupply-controls") or p.name.startswith("recovery-smoke"):
                continue
            if p.name == "projections":
                (dest / p.name).mkdir()
                for child in p.iterdir():
                    if not child.name.endswith("-research"):
                        (dest / p.name / child.name).symlink_to(child.resolve(), target_is_directory=child.is_dir())
                continue
            (dest / p.name).symlink_to(p.resolve(), target_is_directory=p.is_dir())
    pd, od = root / DP / PILOT, root / DP / OWNER
    pa, oa = local_art / PILOT, local_art / OWNER
    require((pa / "projections").resolve().is_relative_to(root), "Projection outputs escape private intake work")
    source_counts = {}
    for name in [PILOT, OWNER]:
        pin = read(root / DP / name / "source-pin-v1.json")
        for item in pin["files"]:
            b = (local_art / name / "source-v1" / item["path"]).read_bytes()
            require(hashlib.sha1(b"blob " + str(len(b)).encode() + b"\0" + b).hexdigest() == item["git_blob"], "Archived source blob differs")
        source_counts[name] = len(pin["files"])
    cpu = {}
    for code, count in [("seleucid1388", 816), ("strategic-fidelity", 792)]:
        result = json.loads(run("cpu-" + code, [py, root / CP / code / "test_observer.py"]))
        require(result["passed"] == count, "CPU control count differs")
        cpu[code] = result
    run("owner-audit", [py, root / CP / "seleucid1388/audit.py"])
    owner_raw = (od / "audit-v1.json").read_bytes()
    require(owner_raw == source(DP + OWNER + "/audit-v1.json"), "Whole owner audit differs")
    fresh_helpers = root / "owner-original-helpers.json"
    run("owner-original-helpers", [py, root / CP / "seleucid1388/original_replay.py", oa / "private/hook-seed1-v2/defender-prewalk-ram.bin", fresh_helpers])
    require(read(fresh_helpers) == read(oa / "private/original-helpers-v4.json"), "Fresh original helper replay differs")
    run("bundle-recovery", [py, root / CP / "strategic-fidelity/verify_bundle.py", "--version", "research"])
    recovery = read(pd / "bundle-verification-research.json")
    require(recovery["members_verified"] == 504 and recovery["geometry_112_states_byte_identical"], "Four-bundle recovery failed")
    archives = []
    for i in range(1, 5):
        m = read(pd / f"artifact-batch0{i}-manifest-v1.json")
        with tarfile.open(pa / m["archive"]) as tar:
            members = tar.getmembers()
            require(len(members) == len(m["members"]) and {x.name for x in members} == {x["name"] for x in m["members"]}, "Archive has unlisted members")
        archives.append(dict(name=m["archive"], bytes=m["bytes"], sha256=m["sha256"], members=len(m["members"])))
    recovered = pa / "recovery-smoke-research"
    tool = recovered / "tools-v7/Probe.dll"
    cases = read(pd / "case-manifest-v3.json")["cases"]
    replays = []
    for case in cases:
        label = case["label"] + "-hook-v1"
        run("original-" + case["label"], [py, root / CP / "strategic-fidelity/prepare_decisions.py", label, "--version", "research"])
        require((pd / label / "original-decisions-research.jsonl").read_bytes() == (pd / label / "original-decisions-v1.jsonl").read_bytes(), "Whole original decision replay differs")
        projection = pa / "projections" / (label + "-research")
        for mode, expected in [("decisions", "native-decisions-v2.jsonl"), ("eligibility", "original-target-eligibility-v1.jsonl"), ("from-scores", "original-target-from-scores-v1.jsonl")]:
            out = root / (case["label"] + "-" + mode + ".jsonl")
            run("native-" + case["label"] + "-" + mode, [dotnet, tool, mode, recovered, projection, out])
            require(out.read_bytes() == (pd / label / expected).read_bytes(), "Whole gated native row stream differs")
        replays.append(case["label"])
    run("resupply-original", [py, root / CP / "strategic-fidelity/resupply_controls.py"])
    require((pd / "resupply-original-controls-v1.json").read_bytes() == source(DP + PILOT + "/resupply-original-controls-v1.json"), "Six original controls differ")
    supply_out = root / "native-resupply.jsonl"
    run("resupply-native", [dotnet, tool, "decisions", recovered, pa / "resupply-controls-v1", supply_out])
    require(supply_out.read_bytes() == (pd / "resupply-native-controls-v2.jsonl").read_bytes(), "Six gated native controls differ")
    run("pilot-analysis", [py, root / CP / "strategic-fidelity/analyze.py", "--version", "research", "--manifest", "case-manifest-v3.json"])
    for old, new in [("summary-v2.json", "summary-research.json"), ("decision-ledger-v2.jsonl", "decision-ledger-research.jsonl"), ("case-summary-v2.csv", "case-summary-research.csv")]:
        require((pd / old).read_bytes() == (pd / new).read_bytes(), "Complete pilot analysis differs")
    # Re-run corrupt expected-input gates using extracted tools and new private paths.
    negatives = []
    import resource
    for name in ["troops", "relations"]:
        d = root / ("negative-" + name)
        d.mkdir()
        src = pa / "projections/N-rome-hook-v1-research"
        for n in ["000.SAV", "manifest.json"]:
            (d / n).write_bytes((src / n).read_bytes())
        expected = read(src / "000.json")
        if name == "troops":
            expected["armies"][0]["units"][0]["troops"] += 1
        else:
            expected["nations"][0]["relations"]["Carthage"] += 1
        (d / "000.json").write_text(json.dumps(expected))
        out = d / "must-not-exist.jsonl"
        p = subprocess.run([dotnet, str(tool), "decisions", str(recovered), str(d), str(out)], capture_output=True,
                           preexec_fn=lambda: resource.setrlimit(resource.RLIMIT_CORE, (0, 0)))
        require(p.returncode != 0 and not out.exists(), "Corrupted-input gate accepted")
        negatives.append(dict(mutation=name, rejected_before_output=True))
    receipt = dict(source_commit=PIN, checker_sha256=sha(Path(__file__).read_bytes()),
                   archived_git_blobs_verified=source_counts, cpu_controls=cpu,
                   owner_audit_exact=True, owner_audit_sha256=sha(owner_raw), owner_audit=json.loads(owner_raw),
                   original_owner_helpers_replayed_exact=True, bundle_recovery=recovery,
                   exact_archive_inventories=archives, regenerated_projection_outputs_private=True,
                   all_original_and_three_native_modes_replayed_cases=replays,
                   pilot_summary=read(pd / "summary-research.json"),
                   pilot_summary_sha256=sha((pd / "summary-research.json").read_bytes()),
                   full_decision_ledger_and_case_csv_equal=True,
                   geometry= {k:v for k,v in read(pd / "geometry-audit-v1.json").items() if k != "rows"},
                   six_resupply_controls_original_and_native_exact=True, negative_gates=negatives,
                   limits=["Offline instruction/retained diagnostic replay, no new original/Wine or whole-turn game run",
                           "Local tree/scorer/primary destination comparisons, not native greedy command-selection/global RNG equality",
                           "112 correlated states from11inputs; geometry covers land/blocking, not sea-weather equality",
                           "Private owner paths/input hashes/full state/RAM excluded; work directory must stay private",
                           "No independent rebuild/model review, production fix or native Windows acceptance",
                           "Local archive/member recovery only; no remote Drive download claim"])
    with a.out.open("x") as f:
        json.dump(receipt, f, indent=2)
        f.write("\n")
    print("PASS owner audit/helpers; 11case/112state original+native diagnostics; 504bundle members; geometry; six supply and negative gates")


if __name__ == "__main__":
    main()
