#!/usr/bin/env python3
"""Offline intake of conquest #157; no Wine/original-game runs or sibling writes.

Requires retained public and private artifacts and .NET/Unicorn. Use --conquest,
--remake, --artifact-root (conquest artifacts/), --work NEW_PRIVATE_DIR, --out NEW.json.
The work directory retains private replay output; never commit or publish it.
"""
import argparse
import csv
import hashlib
import json
import os
import subprocess
import sys
import tarfile
from pathlib import Path

PIN = "b7f11a3ff9b2f93e111c5ea13b6b66e919cc6688"
DATA = "runs/experiments/data/"
CODE = "runs/experiments/"
PARITY, FIX = "run-exp-battle-parity157", "run-exp-faithful-general157"


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def read(p):
    return json.loads(p.read_text())


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    for name in ["conquest", "remake", "artifact-root", "work", "out"]:
        ap.add_argument("--" + name, type=Path, required=True)
    ap.add_argument("--dotnet", type=Path, default=Path("/home/diego/.dotnet/dotnet"))
    a = ap.parse_args()
    os.umask(0o077)
    require(not a.out.exists(), "Output exists")
    a.work.mkdir(mode=0o700, exist_ok=False)
    root = a.work.resolve()

    def git(*args):
        return subprocess.check_output(["git", "-C", str(a.conquest), *args])

    def source(name):
        return git("show", f"{PIN}:{name}")

    def run(argv, expected=0, cwd=None):
        p = subprocess.run(list(map(str, argv)), cwd=cwd, capture_output=True, text=True)
        # Logs may contain owner state or private paths: retain them privately only.
        log = root / f"command-{run.count:03d}.json"
        log.write_text(json.dumps(dict(returncode=p.returncode, stdout=p.stdout, stderr=p.stderr)))
        run.count += 1
        require(p.returncode == expected, "Offline check failed; inspect private work log")
    run.count = 0

    expected_verification = source(DATA + FIX + "/verification-v1.json")
    expected_cpu = source(DATA + PARITY + "/semantic-cpu-v1.json")
    names = []
    for prefix in [DATA + PARITY, DATA + FIX, CODE + "battle-parity157", CODE + "faithful-general157"]:
        names += git("ls-tree", "-r", "--name-only", PIN, prefix).decode().splitlines()
    names += ["state/__init__.py", "state/battle_block.py", "state/sav.py", "state/hook_log.py", "patches/battle_hook.py",
              "tests/test_battle_hook_caves.py", CODE + "tactical25-trace/observer.py"]
    for name in names:
        if name.startswith(DATA + FIX + "/"):
            rel = Path(name).relative_to(DATA + FIX)
            if len(rel.parts) > 1 or rel.name == "verification-v1.json" or rel.name.endswith("-audit-v1.json"):
                continue  # verifier writes fresh outputs; originals stay in Git objects
        if name in [DATA + PARITY + "/semantic-cpu-v1.json", DATA + PARITY + "/semantic-parser-controls-v1.json"]:
            continue
        p = root / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(source(name))
    # Isolate the source tree's implicit tests namespace from installed packages.
    (root / "tests/__init__.py").write_text("")
    fd, pd = root / DATA / FIX, root / DATA / PARITY
    fa, pa = a.artifact_root / FIX, a.artifact_root / PARITY
    local_art = root / "artifacts"
    (local_art / PARITY).mkdir(parents=True)
    for name in ["public", "private", "reference-v1"]:
        (local_art / PARITY / name).symlink_to((pa / name).resolve(), target_is_directory=True)
    (local_art / FIX).mkdir()
    (local_art / FIX / "replay-build-v2").symlink_to((fa / "replay-build-v2").resolve(), target_is_directory=True)

    # Apply only to a disposable four-file tree, with mixed source encodings preserved.
    patch_tree = root / "patch-tree"
    pins = read(fd / "source-pin-v2.json")
    for item in pins["files"]:
        raw = (a.remake / item["path"]).read_bytes()
        require(sha(raw) == item["original_sha256"], "Local tactical source differs from pinned base")
        require(hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest() == item["original_git_blob"], "Source blob differs")
        p = patch_tree / item["path"]
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(raw)
    patch = fd / "faithful-general-portable.patch"
    run(["git", "apply", "--check", patch], cwd=patch_tree)
    run(["git", "apply", patch], cwd=patch_tree)
    for item in pins["files"]:
        raw = (patch_tree / item["path"]).read_bytes()
        require(sha(raw) == item["patched_sha256"], "Applied patch differs from source pin")
        require(raw == (fa / "source-v2" / Path(item["path"]).name).read_bytes(), "Compile overlay differs")

    binary_rows = read(fd / "candidate-binaries-v1.json")["files"]
    for item in binary_rows:
        p = fa / item["file"]
        require(p.stat().st_size == item["bytes"] and sha(p.read_bytes()) == item["sha256"], "Candidate binary differs")
    archives = []
    for name in ["reference-batch01-manifest.json", "pilot-semantic-batch02-manifest.json"]:
        m = read(pd / name)
        archive = pa / m["archive"]
        require(sha(archive.read_bytes()) == m["sha256"] and archive.stat().st_size == m["bytes"], "Public archive differs")
        with tarfile.open(archive) as tar:
            members = tar.getmembers()
            expected = {r["name"]: r for r in m["members"]}
            require(len(members) == len(expected) and {x.name for x in members} == set(expected), "Archive inventory differs")
            for x in members:
                require(x.isfile(), "Unexpected archive member")
                require(x.size == expected[x.name]["bytes"] and sha(tar.extractfile(x).read()) == expected[x.name]["sha256"], "Archive member differs")
        archives.append(dict(name=m["archive"], sha256=m["sha256"], members=len(members)))
    m = read(fd / "candidate-archive-v1.json")
    require(sha((fa / m["archive"]).read_bytes()) == m["sha256"], "Candidate archive differs")
    with tarfile.open(fa / m["archive"]) as tar:
        members = tar.getmembers()
        require(len(members) == len(m["members"]) and {x.name for x in members} == set(m["members"]), "Candidate archive inventory")
        for x in members:
            require(x.isfile(), "Unexpected candidate member")
            allowed = {r["sha256"] for r in binary_rows if Path(r["file"]).name == Path(x.name).name}
            require(sha(tar.extractfile(x).read()) in allowed, "Candidate archive member differs")
    archives.append(dict(name=m["archive"], sha256=m["sha256"], members=len(members)))

    regression = {}
    for label, version, rc in [("before", "regression-before-v1", 1), ("after", "regression-after-v1", 0)]:
        out = root / ("regression-" + label + ".json")
        run([a.dotnet, fa / version / "bin/Regression/debug/Regression.dll", a.remake, out], expected=rc)
        actual = read(out)
        require(actual == read(fd / ("regression-" + label + "-v1.json")), "Full regression result differs")
        regression[label] = actual

    # Unchanged verifier: invokes retained actual compiled ComputerGeneral for 14+1 controls.
    run([sys.executable, root / CODE / "faithful-general157/verify.py"])
    raw = (fd / "verification-v1.json").read_bytes()
    require(raw == expected_verification, "Complete 14-control verification differs")
    verification = json.loads(raw)
    run([sys.executable, root / CODE / "battle-parity157/audit_owner.py"])
    require((pd / "owner-iteration-audit-v4.json").read_bytes() == source(DATA + PARITY + "/owner-iteration-audit-v3.json"), "Complete owner diagnostic audit differs")
    run([sys.executable, root / CODE / "battle-parity157/audit_pilot.py"])
    require((pd / "pilot-audit-v3.json").read_bytes() == source(DATA + PARITY + "/pilot-audit-v2.json"), "Complete pilot audit differs")
    ref = pd / "reference-semantic-v1"
    fields = ["site", "eax", "seed_before", "seed_after", "result", "counter", "side", "flag"]
    with (pa / "reference-v1/battles/hook/hooklog-mix-rg_s1_r5_hook.csv").open() as f:
        old = [tuple(int(r[k], 0) for k in fields) for r in csv.DictReader(f) if r["kind"] == "random"]
    hook = read(ref / "hook-after-writeback.json")
    fresh = [tuple(r[k] for k in fields) for r in hook["records"] if r["kind"] == "random"]
    require(len(old) == 325 and old == fresh, "Fresh reference golden draw gate differs")
    for i in range(1, 16):
        golden = pa / "reference-v1/battles/hook" / f"mix-rg_s1_r5_hook_BATTLE{i:02d}.SAV"
        observed = pa / "public/reference-semantic-v1/runtime/prefix/drive_c/IC2" / f"BATTLE{i:02d}.SAV"
        require(golden.read_bytes() == observed.read_bytes(), "Fresh reference whole-SAV gate differs")
    semantic_summaries = {}
    for label, src in [("reference", ref), ("owner", pa / "private/owner-seed1-semantic-v1")]:
        dest = root / "raw-semantic-redecode" / label
        dest.mkdir(parents=True)
        for n in ["hook.json", "states.json"]:
            (dest / n).write_bytes((src / n).read_bytes())
        run([sys.executable, root / CODE / "battle-parity157/semantic_log.py", dest])
        for n in ["semantic-events-v1.jsonl", "semantic-actions-v1.jsonl", "semantic-summary-v1.json"]:
            require((dest / n).read_bytes() == (src / n).read_bytes(), "Original raw semantic re-decode differs")
        semantic_summaries[label] = read(dest / "semantic-summary-v1.json")
    run([sys.executable, root / CODE / "battle-parity157/test_semantic.py"])
    require((pd / "semantic-cpu-v1.json").read_bytes() == expected_cpu, "Complete CPU test result differs")
    run([sys.executable, root / CODE / "battle-parity157/test_semantic_parser.py"])
    parser = read(pd / "semantic-parser-controls-v1.json")
    require(parser["all_passed"] and len(parser["cases"]) == 6, "Parser corruption controls failed")
    receipt = dict(source_commit=PIN, checker_sha256=sha(Path(__file__).read_bytes()),
                   source_patch_files_verified=4, candidate_binary_files_verified=len(binary_rows),
                   archives=archives, regression=regression,
                   complete_verification_equal=True, verification_sha256=sha(raw), verification=verification,
                   draw_tuples=sum(x["original_draws"] for x in verification["cases"]),
                   available_boundaries=sum(len(x["boundaries"]) for x in verification["cases"]),
                   default_selected_controls=[x["label"] for x in verification["cases"] if not x["selected_provided"]],
                   complete_owner_diagnostic_audit_equal=True, complete_pilot_audit_equal=True, complete_cpu_controls_equal=True,
                   original_raw_semantic_redecode_equal=True, original_semantic_summaries=semantic_summaries,
                   reference_golden_draws_equal=325, reference_golden_whole_saves_equal=15,
                   parser_cases=[dict(case=x["case"], passed=x["passed"], expected_success=x["expected_success"]) for x in parser["cases"]],
                   limits=["Retained compiled engine/tools rerun offline; no new original/Wine/native Windows run or independent rebuild",
                           "Matched original entries, not independent strategic copy-in/writeback or full318 corpus",
                           "State comparisons cover observed slots/grid/counter and terminal RNG, not every hidden runtime field",
                           "Historical control retains assumptions; three pilots default an unobserved Selected to -1",
                           "Private owner outputs and command logs remain in private work directory, never emitted here",
                           "No production fix/optional general implemented or merged by research"])
    with a.out.open("x") as f:
        json.dump(receipt, f, indent=2)
        f.write("\n")
    print("PASS: source/binary/archive checks; before/after6 tests; 14 recorded replays/2331draws/253boundaries; CPU and parser controls")


if __name__ == "__main__":
    main()
