#!/usr/bin/env python3
"""Reproduce bounded #174 fleet controls offline, never launch a game.

--conquest CHECKOUT --artifact-root DIR --work NEW_PRIVATE_DIR --out NEW.json.
No sibling/source/fixture writes. Diagnostic containers are not original Save As.
"""
import argparse
import hashlib
import json
import os
import subprocess
import tarfile
from pathlib import Path

PIN = "8d975efddd66fd81371991936a7fd0cbc58016be"
CODE, DATA = "runs/experiments/strategic-fleet", "runs/experiments/data/run-exp-strategic-fleet"
NAME = "run-exp-strategic-fleet"


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def read(p):
    return json.loads(p.read_text())


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    for n in ["conquest", "artifact-root", "work", "out"]:
        ap.add_argument("--" + n, type=Path, required=True)
    a = ap.parse_args()
    os.umask(0o077)
    require(not a.out.exists(), "Output exists")
    a.work.mkdir(mode=0o700, exist_ok=False)
    root = a.work.resolve()
    py, dotnet = "/home/diego/.local/bin/python3.12", "/home/diego/.dotnet/dotnet"

    def git(*args):
        return subprocess.check_output(["git", "-C", str(a.conquest), *args])

    def source(path):
        return git("show", f"{PIN}:{path}")

    def run(label, argv):
        p = subprocess.run(list(map(str, argv)), capture_output=True, text=True)
        (root / (label + "-execution.json")).write_text(json.dumps(dict(returncode=p.returncode, stdout=p.stdout, stderr=p.stderr)))
        require(p.returncode == 0, "Offline check failed; inspect work log: " + label)

    generated = {"case-manifest-v1.json", "original-fleet-controls-v1.json", "original-score-controls-v1.json", "summary-v1.json"}
    names = git("ls-tree", "-r", "--name-only", PIN, CODE, DATA).decode().splitlines()
    names += ["state/__init__.py", "state/sav.py"]
    for n in names:
        if n.startswith(DATA + "/") and Path(n).name in generated:
            continue
        p = root / n
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(source(n))
    art = root / "artifacts" / NAME
    art.mkdir(parents=True)
    original = a.artifact_root / NAME
    for p in original.iterdir():
        if p.is_file():
            (art / p.name).symlink_to(p.resolve())
    pilot = a.artifact_root / "run-exp-strategic-fidelity"
    (art.parent / "run-exp-strategic-fidelity").symlink_to(pilot.resolve(), target_is_directory=True)
    data, code = root / DATA, root / CODE
    require((art / "controls-v1").resolve().is_relative_to(root), "Output path escapes intake work")
    pin = json.loads(source("runs/experiments/data/run-exp-strategic-fidelity/source-pin-v1.json"))
    for item in pin["files"]:
        b = (pilot / "source-v1" / item["path"]).read_bytes()
        require(hashlib.sha1(b"blob " + str(len(b)).encode() + b"\0" + b).hexdigest() == item["git_blob"], "Pinned production source differs")
    run("original-controls", [py, code / "controls.py"])
    run("original-scores", [py, code / "score_audit.py"])
    for n in ["case-manifest-v1.json", "original-fleet-controls-v1.json", "original-score-controls-v1.json"]:
        require((data / n).read_bytes() == source(DATA + "/" + n), "Whole original record differs: " + n)
    run("recovered-native", [py, code / "verify_bundle.py", "--version", "research"])
    recovery = art / "recovery-research"
    recovered = read(data / "recovery-verification-research.json")
    require(recovered["member_hashes_verified"] == 76 and recovered["compiled_native_rows_byte_identical"] == 14, "Recovery count differs")
    m = read(data / "artifact-manifest-v1.json")
    with tarfile.open(art / m["archive"]) as tar:
        members = tar.getmembers()
        require(len(members) == len(m["members"]) and {x.name for x in members} == {x["name"] for x in m["members"]}, "Archive has unlisted members")
    native = root / "fresh-native-fleet-controls.json"
    run("fresh-native", [dotnet, recovery / "tools/FleetProbe.dll", art / "controls-v1", recovery, native])
    require(native.read_bytes() == source(DATA + "/native-fleet-controls-v1.json"), "All14 fresh native rows differ")
    require(sha((recovery / "tools/IC2.Engine.dll").read_bytes()) == pin["engine_sha256"], "Recovered engine differs from pilot pin")
    import struct
    base = (art / "controls-v1/peace/pre-move.SAV").read_bytes()
    count = struct.unpack_from("<h", base, 100956)[0]
    fleet0 = 100958 + count * 656 + 2
    byte_rows = []
    for label in ["stored-a", "stored-b"]:
        other = (art / "controls-v1" / label / "pre-move.SAV").read_bytes()
        diff = [i for i, (x,y) in enumerate(zip(base,other,strict=True)) if x != y]
        require(diff == list(range(fleet0 + 4, fleet0 + 8)), "Stored-route control changes other bytes")
        byte_rows.append(dict(case=label, only_changed_offsets=diff, fleet0_route_field_only=True))
    require(byte_rows == read(data / "stored-route-byte-control-v1.json"), "Whole stored-route byte proof differs")
    run("summary", [py, code / "audit.py"])
    raw = (data / "summary-v1.json").read_bytes()
    require(raw == source(DATA + "/summary-v1.json"), "Whole fleet summary differs")
    summary = json.loads(raw)
    state_rows = read(native)["rows"]
    state = {x["caseName"]: x for x in state_rows}
    require(state["peace"]["nativeStateSha256"] == state["stored-a"]["nativeStateSha256"] == state["stored-b"]["nativeStateSha256"], "Native state identity differs")
    receipt = dict(source_commit=PIN, checker_sha256=sha(Path(__file__).read_bytes()),
                   source_data_blobs_verified=len(pin["files"]), remake_pin=pin["remake_pin"],
                   original_phase_controls_exact=14, original_score_controls_exact=6,
                   fresh_native_rows_exact=14, fleet_relation_gate_checks=summary["fleet_and_relation_gate_checks"],
                   whole_summary_equal=True, summary_sha256=sha(raw), summary=summary,
                   stored_route_byte_proof=byte_rows, native_absent_a_b_states_and_proposals_equal=True,
                   archive=dict(name=m["archive"], bytes=m["bytes"], sha256=m["sha256"], members=76),
                   limits=["Synthetic original F608 phase/prepass/scorers, intercepted before movement; no original/Wine/game launch",
                           "Native proposals, not full greedy-loop accepted command traces or naval combat/RNG equivalence",
                           "Stored-route+zero-move combination, protected ports, providers, cargo and routing/contact remain untested",
                           "Retained compiled tool replay, not independent rebuild/model review; no production fix or Windows acceptance",
                           "Local recovery only, no remote Drive digest verification"])
    with a.out.open("x") as f:
        json.dump(receipt, f, indent=2)
        f.write("\n")
    print("PASS: 14 original/native controls, six real-RNG scorer controls, 3568 gates, four-byte route proof, 76archive members")


if __name__ == "__main__":
    main()
