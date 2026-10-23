"""Regression tests for the exact checker added in PR #247.

Run: python -I -X utf8 -m pytest checks/test_fsp_u1_wilson_action.py -q -p no:cacheprovider
These finite tests exercise the Python checker; they do not certify the Lean proof.
"""

import importlib.util
from fractions import Fraction as F
from pathlib import Path
import random
import subprocess
import sys
from unittest.mock import Mock

import pytest


CHECKER = Path(__file__).resolve().parent / "independent" / "fsp-u1-wilson-action.py"
ONE = (F(1), F(0))
MINUS_ONE = (F(-1), F(0))
I = (F(0), F(1))
MINUS_I = (F(0), F(-1))
PHASE = (F(3, 5), F(4, 5))


@pytest.fixture
def checker():
    # A fresh module isolates the checker's mutable counters between tests.
    spec = importlib.util.spec_from_file_location("wilson_checker", CHECKER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def field(checker):
    """A 3x3 field with one i link: exactly two plaquettes have real part zero."""
    forward = {(x, mu): ONE for x in checker.sites(2, 3) for mu in range(2)}
    forward[((0, 0), 0)] = I
    return checker.LinkField(2, 3, forward)


@pytest.fixture
def local_gauge(checker):
    g = {x: ONE for x in checker.sites(2, 3)}
    g[(0, 0)], g[(1, 0)], g[(1, 1)] = PHASE, MINUS_ONE, I
    return g


@pytest.mark.parametrize("z,w,expected", [
    (ONE, PHASE, PHASE),
    (I, I, MINUS_ONE),
    (PHASE, (F(3, 5), F(-4, 5)), ONE),
    ((F(2, 3), F(-3, 7)), (F(-5, 11), F(1, 2)), (F(-41, 462), F(122, 231))),
])
def test_complex_product_is_exact(checker, z, w, expected):
    result = checker.cmul(z, w)
    assert result == expected
    assert all(type(component) is F for component in result)


def test_conjugation_and_norm_on_nonunit_rationals(checker):
    z = (F(2, 3), F(-3, 7))
    assert checker.conj(z) == (F(2, 3), F(3, 7))
    assert checker.conj(checker.conj(z)) == z
    assert checker.norm_sq(z) == F(277, 441)
    assert checker.norm_sq((F(0), F(0))) == 0


@pytest.mark.parametrize("t,expected", [
    (F(0), ONE), (F(1), I), (F(-1), MINUS_I),
    (F(1, 2), PHASE), (F(-1, 2), (F(3, 5), F(-4, 5))),
    (F(2), (F(-3, 5), F(4, 5))),
])
def test_rational_unit_parameterization(checker, t, expected):
    assert checker.unit_from_t(t) == expected
    assert all(type(component) is F for component in checker.unit_from_t(t))


def test_large_rational_unit_preserves_exact_norm(checker):
    z = checker.unit_from_t(F(10**40 + 1, 10**40 - 1))
    assert checker.norm_sq(z) == 1
    assert z[0] < 0 < z[1]
    assert all(type(component) is F for component in z)


@pytest.mark.parametrize("index,expected", list(enumerate([ONE, MINUS_ONE, I, MINUS_I])))
def test_random_unit_cardinal_branch(checker, index, expected):
    rng = Mock(spec=random.Random)
    rng.random.return_value = F(0)
    rng.choice.side_effect = lambda choices: choices[index]
    assert checker.random_unit(rng) == expected
    rng.randint.assert_not_called()


def test_random_unit_rational_branch(checker):
    rng = Mock(spec=random.Random)
    rng.random.return_value = F(1)
    rng.randint.side_effect = [-2, 3]
    assert checker.random_unit(rng) == (F(5, 13), F(-12, 13))
    rng.choice.assert_not_called()


@pytest.mark.parametrize("d,L,expected", [
    (0, 3, [()]), (1, 1, [(0,)]),
    (2, 2, [(0, 0), (0, 1), (1, 0), (1, 1)]),
])
def test_sites_cartesian_product(checker, d, L, expected):
    assert checker.sites(d, L) == expected


@pytest.mark.parametrize("x,mu,L,step,expected", [
    ((2, 1), 0, 3, 1, (0, 1)),
    ((1, 0), 1, 3, -1, (1, 2)),
    ((1, 2), 0, 3, 7, (2, 2)),
    ((1, 2), 1, 3, -8, (1, 0)),
    ((1, 2), 1, 3, 0, (1, 2)),
    ((0, 0), 1, 1, 1, (0, 0)),
])
def test_shift_periodic_wrapping(checker, x, mu, L, step, expected):
    original = list(x)
    assert checker.shift(original, mu, L, step) == expected
    assert original == list(x)


@pytest.mark.parametrize("d,L,count", [(0, 3, 0), (1, 3, 0), (2, 1, 1), (2, 2, 4), (2, 3, 9), (3, 2, 24), (4, 2, 96)])
def test_plaquette_count_and_closure(checker, d, L, count):
    paths = checker.plaquettes(d, L)
    assert len(paths) == count
    assert all(len(p) == 5 and p[0] == p[-1] for p in paths)


def test_plaquette_orientation_and_wrapping(checker):
    assert [(2, 1), (0, 1), (0, 2), (2, 2), (2, 1)] in checker.plaquettes(2, 3)
    assert checker.plaquettes(2, 1) == [[(0, 0)] * 5]


def test_link_lookup_uses_forward_then_conjugate_reverse(checker):
    U = checker.LinkField(1, 3, {((2,), 0): PHASE})
    assert U((2,), (0,)) == PHASE
    assert U((0,), (2,)) == (F(3, 5), F(-4, 5))


def test_size_two_prefers_explicit_forward_to_reverse(checker):
    # Both directions are stored on L=2; they need not be conjugates.
    U = checker.LinkField(1, 2, {((0,), 0): I, ((1,), 0): MINUS_ONE})
    assert U((0,), (1,)) == I
    assert U((1,), (0,)) == MINUS_ONE
    reverse_only = checker.LinkField(1, 2, {((1,), 0): I})
    assert reverse_only((0,), (1,)) == MINUS_I


def test_size_one_self_link_prefers_forward(checker):
    U = checker.LinkField(1, 1, {((0,), 0): I})
    assert U((0,), (0,)) == I


@pytest.mark.parametrize("a,b", [((0, 0), (1, 1)), ((0, 0), (0, 0)), ((1, 1), (2, 1))])
def test_unavailable_link_raises_with_edge(checker, a, b):
    U = checker.LinkField(2, 3, {((0, 0), 0): I})
    with pytest.raises(KeyError) as error:
        U(a, b)
    assert error.value.args == ((a, b),)


@pytest.mark.parametrize("d,L", [(0, 3), (1, 1), (2, 2), (2, 3)])
def test_random_field_has_complete_exact_seeded_links(checker, d, L):
    U = checker.random_field(d, L, random.Random(247))
    assert (U.d, U.L) == (d, L)
    assert set(U.forward) == {(x, mu) for x in checker.sites(d, L) for mu in range(d)}
    assert all(checker.norm_sq(z) == 1 and all(type(v) is F for v in z) for z in U.forward.values())
    assert U.forward == checker.random_field(d, L, random.Random(247)).forward


def test_gauge_endpoint_inverse_and_input_preservation(checker, field, local_gauge):
    before, before_g = dict(field.forward), dict(local_gauge)
    transformed = checker.gauge(field, local_gauge)
    # (3/5 + 4i/5) * i * conjugate(-1) = 4/5 - 3i/5.
    assert transformed((0, 0), (1, 0)) == (F(4, 5), F(-3, 5))
    assert (transformed.d, transformed.L) == (2, 3)
    assert set(transformed.forward) == set(before)
    assert all(checker.norm_sq(z) == 1 for z in transformed.forward.values())
    assert field.forward == before
    assert local_gauge == before_g
    assert transformed.forward is not field.forward
    assert transformed((1, 0), (0, 0)) == (F(4, 5), F(3, 5))


def test_gauge_identity_composition_and_inverse(checker, field, local_gauge):
    identity = {x: ONE for x in local_gauge}
    inverse = {x: checker.conj(z) for x, z in local_gauge.items()}
    h = {x: I for x in local_gauge}
    gh = {x: checker.cmul(local_gauge[x], h[x]) for x in local_gauge}
    assert checker.gauge(field, identity).forward == field.forward
    assert checker.gauge(checker.gauge(field, local_gauge), inverse).forward == field.forward
    assert checker.gauge(checker.gauge(field, h), local_gauge).forward == checker.gauge(field, gh).forward


def test_gauge_requires_far_endpoint_value(checker):
    U = checker.LinkField(1, 3, {((0,), 0): I})
    with pytest.raises(KeyError) as error:
        checker.gauge(U, {(0,): ONE})
    assert error.value.args == ((1,),)


@pytest.mark.parametrize("path", [[], [(0, 0)]])
def test_holonomy_without_edges_is_identity(checker, path):
    U = Mock(side_effect=AssertionError("an empty walk must not look up links"))
    assert checker.holonomy(U, path) == ONE
    U.assert_not_called()


def test_holonomy_visits_edges_in_path_order(checker):
    U = Mock(side_effect=[I, PHASE, MINUS_ONE])
    assert checker.holonomy(U, ["a", "b", "c", "a"]) == (F(4, 5), F(-3, 5))
    assert U.call_args_list == [(("a", "b"),), (("b", "c"),), (("c", "a"),)]


def test_open_path_covariance_has_distinct_endpoint_factors(checker, field, local_gauge):
    path = [(0, 0), (1, 0), (1, 1)]
    assert checker.holonomy(field, path) == I
    assert checker.holonomy(checker.gauge(field, local_gauge), path) == PHASE


def test_closed_path_reversal_and_gauge_invariance(checker, field, local_gauge):
    path = [(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)]
    assert checker.holonomy(field, path) == I
    assert checker.holonomy(field, list(reversed(path))) == MINUS_I
    assert checker.holonomy(checker.gauge(field, local_gauge), path) == I


@pytest.mark.parametrize("beta,expected", [(F(0), F(0)), (F(1), F(2)), (F(3, 2), F(3)), (F(-1), F(-2))])
def test_wilson_action_known_nonflat_field(checker, field, beta, expected):
    result = checker.wilson(field, checker.plaquettes(2, 3), beta)
    assert result == expected
    assert type(result) is F


@pytest.mark.parametrize("beta", [F(-2), F(0), F(1), F(7, 2)])
def test_wilson_gauge_invariance_for_any_coupling(checker, field, local_gauge, beta):
    paths = checker.plaquettes(2, 3)
    assert checker.wilson(checker.gauge(field, local_gauge), paths, beta) == 2 * beta


@pytest.mark.parametrize("beta", [F(-1), F(0), F(3, 2)])
def test_empty_plaquette_family_is_exact_zero(checker, beta):
    U = Mock(side_effect=AssertionError("an empty family must not look up links"))
    result = checker.wilson(U, [], beta)
    assert result == 0 and type(result) is F
    U.assert_not_called()


def test_self_link_negative_coupling_witness_uses_wilson(checker):
    U = checker.LinkField(1, 1, {((0,), 0): MINUS_ONE})
    assert checker.wilson(U, [[(0,), (0,)]], F(-1)) == -2
    assert checker.wilson(U, [[(0,), (0,), (0,)]], F(1)) == 0


def test_repeated_plaquettes_keep_multiplicity(checker, field):
    p = [(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)]
    assert checker.wilson(field, [p, p], F(3, 2)) == 3


def test_zero_coupling_does_not_imply_flatness(checker, field):
    paths = checker.plaquettes(2, 3)
    assert any(checker.holonomy(field, p) != ONE for p in paths)
    assert checker.wilson(field, paths, F(0)) == 0


def test_pure_gauge_is_flat_at_positive_coupling(checker, local_gauge):
    flat = checker.LinkField(2, 3, {(x, mu): ONE for x in local_gauge for mu in range(2)})
    pure = checker.gauge(flat, local_gauge)
    assert any(z != ONE for z in pure.forward.values())
    assert all(checker.holonomy(pure, p) == ONE for p in checker.plaquettes(2, 3))
    assert checker.wilson(pure, checker.plaquettes(2, 3), F(5, 3)) == 0


def test_failure_accounting_counts_every_attempt(checker):
    checker.check("repeat", True)
    checker.check("repeat", False)
    checker.check("repeat", False)
    checker.check("other", True)
    assert checker.COUNTS == {"repeat": 3, "other": 1}
    assert checker.FAILURES == ["repeat", "repeat"]


@pytest.mark.parametrize("fail", [False, True])
def test_main_runs_all_parts_with_one_seed_and_reports_status(checker, monkeypatch, capsys, fail):
    calls = []
    rngs = []

    def part(rng, number):
        calls.append(number)
        rngs.append(rng)
        checker.check("zeta", not fail)
        checker.check("alpha", True)

    for number in range(1, 5):
        monkeypatch.setattr(checker, f"part{number}", lambda rng, n=number: part(rng, n))
    monkeypatch.setattr(checker, "part5", lambda: calls.append(5))

    assert checker.main() == (1 if fail else 0)
    assert calls == [1, 2, 3, 4, 5]
    assert all(rng is rngs[0] for rng in rngs)
    assert rngs[0].getstate() == random.Random(1196).getstate()
    lines = capsys.readouterr().out.splitlines()
    assert lines[:2] == ["     4  alpha", "     4  zeta"]
    assert lines[2] == f"checks=8 distinct=2 failures={4 if fail else 0}"
    if fail:
        assert lines[3:] == ["FAILED: zeta"]
    else:
        assert lines[3].startswith("OK: exact U(1) Wilson-action")


@pytest.mark.parametrize("optimized", [False, True])
def test_checker_cli_replays_exact_and_symbolic_checks(optimized):
    result = subprocess.run(
        [sys.executable, "-I", "-X", "utf8", *(["-O"] if optimized else []), str(CHECKER)],
        capture_output=True, text=True, timeout=30,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "checks=6159 distinct=21 failures=0" in result.stdout
    assert "angle form: S(A + d theta) == S(A) (SymPy exact)" in result.stdout
    assert "FAILED:" not in result.stdout
    assert result.stdout.splitlines()[-1].startswith("OK:")


def test_optimized_python_keeps_failure_exit():
    # Stub expensive sampling, inject a failed check, and exercise the real main.
    program = """
import importlib.util
import sys
spec = importlib.util.spec_from_file_location('checker', sys.argv[1])
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)
for number in range(1, 5):
    setattr(checker, f'part{number}', lambda rng: None)
checker.part5 = lambda: None
checker.check('injected regression', False)
sys.exit(checker.main())
"""
    result = subprocess.run(
        [sys.executable, "-I", "-X", "utf8", "-O", "-c", program, str(CHECKER)],
        capture_output=True, text=True, timeout=10,
    )
    assert result.returncode == 1, result.stdout + result.stderr
    assert "checks=1 distinct=1 failures=1" in result.stdout
    assert "FAILED: injected regression" in result.stdout
    assert "OK:" not in result.stdout
