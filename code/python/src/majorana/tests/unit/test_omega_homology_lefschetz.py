r"""
Unit tests for omega_homology lefschetz surface integration.
"""

from omega_engine.crates.homology_theory.thimble_state import StokesData, ThimbleFlowResult
from omega_engine.crates.homology_theory.lefschetz import (
    LefschetzDiagnostic,
    LefschetzPairing,
    lefschetz_diagnostic,
    lefschetz_pair,
    lefschetz_pair_with_defect,
)


def test_lefschetz_pairing_computation():
    flow = ThimbleFlowResult(
        trajectory=[[0.0 + 0.0j]],
        conserved_im_s=0.5,
        max_im_deviation=1e-6,
        target_label=1,
        orientation_sign=1,
    )

    p0 = lefschetz_pair(flow, target_thimble_id=0)
    assert p0 == 0

    p1 = lefschetz_pair(flow, target_thimble_id=1)
    assert p1 == 1

    pair_with_def = lefschetz_pair_with_defect(flow, target_thimble_id=1)
    assert pair_with_def.pairing == 1
    assert pair_with_def.defect == 1e-6


def test_lefschetz_diagnostic_computation():
    stokes = StokesData(
        critical_values={0: 0.5 + 0.0j, 1: -0.5 + 0.0j},
        stokes_matrix={(0, 1): 1},
    )

    diag = lefschetz_diagnostic(stokes)
    assert diag.non_degenerate is True
    assert diag.pairings == {(0, 1): 1}
    assert diag.total_defect == 0.0


