"""Edge and failure paths of the stdlib exact arithmetic engine.

Added 2026-09-03.  `exactsym.py` is the deposit's exact-arithmetic substrate:
every rational certificate, quotient distance and observer tally is computed
through it.  Its happy paths were well covered; its *refusal* paths were not,
and those are the ones that matter here.  The engine deliberately rejects
floats, negative surds, symbolic division, non-integer powers and singular
inverses rather than silently degrading to approximate arithmetic -- if any of
those guards stopped firing, an "exact" certificate could quietly become a
floating-point one.

Each test below names the guarantee it is protecting, not just the line it
happens to cover.

AuthorityEffect: None.
"""

from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path

import pytest

_CODE = str(Path(__file__).resolve().parents[1])
if _CODE not in sys.path:
    sys.path.insert(0, _CODE)

import exactsym as ex
from exactsym import Abs, Matrix, Max, Rational, Symbol, cos, exp, sin, sqrt, symbols


# ---------------------------------------------------------------------------
# the float firewall -- the engine's central promise
# ---------------------------------------------------------------------------

def test_float_is_rejected_by_matrix_and_basic_arithmetic():
    """A float entering exact arithmetic would make every downstream certificate
    approximate while still being labelled exact.  Matrix entries and Basic
    expressions both refuse it."""
    with pytest.raises(TypeError, match="rejects float"):
        Matrix([[0.5]])
    with pytest.raises(TypeError):
        sqrt(2) + 0.5
    with pytest.raises(TypeError):
        Matrix([[1]]) * 0.5
    with pytest.raises(TypeError, match="rejects float"):
        Matrix([[1]]) + Matrix([[0.5]])


def test_the_float_firewall_does_not_extend_to_bare_Rational_scalars():
    """CHARACTERISATION, not an endorsement.

    ``Rational`` is an alias for ``fractions.Fraction``, so
    ``Rational(1) + 0.5`` is resolved by ``Fraction.__add__`` and yields a
    **float** before any of this module's guards can run.  Every certificate
    surface in the deposit goes through ``Matrix`` or ``Basic``, which are
    guarded (see the test above), so this is a latent footgun at the public
    API rather than an active contamination path.

    This test pins the boundary deliberately: if ``Rational`` is ever made a
    guarded subclass, this test fails and says exactly what changed.
    """
    from fractions import Fraction
    assert ex.Rational is Fraction
    mixed = Rational(1) + 0.5
    assert isinstance(mixed, float), (
        "Rational + float no longer yields a float -- the firewall was widened; "
        "update this characterisation test and the note in the module docstring"
    )


def test_unsupported_types_are_rejected():
    with pytest.raises(TypeError):
        sqrt(2) + object()


def test_bool_and_int_coerce_cleanly():
    assert Rational(2) + True == 3
    assert Rational(2) + 3 == 5


@pytest.mark.parametrize("op", ["add", "sub", "rsub", "mul", "truediv", "eq", "ne"])
@pytest.mark.parametrize("factory", [lambda: sqrt(2), lambda: Symbol("x") + 1],
                         ids=["surd", "symbolic"])
def test_basic_binary_ops_return_notimplemented_for_foreign_types(op, factory):
    """Returning NotImplemented (rather than raising) lets Python try the
    reflected operation; swallowing it would break interop silently.

    2026-09-03: this test previously used ``Rational(3)``. ``Rational`` is
    ``fractions.Fraction``, so its ``__add__`` resolves to
    ``Fraction._operator_fallbacks`` and the test exercised the standard
    library rather than ``exactsym.Basic`` -- it passed while asserting
    nothing about the code under test. It now runs against real ``Basic``
    values, both surd and symbolic.
    """
    value = factory()
    assert isinstance(value, ex.Basic), "the test subject must be a Basic, not a Fraction"
    sentinel = object()
    method = {
        "add": value.__add__, "sub": value.__sub__, "rsub": value.__rsub__,
        "mul": value.__mul__, "truediv": value.__truediv__,
        "eq": value.__eq__, "ne": value.__ne__,
    }[op]
    assert method(sentinel) is NotImplemented


