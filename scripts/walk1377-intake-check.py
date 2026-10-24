#!/usr/bin/env python3
"""Offline #1377 intake. No original/Wine run, sibling source or registry writes.

Required: --conquest --remake --artifact-root --exe --work NEW_PRIVATE_DIR --out NEW.json.
Private replay outputs and logs remain under --work; never publish that directory.
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys
import tarfile
import xml.etree.ElementTree as ET
from pathlib import Path

PIN = "e1a943d5f9de8b88787112f137ad8053a699e6e0"
DP = "runs/experiments/data/"
CP = "runs/experiments/"
PACKET, PARITY = "run-exp-battle-residual157", "run-exp-battle-parity157"


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read(p):
    return json.loads(p.read_text())


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    for n in ["conquest", "remake", "artifact-root", "exe", "work", "out"]:
        ap.add_argument("--" + n, type=Path, required=True)
    a = ap.parse_args()
    os.umask(0o077)
    require(not a.out.exists(), "Output exists")
    a.work.mkdir(mode=0o700, exist_ok=False)
    root = a.work.resolve()
    art, pa = a.artifact_root / PACKET, a.artifact_root / PARITY
    dotnet = "/home/diego/.dotnet/dotnet"

    def git(*args):
        return subprocess.check_output(["git", "-C", str(a.conquest), *args])

    def source(n):
        return git("show", f"{PIN}:{n}")

    def run(label, argv, expected=0, env=None):
        p = subprocess.run(list(map(str, argv)), capture_output=True, text=True, env=env)
        (root / (label + "-execution.json")).write_text(json.dumps(dict(returncode=p.returncode, stdout=p.stdout, stderr=p.stderr)))
        require(p.returncode == expected, "Offline check failed; inspect private work logs: " + label)

    names = []
    for prefix in [DP + PACKET, DP + PARITY, CP + "battle-residual157", CP + "battle-parity157"]:
        names += git("ls-tree", "-r", "--name-only", PIN, prefix).decode().splitlines()
    names += ["state/__init__.py", "state/sav.py", "state/battle_block.py", "state/hook_log.py", "patches/battle_hook.py", CP + "tactical25-trace/observer.py"]
    for n in names:
        if n.startswith(DP + PACKET + "/control-replay-v1/") or n == DP + PACKET + "/original-gate-v1.json":
            continue
        p = root / n
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(source(n))
    data = root / DP / PACKET
    local_art = root / "artifacts"
    local_art.mkdir()
    (local_art / PARITY).symlink_to(pa.resolve(), target_is_directory=True)
    (local_art / PACKET).mkdir()
    for n in ["fixtures-v1", "replay-cached-live-v1"]:
        (local_art / PACKET / n).symlink_to((art / n).resolve(), target_is_directory=True)

    identity = read(data / "source-identity-audit-v1.json")
    general = a.artifact_root / "run-exp-faithful-general157/source-v2"
    for item in identity["general_source_blobs_verified"]:
        raw = (general / item["file"]).read_bytes()
        require(hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest() == item["git_blob"], "T206 general source differs")
    helper_dir = a.remake / "tests/IC2.Engine.Tests/Battle/Tactical/GoldenMaster"
    for n, digest in identity["upstream_comparator_source_sha256"].items():
        require(sha((helper_dir / n).read_bytes()) == digest, "Upstream helper source differs")
    pins = read(data / "variant-sources-v1.json")
    rel = "src/IC2.Engine/Battle/Tactical/TacticalMovement.cs"
    raw = (a.remake / rel).read_bytes()
    require(sha(raw) == pins["original_sha256"], "Movement base differs")
    for row in pins["variants"]:
        tree = root / ("patch-" + row["variant"])
        dst = tree / rel
        dst.parent.mkdir(parents=True)
        dst.write_bytes(raw)
        patch = data / ("movement-" + row["variant"] + ".patch")
        p = subprocess.run(["git", "apply", str(patch)], cwd=tree, capture_output=True)
        require(p.returncode == 0, "Isolated patch application failed")
        require(sha(dst.read_bytes()) == row["source_sha256"] and dst.read_bytes() == (art / ("source-" + row["variant"] + "-v1") / "TacticalMovement.cs").read_bytes(), "Patched source differs")

    exe = a.exe.read_bytes()
    require(sha(exe) == "9d753d5de78801f2368d06125cc87f296b92f671b686c39fd6ac149838ebba31", "Original EXE pin")
    import struct
    pe = struct.unpack_from("<I", exe, 60)[0]
    count, opt = struct.unpack_from("<H", exe, pe + 6)[0], struct.unpack_from("<H", exe, pe + 20)[0]
    def code(va, length):
        for i in range(count):
            _, rva, size, off = struct.unpack_from("<4I", exe, pe + 24 + opt + i * 40 + 8)
            if rva <= va - 0x400000 < rva + size:
                start = off + va - 0x400000 - rva
                return exe[start:start + length]
        raise RuntimeError("Code address outside PE")
    for va, expected in [(0x438D66, "8bf8"), (0x438ED1, "66833c854c034a00007e0d"), (0x438EE2, "e825020000")]:
        require(code(va, len(bytes.fromhex(expected))) == bytes.fromhex(expected), "Original instruction guard differs")

    archive_checks = []
    specs = [(read(root / DP / PARITY / "seed2-semantic-batch01-manifest.json"), pa),
             (read(data / "tools-batch02-manifest-v1.json"), art), (read(data / "fixed-tools-batch03-manifest-v1.json"), art)]
    for m, folder in specs:
        archive = folder / m["archive"]
        require(sha(archive.read_bytes()) == m["sha256"] and archive.stat().st_size == m["bytes"], "Archive digest/size differs")
        expected = {x["name"]: x for x in m["members"]}
        with tarfile.open(archive) as tar:
            members = tar.getmembers()
            require(len(members) == len(expected) and {x.name for x in members} == set(expected), "Archive inventory differs")
            for x in members:
                require(x.isfile() and x.size == expected[x.name]["bytes"] and sha(tar.extractfile(x).read()) == expected[x.name]["sha256"], "Archive member differs")
        archive_checks.append(dict(name=m["archive"], bytes=m["bytes"], sha256=m["sha256"], members=len(expected)))
    recovered = read(data / "fixture-recovery-v1.json")
    for x in recovered["files"]:
        b = (art / "fixtures-v1" / x["path"]).read_bytes()
        require(len(b) == x["bytes"] and sha(b) == x["sha256"], "Selected fixture differs")
        require(hashlib.sha1(b"blob " + str(len(b)).encode() + b"\0" + b).hexdigest() == x["git_blob"], "Selected fixture blob differs")
    for x in recovered["byte_identical_alias_pairs"]:
        require((art / "fixtures-v1" / x["hooked"]).read_bytes() == (art / "fixtures-v1" / x["gate"]).read_bytes(), "Alias bytes differ")
    run("original-gate", [sys.executable, root / CP / "battle-residual157/validate.py"])
    require((data / "original-gate-v1.json").read_bytes() == source(DP + PACKET + "/original-gate-v1.json"), "Complete original gate differs")

    env = dict(os.environ, IC2_FIXTURES_DIR=str(art / "full-fixtures-v1"))
    corpus = {}
    for label, dll, expected in [("baseline", "corpus-baseline-v1/bin/Corpus.dll", 1), ("cached-only", "corpus-cached-only-v1/bin/Corpus.dll", 1), ("cached-live", "corpus-cached-live-v1/build/bin/Corpus/debug/Corpus.dll", 0)]:
        output, log = root / (label + ".json"), root / (label + ".jsonl")
        run("corpus-" + label, [dotnet, art / dll, log, output], expected, env)
        for actual, name in [(output, "corpus-" + label + "-v1.json"), (log, "corpus-" + label + "-v1.jsonl")]:
            require(actual.read_bytes() == (data / name).read_bytes(), "Complete corpus rows/summary differ")
        d = read(output)
        corpus[label] = dict(trials=d["trials"], state=d["statePass"], draws=d["drawPass"], failed=d["failed"], complete_record_sha256=sha(output.read_bytes()), failed_trials=[x["trial"] for x in d["rows"] if not x.get("stateEqual") or not x.get("drawsEqual")])
    fixed, regressions = {}, {}
    for label, dll, expected in [("baseline", "corpus-fixed-baseline-v1/bin/Corpus.dll", 1), ("cached-live", "corpus-fixed-cached-live-v1/build/bin/Corpus/debug/Corpus.dll", 0)]:
        out = root / ("fixed-" + label + ".json")
        run("fixed-" + label, [dotnet, art / dll, root / ("fixed-" + label + ".jsonl"), out, "--fixed-only"], expected, env)
        require(out.read_bytes() == (data / ("fixed-" + label + "-v1.json")).read_bytes(), "Fixed-series result differs")
        fixed[label] = {k:v for k,v in read(out).items() if k != "rows"}
    for label, expected in [("baseline", 1), ("cached-only", 1), ("cached-live", 0)]:
        out = root / ("regression-" + label + ".json")
        dll = art / ("movement-regression-" + label + "-v1/bin/MovementRegression/debug/MovementRegression.dll")
        run("regression-" + label, [dotnet, dll, a.remake, out], expected)
        require(read(out) == read(data / ("movement-regression-" + label + "-v1.json")), "Complete regression differs")
        regressions[label] = dict(passed=read(out)["passed"], failed=read(out)["failed"])
    walks = {}
    run_data = root / DP / PARITY / "seed2-residual-v1"
    for label, folder in [("before", "walk-before-build-v1"), ("cached-live", "walk-cached-live-build-v1")]:
        out = root / ("walk-" + label + ".json")
        run("walk-" + label, [dotnet, art / folder / "bin/WalkProbe/debug/WalkProbe.dll", run_data / "states.json", run_data / "semantic-actions-v1.jsonl", a.remake, out])
        require(out.read_bytes() == (data / ("walk-" + label + "-v1.json")).read_bytes(), "Complete conditional Walk trace differs")
        rows = read(out)["rows"]
        walks[label] = dict(calls=len(rows), different=sum(bool(x["differences"]) or not x["rngEqual"] for x in rows))
    original_state = next(x for x in read(run_data / "states.json")["records"] if x["seq"] == 890)
    disputed = next(x for x in read(root / "walk-before.json")["rows"] if x["beginSeq"] == 874)
    field_map = dict(X="x", Y="y", Origin="origin", Type="type", Troops="troops", Quality="quality", Morale="morale", Moves="moves", Shots="shots", Target="target", Name="name")
    claims = [original_state["actor_claim_targets"].count(i) for i in range(40)]
    matches = []
    for i, obs in enumerate(disputed["observations"]):
        if (obs["Counter"] == original_state["counter"] and obs["SideToMove"] == original_state["side"]
            and obs["RandSeed"] == original_state["seed_before"] and obs["Grid"] == original_state["grid"]
            and obs["GeneralClaims"] == claims and all(all(n[k] == o[v] for k,v in field_map.items()) for n,o in zip(obs["Slots"], original_state["slots"], strict=True))):
            matches.append(i)
    require(matches == [14], "Post-rout common-state proof differs")
    original_decode = root / "original-semantic-redecode"
    original_decode.mkdir()
    for n in ["hook.json", "states.json"]:
        (original_decode / n).write_bytes((run_data / n).read_bytes())
    run("raw-semantic", [sys.executable, root / CP / "battle-parity157/semantic_log.py", original_decode])
    for n in ["semantic-events-v1.jsonl", "semantic-actions-v1.jsonl", "semantic-summary-v1.json"]:
        require((original_decode / n).read_bytes() == (run_data / n).read_bytes(), "Raw original semantic re-decode differs")
    replay = root / "seed2-replay.json"
    run("seed2-replay", [dotnet, art / "replay-cached-live-v1/Replay.dll", run_data / "result.json", a.remake, replay])
    require(replay.read_bytes() == (data / "seed2-cached-live-replay-v1.json").read_bytes(), "Complete autonomous seed2 replay differs")
    semantic = root / "seed2-actions.json"
    run("seed2-actions", [sys.executable, root / CP / "battle-parity157/compare_semantic.py", "--original", run_data, "--native", replay, "--output", semantic])
    require(semantic.read_bytes() == (data / "seed2-cached-live-action-comparison-v1.json").read_bytes(), "Complete178-action comparison differs")
    seed1, seed2 = (pa / "semantic-observer-v1.exe").read_bytes(), (art / "semantic-seed2-v1.exe").read_bytes()
    differences = [(x,y) for x,y in zip(seed1,seed2,strict=True) if x != y]
    require(differences == [(1,2),(1,2)], "Seed2 observer changes more than seed immediates")
    run("prior-controls", [sys.executable, root / CP / "battle-residual157/verify_controls.py"])
    expected = source(DP + PACKET + "/control-replay-v1/verification-v1.json")
    actual = (data / "control-replay-v1/verification-v1.json").read_bytes()
    require(actual == expected, "Entire prior14-control record differs")
    test_dll = art / "corpus-fixed-cached-live-v1/build/bin/IC2.Engine.Tests/debug/IC2.Engine.Tests.dll"
    run("upstream-movement", [dotnet, "vstest", test_dll, "--TestCaseFilter:FullyQualifiedName~Battle.Tactical.MovementTests|FullyQualifiedName~Battle.Tactical.ExhaustedMovementTests", "--Logger:trx;LogFileName=movement.trx", "--ResultsDirectory:" + str(root / "movement-tests")], env=env)
    trx = ET.parse(root / "movement-tests/movement.trx")
    counts = trx.find(".//{http://microsoft.com/schemas/VisualStudio/TeamTest/2010}Counters").attrib
    require(counts["total"] == counts["passed"] == "27" and counts["executed"] == "27", "Movement suite count differs")
    receipt = dict(source_commit=PIN, checker_sha256=sha(Path(__file__).read_bytes()), corpus=corpus, fixed=fixed,
                   regressions=regressions, conditional_walks=walks, original_gate_exact=True,
                   selected_fixture_files_verified=len(recovered["files"]), byte_identical_alias_pairs=19,
                   archives=archive_checks, prior14_control_record_exact=True, prior14_record_sha256=sha(actual),
                   upstream_movement_tests=dict(total=27, passed=27, skipped=0),
                   original_instruction_guards_verified=True, t206_general_blobs_verified=4, comparator_source_files_verified=5,
                   post_rout_common_state_verified=True, original_raw_semantic_redecode_equal=True,
                   complete_seed2_replay_and178_action_comparison_equal=True, only_two_seed_immediates_changed=True,
                   limits=["Offline retained binaries and recorded fixtures; no fresh original/Wine or independent rebuild",
                           "Strict helper-defined block/post fields and ordered bounds/results, not every hidden runtime field",
                           "No registry/fixture/sibling production-source changes; no main CI/Godot/Windows claim",
                           "Private corpus, owner data/hashes and full control outputs excluded; work directory must stay private",
                           "Prior historical assumptions and three Selected defaults remain; no separate model review",
                           "Local archive verification only; no Drive download/readback"])
    with a.out.open("x") as f:
        json.dump(receipt, f, indent=2)
        f.write("\n")
    print("PASS: strict318 variants, fixed5, regression5, Walk49, prior14 and upstream27 checks; archives/source/golden gate verified")


if __name__ == "__main__":
    main()
