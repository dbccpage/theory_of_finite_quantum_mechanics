"""Verify PO-034 integrity and evidence mappings, with explicit replay modes."""

from __future__ import annotations

import argparse
import ast
import hashlib
import importlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "code"))
sys.path.insert(0, str(ROOT / "tools"))
from deposit_paths import safe_path  # noqa: E402
from rebuild_release import (  # noqa: E402
    _regular_control,
    archive_path,
    current_entries,
    sha256_file,
    validate,
)
from replay_lean_axiom_census import parse_report  # noqa: E402


def check_evidence(ledger: dict, markdown: str) -> dict[str, int]:
    """Check declared evidence locations without claiming to execute proofs or tests."""
    expected = [
        "PO034-C1", "PO034-C2", "PO034-C3",
        *(f"PO034-C3{letter}" for letter in "abcdef"),
        *(f"PO034-C{i}" for i in range(4, 8)),
    ]
    claims = ledger["claims"]
    if ledger.get("authority_effect") != "None" or [c["id"] for c in claims] != expected:
        raise ValueError("claim IDs or authority scope disagree")
    reported = {d.name for d in parse_report(ROOT)}
    referenced: set[str] = set()
    counts = {"claims": len(claims), "written_only": 0, "numerical_examples": 0}
    for claim in claims:
        if not claim.get("statement") or not claim.get("scope"):
            raise ValueError("claim statement or scope is missing")
        if f"**{claim['id']}**" not in markdown:
            raise ValueError("Markdown ledger is missing a claim")
        evidence = claim["code_evidence"]
        if evidence.get("status") == "not_executed":
            if (
                evidence.get("module") != "none"
                or "functions" in evidence
                or "tests" in evidence
                or not evidence.get("note")
            ):
                raise ValueError("written-only claim advertises numerical evidence")
            written = claim["written_evidence"]
            if not written.get("assumptions") or written.get("execution_status") != "not_executed":
                raise ValueError("written-only assumptions or execution status missing")
            proof = written["proof_location"]
            if proof["path"] != ROOT.name + ".md":
                raise ValueError("written proof must reference the canonical manuscript")
            source = safe_path(ROOT, proof["path"]).read_text(encoding="utf-8")
            heading = proof["heading"]
            expected_lemma = "### Lemma 4.3" + claim["id"][-1] + " ("
            if not heading.startswith(expected_lemma) or heading not in source.splitlines():
                raise ValueError("written proof heading is missing or belongs to another claim")
            section = source.split(heading, 1)[1].split("\n### ", 1)[0]
            if "**Proof.**" not in section:
                raise ValueError("written proof location lacks a proof")
            counts["written_only"] += 1
        elif evidence.get("status") == "numerical_examples":
            module_name = evidence["module"]
            if not module_name.startswith("coda_higher_cell."):
                raise ValueError("unexpected evidence module")
            module = importlib.import_module(module_name)
            if not evidence.get("functions") or not evidence.get("tests"):
                raise ValueError("numerical evidence lacks functions or regression examples")
            for function in evidence["functions"]:
                if not callable(getattr(module, function, None)):
                    raise ValueError(f"missing numerical function: {module_name}.{function}")
            for test in evidence["tests"]:
                relative, name = test.split("::", 1)
                source_tree = ast.parse(safe_path(ROOT, relative).read_text(encoding="utf-8"))
                names = {
                    node.name for node in source_tree.body
                    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
                }
                if name not in names:
                    raise ValueError(f"missing regression example: {test}")
            counts["numerical_examples"] += 1
        else:
            raise ValueError("unknown numerical evidence status")
        formal = claim["lean4_evidence"]
        if not formal.get("scope"):
            raise ValueError("formal evidence lacks a scope")
        if formal.get("status") == "not_mechanized":
            if "module" in formal or "theorems" in formal:
                raise ValueError("unmechanized claim advertises formal declarations")
        elif formal.get("status") == "conditional_abstract":
            source = safe_path(
                ROOT, "lean4/" + formal["module"].replace(".", "/") + ".lean"
            ).read_text(encoding="utf-8")
            declarations = set(re.findall(r"(?m)^theorem\s+(\w+)", source))
            if not formal.get("theorems"):
                raise ValueError("formal evidence lacks theorem targets")
            for name in formal["theorems"]:
                if name not in reported or name.split(".")[-1] not in declarations:
                    raise ValueError(f"missing conditional Lean declaration: {name}")
                referenced.add(name)
        else:
            raise ValueError("unknown formal evidence status")
    if referenced != reported or len(reported) != 7:
        raise ValueError("formal census inventory disagrees with the claim ledger")
    if counts["written_only"] != 6 or counts["numerical_examples"] != 7:
        raise ValueError("written and numerical claim inventories disagree")
    counts["conditional_lean_targets"] = len(reported)
    return counts


