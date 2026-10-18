"""Campaign C500 Block 06: Local Dynamics and Controlled Time Limits.

Evaluates conditional, imported product-formula bounds using exact rationals.
The finite fixture uses A=sigma_x, B=sigma_z. It is not a lattice or
thermodynamic-limit construction. The locality helper evaluates an outside-cone
predicate for a declared velocity; it does not certify a Lieb-Robinson estimate.
Imported bounded self-adjoint operator formulas:
   - First-order error: ||e^{-it(A+B)} - (e^{-itA/n} e^{-itB/n})^n|| <= t^2 / (2n) ||[A, B]||.
   - Second-order: |t|^3/n^2 (||[A,[A,B]]||/24 + ||[B,[B,A]]||/12).
4. Audit of C250 dense-orbit claim:
   - "Dense orbit gives continuous flow" is NARROWED: a dense subgroup of rotations
     does not specify a unique continuous 1-parameter generator. Topology,
     strong continuity and the choice of real-time extension must be declared.
5. Hypothesis pricing for continuous-time limits.

AuthorityEffect: None.
Citation: sealed-derivation-v1 (3100c4e).
"""

from __future__ import annotations

import json
from fractions import Fraction
from typing import Any, Dict


def _exact_rational(value: Fraction) -> Fraction:
    if type(value) not in (int, Fraction):
        raise ValueError("Use an integer or Fraction for an exact rational input.")
    return Fraction(value)


def trotter_first_order_error_bound(t: Fraction, n: int, comm_norm: Fraction) -> Fraction:
    """Evaluate the imported bound for bounded self-adjoint A,B and a supplied norm bound.

    ||e^{-it(A+B)} - (e^{-itA/n} e^{-itB/n})^n|| <= (t^2 / (2n)) * ||[A, B]||.
    """
    if type(n) is not int or n <= 0:
        raise ValueError("Step count n must be positive.")
    t, comm_norm = _exact_rational(t), _exact_rational(comm_norm)
    if comm_norm < 0:
        raise ValueError("A norm bound must be nonnegative.")
    return (t * t * comm_norm) / (2 * n)


def trotter_second_order_error_bound(
    t: Fraction, n: int, a_double_comm_norm: Fraction, b_double_comm_norm: Fraction
) -> Fraction:
    """Evaluate the imported bound for S_2(h)=exp(-ihA/2)exp(-ihB)exp(-ihA/2).

    A,B must be bounded self-adjoint operators. The supplied bounds are for
    ||[A,[A,B]]|| and ||[B,[B,A]]|| separately; the norm of their sum is not
    an admissible substitute. Source: Childs et al., arXiv:1912.08854, section 5.1.
    """
    if type(n) is not int or n <= 0:
        raise ValueError("Step count n must be positive.")
    t = _exact_rational(t)
    a_double_comm_norm = _exact_rational(a_double_comm_norm)
    b_double_comm_norm = _exact_rational(b_double_comm_norm)
    if a_double_comm_norm < 0 or b_double_comm_norm < 0:
        raise ValueError("Norm bounds must be nonnegative.")
    return abs(t)**3 * (a_double_comm_norm / 24 + b_double_comm_norm / 12) / (n * n)


def local_vs_global_observable_error(
    volume_l: int,
    dist_to_boundary: int,
    t: Fraction,
    v_lr: Fraction = Fraction(2, 1),
) -> Dict[str, Any]:
    """Evaluate distance > declared velocity * |t|, without certifying an LR bound.

    A Lieb-Robinson estimate needs an interaction, metric, decay/prefactor,
    observable support/norm and hypotheses uniform in volume. None is supplied.
    Outside a Lieb-Robinson cone, tails can be nonzero.
    """
    if type(volume_l) is not int or volume_l <= 0:
        raise ValueError("Volume must be a positive integer.")
    if type(dist_to_boundary) is not int or not 0 <= dist_to_boundary <= volume_l:
        raise ValueError("Boundary distance must be an integer in [0, volume].")
    t, v_lr = _exact_rational(t), _exact_rational(v_lr)
    if v_lr < 0:
        raise ValueError("The declared velocity must be nonnegative.")
    outside_declared_cone = dist_to_boundary > (v_lr * abs(t))
    return {
        "volume_l": volume_l,
        "dist_to_boundary": dist_to_boundary,
        "evolution_time": str(t),
        "lieb_robinson_velocity": str(v_lr),
        "outside_declared_cone": outside_declared_cone,
        "local_error_independent_of_volume": None,
        "locality_bound_status": "OPEN_MISSING_INTERACTION_AND_BOUND_CONSTANTS",
    }


def audit_c250_dense_orbit_claim() -> Dict[str, Any]:
    """Re-audit C250's claim: 'dense cyclic orbit implies continuous flow':

    VERDICT: NARROWED.
    A dense subgroup of a compact Lie group (e.g. powers of e^{i theta} with theta/2pi irrational)
    does NOT determine a continuous 1-parameter group without:
    1. An explicitly declared topology on the carrier.
    2. A declared continuous group homomorphism R -> G extending the Z-action.
    3. Stone's theorem strong continuity condition lim_{t->0} U(t) psi = psi.
    Sampling powers alone yields a discrete Z-action, not a continuous R-action.
    """
    return {
        "c250_claim": "dense cyclic orbit gives continuous flow",
        "status": "NARROWED",
        "audit_rationale": (
            "Even in the usual circle topology, exp(i*(theta+2*pi*k)*t) gives different "
            "continuous generators with identical integer-time samples for every integer k. "
            "A real-time extension and its topology/continuity must be declared separately."
        ),
        "dense_orbit_alone_implies_continuous_action": False,
    }


