"""Check source custody and package consistency, not historical theorem truth.

The immutable source manifest and the mutable deliverable integrity list
serve different purposes. --write-manifest deliberately refreshes only the
deliverable list after the caller has reviewed changes.
"""

from __future__ import annotations

import hashlib
import json
import re
from argparse import ArgumentParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

from build_claim_index import build_index, render_lean_map
from coda_core import example_results
from deposit_paths import read_manifest, safe_path, walk_files
from run_examples import exact_json

SKIP_DIRECTORIES = {
    ".lake",
    "__pycache__",
    ".pytest_cache",
    ".ipynb_checkpoints",
    ".venv",
    ".git",
    ".mypy_cache",
    ".ruff_cache",
}


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def load(path: Path):
    return json.loads(
        path.read_text(encoding="utf-8-sig"), object_pairs_hook=unique_object
    )


def inside(root: Path, relative: str) -> Path:
    return safe_path(root, relative)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def files(root: Path) -> list[str]:
    excluded = SKIP_DIRECTORIES | {"venv", "dist", "build", "htmlcov", "dev_rips",
                                   "rt", "b", "scratch", "_support", "evidence", "reconstruction_v1"}
    return [path.relative_to(root).as_posix() for path in walk_files(
        root, excluded, {"SHA256SUMS", ".coverage", "DEPOSIT_CHECKLIST.md", ".gitkeep"},
        {".zip", ".pyc", ".pyo", ".tmp", ".log"},
    )]


def source_custody(root: Path) -> set[str]:
    manifest = load(root / "source_manifest.json")
    if manifest["baseline_commit"] != "d435c7f86d2896b1b738d45abd7f47a690dcd388":
        raise ValueError("Unexpected acquisition baseline")
    sources = manifest["sources"]
    if len(sources) != 17 or len({s["source_path"] for s in sources}) != 17:
        raise ValueError("Expected 17 distinct preserved source paths")
    paths = set()
    for row in sources:
        inside(root, row["source_path"])
        path = inside(root, row["preserved_path"])
        if row["preserved_path"] in paths:
            raise ValueError("Two source records share a preserved path")
        paths.add(row["preserved_path"])
        if path.stat().st_size != row["bytes"] or digest(path) != row["sha256"]:
            raise ValueError(f"Source bytes changed: {row['source_path']}")
        data = path.read_bytes()
        blob = hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()
        if blob != row["git_blob"]:
            raise ValueError(f"Source Git blob changed: {row['source_path']}")
    return paths


def validate_claims(root: Path) -> dict:
    actual = load(root / "claim_index.json")
    if actual != build_index(root):
        raise ValueError(
            "Claim index differs from the active ledger; regenerate and review it"
        )
    if (root / "docs/lean_claim_map.md").read_text(encoding="utf-8") != render_lean_map(actual):
        raise ValueError("Supplemental Lean claim map differs from the active ledger")
    legacy = actual["legacy_dispositions"]
    if len(legacy) != 48 or len({r["id"] for r in legacy}) != 48:
        raise ValueError(
            "Expected 48 distinct legacy dispositions in the active ledger"
        )
    current = {row["id"] for row in actual["claims"]}
    if any(
        not row["current_claims"] or not set(row["current_claims"]) <= current
        for row in legacy
    ):
        raise ValueError("Legacy disposition has no valid destination")
    paper = (root / "coda.md").read_text(encoding="utf-8")
    for row in actual["claims"]:
        if paper.count(f"({row['id']}") != 1:
            raise ValueError(f"Missing or duplicate claim marker: {row['id']}")
    return actual


