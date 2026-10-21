"""Independent finite Clifford/Fock oracles and admission/custody challenges.

Claim: urn:omega:fqm:quality:majorana-integrity:v1. AuthorityEffect: None.
The pair-arithmetic oracle below never calls GaussianRat arithmetic. Finite
checks and Python codec checks do not certify a native deployment or theorem.
"""
from fractions import Fraction as F
from itertools import combinations, product
import io
import sys
from types import ModuleType

import pytest
from sympy import Matrix, Rational, ImmutableMatrix, SparseMatrix, ImmutableSparseMatrix

from src.majorana.majorana_modes import (
    MajoranaError, MajoranaMonomial, MajoranaOperator, kitaev_chain_parity,
    anticommutator, commutator, car_nilpotency_witness, main as modes_main,
)
from src.majorana.majorana_fock_algebra import (
    GaussianRat, FockCarrier, gi, first_anticommutation_failure,
)
from src.majorana.scalar import (
    ScalarCertificate, ScalarError, q, hash_rational, hash_rational_vec, certify_scalar,
)
from src.majorana.native_exact_input import as_rational, exact_vector, matrix_wire
from src.majorana.test_majorana_control import (
    CheckError, checked_int, _killed_one, _require_baseline,
)

ZERO, ONE, I = (F(0), F(0)), (F(1), F(0)), (F(0), F(1))


def plus(a, b):
    return a[0] + b[0], a[1] + b[1]


def times(a, b):
    return a[0]*b[0] - a[1]*b[1], a[0]*b[1] + a[1]*b[0]


def pairs(matrix):
    return tuple(tuple((x.re, x.im) for x in row) for row in matrix)


def ident(n, scalar=ONE):
    return tuple(tuple(scalar if r == c else ZERO for c in range(n)) for r in range(n))


def matmul(a, b):
    n = len(a)
    rows = []
    for r in range(n):
        row = []
        for c in range(n):
            value = ZERO
            for k in range(n):
                value = plus(value, times(a[r][k], b[k][c]))
            row.append(value)
        rows.append(tuple(row))
    return tuple(rows)


def adjoint(a):
    return tuple(tuple((a[c][r][0], -a[c][r][1]) for c in range(len(a))) for r in range(len(a)))


def matadd(a, b):
    return tuple(tuple(plus(x, y) for x, y in zip(r, s)) for r, s in zip(a, b))


def scale(a, scalar):
    return tuple(tuple(times(scalar, x) for x in row) for row in a)


def word_oracle(left, right):
    """Adjacent swaps then cancellation: separate algorithm from bisect/set code."""
    word, sign = list(left + right), 1
    while any(word[j] > word[j+1] for j in range(len(word)-1)):
        for j in range(len(word)-1):
            if word[j] > word[j+1]:
                word[j], word[j+1] = word[j+1], word[j]
                sign = -sign
    reduced = []
    for x in word:
        if reduced and reduced[-1] == x:
            reduced.pop()
        else:
            reduced.append(x)
    return F(sign), tuple(reduced)


def test_one_mode_occupation_and_gaussian_arithmetic():
    c = FockCarrier(1)
    assert pairs(c.majorana_generator(1)) == ((ZERO, ONE), (ONE, ZERO))
    assert pairs(c.majorana_generator(2)) == ((ZERO, (F(0), F(-1))), (I, ZERO))
    assert pairs(c.lowering_operator(1)) == ((ZERO, ONE), (ZERO, ZERO))
    assert pairs(c.number_operator(1)) == ((ZERO, ZERO), (ZERO, ONE))
    for a, b in product([GaussianRat(F(1, 3), F(-2, 5)), gi(0), gi(-1, 1)], repeat=2):
        assert (a+b).re == plus((a.re, a.im), (b.re, b.im))[0]
        assert ((a+b).re, (a+b).im) == plus((a.re, a.im), (b.re, b.im))
        assert ((a*b).re, (a*b).im) == times((a.re, a.im), (b.re, b.im))
        assert ((a-b).re, (a-b).im) == plus((a.re, a.im), (-b.re, -b.im))
    assert GaussianRat(F(0), F(0)).is_zero()
    assert not GaussianRat(F(0), F(1)).is_zero()


@pytest.mark.parametrize('modes', [1, 2, 3, 4])
def test_lowering_action_and_occupation(modes):
    carrier = FockCarrier(modes)
    n = 2**modes
    assert carrier.dimension() == n and carrier.modes() == modes
    for j in range(1, modes+1):
        a = pairs(carrier.lowering_operator(j))
        expected = [[ZERO for _ in range(n)] for _ in range(n)]
        mask = 2**(modes-j)
        for state in range(n):
            if state & mask:
                prefix = format(state, f'0{modes}b')[:j-1]
                expected[state-mask][state] = (F((-1)**prefix.count('1')), F(0))
        assert a == tuple(map(tuple, expected))
        assert matmul(a, a) == ident(n, ZERO)
        assert matmul(adjoint(a), a) == pairs(carrier.number_operator(j))
        assert all(a[row][0] == ZERO for row in range(n))


