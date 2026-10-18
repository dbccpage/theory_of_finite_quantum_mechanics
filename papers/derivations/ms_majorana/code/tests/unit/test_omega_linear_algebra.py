import pytest
import math
from fractions import Fraction
from omega_engine.crates.linear_algebra_theory import (
    BasicMatrix,
    ComplexMatrix,
    NumericalDensityMatrix,
    DensityMatrixConfig,
    incidence_matrix,
    incidence_matrix_dmatrix,
    WeightProfile,
    ToleranceProfile,
    NormError,
)


def test_basic_matrix_operations():
    # Construct a matrix
    bm = BasicMatrix.from_row_major(2, 3, [1, 2, 3, 4, 5, 6])
    assert bm.shape() == (2, 3)
    assert bm.rows() == 2
    assert bm.cols() == 3
    assert bm.get(0, 0) == 1
    assert bm.get(1, 2) == 6

    # Test multiplication
    a = BasicMatrix.from_row_major(2, 2, [1, 2, 3, 4])
    b = BasicMatrix.from_row_major(2, 2, [5, 6, 7, 8])
    c = a.mul(b)
    assert c.as_slice() == [19, 22, 43, 50]

    # Test transpose
    a_t = a.try_transpose()
    assert a_t.as_slice() == [1, 3, 2, 4]


def test_complex_matrix_adjoint_and_trace():
    # Z = [[1+i, 2-i], [3i, -1-2i]]
    data = [complex(1, 1), complex(2, -1), complex(0, 3), complex(-1, -2)]
    m = ComplexMatrix.from_row_major(2, 2, data)
    assert m.trace() == complex(0, -1)

    adj = m.adjoint()
    # adj = [[1-i, -3i], [2+i, -1+2i]]
    assert adj.get(0, 0) == complex(1, -1)
    assert adj.get(0, 1) == complex(0, -3)
    assert adj.get(1, 0) == complex(2, 1)
    assert adj.get(1, 1) == complex(-1, 2)


def test_density_matrix_validation():
    # Construct a valid density matrix candidate
    # Rho = [[0.5, 0.1i], [-0.1i, 0.5]]
    data = [0.5, 0.1j, -0.1j, 0.5]
    config = DensityMatrixConfig.default()
    dm = NumericalDensityMatrix.from_validated(2, data, config)
    assert dm.dim() == 2
    assert math.isclose(dm.trace(), 1.0)
    assert math.isclose(dm.purity(), 0.52)
    assert dm.pure() is False

    # Test maximally mixed state
    mm = NumericalDensityMatrix.maximally_mixed(3)
    assert mm.dim() == 3
    assert math.isclose(mm.purity(), 1 / 3)


def test_incidence_matrix_construction():
    edges = [(0, 1), (1, 2)]
    bm = incidence_matrix(3, edges)
    assert bm.rows() == 2
    assert bm.cols() == 3
    # edge 0: (0, 1) -> col 0 = -1, col 1 = 1, col 2 = 0
    assert bm.get(0, 0) == -1
    assert bm.get(0, 1) == 1
    assert bm.get(0, 2) == 0

    dm = incidence_matrix_dmatrix(3, edges)
    assert dm.shape == (2, 3)
    assert dm[0, 0] == -1
    assert dm[0, 1] == 1


def test_norm_profiles():
    wp = WeightProfile.new([Fraction(1, 2), Fraction(2, 3)])
    assert wp.dim() == 2
    assert wp.weights()[0] == Fraction(1, 2)

    tp = ToleranceProfile.new(Fraction(1, 100))
    assert tp.epsilon() == Fraction(1, 100)

    with pytest.raises(NormError):
        WeightProfile.new([0, 1])

    with pytest.raises(NormError):
        ToleranceProfile.new(-0.1)


