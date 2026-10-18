import pytest
from omega_engine.crates.homotopy_type_theory.primitive_difference import (
    PrimitiveDifference,
    ValidatedFiniteCarrier,
    ZeroReflexivityFailure,
    ZeroSymmetryFailure,
    ZeroTransitivityFailure,
    DeltaCongruenceFailure,
    PairCongruenceFailure,
)


# 1. Collapse everything to one class. zero is always True, but delta = x.
class BoolAllZeroNonconstant(PrimitiveDifference[bool, bool]):
    def delta(self, x: bool, y: bool) -> bool:
        return x

    def zero(self, d: bool) -> bool:
        return True


def test_bool_all_zero_nonconstant_has_no_factorization():
    p = BoolAllZeroNonconstant()
    vc = ValidatedFiniteCarrier.try_new(p, [False, True])
    assert vc.num_classes() == 1
    assert not vc.delta_congruent_on_domain()
    assert not vc.delta_factors_through_quotient_on_domain()
    with pytest.raises(DeltaCongruenceFailure):
        vc.try_delta_factor()


def test_delta_congruence_counterexample_reported():
    p = BoolAllZeroNonconstant()
    vc = ValidatedFiniteCarrier.try_new(p, [False, True])
    with pytest.raises(DeltaCongruenceFailure) as exc:
        vc.validate_delta_congruence()
    assert exc.value.x == 0
    assert exc.value.x_prime == 1
    assert exc.value.y == 0
    assert exc.value.y_prime == 0


# 2. Parity difference: delta = (x - y) % 2, zero = (d == 0)
class ParityDifference(PrimitiveDifference[int, int]):
    def delta(self, x: int, y: int) -> int:
        return (x - y) % 2

    def zero(self, d: int) -> bool:
        return d == 0


def test_parity_difference_descends():
    p = ParityDifference()
    vc = ValidatedFiniteCarrier.try_new(p, [0, 1, 2, 3])
    assert vc.num_classes() == 2
    assert vc.delta_congruent_on_domain()
    factor = vc.try_delta_factor()
    c_even = vc.class_of_index(0)  # domain[0] = 0
    c_odd = vc.class_of_index(1)  # domain[1] = 1
    assert factor.apply(c_even, c_odd) == 1


def test_delta_factor_returns_same_value_for_representatives():
    p = ParityDifference()
    vc = ValidatedFiniteCarrier.try_new(p, [0, 1, 2, 3])
    factor = vc.try_delta_factor()
    assert vc.class_of_index(0) == vc.class_of_index(2)
    assert vc.class_of_index(1) == vc.class_of_index(3)
    a = factor.apply(vc.class_of_index(0), vc.class_of_index(1))
    b = factor.apply(vc.class_of_index(2), vc.class_of_index(3))
    assert a == b


def test_class_of_index_is_domain_scoped():
    p = ParityDifference()
    vc = ValidatedFiniteCarrier.try_new(p, [0, 1, 2, 3])
    assert vc.class_of_index(0) is not None
    assert vc.class_of_index(3) is not None
    assert vc.class_of_index(4) is None


def test_cross_carrier_quotient_class_rejected():
    p = ParityDifference()
    a = ValidatedFiniteCarrier.try_new(p, [0, 1, 2, 3])
    b = ValidatedFiniteCarrier.try_new(p, [0, 1, 2, 3])
    assert a.carrier_id != b.carrier_id
    fa = a.try_delta_factor()
    class_from_b = b.class_of_index(0)
    assert fa.apply(class_from_b, class_from_b) is None


# 3. Configurable integer difference with zero laws checks
class IntDiff(PrimitiveDifference[int, int]):
    def __init__(self, zero_fn) -> None:
        self.zero_fn = zero_fn

    def delta(self, x: int, y: int) -> int:
        return x - y

    def zero(self, d: int) -> bool:
        return self.zero_fn(d)


def test_zero_rel_not_reflexive_rejected():
    p = IntDiff(lambda d: False)
    with pytest.raises(ZeroReflexivityFailure) as exc:
        ValidatedFiniteCarrier.try_new(p, [0])
    assert exc.value.x == 0


def test_zero_rel_not_symmetric_rejected():
    # zero(0)=True (reflexive), zero(2)=True, zero(-2)=False
    p = IntDiff(lambda d: d == 0 or d == 2)
    with pytest.raises(ZeroSymmetryFailure) as exc:
        ValidatedFiniteCarrier.try_new(p, [0, 2])
    # x=0, y=2 -> delta(0,2)=-2 (not zero), but delta(2,0)=2 (zero) -> asymmetric
    assert exc.value.x == 1
    assert exc.value.y == 0


def test_zero_rel_not_transitive_rejected():
    # |d|<=1 is reflexive and symmetric but not transitive (0~1, 1~2, 0≁2)
    p = IntDiff(lambda d: abs(d) <= 1)
    with pytest.raises(ZeroTransitivityFailure) as exc:
        ValidatedFiniteCarrier.try_new(p, [0, 1, 2])
    assert exc.value.x == 0
    assert exc.value.y == 1
    assert exc.value.z == 2


def test_quotient_class_is_opaque_and_well_formed():
    p = ParityDifference()
    vc = ValidatedFiniteCarrier.try_new(p, [0, 1, 2, 3])
    for q in vc.residual_quotient():
        assert q.index < vc.num_classes()
        assert q.carrier_id == vc.carrier_id


def test_finite_domain_scope_not_global_claim():
    p = ParityDifference()
    two = ValidatedFiniteCarrier.try_new(p, [0, 1])
    one = ValidatedFiniteCarrier.try_new(p, [0, 2])
    assert two.num_classes() == 2
    assert one.num_classes() == 1


def test_observable_descends_iff_congruent_on_domain():
    p = ParityDifference()
    vc = ValidatedFiniteCarrier.try_new(p, [0, 1, 2, 3])
    assert vc.observable_descends_on_domain(lambda x: x % 2)
    assert not vc.observable_descends_on_domain(lambda x: x)


def test_lggr_local_green_global_red_pair_obstruction():
    p = ParityDifference()
    vc = ValidatedFiniteCarrier.try_new(p, [0, 1, 2, 3])
    lggr = vc.local_green_global_red(lambda x: x % 2, lambda x: x)
    assert lggr.left_descends
    assert not lggr.right_descends
    assert not lggr.pair_descends
    assert lggr.counterexample is not None
    with pytest.raises(PairCongruenceFailure):
        vc.validate_pair_descent_on_domain(lambda x: x % 2, lambda x: x)


def test_lggr_both_descend_pair_descends():
    p = ParityDifference()
    vc = ValidatedFiniteCarrier.try_new(p, [0, 1, 2, 3])
    lggr = vc.local_green_global_red(lambda x: x % 2, lambda x: 0)
    assert lggr.left_descends and lggr.right_descends and lggr.pair_descends
    assert lggr.counterexample is None
    assert vc.validate_pair_descent_on_domain(lambda x: x % 2, lambda x: 0) is not None


