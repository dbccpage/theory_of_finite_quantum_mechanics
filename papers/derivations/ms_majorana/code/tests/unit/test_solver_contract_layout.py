"""Structural gates for the Python SolverKernel v1.2 layout."""

from __future__ import annotations

import ast
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SOLVER_ROOT = REPO_ROOT / "omega_engine" / "crates" / "solver"
OPERATOR_ROOT = REPO_ROOT / "omega_engine" / "crates" / "operator"

RETAINED_SOLVER_MODULES = {
    "solv_cadical_unsat_core.py",
    "solv_gauge_higgs_susy.py",
    "solv_gauge_higgs_susy_derivation.py",
    "solv_l1_obstruction_witness.py",
    "solv_l1_topological_defects.py",
    "solv_langlands_automorphic_matcher.py",
}


def _source(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def _has_handwritten_surface(path: Path) -> bool:
    """Distinguish retained WIPs from generated-only Rust mirrors."""
    source = _source(path)
    marker = source.find("class _RustSurfaceMeta")
    handwritten_source = source if marker < 0 else source[:marker]
    tree = ast.parse(handwritten_source, filename=str(path))
    return any(
        isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        or (
            isinstance(node, ast.ClassDef)
            and node.name not in {"_RustSurfaceMeta", "_RustSurfaceObject"}
        )
        for node in tree.body
    )


def test_top_level_solver_modules_use_canonical_prefix() -> None:
    names = sorted(path.name for path in SOLVER_ROOT.glob("*.py"))
    violations = [
        name for name in names if name != "__init__.py" and not name.startswith("solv_")
    ]
    assert not violations, f"noncanonical top-level solver filenames: {violations}"


def test_solver_package_has_no_legacy_factory_or_registry_files() -> None:
    legacy = sorted(
        path.name
        for path in SOLVER_ROOT.glob("*.py")
        if "factory" in path.stem or "registry" in path.stem
    )
    assert not legacy, f"factory/registry behavior is not a SolverKernel role: {legacy}"
    assert not (SOLVER_ROOT / "base" / "solv_factory.py").exists()


def test_retained_solver_modules_exist_at_top_level() -> None:
    solver_paths = sorted(SOLVER_ROOT.glob("*.py"))
    solver_names = {path.name for path in solver_paths}
    assert RETAINED_SOLVER_MODULES.issubset(solver_names)
