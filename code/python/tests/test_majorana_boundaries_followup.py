"""Follow-up checks retained separately from the initial fault-run inputs.

Claim: urn:omega:fqm:quality:majorana-preflight-followup:v1.
AuthorityEffect: None. Diagnostic resource-policy tests, not native execution.
"""
from fractions import Fraction
import io
import sys

import pytest
from sympy import Matrix, Rational, Symbol

from src.majorana.majorana_modes import (
    MajoranaError, MajoranaOperator, MajoranaMonomial, _add_coeff,
    kitaev_chain_parity, _multiply_modes, main as modes_main,
)
from src.majorana.majorana_fock_algebra import FockCarrier, GaussianRat, gi
from src.majorana.scalar import ScalarError, q
from src.majorana.native_exact_input import as_rational, exact_vector, matrix_wire
from src.majorana.test_majorana_control import CheckError, checked_int


def test_specific_refusal_diagnostics():
    for value, invariant in [(0.5, 'float refused at the Majorana boundary'), (True, 'boolean refused where an integer was required')]:
        with pytest.raises(MajoranaError) as caught:
            MajoranaOperator.mode(value)
        assert caught.value.invariant == invariant
    for value, text in [(0.5, 'float refused at the harness boundary'), (True, 'boolean refused where an integer was required')]:
        with pytest.raises(CheckError) as caught:
            checked_int(value)
        assert caught.value.invariant == text


def test_no_class_callback_at_integer_admission():
    class HostileClass:
        @property
        def __class__(self):
            raise AssertionError('class callback escaped')
    with pytest.raises(MajoranaError):
        MajoranaMonomial.single(HostileClass())


def test_parity_refuses_before_any_blade_allocation(monkeypatch):
    import src.majorana.majorana_modes as module
    def forbidden():
        raise AssertionError('allocation happened before site preflight')
    monkeypatch.setattr(module.MajoranaOperator, 'identity', forbidden)
    with pytest.raises(MajoranaError, match='parity degree budget'):
        kitaev_chain_parity(129)


def test_output_term_refusal_precedes_buffer_change(monkeypatch):
    import src.majorana.majorana_modes as module
    existing, added = MajoranaMonomial((0,)), MajoranaMonomial((1,))
    table = {existing: Fraction(1)}
    monkeypatch.setattr(module, 'MAX_OPERATOR_TERMS', 1)
    with pytest.raises(MajoranaError, match='term budget'):
        _add_coeff(table, added, Fraction(1))
    assert table == {existing: Fraction(1)}
    _add_coeff(table, existing, Fraction(-1))
    assert not table


def test_internal_product_result_degree_budget():
    # Public multiply also checks the constructed blade. This separately tests
    # the helper's result budget, using two already admissible sorted blades.
    left = MajoranaMonomial(tuple(range(256)))
    right = MajoranaMonomial.single(256)
    with pytest.raises(MajoranaError, match='degree budget'):
        _multiply_modes(left.modes, right.modes)


def test_native_exponent_refusal_before_cancelling_normalization():
    with pytest.raises(ValueError, match='exponent/work budgets'):
        as_rational('1e1025/1e1025')
    with pytest.raises(ValueError, match='exponent/work budgets'):
        as_rational('1e-1025/1e-1025')
    assert as_rational('1e1024/1e1024') == 1
    assert as_rational('1e-1024/1e-1024') == 1


def test_scalar_and_codec_text_caps_and_symbolic_refusal():
    with pytest.raises(ScalarError, match='text budget'):
        q('0'*1024 + '1')
    with pytest.raises(ValueError, match='text budget'):
        as_rational('0'*1024 + '1')
    for value in (Rational(1, 2) + Symbol('x'), Matrix([[0.5]]), Matrix([[Symbol('x')]])):
        with pytest.raises(TypeError):
            if type(value) is type(Matrix([[1]])):
                matrix_wire(value)
            else:
                as_rational(value)
    assert exact_vector(range(3), label='v') == Matrix([0, 1, 2])


def test_gaussian_and_operator_oversized_rational_refusal():
    value = Fraction(1 << 1024, 3)
    with pytest.raises(MajoranaError):
        GaussianRat(value, 0)
    with pytest.raises(MajoranaError):
        MajoranaOperator({MajoranaMonomial.identity(): value})


def test_carrier_largest_dimension_and_owned_matrices():
    carrier = FockCarrier(5)
    matrix = carrier.majorana_generator(10)
    assert len(matrix) == 32 and all(len(row) == 32 for row in matrix)
    for column in range(32):
        entries = [(row, matrix[row][column]) for row in range(32) if not matrix[row][column].is_zero()]
        assert len(entries) == 1
        row, value = entries[0]
        assert row == column ^ 1
        assert value == gi(0, (-1 if column & 1 else 1) * (-1)**format(column, '05b')[:4].count('1'))
    matrix[0][1] = gi(99)
    assert carrier.majorana_generator(10)[0][1] != gi(99)


def test_main_domain_refusal_and_failed_diagnostic_write(monkeypatch):
    import src.majorana.majorana_modes as module
    def refuse():
        raise MajoranaError('deliberate fixture refusal')
    monkeypatch.setattr(module, 'car_nilpotency_witness', refuse)
    output = io.StringIO()
    monkeypatch.setattr(sys, 'stdout', output)
    assert modes_main() == 1
    assert output.getvalue() == 'deliberate fixture refusal\n'
    output.close()
    assert modes_main() == 2