def test_rational_is_the_standard_library_fraction():
    """Guard the assumption the test above was silently relying on.

    If ``Rational`` ever stops being ``fractions.Fraction``, the reasoning in
    the surrounding tests about which class handles an operator changes, and
    this test says so directly rather than letting a dud test pass quietly.
    """
    assert ex.Rational is Fraction
    assert Rational(3).__add__(object()) is NotImplemented  # Fraction's own behaviour


# ---------------------------------------------------------------------------
# surds, powers, division
# ---------------------------------------------------------------------------

def test_sqrt_of_negative_is_refused():
    with pytest.raises(ValueError, match="negative"):
        sqrt(-4)


def test_sqrt_of_symbol_is_refused():
    with pytest.raises(TypeError, match="non-constant"):
        sqrt(Symbol("x"))


def test_negative_and_fractional_powers_are_refused_on_expressions():
    """Guarded on ``Basic``.  Bare ``Rational`` is a ``Fraction`` and follows
    Python's own semantics, which is why the guard is stated on expressions."""
    with pytest.raises(TypeError, match="nonnegative integers"):
        sqrt(2) ** -1
    with pytest.raises(TypeError, match="nonnegative integers"):
        sqrt(2) ** 0.5
    assert Rational(2) ** -1 == Fraction(1, 2)


def test_negative_surd_symbol_and_pi_powers_are_refused():
    with pytest.raises(ValueError, match="negative surd powers"):
        ex._normalize_monomial([(("surd", 2), -1)])
    with pytest.raises(ValueError, match="negative symbol powers"):
        ex._normalize_monomial([(("sym", "x"), -1)])
    with pytest.raises(ValueError, match="negative pi powers"):
        ex._normalize_monomial([(("pi",), -1)])


def test_division_by_zero_raises():
    with pytest.raises(ZeroDivisionError):
        Rational(1) / 0


def test_symbolic_division_is_refused_both_ways():
    x = Symbol("x")
    with pytest.raises(TypeError, match="symbolic value"):
        Rational(1) / x
    with pytest.raises(TypeError, match="symbolic value"):
        1 / x


def test_unary_plus_and_abs_of_negative():
    assert +Rational(3) == 3
    assert abs(Rational(-3)) == 3
    assert Abs(-3) == 3


def test_max_requires_an_argument():
    with pytest.raises(TypeError, match="at least one argument"):
        Max()
    assert Max(1, 5, 3) == 5


# ---------------------------------------------------------------------------
# symbols, differentiation, substitution
# ---------------------------------------------------------------------------

def test_symbol_name_must_be_a_nonempty_string():
    with pytest.raises(TypeError, match="nonempty strings"):
        Symbol("")
    with pytest.raises(TypeError, match="nonempty strings"):
        Symbol(None)


def test_symbols_returns_a_single_symbol_for_one_name():
    one = symbols("solo")
    assert str(one) == "solo"
    many = symbols("a b")
    assert len(many) == 2


def test_free_symbols_are_reported():
    x, y = symbols("x y")
    assert {str(s) for s in (x * y + x).free_symbols} == {"x", "y"}
    assert sqrt(2).free_symbols == set()


def test_diff_requires_a_plain_symbol():
    x = Symbol("x")
    with pytest.raises(TypeError, match="plain symbol"):
        (x * x).diff(Rational(2))
    assert (x * x).diff(x) == 2 * x


def test_subs_accepts_symbol_or_name_and_refuses_anything_else():
    x = Symbol("x")
    assert (x + 1).subs({x: 2}) == 3
    assert (x + 1).subs({"x": 2}) == 3
    with pytest.raises(TypeError, match="substitution keys"):
        (x + 1).subs({Rational(1): 2})


# ---------------------------------------------------------------------------
# ordering and sign
# ---------------------------------------------------------------------------

def test_sign_of_symbolic_expression_is_refused():
    x = Symbol("x")
    with pytest.raises(TypeError, match="free symbols"):
        bool(x < 1)


