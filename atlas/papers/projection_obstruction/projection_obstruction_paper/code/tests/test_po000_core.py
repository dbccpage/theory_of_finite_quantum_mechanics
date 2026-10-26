"""
Lev Landau Invariant & Unit Tests for projection_obstruction_paper.
Verifies exact arithmetic, observation map projections, and cochain presentations.
"""

import sys
from pathlib import Path
from fractions import Fraction
import pytest

_code_dir = Path(__file__).resolve().parents[1]
if str(_code_dir) not in sys.path:
    sys.path.insert(0, str(_code_dir))

from exactsym import Matrix, Rational

from exact import as_rational, check_2cell_coboundary_zero
from cochain_presentation import ObservationMap


def test_2cell_coboundary_zero():
    """Verify 2-cell boundary coboundary sum delta^1 theta = 0 over a 3-cycle."""
    assert check_2cell_coboundary_zero("1/3", "2/3", "-1")
    assert not check_2cell_coboundary_zero("1/3", "1/3", "1/3")


def test_as_rational_exact_types():
    """Verify as_rational accepts int, Fraction, str, Rational and rejects float."""
    assert as_rational(5) == Rational(5)
    assert as_rational(Fraction(1, 3)) == Rational(1, 3)
    assert as_rational("3/4") == Rational(3, 4)
    assert as_rational(Rational(2, 5)) == Rational(2, 5)

    with pytest.raises(TypeError, match="exact arithmetic rejects float"):
        as_rational(3.14159)


def test_observation_map_projection():
    """Verify ObservationMap applies exact linear transformation q_e : R_e -> V_e."""
    mat = Matrix([[1, 2], [3, 4]])
    obs = ObservationMap(edge_id="e_01", matrix=mat)

    res = Matrix([[2], [1]])
    projected = obs.observe(res)
    assert projected == Matrix([[4], [10]])

    bad_res = Matrix([[1], [2], [3]])
    with pytest.raises(ValueError, match="residual for 'e_01' has shape"):
        obs.observe(bad_res)
