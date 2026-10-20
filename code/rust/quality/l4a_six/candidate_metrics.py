"""Calibrated metrics for explicitly named staged sources; never awards grades."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path as _FilesystemPath
import sys as _contract_sys
_contract_sys.path.insert(0, str(_FilesystemPath(__file__).resolve().parents[4] / "scripts"))
from contract_scores import RecordPath as Path, copy_file as _copy_record_file
import shutil
from replay import ROOT, RUST, digest, write, execute, remove_owned
from records import metric_ceiling


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("sources", nargs="+", type=Path)
    parser.add_argument("--min-free-mib", type=int, choices=(512, 1024), default=1024,
        help="Cold reserve for the small, pinned metric tool; not a peak allocation bound.")
    args = parser.parse_args()
    sources = {str(path.resolve().relative_to(ROOT)): digest(path.resolve()) for path in args.sources}
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-candidate-metrics"
    out = ROOT / "evidence/quality/l4a_six" / stamp
    out.mkdir()
    work = RUST / "target/l4a-six" / stamp
    work.mkdir(parents=True)
    tool = RUST / "quality/category_homology/rust_metrics"
    tool_sources = {str(path.relative_to(ROOT)): digest(path) for path in tool.rglob("*")
        if path.is_file() and path.suffix in (".rs", ".toml", ".lock") and "target" not in path.relative_to(tool).parts}
    _copy_record_file(__file__, out / "measure.py")
    _copy_record_file(Path(__file__).with_name("replay.py"), out / "replay.py")
    receipt = {"AuthorityEffect": "None", "scope": "Source structure only; no runtime cost or engineering grade is inferred.",
        "sources": sources, "metric_tool_sources": tool_sources, "runs": [],
        "runner_sha256": digest(out / "measure.py"), "helper_sha256": digest(out / "replay.py"),
        "minimum_free_cold_build_bytes": args.min_free_mib * 1024**2, "free_before": shutil.disk_usage(ROOT).free}
    print(out, flush=True)
    try:
        if receipt["free_before"] < receipt["minimum_free_cold_build_bytes"]:
            receipt["refusal"] = "Selected cold-build reserve unavailable"
            return
        common = ["--offline", "--quiet", "--manifest-path", str(tool / "Cargo.toml"), "--target-dir", str(work / "build")]
        for action in ("test", "build"):
            result = execute(["cargo", action, *common], tool, out / (action + ".log"))
            receipt["runs"].append(result)
            if result["exit_code"] != 0 or result["timed_out"]:
                return
        result = execute([str(work / "build/debug/tfqm_rust_metrics.exe"), *(str(ROOT / name) for name in sources)], ROOT, out / "metrics.json")
        receipt["runs"].append(result)
        if result["exit_code"] == 0 and not result["timed_out"]:
            measured = json.loads((out / "metrics.json").read_text(encoding="utf8"))
            receipt["ceilings"] = {name: {"ceiling": metric_ceiling(functions)[0], "production_bodies": len(functions),
                "exceeding": metric_ceiling(functions)[1]} for name, functions in measured.items()}
    finally:
        receipt["sources_unchanged"] = all(digest(ROOT / name) == pin for name, pin in sources.items())
        receipt["tool_sources_unchanged"] = all(digest(ROOT / name) == pin for name, pin in tool_sources.items())
        receipt["owned_cache_file_bytes_before_cleanup"] = sum(path.stat().st_size for path in (work / "build").rglob("*") if path.is_file())
        remove_owned(work / "build", work)
        receipt["owned_build_removed"] = True
        write(out / "receipt.json", receipt)


if __name__ == "__main__":
    main()