def test_ordering_on_exact_constants():
    assert Rational(1) < Rational(2)
    assert Rational(2) <= Rational(2)
    assert Rational(3) > Rational(2)
    assert Rational(2) >= Rational(2)
    assert sqrt(2) < 2
    assert sqrt(2) > 1


def test_zero_renders_and_compares():
    # a Basic that collapses to zero renders as "0"; note that Basic - Basic
    # collapses all the way to a Fraction when the result is constant, which is
    # why the zero under test is built as an explicit product.
    zero = sqrt(2) * 0
    assert str(zero) == "0"
    assert zero == 0
    assert Symbol("x") - Symbol("x") == 0


def test_hash_is_stable_for_equal_values():
    assert hash(Rational(4)) == hash(Rational(4))
    assert hash(Matrix([[1]])) == hash(Matrix([[1]]))


# ---------------------------------------------------------------------------
# transcendental helpers
# ---------------------------------------------------------------------------

def test_exp_of_zero_is_one_and_symbolic_exp_is_refused():
    assert exp(0) == 1
    with pytest.raises(TypeError, match="non-constant"):
        exp(Symbol("x"))


@pytest.mark.parametrize("k,expected_cos,expected_sin", [
    (0, 1, 0),
    (1, 0, 1),
    (2, -1, 0),
    (3, 0, -1),
])
def test_trig_at_rational_multiples_of_half_pi(k, expected_cos, expected_sin):
    angle = ex.pi * Rational(k) / 2
    assert cos(angle) == expected_cos
    assert sin(angle) == expected_sin


def test_trig_elsewhere_is_refused():
    with pytest.raises(TypeError, match="rational multiples"):
        cos(Rational(1))
    with pytest.raises(TypeError, match="rational multiples"):
        sin(Rational(1))
    with pytest.raises(TypeError, match="rational multiples"):
        cos(Symbol("x"))
    with pytest.raises(TypeError, match="rational multiples"):
        sin(Symbol("x"))


# ---------------------------------------------------------------------------
# Matrix construction and indexing
# ---------------------------------------------------------------------------

def test_matrix_constructor_rejects_bad_shapes_and_types():
    with pytest.raises(TypeError, match="dimensions must be integers"):
        Matrix("a", "b", [1])
    with pytest.raises(TypeError, match="data must be a list or tuple"):
        Matrix(1, 1, 5)
    with pytest.raises(ValueError, match="length does not match"):
        Matrix(2, 2, [1, 2, 3])
    with pytest.raises(TypeError, match="one data argument"):
        Matrix(1, 2, 3, 4)
    with pytest.raises(TypeError, match="cannot build a Matrix"):
        Matrix(5)
    with pytest.raises(ValueError, match="equal length"):
        Matrix([[1, 2], [3]])


def test_empty_matrix_is_constructible():
    empty = Matrix([])
    assert empty.shape == (0, 0)
    assert len(empty) == 0


def test_matrix_indexing_bounds_and_types():
    m = Matrix([[1, 2], [3, 4]])
    assert m[0, 1] == 2
    assert m[3] == 4
    with pytest.raises(IndexError, match="out of range"):
        m[9]
    with pytest.raises(TypeError, match="unsupported matrix index"):
        m[object()]
    with pytest.raises(TypeError, match="index component"):
        m[object(), 0]


def test_matrix_slice_indexing():
    m = Matrix([[1, 2], [3, 4]])
    assert m[0:2, 0].shape == (2, 1)


# ---------------------------------------------------------------------------
# Matrix algebra
# ---------------------------------------------------------------------------

def test_shape_mismatch_is_reported_for_add_sub_and_mul():
    a = Matrix([[1, 2]])
    b = Matrix([[1], [2]])
    with pytest.raises(ValueError, match="differ"):
        a + Matrix([[1, 2, 3]])
    with pytest.raises(ValueError, match="differ"):
        a - Matrix([[1, 2, 3]])
    with pytest.raises(ValueError):
        b * b


