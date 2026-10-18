"""Reproduce the source inventory; this does not run tests or certify mathematics.

Run this file directly with --write to refresh the inventory, or --check to
compare it with current sources. Historical source receipts are not rewritten.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

OWNERS = (
    "omega_number_theory", "omega_linear_algebra", "omega_lie_theory",
    "omega_quantum_physics", "omega_sheaf_theory", "omega_mub",
    "omega_finite_probability", "omega_category_theory", "omega_combinatorics",
    "omega_fusion_categories", "omega_functional", "omega_general_relativity",
    "omega_homology", "omega_holonomy", "omega_homotopy_type_theory",
    "omega_solvers", "omega_wdp",
)


def collect(root: Path) -> dict:
    def entry(path: Path) -> dict:
        content = path.read_bytes()
        return {"path": path.relative_to(root).as_posix(),
                "sha256": hashlib.sha256(content).hexdigest(),
                "lines": len(content.splitlines())}

    lean_dir = root / "lean4/quantum_mechanics"
    modules = []
    for path in sorted(lean_dir.glob("*.lean")):
        if path.name == "lakefile.lean":
            continue
        row = entry(path)
        row["imports"] = re.findall(r"^import\s+(\S+)", path.read_text(), re.M)
        modules.append(row)
    rust = {}
    for owner in OWNERS:
        directory = root / "omega_engine/crates_rs" / owner
        paths = sorted(path for path in directory.rglob("*.rs")
                       if not {"target", ".git"}.intersection(path.relative_to(directory).parts))
        rust[owner] = {"files": [entry(path) for path in paths],
                       "source_files": sum("src" in path.relative_to(directory).parts for path in paths),
                       "test_files": sum("tests" in path.relative_to(directory).parts for path in paths),
                       "total_files": len(paths)}
    return {"schema": "finite-qm.source-inventory.v1",
            "scope": "All top-level canonical QM Lean modules and Rust files in the 17 named owners",
            "limits": "Hashes and counts establish inventory coverage, not semantic review, successful compilation, axiom purity, or theorem scope. See the accompanying review for actual validation.",
            "lean_configuration": [entry(lean_dir / name) for name in
                                   ("lakefile.lean", "lake-manifest.json", "lean-toolchain")],
            "lean_modules": modules, "rust_owners": rust}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    parser.add_argument("--manifest", action="store_true",
                        help="also refresh/check the current paper manifest (requires PyYAML; stage new files first)")
    parser.add_argument("--paper-only", action="store_true",
                        help="with --manifest, retain the historical Lean/Rust review inventory")
    args = parser.parse_args()
    if args.paper_only and not args.manifest:
        parser.error("--paper-only requires --manifest")
    root = next(parent for parent in Path(__file__).resolve().parents
                if (parent / "omega_engine/crates_rs/Cargo.toml").is_file())
    project = root / "omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm"
    output = project / "research/qm_weyl_gleason_source_inventory.json"
    if not args.paper_only:
        data = collect(root)
        rendered = json.dumps(data, indent=2) + "\n"
        if args.write:
            output.write_text(rendered)
        elif output.read_text() != rendered:
            raise SystemExit("Source inventory differs; rerun --write after review")
    if args.manifest:
        import yaml
        manifest = project / "finite_qm_file_manifest.yaml"
        data = yaml.safe_load(manifest.read_text())
        old = {row["path"].replace("\\", "/"): row for row in data["files"]}
        tracked = subprocess.check_output(
            ["git", "-C", str(root), "ls-files", "-z", "--", str(project)], text=True)
        paths = {}
        for relative in sorted(filter(None, tracked.split("\0"))):
            path = root / relative
            if path in (manifest, project / "SHA256SUMS") or path.is_symlink() or not path.is_file():
                continue
            key = path.relative_to(project).as_posix()
            if key.split("/", 1)[0] == "dist" or ("/" not in key and path.suffix.lower() == ".zip"):
                continue
            paths[key] = path
        ordered = [key for key in old if key in paths] + sorted(paths.keys() - old.keys())
        rows = []
        for key in ordered:
            path = paths[key]
            row = dict(old.get(key, {
                "path": key, "current_name": path.name,
                "proposed_new_name": path.name, "proposed_decomposition": key,
                "kind": "markdown_spec" if path.suffix == ".md" else path.suffix.lstrip(".") or "file",
            }))
            content = path.read_bytes()
            row.update(sha256=hashlib.sha256(content).hexdigest(), size_bytes=len(content))
            rows.append(row)
        data["metadata"].update(
            cataloged_count=len(rows),
            scope="Current tracked regular files, excluding this manifest, SHA256SUMS, dist/ outputs and root-level ZIP archives; nested historical ZIPs retain catalog custody and historical receipts retain their recorded revision scopes",
            directories_walked=sorted({row["path"].replace("\\", "/").split("/")[0]
                                      for row in rows if "/" in row["path"].replace("\\", "/")}),
        )
        data["files"] = rows
        content = yaml.safe_dump(data, sort_keys=False, allow_unicode=True)
        if args.write:
            manifest.write_text(content)
        elif manifest.read_text() != content:
            raise SystemExit("Paper file manifest differs; stage new files and rerun --write --manifest")
        print(f"{len(rows)} paper files in current manifest")
        if args.paper_only:
            return
        data = collect(root)
    print(f"{len(data['lean_modules'])} Lean modules; "
          f"{sum(row['total_files'] for row in data['rust_owners'].values())} Rust files; "
          f"{len(OWNERS)} owners")


if __name__ == "__main__":
    main()
