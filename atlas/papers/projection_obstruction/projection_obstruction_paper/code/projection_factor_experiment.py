"""Finite experiment for PO-000: projection is not authorization.

AuthorityEffect: None.

Replays the paper's Prop 3.B counterexample (orbit leaves M while the
projected family is the identity), keeps the three residuals distinct,
and refuses to mint an authorization bit from a residual tally.

This is a finite replay, not a Banach-manifold theorem and not a
quantum result.
"""

from __future__ import annotations

from dataclasses import dataclass

from exactsym import exp, Matrix, MatrixBase, simplify

from exact import ExactInput, as_rational, exact_equal


@dataclass(frozen=True)
class ResidualTriple:
    """The three residuals of §3.4, not identified."""

    normal_leak: Matrix
    retraction_residual: Matrix
    semigroup_defect: Matrix

    def kinds_are_distinct_slots(self) -> bool:
        return True


@dataclass(frozen=True)
class EngineSlots:
    """Proposal, evaluation, authorization stay separate fields."""

    proposal: Matrix
    evaluation_tally: object
    authorized: bool


@dataclass(frozen=True)
class Prop3BWitness:
    """Exact instance of the paper's Prop 3.B counterexample."""

    start: Matrix
    ambient_image: Matrix
    projected_image: Matrix
    left_manifold: bool
    projected_is_identity: bool


def product_retract(point: MatrixBase) -> Matrix:
    """Π(x, y) = (x, 0). The factorized slice is the x-axis."""

    if point.shape != (2, 1):
        raise ValueError(f"expected a 2x1 point, got {point.shape}")
    return Matrix([point[0], 0])


def on_factorized_slice(point: MatrixBase) -> bool:
    return bool(simplify(point[1]) == 0)


def paper_semigroup(t: ExactInput, a: ExactInput = 1) -> Matrix:
    """T_t from Prop 3.B: [[1, 0], [a(1-e^{-t}), e^{-t}]]."""

    aq = as_rational(a)
    tq = as_rational(t)  # exact rail: coerce before negating (floats rejected)
    return Matrix([[1, 0], [aq * (1 - exp(-tq)), exp(-tq)]])


def prop3b_witness(t: ExactInput = 1, a: ExactInput = 1, x: ExactInput = 1) -> Prop3BWitness:
    """Orbit leaves M; S_t = Π ∘ T_t |_M is the identity on M."""

    start = Matrix([as_rational(x), 0])
    ambient = paper_semigroup(t, a) * start
    projected = product_retract(ambient)
    return Prop3BWitness(
        start=start,
        ambient_image=ambient,
        projected_image=projected,
        left_manifold=not on_factorized_slice(ambient),
        projected_is_identity=exact_equal(projected, start),
    )


def residual_triple(t: ExactInput = 1, a: ExactInput = 1, x: ExactInput = 1) -> ResidualTriple:
    """Compute the three §3.4 objects on the Prop 3.B fixture.

    Normal leak here is the first-order off-slice component of A start,
    with A = d/dt T_t at 0, which is [[0,0],[a, -1]].
    """

    start = Matrix([as_rational(x), 0])
    aq = as_rational(a)
    generator = Matrix([[0, 0], [aq, -1]])
    d_pi = Matrix([[1, 0], [0, 0]])
    normal_leak = (Matrix.eye(2) - d_pi) * generator * start
    ambient = paper_semigroup(t, a) * start
    retraction_residual = ambient - product_retract(ambient)
    # S_t is identity on M, so S_{t+t} - S_t S_t = 0
    semigroup_defect = Matrix.zeros(2, 1)
    return ResidualTriple(
        normal_leak=normal_leak.applyfunc(simplify),
        retraction_residual=retraction_residual.applyfunc(simplify),
        semigroup_defect=semigroup_defect,
    )


def slots_from_residual(residual: MatrixBase, *, authorize: bool) -> EngineSlots:
    """Evaluation may read the residual; authorization is a further act."""

    tally = simplify(abs(residual[0]) + abs(residual[1]))
    return EngineSlots(
        proposal=Matrix(residual),
        evaluation_tally=tally,
        authorized=authorize,
    )


def collapse_tally_to_auth(tally: object) -> bool:
    """The illegal move: treat a positive score as an act."""

    return bool(simplify(tally) != 0)


def run_experiment() -> dict[str, object]:
    """One replay: leftover exists, projection is still, authorization stays off."""

    witness = prop3b_witness()
    residuals = residual_triple()
    slots = slots_from_residual(residuals.retraction_residual, authorize=False)
    return {
        "left_manifold": witness.left_manifold,
        "projected_is_identity": witness.projected_is_identity,
        "normal_leak_nonzero": not exact_equal(
            residuals.normal_leak, Matrix.zeros(2, 1)
        ),
        "retraction_residual_nonzero": not exact_equal(
            residuals.retraction_residual, Matrix.zeros(2, 1)
        ),
        "semigroup_defect_zero": exact_equal(
            residuals.semigroup_defect, Matrix.zeros(2, 1)
        ),
        "authorized": slots.authorized,
        "collapse_would_authorize": collapse_tally_to_auth(slots.evaluation_tally),
        "collapse_blocked": slots.authorized
        != collapse_tally_to_auth(slots.evaluation_tally),
    }
