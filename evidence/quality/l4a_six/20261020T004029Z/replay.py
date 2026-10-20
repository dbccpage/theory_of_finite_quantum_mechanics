"""Source-pinned, offline six-directory baseline. No automatic grade awards.

AuthorityEffect: None. Python 3.11+. Build outputs belong to this replay only.
"""

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
import tomllib

ROOT = Path(__file__).resolve().parents[4]
RUST = ROOT / "code/rust"
GROUPS = ("holonomy", "homology", "homotopy_type_theory", "lie_theory",
          "linear_algebra", "local_green_global_red_lggr")
PACKAGES = ("tfqm_holonomy", "tfqm_homotopy_type_theory", "tfqm_lie_theory",
            "tfqm_local_green_global_red_lggr", "tfqm_homology_linear_audit")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def subjects():
    return sorted(p for group in GROUPS for p in (RUST / "src" / group).rglob("*")
                  if p.is_file() and (p.suffix == ".rs" or p.name == "Cargo.toml"))


def inventory():
    return {p.relative_to(ROOT).as_posix(): digest(p)
            for p in [ROOT / "SCORING.md", RUST / "Cargo.toml", *subjects()]}


def execute(command, cwd, log, timeout=900):
    started = time.monotonic()
    overlay = {"CARGO_INCREMENTAL": "0", "CARGO_BUILD_JOBS": "2"}
    with log.open("w", encoding="utf-8") as stream:
        process = subprocess.Popen(command, cwd=cwd, stdout=stream, stderr=subprocess.STDOUT,
                                   env={**os.environ, **overlay})
        try:
            code, timed_out = process.wait(timeout=timeout), False
        except subprocess.TimeoutExpired:
            subprocess.run(["taskkill", "/PID", str(process.pid), "/T", "/F"], capture_output=True)
            process.wait()
            code, timed_out = None, True
    return {"command": command, "cwd": str(cwd), "exit_code": code, "timed_out": timed_out,
            "elapsed_seconds": round(time.monotonic() - started, 3), "environment": overlay,
            "log": log.relative_to(ROOT).as_posix(), "log_sha256": digest(log)}


def snapshot(work):
    work.mkdir(parents=True)
    for subject in subjects():
        target = work / subject.relative_to(RUST)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(subject, target)
    dependencies = tomllib.loads((RUST / "Cargo.toml").read_text())["dependencies"]
    selected = ("num-rational", "num-bigint", "num-traits", "num-integer", "serde",
                "serde_json", "thiserror", "blake3", "hex", "nalgebra", "linear_algebra", "omega_homology")
    lines = ["[workspace]", 'members = [".", "src/holonomy", "src/homotopy_type_theory", '
             '"src/lie_theory", "src/local_green_global_red_lggr"]', 'resolver = "2"',
             "[package]", 'name = "tfqm_homology_linear_audit"', 'version = "0.0.0"',
             'edition = "2021"', '[lib]', 'name = "theory_of_finite_qm"', "[dependencies]"]
    for name in selected:
        value = dependencies[name]
        encoded = json.dumps(value) if isinstance(value, str) else "{ " + ", ".join(
            f"{k} = {json.dumps(v)}" for k, v in value.items()) + " }"
        lines.append(f"{name} = {encoded}")
    lines += ["[profile.dev]", "debug = 0", "[profile.test]", "debug = 0",
              "[profile.release]", "debug = 0", "overflow-checks = true"]
    (work / "Cargo.toml").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (work / "src/lib.rs").write_text("pub mod linear_algebra;\npub mod homology;\n", encoding="utf-8")


def dependency_sources(metadata):
    """Bind Rust/manifest/build-script inputs, not authorship or exact compiler reads."""
    paths = set()
    for package in metadata["packages"]:
        base = Path(package["manifest_path"]).parent
        for folder, dirs, names in os.walk(base):
            dirs[:] = [d for d in dirs if d not in (".git", "target", "__pycache__")]
            paths.update(Path(folder) / n for n in names
                         if Path(n).suffix in (".rs", ".toml", ".lock"))
    return {str(p.resolve()): digest(p) for p in sorted(paths)}


