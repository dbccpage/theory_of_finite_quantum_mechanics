"""Run actual-package expected-defect controls, separate from correctness baselines.

AuthorityEffect: None. Does not repair sources or certify absent failures.
"""
from datetime import datetime, timezone
from pathlib import Path as _FilesystemPath
import sys as _contract_sys
_contract_sys.path.insert(0, str(_FilesystemPath(__file__).resolve().parents[4] / "scripts"))
from contract_scores import RecordPath as Path, copy_file as _copy_record_file
import json
import shutil
import subprocess
from replay import ROOT, RUST, COMPOSITION_SOURCES, inventory, digest, write, snapshot, execute, dependency_sources, remove_owned


def main():
    probe = ROOT / "evidence/quality/l4a_six/20261020-curvature-control"
    pins = json.loads((probe / "source_pins.json").read_text(encoding="utf8"))
    assert digest(probe / "control.rs") == pins["controls_sha256"]
    assert all(digest(ROOT / name) == pin for name, pin in pins["sources"].items())
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-curvature-control"
    out = ROOT / "evidence/quality/l4a_six" / stamp
    out.mkdir()
    work = RUST / "target/l4a-six" / stamp
    sources = inventory()
    write(out / "source_manifest.json", sources)
    _copy_record_file(__file__, out / "control.py")
    _copy_record_file(Path(__file__).with_name("replay.py"), out / "replay.py")
    _copy_record_file(probe / "control.rs", out / "control.rs")
    _copy_record_file(probe / "source_pins.json", out / "source_pins.json")
    receipt = {"AuthorityEffect": "None", "evaluation_timestamp": datetime.now(timezone.utc).isoformat(),
        "scope": "Actual scoped holonomy package and public inputs. Expected-defect observations are not ordinary passing baseline cases or a grade promotion.",
        "runner_sha256": digest(out / "control.py"), "helper_sha256": digest(out / "replay.py"),
        "controls_sha256": digest(out / "control.rs"), "source_manifest_sha256": digest(out / "source_manifest.json"),
        "versions": {name: subprocess.check_output([name, "--version"], text=True).strip() for name in ("cargo", "rustc")},
        "runs": [], "minimum_free_build_bytes": 1024**3}
    # One-GiB admission is specific to this package/control target. Its prior
    # same-source complete package cache was 384,085,379 bytes; a 512-MiB
    # additional reserve fits. This is not a bound on peak compiler activity.
    reference = ROOT / "evidence/quality/l4a_six/20261020T145348Z-mutations/receipt.json"
    previous = json.loads(reference.read_text(encoding="utf8"))
    reference_sources = json.loads(reference.with_name("source_manifest.json").read_text(encoding="utf8"))
    assert reference_sources.keys() == sources.keys()
    differences = {name: {"before": reference_sources[name], "current": sources[name]}
                   for name in sources if sources[name] != reference_sources[name]}
    # A supplementary QM adapter is not compiled by the holonomy package.
    # Keep that live drift explicit; it cannot change this package's footprint.
    assert differences.keys() <= {path.relative_to(ROOT).as_posix() for path in COMPOSITION_SOURCES}
    observed = next(run for run in previous["baselines"] if run["package"] == "tfqm_holonomy")
    assert observed["exit_code"] == 0 and not observed["timed_out"]
    assert digest(ROOT / observed["log"]) == observed["log_sha256"]
    cache = observed["disk_observation"]["completed_cache_file_bytes"]
    assert cache + 512 * 1024**2 <= receipt["minimum_free_build_bytes"]
    receipt["headroom_reference"] = {"path": reference.relative_to(ROOT).as_posix(), "sha256": digest(reference),
        "completed_cache_file_bytes": cache, "additional_margin_bytes": 512 * 1024**2,
        "outside_holonomy_source_differences": differences,
        "scope": "Completed-cache endpoint observation, not a peak-space guarantee."}
    print(out, flush=True)
    dependencies = None
    findings = []
    mechanisms = []
    try:
        snapshot(work)
        _copy_record_file(probe / "control.rs", work / "src/holonomy/tests/curvature_control.rs")
        meta = subprocess.run(["cargo", "metadata", "--offline", "--quiet", "--format-version", "1"], cwd=work, capture_output=True, text=True)
        (out / "cargo_metadata.json").write_text(meta.stdout, encoding="utf8")
        (out / "metadata_stderr.log").write_text(meta.stderr, encoding="utf8")
        receipt["metadata_capture"] = {"command": meta.args, "cwd": str(work), "exit_code": meta.returncode,
            "sha256": digest(out / "cargo_metadata.json"), "stderr_sha256": digest(out / "metadata_stderr.log")}
        if meta.returncode != 0:
            return
        dependencies = dependency_sources(json.loads(meta.stdout))
        metadata = json.loads(meta.stdout)
        package_ids = {package["name"]: package["id"] for package in metadata["packages"]}
        nodes = {node["id"]: node for node in metadata["resolve"]["nodes"]}
        closure, pending = set(), [package_ids["tfqm_holonomy"]]
        while pending:
            identity = pending.pop()
            if identity not in closure:
                closure.add(identity)
                pending.extend(dependency["pkg"] for dependency in nodes[identity]["deps"])
        assert package_ids["tfqm_homology_linear_audit"] not in closure
        receipt["compiled_package_dependency_closure"] = sorted(closure)
        write(out / "dependency_sources.json", dependencies)
        receipt["dependency_sources_sha256"] = digest(out / "dependency_sources.json")
        receipt["free_before_build"] = shutil.disk_usage(ROOT).free
        if receipt["free_before_build"] < receipt["minimum_free_build_bytes"]:
            receipt["refusal"] = "Selected holonomy-control disk reserve unavailable"
            return
        run = execute(["cargo", "test", "--offline", "--locked", "--quiet", "--target-dir", str(work / "build"),
            "-p", "tfqm_holonomy", "--test", "curvature_control", "--", "--nocapture"], work, out / "control.log")
        receipt["runs"].append(run)
        log = (out / "control.log").read_text(encoding="utf8")
        success = run["exit_code"] == 0 and not run["timed_out"] and "POSITIVE_CONTROL" in log
        findings.append({"source": "code/rust/src/holonomy/curvature.rs", "gate": "G3", "affected_gates": ["G3"],
            "reproduced": success and "DEFECT_CONFIRMED" in log,
            "witness": "A 1-dimensional valid triangle connection is modified through public forward storage to use a canonical 2x1 last transport. The actual loop boundary returns shape 2x1; plaquette curvature then panics indexing the 1x1 identity at index 1. The exact panic payload and valid triangle control are asserted."})
        mechanisms.append({"source": "code/rust/src/holonomy/curvature.rs", "gate": "G5", "grade": "D",
            "reproduced": success and "MECHANISM_ABSENT" in log,
            "witness": "curvature_commutator computes a 1x1 output despite caller-supplied zero cell and work limits. The _limits argument is unused. This is an observed missing operational mechanism, not a structural CCN E claim."})
    finally:
        receipt["sources_unchanged"] = sources == inventory()
        receipt["dependency_sources_unchanged"] = dependencies is not None and all(Path(name).is_file() and digest(Path(name)) == pin for name, pin in dependencies.items())
        write(out / "findings.json", findings)
        write(out / "mechanism_findings.json", mechanisms)
        receipt["findings_sha256"] = digest(out / "findings.json")
        receipt["mechanism_findings_sha256"] = digest(out / "mechanism_findings.json")
        remove_owned(work / "build", work)
        receipt["owned_build_removed"] = True
        write(out / "receipt.json", receipt)


if __name__ == "__main__":
    main()
