"""Audit every governed Python/Rust source under code/ without assigning grades.

Run from any directory. --output is a new directory: existing reports are never
replaced. Build the repository's standalone rust_metrics crate and pass its
binary to include syn parsing; omission is explicitly reported as unrun.
AuthorityEffect: None. Syntax, source custody and companion validity are not
semantic correctness, compilation, test coverage or L5 certification.
"""
from __future__ import annotations

import argparse
import ast
import csv
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import score_scope_contracts as contracts

ROOT = contracts.ROOT


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def collect(rust_metrics_bin: Path | None) -> tuple[dict, str]:
    paths = [p for p in contracts.source_paths() if contracts.rel(p).startswith("code/")]
    # Bind observations to both ends of the audit. This detects ordinary source
    # edits during the run, not hostile filesystem races or changes and reverts.
    before = {contracts.rel(p): digest(p) for p in paths}
    audit, contracts_ok = contracts.audit_population(paths)
    python_errors, assert_candidates, rows = [], [], []
    source_lines = 0
    for path, contract in zip(paths, audit["artifacts"]):
        name = contracts.rel(path)
        if name != contract["path"]:
            raise ValueError("contract audit population/order disagreement")
        raw = path.read_bytes()
        lines = len(raw.splitlines())
        source_lines += lines
        if path.suffix == ".py":
            try:
                tree = ast.parse(raw, filename=name)
                compile(tree, name, "exec")
            except (SyntaxError, ValueError) as error:
                python_errors.append({"path": name, "error": str(error)})
            else:
                if "tests" not in path.parts and not path.name.startswith("test_"):
                    for node in ast.walk(tree):
                        if isinstance(node, ast.Assert):
                            assert_candidates.append({"path": name, "line": node.lineno})
        rows.append([name, before[name], len(raw), lines, contract["valid"],
                     contract.get("assessment_status"), contract.get("score_token"),
                     contract.get("error", "")])
    rust = {"status": "unrun", "reason": "no rust_metrics binary supplied"}
    if rust_metrics_bin is not None:
        binary = rust_metrics_bin.resolve(strict=True)
        rust_paths = [contracts.rel(p) for p in paths if p.suffix == ".rs"]
        result = subprocess.run([str(binary), *rust_paths], cwd=ROOT,
                                capture_output=True, text=True, check=False)
        rust = {"binary_sha256": digest(binary), "exit_code": result.returncode,
                "status": "passed" if result.returncode == 0 else "failed",
                "source_count": len(rust_paths), "stderr": result.stderr}
        if result.returncode == 0:
            metrics = json.loads(result.stdout)
            if set(metrics) != set(rust_paths):
                raise ValueError("Rust parser omitted or added source paths")
            rust["scope"] = "syn parse only; no Rust name/type checking, macro expansion or dependency build"
    changed = [contracts.rel(p) for p in paths if digest(p) != before[contracts.rel(p)]]
    buffer = io.StringIO(newline="")
    writer = csv.writer(buffer, delimiter="\t", lineterminator="\n")
    writer.writerow(["path", "sha256", "bytes", "lines", "companion_valid", "assessment_status", "score_token", "error"])
    writer.writerows(rows)
    result = {
        "schema": "tfqm.code-quality-observation.v1", "AuthorityEffect": "None",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "scope": "governed code/**/*.py and code/**/*.rs, tracked and ordinary untracked; policy exclusions apply",
        "source_lines": source_lines, "contracts": audit["summary"],
        "contract_errors": audit["errors"] + audit["grandfathered_errors"],
        "python_syntax_errors": python_errors, "rust_syntax": rust,
        "runtime_assert_review_candidates": assert_candidates,
        "assert_candidate_limit": "An AST assert is a review candidate, not evidence of a defect or a gate grade.",
        "changed_during_audit": changed,
        "observations_passed": contracts_ok and not audit["grandfathered_errors"] and not python_errors
                               and not changed and rust["status"] == "passed",
        "certification": "No semantic, test-coverage, safety, capability or L5 certification is assigned.",
    }
    return result, buffer.getvalue()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path, help="new report directory")
    parser.add_argument("--rust-metrics-bin", type=Path)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("output directory already exists; choose a fresh report location")
    result, inventory = collect(args.rust_metrics_bin)
    args.output.mkdir(parents=True, exist_ok=False)
    (args.output / "sources.tsv").write_text(inventory, encoding="utf-8")
    result["sources_tsv_sha256"] = digest(args.output / "sources.tsv")
    (args.output / "audit.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "sources": result["contracts"]["sources"],
                      "observations_passed": result["observations_passed"],
                      "certification": result["certification"]}))
    return 0 if result["observations_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