def remove_owned(path, parent):
    if path.resolve().parent != parent.resolve():
        raise RuntimeError("Refusing cleanup outside the replay's owned parent")
    if path.exists():
        shutil.rmtree(path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--package", choices=PACKAGES, action="append")
    parser.add_argument("--test-filter")
    parser.add_argument("--release", action="store_true")
    parser.add_argument("--metrics", action="store_true")
    parser.add_argument("--doctests", action="store_true")
    args = parser.parse_args()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output = ROOT / "evidence/quality/l4a_six" / stamp
    output.mkdir(parents=True)
    work = RUST / "target/l4a-six" / stamp
    sources = inventory()
    write(output / "source_manifest.json", sources)
    shutil.copyfile(__file__, output / "replay.py")
    versions = {name: subprocess.check_output([name, "--version"], text=True).strip()
                for name in ("cargo", "rustc")}
    receipt = {"AuthorityEffect": "None", "versions": versions, "python": sys.version,
               "source_manifest_sha256": digest(output / "source_manifest.json"),
               "runner_sha256": digest(output / "replay.py"), "runs": [],
               "build_cache_disposals": [],
               "scope": "Scoped source snapshot; external dependencies remain explicit. No full workspace or L4A certification."}
    print(output, flush=True)
    try:
        snapshot(work)
        metadata_run = execute(["cargo", "metadata", "--offline", "--format-version", "1"],
                               work, output / "metadata.log")
        receipt["runs"].append(metadata_run)
        if metadata_run["exit_code"] != 0:
            return
        # Cargo metadata emits JSON to stdout and progress to stderr; obtain separated streams.
        meta_command = ["cargo", "metadata", "--offline", "--quiet", "--format-version", "1"]
        meta = subprocess.run(meta_command, cwd=work, capture_output=True, text=True, check=True)
        (output / "cargo_metadata.json").write_text(meta.stdout, encoding="utf-8")
        receipt["metadata_capture"] = {"command": meta_command, "cwd": str(work),
                                       "exit_code": meta.returncode,
                                       "sha256": digest(output / "cargo_metadata.json")}
        dependencies = dependency_sources(json.loads(meta.stdout))
        write(output / "dependency_sources.json", dependencies)
        receipt["dependency_sources_sha256"] = digest(output / "dependency_sources.json")
        receipt["dependency_scope"] = "Resolved package .rs/.toml/.lock files; excludes non-Rust included assets and compiler expansion."
        common = ["--offline", "--target-dir", str(work / "build"), "--quiet"]
        for package in args.package or PACKAGES:
            if shutil.disk_usage(ROOT).free < 3 * 1024**3:
                remove_owned(work / "build", work)
                receipt["build_cache_disposals"].append({"before_package": package,
                    "reason": "Completed Cargo cache removed to recover 3 GiB headroom."})
            if shutil.disk_usage(ROOT).free < 3 * 1024**3:
                receipt["runs"].append({"package": package, "started": False, "reason": "Less than 3 GiB free"})
                break
            command = ["cargo", "test", *common, "-p", package, "--tests"]
            if args.release:
                command.append("--release")
            if args.test_filter:
                command.append(args.test_filter)
            result = execute(command, work, output / (package + ".log"))
            receipt["runs"].append(result)
            print(package, result["exit_code"], result["elapsed_seconds"], flush=True)
            if args.doctests and result["exit_code"] == 0:
                doc_command = ["cargo", "test", *common, "-p", package, "--doc"]
                doc_run = execute(doc_command, work, output / (package + "-doctests.log"))
                receipt["runs"].append(doc_run)
                print(package, "doctests", doc_run["exit_code"], flush=True)
        if args.metrics:
            tool = RUST / "quality/category_homology/rust_metrics"
            metric_build = work / "metrics-build"
            common_metrics = ["--offline", "--manifest-path", str(tool / "Cargo.toml"),
                              "--target-dir", str(metric_build), "--quiet"]
            calibration = execute(["cargo", "test", *common_metrics], tool, output / "metric_calibration.log")
            receipt["runs"].append(calibration)
            built = execute(["cargo", "build", *common_metrics], tool, output / "metric_build.log")
            receipt["runs"].append(built)
            if calibration["exit_code"] == built["exit_code"] == 0:
                paths = [p.relative_to(ROOT).as_posix() for p in subjects() if p.suffix == ".rs"]
                receipt["runs"].append(execute([str(metric_build / "debug/tfqm_rust_metrics.exe"), *paths],
                                               ROOT, output / "metrics.json"))
                receipt["metric_tool_sources"] = {
                    p.relative_to(ROOT).as_posix(): digest(p) for p in sorted(tool.rglob("*")) if p.is_file()}
        receipt["dependency_sources_unchanged"] = all(Path(p).is_file() and digest(Path(p)) == h
                                                      for p, h in dependencies.items())
        if (work / "Cargo.lock").is_file():
            shutil.copyfile(work / "Cargo.lock", output / "Cargo.lock")
        shutil.copyfile(work / "Cargo.toml", output / "snapshot.Cargo.toml")
    finally:
        receipt["sources_unchanged"] = sources == inventory()
        receipt["snapshot_sources"] = {str(p.relative_to(work)): digest(p) for p in work.rglob("*.rs")
                                       if "build" not in p.relative_to(work).parts and "metrics-build" not in p.relative_to(work).parts}
        remove_owned(work / "build", work)
        remove_owned(work / "metrics-build", work)
        receipt["owned_builds_removed"] = True
        write(output / "receipt.json", receipt)


if __name__ == "__main__":
    main()
