"""Serial local integration checks, with per-build cleanup. AuthorityEffect None."""

from datetime import datetime, timezone
from pathlib import Path
import json
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "code/rust/quality/category_homology"))
import run_audit as audit


def execute_clean(command, cwd, output, work):
    build = work / "target"
    if build.exists():
        raise RuntimeError("A fresh build tree is required")
    try:
        return audit.execute_build(command, cwd, output, timeout=900)
    finally:
        audit.clear_debug_outputs(build, work)
        if build.exists():
            shutil.rmtree(build)


def main():
    output = Path(__file__).resolve().parent
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    work = ROOT / "code/rust/target/pr-review-current-workspace"
    work.mkdir(parents=True, exist_ok=True)
    command = ["cargo", "check", "--manifest-path", str(ROOT / "code/rust/Cargo.toml"),
               "--workspace", "--lib", "--offline", "--locked", "--config",
               "profile.dev.debug=0", "--target-dir", str(work / "target")]
    run = execute_clean(command, ROOT, output / "workspace-current-check.log", work)
    run.update(source_commit=head, main_base="5ed88c23cd2b5036109f689f6af848c2d6431318")
    audit.write_json(output / "workspace-current-check.json", run)
    print("Current workspace library check:", run["exit_code"], flush=True)
    if run["exit_code"] != 0:
        print((output / "workspace-current-check.log").read_text(encoding="utf-8", errors="replace")[-9000:])
        return 1
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-current-homology"
    receipt = ROOT / "evidence/quality/category_homology" / stamp
    receipt.mkdir()
    work = ROOT / "code/rust/target/category-homology-audit" / stamp
    audit.snapshot(work, "homology")
    inputs = audit.inventory()
    audit.write_json(receipt / "source_manifest.json", inputs)
    roots, dependencies = audit.bind_dependencies(work, receipt)
    command = ["cargo", "test", "--target-dir", str(work / "target"), "-p",
               "tfqm_category_homology_audit", "--lib", "--offline", "--locked", "--quiet", "homology"]
    run = execute_clean(command, work, receipt / "homology.log", work)
    summary = {
        "AuthorityEffect": "None", "source_commit": head, "run": run,
        "source_unchanged": inputs == audit.inventory(),
        "dependencies_unchanged": dependencies == audit.dependency_inventory(roots),
        "scope": "One fresh homology integration test on updated providers; no mutation or grade promotion.",
        "all_files_L5A": False, "build_tree_removed": not (work / "target").exists(),
    }
    audit.write_json(receipt / "summary.json", summary)
    audit.write_json(output / "current-homology-receipt.json", {"receipt": receipt.relative_to(ROOT).as_posix()})
    print(json.dumps(summary, indent=2), flush=True)
    return 0 if run["exit_code"] == 0 and summary["source_unchanged"] and summary["dependencies_unchanged"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
