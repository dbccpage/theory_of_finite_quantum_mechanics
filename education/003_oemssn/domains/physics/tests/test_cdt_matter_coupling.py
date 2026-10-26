"""Tests of retained finite calculations and declared fixtures.
Physical recovery and removed certificate wrappers are outside this test scope.
"""

import math
import random
import subprocess
import sys
from pathlib import Path

import yaml

current_dir = Path(__file__).resolve().parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

from cdt_matter_coupling import (
    CompactLatticeGaugeField,
    CompactSu2GaugeField,
    CoupledCdtMatterEngine,
    SimplicialScalarField,
    Su2LinkVariable,
)


def test_lean4_cdt_matter_coupling_theorems():
    """Validates that Lean 4 regge_wdw_core.lean with matter coupling theorems compiles cleanly."""
    lean_file = current_dir.parent / "lean4" / "regge_wdw_core.lean"
    assert lean_file.exists(), f"Missing Lean file: {lean_file}"
    res = subprocess.run(["lean", str(lean_file)], capture_output=True, text=True)
    assert res.returncode == 0, f"Lean compilation error:\n{res.stderr}"




def test_u1_gauge_invariance_exact_cancellation():
    """Validates that local U(1) vertex gauge transformations leave Wilson action invariant to machine zero."""
    rng = random.Random(12345)
    num_v, edges, triangles, _ = CoupledCdtMatterEngine.build_cdt_sandwich_complex(L=3)

    links = {(u, v): rng.uniform(-math.pi, math.pi) for u, v in edges}
    gauge = CompactLatticeGaugeField(num_v, links, triangles, beta_gauge=2.5)

    # Test 20 random local gauge transformations
    for trial in range(20):
        alpha = {v: rng.uniform(-math.pi, math.pi) for v in range(num_v)}
        s_orig, s_trans, res, is_inv = gauge.audit_gauge_invariance(alpha)
        assert is_inv is True, f"Trial {trial} failed: res = {res}"
        assert res <= 1e-12, f"Trial {trial} residual exceeded tolerance: {res}"


def test_su2_gauge_invariance_exact_cancellation():
    """Validates that non-abelian SU(2) local gauge transformations leave Wilson action invariant."""
    rng = random.Random(54321)
    num_v, edges, triangles, _ = CoupledCdtMatterEngine.build_cdt_sandwich_complex(L=3)

    su2_gauge = CompactSu2GaugeField(num_v, triangles, beta_su2=3.0)
    for u, v in edges:
        su2_gauge.set_link(u, v, Su2LinkVariable.random(rng))

    for trial in range(10):
        g = {v: Su2LinkVariable.random(rng) for v in range(num_v)}
        s_orig, s_trans, res, is_inv = su2_gauge.audit_gauge_invariance(g)
        assert is_inv is True, f"Trial {trial} failed: res = {res}"
        assert res <= 1e-12, f"Trial {trial} residual exceeded tolerance: {res}"


def test_scalar_dirichlet_energy_positivity():
    """Validates that scalar field kinetic Dirichlet energy is non-negative and vanishes on uniform fields."""
    num_v, edges, _, _ = CoupledCdtMatterEngine.build_cdt_sandwich_complex(L=3)
    weights = {(u, v): 1.0 for u, v in edges}

    # Uniform field -> kinetic energy = 0
    uniform_vals = [3.14159] * num_v
    scalar_uniform = SimplicialScalarField(num_v, uniform_vals, edges, weights, mass_sq=1.0)
    assert abs(scalar_uniform.kinetic_energy()) < 1e-12
    assert scalar_uniform.potential_energy() > 0

    # Fluctuating field -> kinetic energy strictly > 0
    rng = random.Random(999)
    fluc_vals = [rng.gauss(0, 1) for _ in range(num_v)]
    scalar_fluc = SimplicialScalarField(num_v, fluc_vals, edges, weights, mass_sq=1.0)
    assert scalar_fluc.kinetic_energy() > 0.0
    assert scalar_fluc.total_action() > 0.0