def validate_lean(root: Path, claims: dict) -> int:
    mapped = [name for row in claims["claims"] for name in row["lean_declarations"]]
    audit_source = (root / "lean4/AxiomAudit.lean").read_text(encoding="utf-8")
    audit_names = re.findall(r"^#print axioms (Coda\.\w+)$", audit_source, re.M)
    receipt = (root / "lean4/axiom_report.txt").read_text(encoding="utf-8-sig")
    receipt_names = re.findall(
        r"^'(Coda\.\w+)' (?:does not depend|depends)", receipt, re.M
    )
    if (
        len(audit_names) != 20
        or set(mapped) != set(audit_names)
        or set(receipt_names) != set(audit_names)
    ):
        raise ValueError(
            "Claim map, audit command, and twenty-name audit output differ"
        )
    theorem_names: list[str] = []
    lakefile_path = root / "lean4/lakefile.lean"
    src_dir = root / "lean4"
    if lakefile_path.exists():
        lakefile = lakefile_path.read_text(encoding="utf-8")
        src_match = re.search(r'srcDir\s*:=\s*"([^"]+)"', lakefile)
        if src_match and src_match.group(1) != ".":
            src_dir = (root / "lean4" / src_match.group(1)).resolve()
        roots_match = re.search(r"roots\s*:=\s*#\[(.*?)\]", lakefile, re.DOTALL)
        active_modules = re.findall(r"`(\w+)", roots_match.group(1)) if roots_match else ["Foundations", "Boundaries", "Coda"]
    else:
        active_modules = ["Foundations", "Boundaries", "Coda"]

    lean_files = [src_dir / f"{name}.lean" for name in active_modules]
    for path in lean_files:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        if re.search(r"\b(?:sorry|admit|axiom|native_decide)\b", text):
            raise ValueError(f"Unreviewed proof escape or axiom in {path.name}")
        theorem_names.extend(
            f"Coda.{n}" for n in re.findall(r"^theorem (\w+)", text, re.M)
        )
    if set(theorem_names) != set(audit_names) or len(theorem_names) != 20:
        raise ValueError("The audit does not cover every local theorem")
    permitted = {
        "Coda.image_factor_spec": "Classical.choice",
        "Coda.image_factor_iff": "Classical.choice",
        "Coda.image_factor_unique": "Quot.sound",
    }
    for name in audit_names:
        expected = (
            f"'{name}' depends on axioms: [{permitted[name]}]"
            if name in permitted
            else f"'{name}' does not depend on any axioms"
        )
        if expected not in receipt.splitlines():
            raise ValueError(f"Axiom report does not match the stated scope: {name}")
    return len(audit_names)


def validate_links(root: Path, paths: list[str], historical: set[str]) -> int:
    count = 0
    for relative in paths:
        if not relative.endswith(".md") or relative in historical:
            continue
        path = root / relative
        text = path.read_text(encoding="utf-8-sig")
        for target in re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", text):
            split = urlsplit(target)
            if split.scheme or split.netloc:
                continue
            dest = (path.parent / unquote(split.path)).resolve() if split.path else path
            if not dest.is_relative_to(root) or not dest.exists():
                raise ValueError(f"Unresolved package link in {relative}: {target}")
            count += 1
    return count


def validate_examples_and_notebook(root: Path) -> int:
    expected = json.loads(json.dumps(example_results(), default=exact_json))
    if load(root / "code/fixtures/examples.json") != expected:
        raise ValueError("Stored exact examples differ from a fresh computation")
    legacy = load(root / "code/fixtures/legacy_counterexample.json")
    if not (
        legacy["distinct_arrows"]
        and legacy["identical_span_data"]
        and legacy["legacy_checker_reports_faithful"]
        and legacy["target_status"] == "OPEN"
    ):
        raise ValueError("Legacy counterexample receipt lost its scope")
    notebook = load(root / "jupyter_notebooks/01_coda_walkthrough.ipynb")
    code = [cell for cell in notebook["cells"] if cell["cell_type"] == "code"]
    if len(code) != 8 or [c["execution_count"] for c in code] != list(range(1, 9)):
        raise ValueError("Notebook does not retain all eight executed cells")
    if any(
        output.get("output_type") == "error"
        for cell in code
        for output in cell["outputs"]
    ):
        raise ValueError("Notebook contains a recorded execution error")
    return len(code)


def integrity(root: Path, paths: list[str], write: bool) -> None:
    manifest = root / "SHA256SUMS"
    if write:
        manifest.write_text(
            "".join(f"{digest(root / path)}  {path}\n" for path in paths),
            encoding="utf-8",
            newline="\n",
        )
        return
    entries = dict(read_manifest(root, manifest))
    if set(entries) != set(paths):
        raise ValueError(
            "Integrity manifest does not cover exactly the deliverable inventory"
        )
    for path, expected in entries.items():
        if digest(root / path) != expected:
            raise ValueError(f"Deliverable bytes changed: {path}")


def verify(root: Path, write: bool = False) -> dict:
    historical = source_custody(root)
    paths = files(root)
    for directory in ("code", "lean4", "jupyter_notebooks", "images"):
        if not (root / directory).is_dir():
            raise ValueError(f"Missing requested directory: {directory}")
    claims = validate_claims(root)
    lean_count = validate_lean(root, claims)
    links = validate_links(root, paths, historical)
    cells = validate_examples_and_notebook(root)
    integrity(root, paths, write)
    return {
        "source_files_preserved": len(historical),
        "current_claims": len(claims["claims"]),
        "legacy_dispositions": 48,
        "audited_lean_declarations": lean_count,
        "executed_notebook_cells_recorded": cells,
        "local_links_checked": links,
        "deliverable_files_hashed": len(paths),
        "integrity_action": "written" if write else "verified",
        "scope": "Package consistency; no semantic promotion of historical claims",
        "authority_effect": "None",
    }


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--write-manifest", action="store_true")
    args = parser.parse_args()
    print(
        json.dumps(
            verify(Path(__file__).resolve().parents[1], args.write_manifest), indent=2
        )
    )
