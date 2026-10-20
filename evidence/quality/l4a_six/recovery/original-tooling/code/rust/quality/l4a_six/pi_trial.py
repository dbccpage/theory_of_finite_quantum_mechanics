"""Small standalone Cargo trial of the staged finite Pi model. AuthorityEffect: None."""
import json
import argparse
import tomllib
from pathlib import Path
import shutil
import subprocess
from datetime import datetime, timezone
from collections import Counter
from replay import ROOT, RUST, inventory, digest, write, execute, dependency_sources, remove_owned
from scalar_port_faults import block
from mutations import classify


from hott_model_faults import pi_recipes as recipes, unit_recipes


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--module", choices=("pi_type", "unit_type"), default="pi_type")
    parser.add_argument("--candidate-dir", type=Path)
    parser.add_argument("--min-free-mib", type=int, choices=(512, 1024), default=1024,
        help="Cold reserve for this small five-dependency HoTT package only; not a peak-space guarantee.")
    args = parser.parse_args()
    module = args.module
    manifest = tomllib.loads((RUST / "src/homotopy_type_theory/Cargo.toml").read_text(encoding="utf8"))
    assert set(manifest["dependencies"]) == {"serde", "serde_json", "thiserror", "sha2", "hex"}
    assert not manifest.get("build-dependencies"), "Reassess the small-package build envelope"
    stem = "pi" if module == "pi_type" else "unit"
    candidate = (args.candidate_dir.resolve() if args.candidate_dir
        else ROOT / ("evidence/quality/l4a_six/20261020-" + stem + "-candidate"))
    original_manifest = json.loads((candidate / "candidate.json").read_text(encoding="utf8"))
    assert digest(ROOT / original_manifest["source"]) == original_manifest["origin_sha256"]
    original = (candidate / (module + ".rs")).read_bytes()
    assert digest(candidate / (module + ".rs")) == original_manifest["candidate_sha256"]
    entries = (recipes if module == "pi_type" else unit_recipes)(original.decode("utf8"))
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + stem + "-trial"
    out = ROOT / "evidence/quality/l4a_six" / stamp
    out.mkdir()
    work = RUST / "target/l4a-six" / stamp
    work.mkdir(parents=True)
    sources = inventory()
    write(out / "source_manifest.json", sources)
    shutil.copyfile(__file__, out / "trial.py")
    shutil.copyfile(Path(__file__).with_name("replay.py"), out / "replay.py")
    shutil.copyfile(candidate / (module + ".rs"), out / "candidate.rs")
    shutil.copyfile(candidate / "candidate.json", out / "candidate_manifest.json")
    receipt = {"AuthorityEffect": "None", "scope": "Separate " + module + " candidate in the actual HoTT package source, with standalone workspace/profile declarations. Not installed-source or whole-root evidence.",
        "candidate_manifest_sha256": digest(out / "candidate_manifest.json"),
        "source_manifest_sha256": digest(out / "source_manifest.json"), "candidate_sha256": digest(out / "candidate.rs"),
        "runner_sha256": digest(out / "trial.py"), "helper_sha256": digest(out / "replay.py"),
        "versions": {name: subprocess.check_output([name, "--version"], text=True).strip() for name in ("rustc", "cargo")},
        "baselines": [], "restored_baselines": [], "admissions": []}
    receipt["cold_reserve_bytes"] = args.min_free_mib * 1024**2
    receipt["build_envelope"] = "Standalone five-dependency HoTT package, debug=0, two build jobs, no external path dependencies. Reserve is an admission observation, not a compiler allocation bound."
    print(out, flush=True)
    dependencies = None
    def run(name, mode):
        warm = (work / "target/debug/deps").is_dir()
        minimum = (256 * 1024**2) if warm else receipt["cold_reserve_bytes"]
        free = shutil.disk_usage(ROOT).free
        receipt["admissions"].append({"warm_cache": warm, "free_bytes": free, "required_free_bytes": minimum, "admitted": free >= minimum})
        if free < minimum:
            return dict(started=False, exit_code=None, timed_out=False, reason="Small-package disk reserve unavailable")
        selection = ["--lib", module] if mode == "unit" else ["--doc"] if mode == "doc" else []
        return execute(["cargo", "test", "--offline", "--quiet", *selection], work, out / (name + ".log"))
    try:
        for path in (RUST / "src/homotopy_type_theory").rglob("*"):
            if path.is_file() and (path.suffix == ".rs" or path.name == "Cargo.toml"):
                target = work / path.relative_to(RUST / "src/homotopy_type_theory")
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(path, target)
        with (work / "Cargo.toml").open("a", encoding="utf8") as stream:
            stream.write("\n[workspace]\n[profile.dev]\ndebug=0\n[profile.test]\ndebug=0\n")
        (work / (module + ".rs")).write_bytes(original)
        meta = subprocess.run(["cargo", "metadata", "--offline", "--quiet", "--format-version", "1"], cwd=work, capture_output=True, text=True)
        (out / "cargo_metadata.json").write_text(meta.stdout, encoding="utf8")
        (out / "metadata_stderr.log").write_text(meta.stderr, encoding="utf8")
        receipt["metadata"] = {"command": meta.args, "cwd": str(work), "exit_code": meta.returncode,
            "sha256": digest(out / "cargo_metadata.json"), "stderr_sha256": digest(out / "metadata_stderr.log")}
        if meta.returncode != 0:
            return
        dependencies = dependency_sources(json.loads(meta.stdout))
        write(out / "dependency_sources.json", dependencies)
        receipt["dependency_sources_sha256"] = digest(out / "dependency_sources.json")
        baseline = run("baseline", "all")
        receipt["baselines"].append(baseline)
        print("baseline", baseline["exit_code"], flush=True)
        if baseline["exit_code"] != 0:
            return
        path = work / (module + ".rs")
        for entry in entries:
            try:
                path.write_bytes(original.decode("utf8").replace(entry["before"], entry["after"], 1).encode("utf8"))
                entry["candidate_sha256"] = digest(path)
                entry["run"] = run(entry["id"], entry["mode"])
                if entry["run"].get("started") is False:
                    entry["reason"] = entry["run"]["reason"]
                    break
                entry["outcome"], entry["reason"] = classify(entry["run"], out)
                print(entry["id"], entry["outcome"], flush=True)
            finally:
                path.write_bytes(original)
                entry["source_restored"] = digest(path) == receipt["candidate_sha256"]
                write(out / "mutations.json", entries)
        receipt["restored_baselines"].append(run("restored", "all"))
    finally:
        receipt["live_sources_unchanged"] = sources == inventory()
        receipt["candidate_unchanged"] = digest(candidate / (module + ".rs")) == receipt["candidate_sha256"]
        receipt["dependencies_unchanged"] = dependencies is not None and all(Path(name).is_file() and digest(Path(name)) == pin for name, pin in dependencies.items())
        counts = Counter(entry["outcome"] for entry in entries)
        for outcome in ("killed", "survived", "demonstrably_equivalent", "invalid", "inconclusive", "unrun"):
            counts.setdefault(outcome, 0)
        denominator = sum(counts[name] for name in ("killed", "survived", "inconclusive", "unrun"))
        receipt["accounting"] = {**counts, "conservative_ratio": counts["killed"] / denominator if denominator else None}
        write(out / "mutations.json", entries)
        receipt["mutations_sha256"] = digest(out / "mutations.json")
        if (work / "Cargo.lock").is_file():
            shutil.copyfile(work / "Cargo.lock", out / "Cargo.lock")
        receipt["owned_cache_file_bytes_before_cleanup"] = sum(path.stat().st_size for path in (work / "target").rglob("*") if path.is_file())
        remove_owned(work / "target", work)
        receipt["owned_build_removed"] = True
        write(out / "receipt.json", receipt)


if __name__ == "__main__":
    main()
