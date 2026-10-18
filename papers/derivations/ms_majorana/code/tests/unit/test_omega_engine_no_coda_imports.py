"""Guard: omega_engine must not import the coda package (no reverse deps, no shims)."""
from __future__ import annotations

import re
from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parents[1]
_OE = _ROOT / "omega_engine"
_CODA_IMPORT = re.compile(
    r"(?:from|import)\s+anomalon\.coda(?:\.|\s|$)|(?:from|import)\s+coda(?:\.|\s|$)"
)


def _python_files():
    for path in _OE.rglob("*.py"):
        if "__pycache__" in path.parts:
            continue
        yield path


def test_omega_engine_has_no_coda_imports() -> None:
    offenders: list[str] = []
    for path in _python_files():
        text = path.read_text(encoding="utf-8", errors="ignore")
        for lineno, line in enumerate(text.splitlines(), 1):
            if "codaq" in line:
                continue
            if _CODA_IMPORT.search(line):
                rel = path.relative_to(_ROOT).as_posix()
                offenders.append(f"{rel}:{lineno}: {line.strip()}")
    assert offenders == [], "omega_engine must not import coda:\n" + "\n".join(offenders)


def test_moved_kernel_paths_absent_from_coda() -> None:
    """No shims: deleted authority losers must not remain under coda/."""
    forbidden = {
        "solver_of_solvers.py",
        "higher_simplex_assembly.py",
        "cochain_presentation.py",
        "exact.py",
        "cochain_complex.py",
        "dda_engine.py",
        "dda_cascade_router.py",
        "degree_generic_residual.py",
        "gf2_schema.py",
        "parity_carrier.py",
        "surface_carrier.py",
        "tetron_carrier.py",
        "graph_to_complex.py",
        "graph_complex.py",
        "classifier.py",
        "exact_algebraic_verifier.py",
        "harmonic.py",
        "terminalizer.py",
        "trace.py",
        "ambiguity_demo.py",
        "gallery_demo.py",
        "ising_demo.py",
        "kitaev_majorana_benchmark.py",
        "kitaev_ring_majorana_benchmark.py",
        "microsoft_majorana_braiding_benchmark.py",
        "tetron_homology_benchmark.py",
        "tgp_demo.py",
        "coda_engine.py",
        "covering_edge.py",
        "family_bound.py",
        "transfer.py",
        "cochain_adapter.py",
        "retraction_geometry.py",
        "replica_hierarchy.py",
        "replica_hierarchy_validation.py",
        "graph_coloring_cohomology.py",
        "observer_carriers.py",
        "levels_crosswalk.py",
        "projection_obstruction_engine.py",
        "residual_composition.py",
        "majorana_cohomology_bridge.py",
        "quantum_lattice.py",
        "short_time_defect_numerical_certificate.py",
        "certified_residual_integration.py",
        "wired_engine.py",
        "epk_overlay.py",
        "qm_020_dda_bridge.py",
        "cross_validate_dda_claims.py",
        "evidence.py",
        "claim_coverage.py",
        "artifact_bundle.py",
        "verify_certificate.py",
        "falsification_sandbox.py",
        "inline_code_companion.py",
        "replay.py",
        "worked_examples.py",
    }
    present = {p.name for p in (_ROOT / "coda").glob("*.py")}
    leftovers = sorted(forbidden & present)
    assert leftovers == [], f"coda still has dual-home losers (shims forbidden): {leftovers}"


def test_coda_engine_lives_only_in_quarantine() -> None:
    q = _ROOT / "coda" / "quarantine" / "coda_engine.py"
    assert q.is_file(), "quarantined coda_engine.py missing"
    assert not (_ROOT / "coda" / "coda_engine.py").exists()


