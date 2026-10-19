"""Pytest bootstrap and local decoupling bridge for Paper 026 test suite.

Decouples Paper 026 from legacy omega_engine/crates/ by mapping legacy crate imports
directly to local paper code (`code/`) and local support modules (`tests/support/`).

The bridge resolves only the legacy ``omega_engine.crates.*`` namespace. No
directory is put at the front of ``sys.path``: every other import, including
``omega_engine_pfp``, resolves from the repository root that pytest.ini
already places on the path, so no local copy can shadow a real package.

The one path entry kept is ``code/``, appended last. The four deposited tests
(pinned in sha256sums) import the top-level module ``majorana_evaluator``, and
verify_deposit.py measures ``--cov=majorana_evaluator``. It runs
``python -m pytest`` from ``code/``, which already has ``code/`` on the path; a
run from the repository root does not, so the entry is added here. Appended, it
can only satisfy a name that nothing earlier on the path provides.

Preserves AuthorityEffect: None throughout.
"""

from __future__ import annotations

import sys
from importlib.abc import MetaPathFinder
from importlib.machinery import ModuleSpec
from importlib.util import spec_from_file_location
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parent
CODE_DIR = TESTS_DIR.parent
SUPPORT_DIR = TESTS_DIR / "support"
def _find_repo_root(start: Path) -> Path:
    for parent in [start, *start.parents]:
        if (parent / ".git").exists() or (parent / "pyproject.toml").exists():
            return parent
    return start.parents[4]


REPO_ROOT = _find_repo_root(CODE_DIR)

if str(CODE_DIR) not in sys.path:
    sys.path.append(str(CODE_DIR))


class Paper026CratesBridgeFinder(MetaPathFinder):
    """Import hook resolving legacy omega_engine.crates.* into local paper assets."""

    FLAT_NAMESPACES = frozenset(
        {
            "homology_theory",
            "linear_algebra_theory",
            "residuals",
            "type",
            "solver",
            "quantum_physics",
            "operator",
            "engine",
            "pipeline",
            "runtime",
            "certificate",
            "trace",
            "discrete_deformation_algebra",
            "functional",
            "evaluator",
            "prompt_civilization",
            "terminalizers",
            "state",
            "projection_obstruction",
            "carrier",
        }
    )

    SEARCH_DIRS = (CODE_DIR, SUPPORT_DIR)

    def find_spec(self, fullname: str, path: object = None, target: object = None) -> ModuleSpec | None:
        # Coda smoke tests expect ImportError when importing omega_engine.crates.coda.*
        if fullname == "omega_engine.crates.coda" or fullname.startswith("omega_engine.crates.coda."):
            return None

        if fullname == "omega_engine":
            oe_dir = REPO_ROOT / "omega_engine"
            init_file = oe_dir / "__init__.py"
            if init_file.is_file():
                return spec_from_file_location(fullname, str(init_file), submodule_search_locations=[str(oe_dir)])
            spec = ModuleSpec(fullname, None, is_package=True)
            spec.submodule_search_locations = [str(oe_dir)] if oe_dir.exists() else []
            return spec

        if fullname == "omega_engine.crates":
            spec = ModuleSpec(fullname, None, is_package=True)
            spec.submodule_search_locations = [str(d) for d in self.SEARCH_DIRS if d.exists()]
            return spec

        if not fullname.startswith("omega_engine.crates."):
            return None

        parts = fullname.split(".")[2:]
        first = parts[0]
        rest = parts[1:]

        # If it's a flat namespace root (e.g. omega_engine.crates.residuals, omega_engine.crates.solver, etc.)
        if len(parts) == 1 and first in self.FLAT_NAMESPACES:
            for search_base in self.SEARCH_DIRS:
                cand_dir = search_base / first
                init_file = cand_dir / "__init__.py"
                if init_file.is_file():
                    return spec_from_file_location(fullname, str(init_file), submodule_search_locations=[str(cand_dir)])
            spec = ModuleSpec(fullname, None, is_package=True)
            spec.submodule_search_locations = [str(d) for d in self.SEARCH_DIRS if d.exists()]
            return spec

        # If it's inside a flat namespace, check candidate files across all roots
        if len(parts) >= 2 and first in self.FLAT_NAMESPACES:
            # First check direct path in support, code, or p002: e.g. SUPPORT_DIR / Path(*parts)
            for search_base in self.SEARCH_DIRS:
                cand_dir = search_base / Path(*parts)
                if cand_dir.is_dir():
                    init_file = cand_dir / "__init__.py"
                    if init_file.is_file():
                        return spec_from_file_location(fullname, str(init_file), submodule_search_locations=[str(cand_dir)])
                    spec = ModuleSpec(fullname, None, is_package=True)
                    spec.submodule_search_locations = [str(cand_dir)]
                    return spec

                cand_file = search_base / (Path(*parts).as_posix() + ".py")
                if cand_file.is_file():
                    return spec_from_file_location(fullname, str(cand_file))

            # Then check flattened relative to search_base: e.g. CODE_DIR / Path(*rest).py
            mod_rel = Path(*rest)
            for search_base in self.SEARCH_DIRS:
                cand_file = search_base / (mod_rel.as_posix() + ".py")
                if cand_file.is_file():
                    return spec_from_file_location(fullname, str(cand_file))

                cand_dir = search_base / mod_rel
                if cand_dir.is_dir():
                    init_file = cand_dir / "__init__.py"
                    if init_file.is_file():
                        return spec_from_file_location(fullname, str(init_file), submodule_search_locations=[str(cand_dir)])
                    spec = ModuleSpec(fullname, None, is_package=True)
                    spec.submodule_search_locations = [str(cand_dir)]
                    return spec

        # For any other package (e.g. majorana, prime, domain, representation)
        for search_base in self.SEARCH_DIRS:
            candidate_dir = search_base / Path(*parts)
            if candidate_dir.is_dir():
                init_file = candidate_dir / "__init__.py"
                if init_file.is_file():
                    return spec_from_file_location(fullname, str(init_file), submodule_search_locations=[str(candidate_dir)])
                spec = ModuleSpec(fullname, None, is_package=True)
                spec.submodule_search_locations = [str(candidate_dir)]
                return spec

            candidate_file = search_base / (Path(*parts).as_posix() + ".py")
            if candidate_file.is_file():
                return spec_from_file_location(fullname, str(candidate_file))

        return None


# Install bridge finder at highest precedence
if not any(isinstance(finder, Paper026CratesBridgeFinder) for finder in sys.meta_path):
    sys.meta_path.insert(0, Paper026CratesBridgeFinder())