@pytest.mark.parametrize("op", ["add", "sub", "mul", "truediv", "eq", "ne"])
def test_matrix_binary_ops_return_notimplemented_for_foreign_types(op):
    m = Matrix([[1]])
    sentinel = object()
    method = {
        "add": m.__add__, "sub": m.__sub__, "mul": m.__mul__,
        "truediv": m.__truediv__, "eq": m.__eq__, "ne": m.__ne__,
    }[op]
    assert method(sentinel) is NotImplemented


def test_scalar_multiplication_both_sides():
    m = Matrix([[1, 2]])
    assert (m * 2) == Matrix([[2, 4]])
    assert (2 * m) == Matrix([[2, 4]])
    assert (m / 2) == Matrix([[Rational(1, 2), 1]])


def test_stacking_requires_matching_dimensions():
    assert Matrix.vstack() == Matrix.zeros(0, 0)
    with pytest.raises(ValueError, match="equal column counts"):
        Matrix.vstack(Matrix([[1]]), Matrix([[1, 2]]))
    with pytest.raises(ValueError, match="equal row counts"):
        Matrix([[1]]).row_join(Matrix([[1], [2]]))
    assert Matrix([[1]]).row_join(Matrix([[2]])).shape == (1, 2)


def test_string_forms_round_trip():
    m = Matrix([[1, 2]])
    assert str(m).startswith("Matrix([")
    assert repr(m) == str(m)


# ---------------------------------------------------------------------------
# linear algebra: rank, inverse, nullspace, solve
# ---------------------------------------------------------------------------

def test_rank_of_empty_and_singular_matrices():
    assert Matrix.zeros(0, 0).rank() == 0
    assert Matrix([[1, 2], [2, 4]]).rank() == 1
    assert Matrix([[1, 0], [0, 1]]).rank() == 2


def test_inverse_requires_square_and_nonsingular():
    with pytest.raises(ValueError, match="only square"):
        Matrix([[1, 2]]).inv()
    with pytest.raises(ValueError, match="not invertible"):
        Matrix([[1, 2], [2, 4]]).inv()
    inverse = Matrix([[2, 0], [0, 4]]).inv()
    assert inverse == Matrix([[Rational(1, 2), 0], [0, Rational(1, 4)]])


def test_nullspace_is_empty_for_full_rank_and_spans_the_kernel_otherwise():
    assert Matrix([[1, 0], [0, 1]]).nullspace() == []
    basis = Matrix([[1, 1]]).nullspace()
    assert len(basis) == 1
    assert (Matrix([[1, 1]]) * basis[0]) == Matrix([[0]])


def test_gauss_jordan_solve_shapes_and_inconsistency():
    a = Matrix([[1, 0], [0, 1]])
    with pytest.raises(ValueError, match="matching column vector"):
        a.gauss_jordan_solve(Matrix([[1, 2]]))
    solution, params = a.gauss_jordan_solve(Matrix([[3], [4]]))
    assert solution == Matrix([[3], [4]])
    # a full-rank square system has no free parameters
    assert params.shape == (0, 1)
    with pytest.raises(ValueError, match="no solution"):
        Matrix([[1], [0]]).gauss_jordan_solve(Matrix([[1], [1]]))


def test_zero_system_returns_zero_solution():
    solution, params = Matrix.zeros(1, 2).gauss_jordan_solve(Matrix([[0]]))
    assert solution == Matrix.zeros(2, 1)
    assert params == Matrix.zeros(2, 1)


def test_jacobian_requires_a_vector():
    x, y = symbols("x y")
    with pytest.raises(ValueError, match="requires a vector"):
        Matrix([[x, y], [y, x]]).jacobian([x, y])
    jac = Matrix([[x * y], [x + y]]).jacobian([x, y])
    assert jac.shape == (2, 2)


def test_rational_rows_refuses_symbolic_entries():
    x = Symbol("x")
    with pytest.raises(TypeError):
        Matrix([[x]]).rank()