@pytest.mark.parametrize('modes', [1, 2, 3])
def test_car_parity_and_braids(modes):
    c = FockCarrier(modes)
    n = c.dimension()
    gs = [c.majorana_generator(a) for a in range(1, 2*modes+1)]
    assert first_anticommutation_failure(gs) is None
    cs = [pairs(c.lowering_operator(j)) for j in range(1, modes+1)]
    for j, k in product(range(modes), repeat=2):
        assert matadd(matmul(cs[j], cs[k]), matmul(cs[k], cs[j])) == ident(n, ZERO)
        assert matadd(matmul(cs[j], adjoint(cs[k])), matmul(adjoint(cs[k]), cs[j])) == ident(n, ONE if j == k else ZERO)
    gamma_word = ident(n)
    phase = ONE
    for g in gs:
        gamma_word = matmul(gamma_word, pairs(g))
    for _ in range(modes):
        phase = times(phase, (F(0), F(-1)))
    parity = pairs(c.parity_operator())
    assert scale(gamma_word, phase) == parity
    assert kitaev_chain_parity(modes).terms == {MajoranaMonomial(tuple(range(2*modes))): F(1)}
    braids = [pairs(c.braid_unitary(a)) for a in range(1, 2*modes)]
    for a in braids:
        assert matmul(adjoint(a), a) == ident(n)
        assert matmul(a, parity) == matmul(parity, a)
    for a, b in zip(braids, braids[1:]):
        assert matmul(matmul(a, b), a) == matmul(matmul(b, a), b)
    for j, k in combinations(range(len(braids)), 2):
        if k-j > 1:
            assert matmul(braids[j], braids[k]) == matmul(braids[k], braids[j])
    for even in (False, True):
        restricted = pairs(c.restrict_to_sector(c.parity_operator(), even))
        assert restricted == ident(n//2, ONE if even else (F(-1), F(0)))
    with pytest.raises(MajoranaError, match='mixes parity'):
        c.restrict_to_sector(gs[0], True)


def test_blade_word_law_and_associativity():
    labels = [s for k in range(5) for s in combinations(range(4), k)]
    blades = [MajoranaMonomial(s) for s in labels]
    for a, b in product(blades, repeat=2):
        sign, blade = a.multiply(b)
        assert (sign, blade.modes) == word_oracle(a.modes, b.modes)
    for a, b, c in product(blades, repeat=3):
        s1, ab = a.multiply(b)
        s2, lhs = ab.multiply(c)
        s3, bc = b.multiply(c)
        s4, rhs = a.multiply(bc)
        assert (s1*s2, lhs) == (s3*s4, rhs)
    a, b = MajoranaOperator.mode(0), MajoranaOperator.mode(1)
    assert anticommutator(a, b).is_zero()
    assert anticommutator(a, a).scalar_value() == 2
    assert commutator(a, b).terms == {MajoranaMonomial((0, 1)): F(2)}
    assert a.add(b).multiply(a.add(b)) == MajoranaOperator({MajoranaMonomial.identity(): F(2)})
    assert not a.is_scalar() and a.scalar_value() == 0
    assert MajoranaOperator.zero().is_scalar()
    assert car_nilpotency_witness() == 0


class IntChild(int):
    pass


class FractionChild(F):
    def __add__(self, other):
        raise AssertionError('user arithmetic callback executed')


class ContainerChild(list):
    def __iter__(self):
        raise AssertionError('user iteration callback executed')


class Pretender:
    @property
    def __class__(self):
        raise AssertionError('user class callback executed')


def test_closed_values_owned_terms_and_reinitialization():
    mon = MajoranaMonomial((2, 0))
    assert mon.modes == (0, 2)
    data = {mon: F(1, 3)}
    op = MajoranaOperator(data)
    data.clear()
    export = op.terms
    export[mon] = 0.5  # deliberately unadmitted value in detached export
    assert op.terms == {mon: F(1, 3)}
    for obj, args in [(mon, ((3,),)), (op, ({},)), (GaussianRat(F(1), F(0)), (0, 0)), (FockCarrier(1), (2,)), (certify_scalar(1), (2, '2/1'))]:
        with pytest.raises((MajoranaError, ScalarError), match='already initialized'):
            obj.__init__(*args)
        assert obj != Pretender()
        with pytest.raises(TypeError):
            type('Forbidden', (type(obj),), {})
    for value in (True, 0.5, IntChild(1), FractionChild(1, 2), Pretender()):
        with pytest.raises(ScalarError):
            q(value)
        with pytest.raises(MajoranaError):
            GaussianRat(value, 0)
        with pytest.raises((ValueError, TypeError)):
            as_rational(value)
    for value in (True, 1.0, IntChild(1), Pretender()):
        with pytest.raises(MajoranaError):
            MajoranaMonomial.single(value)
        with pytest.raises(CheckError):
            checked_int(value)
    for terms in (None, ContainerChild([]), {mon: FractionChild(1)}):
        with pytest.raises(MajoranaError):
            MajoranaOperator(terms)
    with pytest.raises(MajoranaError):
        MajoranaMonomial((1, 1))
    with pytest.raises(MajoranaError):
        MajoranaMonomial.single(-1)
    with pytest.raises(MajoranaError):
        MajoranaMonomial([1])
    with pytest.raises(MajoranaError):
        gi(F(1))
    with pytest.raises(MajoranaError):
        gi(1) + 1


def test_scalar_certificates_and_wire_grammars():
    assert q(' -6/8 ') == F(-3, 4)
    assert hash_rational(2, -4) == '-1/2'
    assert hash_rational_vec([1, F(-1, 2)]) == '1/1,-1/2'
    assert hash_rational_vec(()) == ''
    assert certify_scalar('2/4') == ScalarCertificate(F(1, 2), '1/2')
    assert hash(certify_scalar(1)) == hash(ScalarCertificate(1, '1/1'))
    for text in ('0.5', '1e3', '', '1/0', 'no'):
        with pytest.raises(ScalarError):
            q(text)
    for value, text in [(1, '2/1'), (1, '2/2'), (1, 1), (1, '1'*1025)]:
        with pytest.raises(ScalarError):
            ScalarCertificate(value, text)
    with pytest.raises(ScalarError):
        hash_rational(1, 0)
    assert as_rational('0.5') == Rational(1, 2)
    assert as_rational('1e3') == 1000
    assert as_rational('1/-2') == Rational(-1, 2)
    assert as_rational('0.1/0.2') == Rational(1, 2)
    assert as_rational('1e1000/1e1000') == 1
    for value in [Rational(0), Rational(1), Rational(-1), Rational(2), Rational(1, 2), Rational(2, 3), F(-2, 3)]:
        assert as_rational(value) == value
    for text in ('nan', 'oo', '1/0', '1/2/3', '1e1025', '1e-1025', '1'*1025):
        with pytest.raises(ValueError):
            as_rational(text)
    for constructor in [Matrix, ImmutableMatrix, SparseMatrix, ImmutableSparseMatrix]:
        source = constructor(2, 1, [Rational(1, 2), Rational(-2, 3)])
        assert matrix_wire(source) == {'rows': 2, 'cols': 1, 'data': [['1/2'], ['-2/3']]}
        assert exact_vector(source, label='v') == Matrix([Rational(1, 2), Rational(-2, 3)])
    assert matrix_wire(Matrix(0, 3, [])) == {'rows': 0, 'cols': 3, 'data': []}
    assert matrix_wire(Matrix(3, 0, [])) == {'rows': 3, 'cols': 0, 'data': [[], [], []]}
    for shape in [(0, 0), (0, 1), (1, 0)]:
        assert exact_vector(Matrix(*shape, []), label='empty').shape == (0, 1)
    original = [1, '1/2']
    vector = exact_vector(original, label='v')
    original.clear()
    assert vector == Matrix([1, Rational(1, 2)])
    source = Matrix([[1]])
    wire = matrix_wire(source)
    source[0, 0] = 2
    assert wire['data'] == [['1']]


def test_shape_and_resource_refusals(monkeypatch):
    import src.majorana.majorana_modes as modes
    import src.majorana.majorana_fock_algebra as fock
    import src.majorana.native_exact_input as native
    big = 1 << 1024
    for fn in (q, checked_int, MajoranaMonomial.single, lambda x: GaussianRat(x, 0), as_rational):
        with pytest.raises(ValueError if fn is not checked_int else CheckError):
            fn(big)
    assert q((1 << 1023)-1) == (1 << 1023)-1
    with pytest.raises(ValueError):
        as_rational(Rational(big, 3))
    with pytest.raises(ScalarError):
        hash_rational(F((1 << 1023)-1), F(1, (1 << 1023)-1))
    assert len(hash_rational_vec([0]*4096).split(',')) == 4096
    for value in ([0]*4097, ContainerChild([1])):
        with pytest.raises(ScalarError):
            hash_rational_vec(value)
    assert len(MajoranaMonomial(tuple(range(256))).modes) == 256
    with pytest.raises(MajoranaError):
        MajoranaMonomial(tuple(range(257)))
    with pytest.raises(MajoranaError):
        MajoranaMonomial(tuple(range(256))).multiply(MajoranaMonomial.single(257))
    terms = {MajoranaMonomial.single(j): F(1) for j in range(4096)}
    owned = MajoranaOperator(terms)
    assert len(owned.terms) == 4096
    with pytest.raises(MajoranaError):
        owned.add(MajoranaOperator.mode(4096))
    terms[MajoranaMonomial.single(4096)] = F(0)
    with pytest.raises(MajoranaError):
        MajoranaOperator(terms)
    with pytest.raises(MajoranaError, match='product budget'):
        owned.multiply(owned)
    a = MajoranaOperator({MajoranaMonomial((0, 1)): F(1)})
    monkeypatch.setattr(modes, 'MAX_TERM_MODE_WORK', 3)
    with pytest.raises(MajoranaError, match='mode-work'):
        a.multiply(a)
    monkeypatch.setattr(modes, 'MAX_WORK_BITS', 2)
    with pytest.raises(MajoranaError, match='bit budget'):
        MajoranaOperator({MajoranaMonomial.identity(): F(4)}).multiply(a)
    with pytest.raises(MajoranaError):
        kitaev_chain_parity(129)
    assert kitaev_chain_parity(0) == MajoranaOperator.identity()
    assert FockCarrier(5).dimension() == 32
    for count in (0, 6, True, 1.0):
        with pytest.raises(MajoranaError):
            FockCarrier(count)
    c = FockCarrier(1)
    for method, end in [(c.majorana_generator, 2), (c.number_operator, 1), (c.lowering_operator, 1), (c.braid_unitary, 1)]:
        for invalid in (0, -1, end+1, True, 1.0):
            with pytest.raises(MajoranaError):
                method(invalid)
    assert first_anticommutation_failure([]) is None
    assert first_anticommutation_failure([[], []]) is None
    assert first_anticommutation_failure([[[gi(0)]]]) == (1, 1)
    assert first_anticommutation_failure([[[gi(1)]], [[gi(1)]]]) == (1, 2)
    for value in ([[], [[gi(1)]]], [[[gi(1), gi(0)]]], [[[1]]], ContainerChild([]), [[]]*33):
        with pytest.raises(MajoranaError):
            first_anticommutation_failure(value)
    monkeypatch.setattr(fock, 'MAX_RELATION_PRODUCTS', 1)
    with pytest.raises(MajoranaError, match='CAR product budget'):
        first_anticommutation_failure([c.majorana_generator(1)])
    with pytest.raises(MajoranaError):
        c.restrict_to_sector([[gi(1)]], True)
    with pytest.raises(MajoranaError):
        c.restrict_to_sector(c.parity_operator(), 1)
    for value in (ContainerChild([1]), range(1025), range(1 << 100)):
        with pytest.raises((TypeError, ValueError)):
            exact_vector(value, label='v')
    for label in (True, 'x'*257):
        with pytest.raises((TypeError, ValueError)):
            exact_vector([], label=label)
    with pytest.raises(ValueError):
        exact_vector(Matrix([[1, 2]]), label='v')
    with pytest.raises(TypeError):
        matrix_wire([[1]])
    with pytest.raises(ValueError):
        matrix_wire(Matrix(0, 1025, []))
    monkeypatch.setattr(native, 'MAX_MATRIX_ENTRIES', 3)
    with pytest.raises(ValueError):
        matrix_wire(Matrix.eye(2))


def test_mutant_protocol_restores_modules_and_does_not_invent_kills():
    name = '_majorana_integrity_candidate'
    prior = ModuleType(name)
    sys.modules[name] = prior
    try:
        for replacement in ('x = (', 'raise ImportError("fixture")'):
            with pytest.raises(CheckError, match='not counted as a kill'):
                _killed_one('x = 1', 'invalid', 'x = 1', replacement, name, '', lambda ns: False)
            assert sys.modules[name] is prior
        assert _killed_one('x = 1', 'real', '1', '2', name, '', lambda ns: ns['x'] == 1)
        assert not _killed_one('x = 1', 'equivalent', '1', '1', name, '', lambda ns: True)
        def broken_oracle(ns):
            raise RuntimeError('oracle infrastructure failed')
        with pytest.raises(RuntimeError, match='infrastructure'):
            _killed_one('x = 1', 'oracle', '1', '2', name, '', broken_oracle)
        assert sys.modules[name] is prior
    finally:
        sys.modules.pop(name, None)
    _require_baseline('x = 1', '', 'integrity', lambda ns: ns['x'] == 1)
    assert 'baseline_integrity' not in sys.modules


def test_seal_closed_stdout(monkeypatch):
    class Closed(io.StringIO):
        def write(self, text):
            raise OSError('closed fixture')
    monkeypatch.setattr(sys, 'stdout', Closed())
    assert modes_main() == 2
