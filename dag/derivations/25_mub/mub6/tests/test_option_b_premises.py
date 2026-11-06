"""Exact falsification of trace-frame gauge invariance suggested for Route C."""

from fractions import Fraction

from mub_verify.cyclotomic import Cyc24


def test_trace_fourth_power_changes_under_mu_basis_column_phases():
    zeta6 = Cyc24.zeta(4)
    zero = Cyc24.zero()
    six = Cyc24.rat(Fraction(6))
    raw = [[zeta6 ** (j * k) for k in range(6)] for j in range(6)]
    phases = [zeta6 ** (-k * k) for k in range(6)]
    gauged = [[raw[j][k] * phases[k] for k in range(6)] for j in range(6)]

    # Both raw matrices give unitary bases after division by sqrt(6), and
    # every entry has modulus one, so both are unbiased to the standard basis.
    for matrix in (raw, gauged):
        for j in range(6):
            for k in range(6):
                assert matrix[j][k].abs_sq() == Cyc24.one()
                inner = sum(
                    (matrix[r][j].conj() * matrix[r][k] for r in range(6)), zero
                )
                assert inner == (six if j == k else zero)

    trace = sum((raw[j][j] for j in range(6)), zero)
    gauged_trace = sum((gauged[j][j] for j in range(6)), zero)
    scale = Cyc24.rat(Fraction(1, 6))
    assert (trace.abs_sq() * scale) ** 2 == zero
    assert (gauged_trace.abs_sq() * scale) ** 2 == Cyc24.rat(Fraction(36))


def test_fourier_six_cross_ratio_is_not_a_fourth_root():
    one = Cyc24.one()
    zeta6 = Cyc24.zeta(4)
    # The top-left 2-by-2 Fourier corner is [[1, 1], [1, zeta6]].
    # Row/column rephasing cancels in this ratio. An all-fourth-root matrix
    # would have fourth-root cross ratios in every such corner.
    cross_ratio = zeta6 * one * (one * one).conj()
    assert cross_ratio ** 4 != one
