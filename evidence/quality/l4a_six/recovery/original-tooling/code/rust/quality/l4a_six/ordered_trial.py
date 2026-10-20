"""Source-pinned trial of the ordered-algebra candidate. AuthorityEffect: None.

Copies current admitted modules and overlays only the separate candidate. Does
not modify live source or award a grade. Owned caches are removed on completion.
"""
from datetime import datetime, timezone
import argparse
from collections import Counter
from pathlib import Path
import json
import shutil
import subprocess
from replay import ROOT, RUST, inventory, digest, write, snapshot, execute, dependency_sources, remove_owned


def admit_build(work, receipt):
    """Keep a reserve after the first completed build instead of charging it twice.

    Cold compilation requires two GiB. Subsequent invocations reuse that same
    owned cache and require one GiB still free. This is an admission observation,
    not a reservation or a bound on compiler allocation.
    """
    warm = (work / "build/debug/deps").is_dir()
    minimum = (1 if warm else 2) * 1024**3
    free = shutil.disk_usage(ROOT).free
    receipt["build_admissions"].append({"cache_present": warm, "free_bytes": free,
        "required_free_bytes": minimum, "admitted": free >= minimum})
    return free >= minimum


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--faults", action="store_true")
    parser.add_argument("--metrics", action="store_true")
    args = parser.parse_args()
    candidate = Path(__file__).with_name("ordered_port") / "ordered.rs"
    origin_path = candidate.with_name("origin.json")
    origin = json.loads(origin_path.read_text(encoding="utf8"))
    assert digest(ROOT / origin["source"]) == origin["sha256"], "Candidate origin changed"
    entries = []
    if args.faults:
        from ordered_fault_recipes import recipes
        entries = recipes(candidate.read_bytes().decode("utf8"))
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-ordered-trial"
    out = ROOT / "evidence/quality/l4a_six" / stamp
    out.mkdir()
    work = RUST / "target/l4a-six" / stamp
    sources = inventory()
    write(out / "source_manifest.json", sources)
    shutil.copyfile(__file__, out / "trial.py")
    shutil.copyfile(Path(__file__).with_name("replay.py"), out / "replay.py")
    shutil.copyfile(candidate, out / "candidate.rs")
    shutil.copyfile(origin_path, out / "origin.json")
    if args.faults:
        for name in ("ordered_fault_recipes.py", "scalar_port_faults.py"):
            shutil.copyfile(Path(__file__).with_name(name), out / name)
    write(out / "mutations.json", entries)
    receipt = {"AuthorityEffect": "None", "scope": "Separate ordered candidate only; no integrated grade or whole-root package execution.",
        "source_manifest_sha256": digest(out / "source_manifest.json"), "candidate_sha256": digest(candidate),
        "runner_sha256": digest(out / "trial.py"), "helper_sha256": digest(out / "replay.py"),
        "versions": {name: subprocess.check_output([name, "--version"], text=True).strip() for name in ("rustc", "cargo")},
        "runs": [], "restored_runs": [], "faults_requested": args.faults,
        "metric_runs": [], "build_admissions": [],
        "warm_cache_minimum_free_bytes": 1024**3,
        "minimum_free_build_bytes": 2 * 1024**3}
    if args.faults:
        receipt["recipe_sources"] = {name: digest(out / name)
            for name in ("ordered_fault_recipes.py", "scalar_port_faults.py")}
    print(out, flush=True)
    dependencies = None
    try:
        snapshot(work)
        shutil.copyfile(candidate, work / "src/linear_algebra/ordered.rs")
        command = ["cargo", "metadata", "--offline", "--quiet", "--format-version", "1"]
        metadata = subprocess.run(command, cwd=work, capture_output=True, text=True)
        (out / "cargo_metadata.json").write_text(metadata.stdout, encoding="utf8")
        (out / "metadata_stderr.log").write_text(metadata.stderr, encoding="utf8")
        receipt["metadata"] = {"command": command, "cwd": str(work), "exit_code": metadata.returncode,
            "sha256": digest(out / "cargo_metadata.json"), "stderr_sha256": digest(out / "metadata_stderr.log")}
        if metadata.returncode != 0:
            return
        dependencies = dependency_sources(json.loads(metadata.stdout))
        write(out / "dependency_sources.json", dependencies)
        receipt["dependency_sources_sha256"] = digest(out / "dependency_sources.json")
        for name, selection in [("ordered", ["--lib", "linear_algebra::ordered"]), ("doctests", ["--doc"])]:
            if not admit_build(work, receipt):
                receipt["runs"].append({"started": False, "reason": "Build reserve unavailable; see build_admissions"})
                break
            run = execute(["cargo", "test", "--offline", "--quiet", "--target-dir", str(work / "build"),
                "-p", "tfqm_homology_linear_audit", *selection], work, out / (name + ".log"))
            receipt["runs"].append(run)
            print(name, run["exit_code"], flush=True)
            if run["exit_code"] != 0 or run["timed_out"]:
                break
        if args.faults and len(receipt["runs"]) == 2 and all(
                run.get("exit_code") == 0 and not run.get("timed_out") for run in receipt["runs"]):
            target = work / "src/linear_algebra/ordered.rs"
            original = target.read_bytes()
            source = original.decode("utf8")
            for entry in entries:
                if not admit_build(work, receipt):
                    entry["reason"] = "Build reserve unavailable; no execution inferred"
                    break
                try:
                    assert source.count(entry["before"]) == 1, entry["id"]
                    target.write_bytes(source.replace(entry["before"], entry["after"], 1).encode("utf8"))
                    entry["candidate_sha256"] = digest(target)
                    selection = ["--doc"] if entry["target"] == "doc" else ["--lib", "linear_algebra::ordered"]
                    run = execute(["cargo", "test", "--offline", "--quiet", "--target-dir", str(work / "build"),
                        "-p", "tfqm_homology_linear_audit", *selection], work, out / (entry["id"] + ".log"))
                    entry["run"] = run
                    log = (ROOT / run["log"]).read_text(encoding="utf8")
                    entry["outcome"] = ("inconclusive" if run["timed_out"] else "survived" if run["exit_code"] == 0
                        else "invalid" if "could not compile" in log or "error[E" in log
                        else "killed" if "test result: FAILED" in log else "inconclusive")
                    print(entry["id"], entry["outcome"], flush=True)
                finally:
                    target.write_bytes(original)
                    entry["source_restored"] = digest(target) == digest(candidate)
                    write(out / "mutations.json", entries)
            for name, selection in [("ordered", ["--lib", "linear_algebra::ordered"]), ("doctests", ["--doc"])]:
                if not admit_build(work, receipt):
                    receipt["restored_runs"].append({"started": False, "reason": "Build reserve unavailable; see build_admissions"})
                    break
                run = execute(["cargo", "test", "--offline", "--quiet", "--target-dir", str(work / "build"),
                    "-p", "tfqm_homology_linear_audit", *selection], work, out / (name + "-restored.log"))
                receipt["restored_runs"].append(run)
                print("restored", name, run["exit_code"], flush=True)
        if args.metrics:
            # All test invocations have finished. Release their cache before
            # compiling the separate calibrated metric executable.
            remove_owned(work / "build", work)
            tool = RUST / "quality/category_homology/rust_metrics"
            build = work / "metrics-build"
            common = ["--offline", "--manifest-path", str(tool / "Cargo.toml"),
                "--target-dir", str(build), "--quiet"]
            for action in ("test", "build"):
                if shutil.disk_usage(ROOT).free < receipt["minimum_free_build_bytes"]:
                    receipt["metric_runs"].append({"started": False, "exit_code": None,
                        "timed_out": False, "reason": "Two GiB headroom unavailable"})
                    break
                run = execute(["cargo", action, *common], tool, out / ("metric-" + action + ".log"))
                receipt["metric_runs"].append(run)
                if run["exit_code"] != 0 or run["timed_out"]:
                    break
            if len(receipt["metric_runs"]) == 2 and all(
                    run["exit_code"] == 0 and not run["timed_out"] for run in receipt["metric_runs"]):
                receipt["metric_runs"].append(execute([str(build / "debug/tfqm_rust_metrics.exe"),
                    str(work / "src/linear_algebra/ordered.rs")], ROOT, out / "metrics.json"))
                receipt["metric_tool_sources"] = {str(path.relative_to(ROOT)): digest(path)
                    for path in tool.rglob("*") if path.is_file()
                    and path.suffix in (".rs", ".toml", ".lock") and "target" not in path.relative_to(tool).parts}
    finally:
        receipt["live_sources_unchanged"] = sources == inventory()
        receipt["candidate_unchanged"] = digest(candidate) == receipt["candidate_sha256"]
        receipt["dependencies_unchanged"] = (dependencies is not None and all(
            Path(p).is_file() and digest(Path(p)) == h for p, h in dependencies.items()))
        counts = Counter(entry["outcome"] for entry in entries)
        for outcome in ("killed", "survived", "demonstrably_equivalent", "invalid", "inconclusive", "unrun"):
            counts.setdefault(outcome, 0)
        denominator = sum(counts[key] for key in ("killed", "survived", "inconclusive", "unrun"))
        receipt["accounting"] = {**counts, "conservative_ratio": counts["killed"] / denominator if denominator else None}
        write(out / "mutations.json", entries)
        receipt["mutations_sha256"] = digest(out / "mutations.json")
        remove_owned(work / "build", work)
        remove_owned(work / "metrics-build", work)
        receipt["owned_build_removed"] = True
        write(out / "receipt.json", receipt)


if __name__ == "__main__":
    main()