def check_claim_ledger() -> dict[str, int]:
    ledger = yaml.safe_load((ROOT / "claim_ledger.yaml").read_text(encoding="utf-8"))
    md = (ROOT / "claim_ledger.md").read_bytes()
    if md != (ROOT / f"{ROOT.name}_claim_ledger.md").read_bytes():
        raise ValueError("Markdown claim ledger aliases disagree")
    counts = check_evidence(ledger, md.decode("utf-8"))
    if (ROOT / ".zenodo.json").read_bytes() != (ROOT / "zenodo_metadata.json").read_bytes():
        raise ValueError("publication metadata aliases disagree")
    scope = json.loads((ROOT / "lean4/evidence_scope.json").read_text(encoding="utf-8"))
    for entry in scope["sources"]:
        current = hashlib.sha256(safe_path(ROOT, entry["path"]).read_bytes()).hexdigest()
        if current != entry["current_sha256"]:
            raise ValueError("Lean source binding is stale")
    report_digest = hashlib.sha256((ROOT / "lean4/axiom_report.txt").read_bytes()).hexdigest()
    if report_digest != scope["axiom_report_sha256"]:
        raise ValueError("stored axiom-report binding is stale")
    notebook = json.loads(
        (ROOT / "jupyter_notebooks/034_higher_cell_projection_demo.ipynb").read_text(encoding="utf-8")
    )
    sources = [
        {"type": cell["cell_type"], "source": "".join(cell["source"])} for cell in notebook["cells"]
    ]
    digest = hashlib.sha256(json.dumps(sources, sort_keys=True).encode()).hexdigest()
    execution = notebook["metadata"]["po034_execution"]
    if digest != execution["cell_source_sha256"]:
        raise ValueError("recorded notebook source binding is stale")
    receipt = (ROOT / "docs/pdf_build_receipt.md").read_text(encoding="utf-8")
    for label, relative in [
        ("Canonical Markdown", ROOT.name + ".md"),
        ("TeX", ROOT.name + ".tex"),
        ("PDF", ROOT.name + ".pdf"),
        ("Figure", "public_export/fig1_overview.png"),
    ]:
        digest = hashlib.sha256(safe_path(ROOT, relative).read_bytes()).hexdigest()
        if f"{label} SHA-256: {digest}" not in receipt:
            raise ValueError(f"stale {label} build receipt")
    print(
        "PASS claim mappings: 13 claims; 6 written-only; 7 numerical example mappings; "
        "7 stored conditional abstract Lean targets (no fresh execution implied)"
    )
    return counts


def release_snapshot(archive: Path | None = None) -> tuple:
    errors = validate(ROOT, archive)
    if errors:
        raise ValueError("\n".join(errors))
    selected = archive or archive_path(ROOT)
    controls = [ROOT / "MANIFEST.sha256", ROOT / "SHA256SUMS", selected]
    for control in controls:
        _regular_control(control)
    return tuple(current_entries(ROOT)), tuple((str(p), sha256_file(p)) for p in controls)


def run(command: list[str], label: str, initial: tuple, archive: Path | None) -> bool:
    try:
        env = dict(os.environ, PYTEST_DISABLE_PLUGIN_AUTOLOAD="1")
        result = subprocess.run(
            command, cwd=ROOT, env=env, capture_output=True, text=True, timeout=60, check=False
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        print(f"FAIL {label}: {error}")
        return False
    try:
        if release_snapshot(archive) != initial:
            raise ValueError("release tree or controls changed during replay")
    except (OSError, ValueError) as error:
        print(f"FAIL post-replay custody: {error}")
        return False
    output = (result.stdout + result.stderr).strip()
    print(f"{'PASS' if result.returncode == 0 else 'FAIL'} {label}")
    if output:
        print(output[-4000:])
    return result.returncode == 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--review",
        action="store_true",
        help="numerical review only; fresh Lean/kernel gates remain separate",
    )
    parser.add_argument("--integrity-only", action="store_true", help="check mappings and bytes only")
    parser.add_argument("--archive", type=Path, help="exact release ZIP to qualify")
    args = parser.parse_args()
    archive = args.archive.absolute() if args.archive else None
    try:
        initial = release_snapshot(archive)
        print("PASS complete payload, manifests, and canonical ZIP")
        check_claim_ledger()
    except (OSError, ValueError, KeyError, TypeError, yaml.YAMLError) as error:
        print(f"FAIL package contract: {error}")
        return 1
    if args.integrity_only:
        print("PASS integrity only; tests, notebook execution, and Lean compilation not run")
        return 0

    def replay(command: list[str], label: str) -> bool:
        return run(command, label, initial, archive)

    py = sys.executable
    checks = [
        replay([py, "-m", "pytest", "code/tests", "-q", "--import-mode=importlib"], "numerical regressions"),
        replay([py, "tools/replay_lean_axiom_census.py", "--check"], "static Lean census"),
    ]
    if args.review:
        checks.append(
            replay([py, "scripts/replay_notebook.py", "--direct"], "direct Python notebook replay")
        )
        print("REVIEW MODE: fresh pinned Lean and native Jupyter are not claimed.")
    else:
        checks.append(
            replay([py, "tools/replay_lean_axiom_census.py", "--replay"], "fresh pinned Lean replay")
        )
        checks.append(replay([py, "scripts/replay_notebook.py"], "native Jupyter replay"))
    passed = all(checks)
    print(
        ("PASS" if passed else "FAIL")
        + (" numerical review" if args.review else " complete replay gate")
        + "; authority effect: None"
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
