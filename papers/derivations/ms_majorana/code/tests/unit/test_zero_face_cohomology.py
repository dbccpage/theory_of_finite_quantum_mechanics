from __future__ import annotations
"""A complex with no 2-cells still has cohomology.

REVIEW P2. The design doc claimed that without `C^2` there is "no cohomology
class". That is false: with `C^2 = 0` the map `d_1` is zero, so everything is
closed and `H^1 = C^1 / im d_0`, nontrivial whenever the graph has `b_1 >= 1`.

AuthorityEffect: None.
"""


from omega_engine.crates.majorana.engines.classifier import classify

D0 = [[1, 1], [1, 1]]
D1_ZERO = [[0, 0]]


def test_zero_face_complex_still_has_cohomology() -> None:
    """`b_1 = 1` with no faces gives `dim H^1 = 1`, not 0."""
    result = classify(D0, D1_ZERO, [1, 0])
    assert result["dim_h1"] == 1, (
        "with C^2 = 0, H^1 = C^1 / im d_0; a b_1 = 1 graph has a nontrivial class"
    )


def test_zero_face_residual_is_typed_not_exact() -> None:
    """A cycle representative is closed but not exact, so it types."""
    result = classify(D0, D1_ZERO, [1, 0])
    assert result["terminal_status"] in {"TypedHarmonic", "ClosedResidual"}, result
    assert result["terminal_status"] != "Exact"
    assert result["terminal_status"] != "OpenObstruction", (
        "d_1 = 0 makes OpenObstruction genuinely unreachable -- that part was right"
    )


def test_zero_face_exact_residual_still_classifies_exact() -> None:
    """Anti-vacuity: the zero-face complex is not simply refusing everything."""
    result = classify(D0, D1_ZERO, [1, 1])
    assert result["terminal_status"] == "Exact", result



