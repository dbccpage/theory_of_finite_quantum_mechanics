"""Independent snapshot trial of the next holonomy matrix admission candidate.

AuthorityEffect: None. Staged results do not certify the installed source.
"""
import argparse
from collections import Counter
from datetime import datetime, timezone
import json
from pathlib import Path as _FilesystemPath
import sys as _contract_sys
_contract_sys.path.insert(0, str(_FilesystemPath(__file__).resolve().parents[4] / "scripts"))
from contract_scores import RecordPath as Path, copy_file as _copy_record_file
import shutil
import subprocess
from replay import ROOT, RUST, inventory, digest, write, snapshot, execute, dependency_sources, remove_owned
from mutations import candidates, matching_literals, classify


def read(path):
    return json.loads(path.read_text(encoding="utf8"))


def recipes():
    result = []
    for entry in candidates():
        if entry["source"] != "code/rust/src/holonomy/matrix.rs":
            continue
        entry = {**entry, "target": "doc" if entry["id"].split("-", 1)[0] in ("MX14", "MX15", "MX16") else "integration"}
        if "self.numer() != reduced.numer()" in entry["before"]:
            entry["before"] = "if !self.numer().gcd(self.denom()).is_one() {"
        result.append(entry)
    result.extend([
        {"id": "HM01-conjugate-sign", "before": "im: -value.value.im.clone(),", "after": "im: value.value.im.clone(),", "target": "integration", "outcome": "unrun"},
        {"id": "HM02-trace-sum", "before": "tr = add_ref(&tr, self.at(i, i));", "after": "tr = sub_ref(&tr, self.at(i, i));", "target": "integration", "outcome": "unrun"},
    ])
    assert len({entry["id"] for entry in result}) == len(result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", type=Path, required=True)
    args = parser.parse_args()
    candidate = args.candidate.resolve()
    origin = read(candidate / "candidate.json")
    assert all(digest(ROOT / name) == pin for name, pin in origin["origins"].items())
    assert all(digest(candidate / "candidate" / name) == pin for name, pin in origin["candidates"].items())
    entries = recipes()
    matrix = candidate / "candidate/matrix.rs"
    text = matrix.read_bytes().decode("utf8")
    assert all(matching_literals(text, entry["before"], entry["after"]) is not None for entry in entries)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-holonomy-matrix-trial"
    out = ROOT / "evidence/quality/l4a_six" / stamp
    out.mkdir()
    work = RUST / "target/l4a-six" / stamp
    sources = inventory()
    write(out / "source_manifest.json", sources)
    _copy_record_file(__file__, out / "trial.py")
    _copy_record_file(Path(__file__).with_name("replay.py"), out / "replay.py")
    _copy_record_file(Path(__file__).with_name("mutations.py"), out / "mutations.py")
    write(out / "mutations.json", entries)
    receipt = {"AuthorityEffect": "None", "scope": "Separate staged holonomy admission candidate, not installed-source integration or grade evidence.",
        "candidate_manifest": str((candidate / "candidate.json").relative_to(ROOT)),
        "candidate_manifest_sha256": digest(candidate / "candidate.json"),
        "source_manifest_sha256": digest(out / "source_manifest.json"),
        "runner_sha256": digest(out / "trial.py"), "helper_sha256": digest(out / "replay.py"),
        "classification_source_sha256": digest(out / "mutations.py"),
        "versions": {name: subprocess.check_output([name, "--version"], text=True).strip() for name in ("rustc", "cargo")},
        "baselines": [], "restored_baselines": [], "metric_runs": [], "build_admissions": []}
    print(out, flush=True)
    dependencies = None
    def run(log, target):
        warm = (work / "build/debug/deps").is_dir()
        free = shutil.disk_usage(ROOT).free
        minimum = (1 if warm else 2) * 1024**3
        receipt["build_admissions"].append({"cache_present": warm, "free_bytes": free, "required_free_bytes": minimum, "admitted": free >= minimum})
        if free < minimum:
            return {"started": False, "exit_code": None, "timed_out": False, "reason": "Cold/warm reserve unavailable"}
        selection = ["--doc"] if target == "doc" else ["--test", "matrix_contracts"] if target == "integration" else []
        return execute(["cargo", "test", "--offline", "--quiet", "--target-dir", str(work / "build"), "-p", "tfqm_holonomy", *selection], work, out / log)
    try:
        snapshot(work)
        for name in origin["candidates"]:
            _copy_record_file(candidate / "candidate" / name, work / "src/holonomy" / name)
        command = ["cargo", "metadata", "--offline", "--quiet", "--format-version", "1"]
        meta = subprocess.run(command, cwd=work, capture_output=True, text=True)
        (out / "cargo_metadata.json").write_text(meta.stdout, encoding="utf8")
        (out / "metadata_stderr.log").write_text(meta.stderr, encoding="utf8")
        receipt["metadata"] = {"command": command, "cwd": str(work), "exit_code": meta.returncode, "sha256": digest(out / "cargo_metadata.json"), "stderr_sha256": digest(out / "metadata_stderr.log")}
        if meta.returncode != 0:
            return
        dependencies = dependency_sources(json.loads(meta.stdout))
        write(out / "dependency_sources.json", dependencies)
        receipt["dependency_sources_sha256"] = digest(out / "dependency_sources.json")
        baseline = run("baseline.log", "all")
        receipt["baselines"].append(baseline)
        print("baseline", baseline["exit_code"], flush=True)
        if baseline["exit_code"] != 0:
            return
        path = work / "src/holonomy/matrix.rs"
        original = path.read_bytes()
        for entry in entries:
            try:
                before, after = matching_literals(original.decode("utf8"), entry["before"], entry["after"])
                path.write_bytes(original.decode("utf8").replace(before, after, 1).encode("utf8"))
                entry["candidate_sha256"] = digest(path)
                execution = run(entry["id"] + ".log", entry["target"])
                entry["run"] = execution
                if execution.get("started") is False:
                    entry["reason"] = execution["reason"]
                    break
                entry["outcome"], entry["reason"] = classify(execution, out)
                print(entry["id"], entry["outcome"], flush=True)
            finally:
                path.write_bytes(original)
                entry["source_restored"] = digest(path) == digest(matrix)
                write(out / "mutations.json", entries)
        restored = run("restored.log", "all")
        receipt["restored_baselines"].append(restored)
        print("restored", restored["exit_code"], flush=True)
    finally:
        receipt["live_sources_unchanged"] = sources == inventory()
        receipt["candidates_unchanged"] = all(digest(candidate / "candidate" / name) == pin for name, pin in origin["candidates"].items())
        receipt["dependencies_unchanged"] = dependencies is not None and all(Path(name).is_file() and digest(Path(name)) == pin for name, pin in dependencies.items())
        counts = Counter(entry["outcome"] for entry in entries)
        for name in ("killed", "survived", "demonstrably_equivalent", "invalid", "inconclusive", "unrun"):
            counts.setdefault(name, 0)
        denominator = sum(counts[name] for name in ("killed", "survived", "inconclusive", "unrun"))
        receipt["accounting"] = {**counts, "conservative_ratio": counts["killed"] / denominator if denominator else None}
        write(out / "mutations.json", entries)
        receipt["mutations_sha256"] = digest(out / "mutations.json")
        remove_owned(work / "build", work)
        receipt["owned_build_removed"] = True
        write(out / "receipt.json", receipt)


if __name__ == "__main__":
    main()