def price_continuous_generator_hypotheses() -> Dict[str, Any]:
    """Price the exact hypotheses required to obtain continuous-time dynamics from finite steps."""
    return {
        "continuous_generator_hypotheses_priced": True,
        "hypotheses": [
            {
                "hypothesis_id": "CONT-HYP-1",
                "name": "Declared Topology",
                "price": "Must choose norm or strong operator topology; discrete algebra has none.",
                "status": "DECLARED",
            },
            {
                "hypothesis_id": "CONT-HYP-2",
                "name": "Stone Strong Continuity",
                "price": "Require a one-parameter unitary group strongly continuous at t=0; continuity alone does not supply the group law.",
                "status": "DECLARED",
            },
            {
                "hypothesis_id": "CONT-HYP-3",
                "name": "Thermodynamic Quasi-Local C*-Algebra",
                "price": "Inductive limit norm completion of local algebras A_L as L -> infty.",
                "status": "DECLARED",
            },
            {
                "hypothesis_id": "CONT-HYP-4",
                "name": "Lieb-Robinson Finite Velocity",
                "price": "Specify interaction range/decay, geometry, support norms and constants uniform in volume; a termwise norm alone is insufficient.",
                "status": "OPEN",
            },
        ],
    }


def generate_canonical_block06_receipt() -> Dict[str, Any]:
    """Generate the finite Pauli bound fixture and the open locality obligations."""
    t = Fraction(1, 2)
    # For A=sigma_x, B=sigma_z, C* C=4I and both nested commutators square to 16I.
    comm_norm = Fraction(2, 1)
    a_double_comm = b_double_comm = Fraction(4, 1)

    steps = [10, 20, 50, 100, 200, 500, 1000]
    first_order_errors = []
    second_order_errors = []
    for n in steps:
        e1 = trotter_first_order_error_bound(t, n, comm_norm)
        e2 = trotter_second_order_error_bound(t, n, a_double_comm, b_double_comm)
        first_order_errors.append({"n": n, "bound": str(e1), "bound_float": float(e1)})
        second_order_errors.append({"n": n, "bound": str(e2), "bound_float": float(e2)})

    local_vs_global = [
        local_vs_global_observable_error(volume_l=10, dist_to_boundary=4, t=Fraction(1, 1)),
        local_vs_global_observable_error(volume_l=50, dist_to_boundary=4, t=Fraction(1, 1)),
        local_vs_global_observable_error(volume_l=100, dist_to_boundary=4, t=Fraction(1, 1)),
    ]

    dense_audit = audit_c250_dense_orbit_claim()
    pricing = price_continuous_generator_hypotheses()

    return {
        "authority_effect": "None",
        "citation": "sealed-derivation-v1 (3100c4e)",
        "campaign": "C500",
        "block": "block_06",
        "global_targets": "C500-T426..C500-T450",
        "terminal_outcome": "CONDITIONAL_PRODUCT_FORMULA_BOUNDS_LOCALITY_OPEN",
        "predecessor_binding_status": "NOT_VERIFIED_BY_KERNEL",
        "trotter_error_bounds": {
            "source": "https://arxiv.org/abs/1912.08854 (section 5.1; imported bounded self-adjoint operator estimates)",
            "fixture": {"A": [[0, 1], [1, 0]], "B": [[1, 0], [0, -1]]},
            "time_t": str(t),
            "commutator_norm": str(comm_norm),
            "a_double_commutator_norm": str(a_double_comm),
            "b_double_commutator_norm": str(b_double_comm),
            "first_order_series": first_order_errors,
            "second_order_series": second_order_errors,
        },
        "local_vs_global_errors": local_vs_global,
        "dense_orbit_audit": dense_audit,
        "hypothesis_pricing": pricing,
        "machine_bet_clauses": {
            "finite_product_formula_has_explicit_error_bound": True,
            "dense_orbit_alone_implies_continuous_action": False,
            "continuous_generator_hypotheses_are_priced": True,
            "c250_dense_orbit_claim_status": "NARROWED",
            "every_numerical_bound_has_a_certified_error_enclosure": False,
            "product_formula_theorem_status": "IMPORTED_BOUNDED_SELF_ADJOINT_THEOREM_WITH_FINITE_FIXTURE",
            "locality_and_thermodynamic_limit_status": "OPEN",
        },
    }


if __name__ == "__main__":
    receipt = generate_canonical_block06_receipt()
    print(json.dumps(receipt, indent=2))

__all__ = ['audit_c250_dense_orbit_claim', 'generate_canonical_block06_receipt', 'local_vs_global_observable_error', 'price_continuous_generator_hypotheses', 'trotter_first_order_error_bound', 'trotter_second_order_error_bound']
