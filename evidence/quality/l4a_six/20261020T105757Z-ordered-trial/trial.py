"""Source-pinned trial of the ordered-algebra candidate. AuthorityEffect: None.

Copies current admitted modules and overlays only the separate candidate. Does
not modify live source or award a grade. Owned caches are removed on completion.
"""
from datetime import datetime, timezone
from pathlib import Path
import json
import shutil
import subprocess
from replay import ROOT, RUST, inventory, digest, write, snapshot, execute, dependency_sources, remove_owned


def main():
    candidate = Path(__file__).with_name("ordered_port") / "ordered.rs"
    origin_path = candidate.with_name("origin.json")
    origin = json.loads(origin_path.read_text(encoding="utf8"))
    assert digest(ROOT / origin["source"]) == origin["sha256"], "Candidate origin changed"
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
    receipt = {"AuthorityEffect": "None", "scope": "Separate ordered candidate only; no integrated grade or whole-root package execution.",
        "source_manifest_sha256": digest(out / "source_manifest.json"), "candidate_sha256": digest(candidate),
        "runner_sha256": digest(out / "trial.py"), "helper_sha256": digest(out / "replay.py"),
        "versions": {name: subprocess.check_output([name, "--version"], text=True).strip() for name in ("rustc", "cargo")},
        "runs": [], "minimum_free_build_bytes": 2 * 1024**3}
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
            if shutil.disk_usage(ROOT).free < receipt["minimum_free_build_bytes"]:
                receipt["runs"].append({"started": False, "reason": "Two GiB headroom unavailable"})
                break
            run = execute(["cargo", "test", "--offline", "--quiet", "--target-dir", str(work / "build"),
                "-p", "tfqm_homology_linear_audit", *selection], work, out / (name + ".log"))
            receipt["runs"].append(run)
            print(name, run["exit_code"], flush=True)
            if run["exit_code"] != 0 or run["timed_out"]:
                break
    finally:
        receipt["live_sources_unchanged"] = sources == inventory()
        receipt["candidate_unchanged"] = digest(candidate) == receipt["candidate_sha256"]
        receipt["dependencies_unchanged"] = (dependencies is not None and all(
            Path(p).is_file() and digest(Path(p)) == h for p, h in dependencies.items()))
        remove_owned(work / "build", work)
        receipt["owned_build_removed"] = True
        write(out / "receipt.json", receipt)


if __name__ == "__main__":
    main()
