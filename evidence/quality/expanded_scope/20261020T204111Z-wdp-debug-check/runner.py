"""Source-pinned WDP debug compilation baseline, not a test/grade receipt."""
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[4]
spec = importlib.util.spec_from_file_location("expanded_dependency_capture", Path(__file__).parents[1] / "l4a_qm_six/replay.py")
capture = importlib.util.module_from_spec(spec)
spec.loader.exec_module(capture)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output = ROOT / "evidence/quality/expanded_scope" / (stamp + "-wdp-debug-check")
    output.mkdir(parents=True)
    (output / "runner.py").write_bytes(Path(__file__).read_bytes())
    receipt = {"AuthorityEffect": "None", "status": "RUNNING", "python": sys.version,
               "runner_sha256": sha(Path(__file__)), "capture_helper_sha256": sha(Path(capture.__file__)),
               "runs": [], "scope": "WDP debug library compilation only; no unit/integration execution or L4 grade certification."}
    print(output.relative_to(ROOT).as_posix(), flush=True)
    metadata_command = ["cargo", "metadata", "--offline", "--locked", "--format-version", "1", "--manifest-path", "code/rust/Cargo.toml"]
    with (output / "metadata.json").open("w", encoding="utf-8") as stream, (output / "metadata.stderr.log").open("w", encoding="utf-8") as errors:
        metadata = subprocess.run(metadata_command, cwd=ROOT, stdout=stream, stderr=errors)
    receipt["metadata"] = {"command": metadata_command, "exit_code": metadata.returncode,
        "sha256": sha(output / "metadata.json"), "stderr_sha256": sha(output / "metadata.stderr.log")}
    if metadata.returncode:
        receipt["status"] = "METADATA_UNAVAILABLE"
    else:
        resolved = json.loads((output / "metadata.json").read_text())
        dependencies = capture.dependency_sources(resolved)
        for name in [ROOT / "code/rust/Cargo.toml", ROOT / "code/rust/Cargo.lock"]:
            dependencies[str(name)] = sha(name)
        (output / "inputs.json").write_text(json.dumps(dependencies, indent=2) + "\n")
        receipt["inputs_sha256"] = sha(output / "inputs.json")
        receipt["input_scope"] = "Resolved package Rust/manifest/lock sources; non-Rust included assets and compiler expansion remain unbound."
        command = ["cargo", "check", "--offline", "--locked", "--manifest-path", "code/rust/Cargo.toml",
                   "-p", "tfqm_wdp", "--lib", "--target-dir", "code/rust/target/expanded-scope-wdp"]
        execution = capture.execute(command, ROOT, output / "check.log", timeout=900)
        receipt["runs"].append(execution)
        receipt["inputs_unchanged"] = all(Path(p).is_file() and sha(Path(p)) == h for p, h in dependencies.items())
        receipt["status"] = "PASS" if execution["exit_code"] == 0 and receipt["inputs_unchanged"] else "FAILED_OR_INCONCLUSIVE"
    (output / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt), flush=True)


if __name__ == "__main__":
    main()
