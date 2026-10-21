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
    testing = "--test" in sys.argv[1:]
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output = ROOT / "evidence/quality/expanded_scope" / (stamp + ("-wdp-debug-tests" if testing else "-wdp-debug-check"))
    output.mkdir(parents=True)
    (output / "runner.py").write_bytes(Path(__file__).read_bytes())
    receipt = {"AuthorityEffect": "None", "status": "RUNNING", "python": sys.version,
               "runner_sha256": sha(Path(__file__)), "capture_helper_sha256": sha(Path(capture.__file__)),
               "runs": [], "scope": ("WDP debug library unit tests only; no all-target, release or L4 grade certification." if testing else "WDP debug library compilation only; no unit/integration execution or L4 grade certification.")}
    print(output.relative_to(ROOT).as_posix(), flush=True)
    compiler = subprocess.run(["rustc", "-vV"], capture_output=True, text=True, check=True)
    (output / "rustc-version.txt").write_text(compiler.stdout, encoding="utf-8")
    host = next(line.removeprefix("host: ") for line in compiler.stdout.splitlines() if line.startswith("host: "))
    receipt["compiler"] = {"host": host, "version_sha256": sha(output / "rustc-version.txt")}
    metadata_command = ["cargo", "metadata", "--offline", "--locked", "--format-version", "1", "--filter-platform", host, "--manifest-path", "code/rust/Cargo.toml"]
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
        command = ["cargo", "test" if testing else "check", "--offline", "--locked", "--manifest-path", "code/rust/Cargo.toml",
                   "-p", "tfqm_wdp", "--lib", "--target-dir", "code/rust/target/expanded-scope-wdp"]
        execution = capture.execute(command, ROOT, output / "check.log", timeout=900)
        receipt["runs"].append(execution)
        receipt["inputs_unchanged"] = all(Path(p).is_file() and sha(Path(p)) == h for p, h in dependencies.items())
        receipt["status"] = "PASS" if execution["exit_code"] == 0 and receipt["inputs_unchanged"] else "FAILED_OR_INCONCLUSIVE"
    (output / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt), flush=True)


if __name__ == "__main__":
    main()
