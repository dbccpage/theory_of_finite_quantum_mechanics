"""Source-bound Rust AST metric replay, with per-build disposal. Python 3.11+."""

from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import subprocess

from run_audit import ROOT, RUST, clear_debug_outputs, digest, execute, execute_build, inventory, write_json


def main():
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    receipt = ROOT / "evidence/quality/category_homology" / (stamp + "-metrics")
    receipt.mkdir(parents=True)
    work = RUST / "target/rust-metrics" / stamp
    work.mkdir(parents=True)
    build = work / "target"
    tool = Path(__file__).resolve().parent / "rust_metrics"
    sources = inventory()
    write_json(receipt / "source_manifest.json", sources)
    common = ["--manifest-path", str(tool / "Cargo.toml"), "--target-dir", str(build), "--offline", "--quiet"]
    runs = []
    copied_binary = work / "metrics.exe"
    try:
        try:
            runs.append(execute_build(["cargo", "test", *common], tool, receipt / "calibration.log"))
        finally:
            clear_debug_outputs(build, work)
        if runs[-1]["exit_code"] != 0:
            raise RuntimeError("AST metric calibration failed")
        try:
            runs.append(execute_build(["cargo", "build", *common], tool, receipt / "build.log"))
            if runs[-1]["exit_code"] == 0:
                shutil.copyfile(build / "debug/tfqm_rust_metrics.exe", copied_binary)
        finally:
            clear_debug_outputs(build, work)
        if runs[-1]["exit_code"] != 0:
            raise RuntimeError("AST metric build failed")
        paths = sorted(key for key in sources if key.endswith(".rs"))
        # Relative paths keep the output portable; the execution cwd is bound.
        runs.append(execute([str(copied_binary), *paths], ROOT, receipt / "metrics.json"))
        if runs[-1]["exit_code"] != 0:
            raise RuntimeError("Rust source parse failed")
        if sources != inventory():
            raise RuntimeError("Source changed during metric replay")
        write_json(receipt / "receipt.json", {
            "AuthorityEffect": "None", "tool": "syn 3.0.9 source AST",
            "sources_unchanged": True, "source_manifest_sha256": digest(receipt / "source_manifest.json"),
            "tool_sources": {p.relative_to(ROOT).as_posix(): digest(p) for p in sorted(tool.rglob("*")) if p.is_file()},
            "runner_sha256": digest(Path(__file__)), "runs": runs,
            "versions": {name: subprocess.check_output([name, "--version"], text=True).strip() for name in ("cargo", "rustc")},
            "claim": "Declared source metrics only; opaque macros and unexpanded cfg are not certified execution flow.",
        })
        print("Receipt:", receipt)
        records = json.loads((receipt / "metrics.json").read_text())
        exceeded = []
        for path, functions in records.items():
            for function in functions:
                if function["ccn"] > 10 or function["cognitive_upper_bound"] > 15 or function["control_nesting"] > 3:
                    exceeded.append({"path": path, **function})
        write_json(receipt / "exceeding_a.json", exceeded)
        print(len(records), "files parsed;", len(exceeded), "functions exceed at least one A structural ceiling")
    finally:
        # Only this run's resolved child is disposable; never delete arbitrary target trees.
        if work.resolve().parent != (RUST / "target/rust-metrics").resolve():
            raise RuntimeError("Unsafe metric cleanup target")
        shutil.rmtree(work)


if __name__ == "__main__":
    main()
