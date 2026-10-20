"""Actual root-crate QM consumer replay; no full-suite success is inferred.

AuthorityEffect: None. Frozen Cargo resolution and an owned build directory.
"""

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import subprocess

from replay import ROOT, RUST, digest, write, inventory, execute, remove_owned, dependency_sources


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test-filter", action="append")
    args = parser.parse_args()
    filters = args.test_filter or ["qm::tests::test_qubit_pure_state_and_pauli_expectation"]
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output = ROOT / "evidence/quality/l4a_six" / (stamp + "-qm-consumer")
    output.mkdir(parents=True)
    work = RUST / "target/l4a-six" / (stamp + "-qm-consumer")
    work.mkdir(parents=True)
    sources = inventory()
    write(output / "source_manifest.json", sources)
    shutil.copyfile(__file__, output / "consumer.py")
    shutil.copyfile(Path(__file__).with_name("replay.py"), output / "replay.py")
    receipt = {"AuthorityEffect": "None", "claim": "Actual root library compilation plus the explicitly selected consumer tests; not a full root or workspace test run.",
               "test_filters": filters, "runs": [],
               "versions": {n: subprocess.check_output([n, "--version"], text=True).strip() for n in ("cargo", "rustc")},
               "runner_sha256": digest(output / "consumer.py"), "helper_sha256": digest(output / "replay.py"),
               "source_manifest_sha256": digest(output / "source_manifest.json"),
               "cargo_lock_before": digest(RUST / "Cargo.lock")}
    print(output, flush=True)
    try:
        verbose_version = subprocess.check_output(["rustc", "-vV"], text=True)
        host = next(line.removeprefix("host: ") for line in verbose_version.splitlines() if line.startswith("host: "))
        receipt["host"] = host
        receipt["metadata_scope"] = "Host-target dependency resolution; no other-platform compilation is claimed."
        command = ["cargo", "metadata", "--frozen", "--quiet", "--format-version", "1", "--filter-platform", host]
        meta = subprocess.run(command, cwd=RUST, text=True, capture_output=True)
        (output / "cargo_metadata.json").write_text(meta.stdout, encoding="utf-8")
        (output / "cargo_metadata_stderr.log").write_text(meta.stderr, encoding="utf-8")
        receipt["metadata_capture"] = {"command": command, "cwd": str(RUST), "exit_code": meta.returncode,
            "sha256": digest(output / "cargo_metadata.json"), "stderr_sha256": digest(output / "cargo_metadata_stderr.log")}
        if meta.returncode != 0:
            return
        metadata = json.loads(meta.stdout)
        dependencies = dependency_sources(metadata)
        write(output / "dependency_sources.json", dependencies)
        receipt["dependency_sources_sha256"] = digest(output / "dependency_sources.json")
        if shutil.disk_usage(ROOT).free < 3 * 1024**3:
            receipt["run"] = {"started": False, "exit_code": None, "reason": "Less than 3 GiB free"}
            return
        for index, selected in enumerate(filters):
            run = execute(["cargo", "--config", "profile.dev.debug=0", "--config", "profile.test.debug=0",
                           "test", "--frozen", "--target-dir", str(work / "build"), "--quiet",
                           "-p", "theory_of_finite_qm", "--lib", selected],
                          RUST, output / f"consumer-{index}.log")
            receipt["runs"].append(run)
            receipt["run"] = run
            print(selected, run["exit_code"], flush=True)
            if run["exit_code"] != 0 or run["timed_out"]:
                break
        receipt["all_runs_passed"] = (len(receipt["runs"]) == len(filters)
            and all(run["exit_code"] == 0 and not run["timed_out"] for run in receipt["runs"]))
        receipt["dependency_sources_unchanged"] = dependencies == dependency_sources(metadata)
    finally:
        receipt["sources_unchanged"] = sources == inventory()
        receipt["cargo_lock_unchanged"] = receipt["cargo_lock_before"] == digest(RUST / "Cargo.lock")
        remove_owned(work / "build", work)
        receipt["owned_build_removed"] = True
        write(output / "receipt.json", receipt)
        print(json.dumps({name: receipt.get(name) for name in ("run", "sources_unchanged", "cargo_lock_unchanged")}), flush=True)


if __name__ == "__main__":
    main()
