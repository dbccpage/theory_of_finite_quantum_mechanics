from fractions import Fraction

from witnessed_difference.cochains import FiniteComplex, d0, d1, finite_quotient_l1
from witnessed_difference.ground import triangle_boundary, triangle_identity
from witnessed_difference.outcomes import Accepted
from witnessed_difference.receipts import make_receipt, verify_receipt
from witnessed_difference.symmetry import exhaustive_relation_audit


def test_primitive_difference_to_cochain_to_receipt_vertical_slice() -> None:
    symmetry = exhaustive_relation_audit(3)
    assert symmetry["invariant_relation_count"] == 4
    assert triangle_identity("same", "different", "same")
    boundary = triangle_boundary("same", "different", "same")

    complex_ = FiniteComplex(("a", "b", "c"), (("a", "b"), ("b", "c"), ("a", "c")), (("a", "b", "c"),))
    potential = {"a": 0, "b": 1, "c": 0}
    cochain = d0(complex_, potential)
    assert d1(complex_, cochain) == {("a", "b", "c"): Fraction(0)}

    quotient = finite_quotient_l1(complex_, cochain, ({"a": 0, "b": 0, "c": 0}, potential))
    assert isinstance(quotient, Accepted) and quotient.value[0] == 0

    inputs = {"n": 3, "triangle_boundary": tuple(int(item) for item in boundary)}
    output = {"invariants": symmetry["invariant_relation_count"], "quotient_l1": quotient.value[0]}
    receipt = make_receipt("finite-foundation-slice", inputs, output, ("WDP-CH01-P01", "WDP-CH03-P01"))
    assert isinstance(receipt, Accepted)
    assert isinstance(verify_receipt(receipt.value, inputs, output), Accepted)
# Executable finite evidence; AuthorityEffect: None.
