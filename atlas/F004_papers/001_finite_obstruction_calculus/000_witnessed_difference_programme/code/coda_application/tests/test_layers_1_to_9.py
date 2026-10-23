# -*- coding: utf-8 -*-
"""
test_layers_1_to_9.py: Comprehensive unit tests for all 9 layers of the CODA stack.

AuthorityEffect: None.
"""

from __future__ import annotations

import dataclasses

import pytest
from sympy import Matrix, Rational
from witnessed_difference.native_functionals import dual_bound

from coda_application.infrastructure.native_functional_adapter import NativeFunctionalEvaluator
from coda_application.domain.entities import ProblemInstance, TerminalKind
from coda_application.domain.layers import (
    Layer1FOC,
    Layer2MUR,
    Layer3CS,
    Layer4CSQ,
    Layer5Q,
    Layer6A,
    Layer7OR,
    Layer8FDA,
    Layer9GTLA,
)
from coda_application.domain.value_objects import ExactRational, FirewallDecision, LayerId


@pytest.fixture
def base_problem() -> ProblemInstance:
    """Fixture returning a canonical baseline ProblemInstance."""
    d0 = Matrix([[-1, 1], [1, -1]])
    d1 = Matrix.zeros(1, 2)
    defect = Matrix([Rational(0), Rational(0)])

    return ProblemInstance(
        problem_id="test_base_instance",
        raw_data="base_payload",
        candidate_sieve=("cand1", "cand2"),
        coarse_profile=(0, 1),
        fine_profile=(0, 1),
        projection_map={0: 0, 1: 1},
        local_sections={"U0": (Rational(1, 2),), "U1": (Rational(1, 2),)},
        overlaps={("U0", "U1"): True},
        d0=d0,
        d1=d1,
        defect_cochain=defect,
        fda_license_granted=False,
        enclosure_interval=(Rational(0), Rational(1)),
    )


def test_layer1_foc_zero_defect_and_obstruction(base_problem):
    """Test Layer 1 FOC with both zero defect and non-trivial obstruction with dual witness."""
    # 1. Zero defect
    rec, phi1, gamma2, witness = Layer1FOC.evaluate(base_problem, evaluator=NativeFunctionalEvaluator())
    assert rec.layer_id == LayerId.FOC
    assert rec.succeeded is True
    assert phi1.numerator == 0
    assert gamma2.numerator == 0
    assert witness is None

    # 2. Obstructed cochain: [1, 0]^T not in im(d0)
    obstructed = dataclasses.replace(base_problem, defect_cochain=Matrix([Rational(1), Rational(0)]))
    rec_obs, phi1_obs, gamma2_obs, witness_obs = Layer1FOC.evaluate(obstructed, evaluator=NativeFunctionalEvaluator())
    assert rec_obs.succeeded is True
    assert phi1_obs.numerator > 0
    assert gamma2_obs.numerator == 0
    assert witness_obs is not None
    assert dual_bound([[-1, 1], [1, -1]], 2, [1, 0], [1, 1], witness_obs.fractions) == phi1_obs.fraction


def test_layer2_mur_transport_and_commutation(base_problem):
    """Test Layer 2 MUR commutation defect and overlap transport."""
    rec, loss = Layer2MUR.evaluate(base_problem, evaluator=NativeFunctionalEvaluator())
    assert rec.layer_id == LayerId.MUR
    assert rec.succeeded is True
    assert loss.numerator == 0

    # Introduce incompatible overlap
    incompatible = dataclasses.replace(base_problem, overlaps={("U0", "U1"): False})
    rec_fail, loss_fail = Layer2MUR.evaluate(incompatible, evaluator=NativeFunctionalEvaluator())
    assert rec_fail.succeeded is False
    assert loss_fail.numerator > 0


def test_layer3_cs_continuum_shadow_refinement(base_problem):
    """Check the declared finite projection between the fine and coarse label sets."""
    rec, consistent = Layer3CS.evaluate(base_problem)
    assert rec.layer_id == LayerId.CS
    assert rec.succeeded is True
    assert consistent is True

    # Inconsistent projection: fine element 0 maps outside coarse profile
    inconsistent = dataclasses.replace(base_problem, projection_map={0: 999, 1: 1})
    rec_fail, consistent_fail = Layer3CS.evaluate(inconsistent)
    assert rec_fail.succeeded is False
    assert consistent_fail is False


def test_layer4_cs_q_metric_separation_bounds(base_problem):
    """Check compatible equal vectors and one nonzero finite separation."""
    # Identical values on a declared-compatible overlap are required agreement, not a collision
    rec, sep = Layer4CSQ.evaluate(base_problem, evaluator=NativeFunctionalEvaluator())
    assert rec.layer_id == LayerId.CS_Q
    assert rec.succeeded is True

    # Perturb section U1 to introduce exact nonzero separation
    separated = dataclasses.replace(base_problem, local_sections={"U0": (Rational(1, 2),), "U1": (Rational(3, 4),)})
    rec_sep, sep_val = Layer4CSQ.evaluate(separated, evaluator=NativeFunctionalEvaluator())
    assert rec_sep.succeeded is True
    assert sep_val.sympy_rational == Rational(1, 4)


def test_layer5_q_continuum_enclosure_boundaries(base_problem):
    """Test Layer 5 Q interval enclosure and diameter tracking."""
    rec, diam = Layer5Q.evaluate(base_problem)
    assert rec.layer_id == LayerId.Q
    assert rec.succeeded is True
    assert diam.sympy_rational == Rational(1)

    # Inverted interval -> failure
    inverted = dataclasses.replace(base_problem, enclosure_interval=(Rational(2), Rational(1)))
    rec_inv, _ = Layer5Q.evaluate(inverted)
    assert rec_inv.succeeded is False


def test_layer6_a_residue_cokernel_accounting(base_problem):
    """Test Layer 6 A residue classification and anomalon retention."""
    # Zero residual
    rec_zero, has_res_zero = Layer6A.evaluate(base_problem, ExactRational(0, 1), ExactRational(0, 1))
    assert rec_zero.layer_id == LayerId.A
    assert rec_zero.succeeded is True
    assert has_res_zero is False

    # Coherent residual (Phi_1 > 0, Gamma_2 == 0)
    rec_anom, has_res_anom = Layer6A.evaluate(base_problem, ExactRational(1, 1), ExactRational(0, 1))
    assert rec_anom.succeeded is True
    assert has_res_anom is True
    assert "Anomalon" in rec_anom.diagnostic_message


def test_layer7_or_hard_refusal_sieve(base_problem):
    """Test Layer 7 OR hard refusal triggers."""
    # Baseline: no refusal
    rec, refused = Layer7OR.evaluate(base_problem, ExactRational(0, 1))
    assert rec.layer_id == LayerId.OR
    assert rec.succeeded is True
    assert refused is False

    # Trigger 1: Empty candidate sieve (OR-T5)
    empty = dataclasses.replace(base_problem, candidate_sieve=())
    rec_empty, refused_empty = Layer7OR.evaluate(empty, ExactRational(0, 1))
    assert rec_empty.succeeded is False
    assert refused_empty is True


def test_layer8_fda_authority_firewall_rules(base_problem):
    """Test Layer 8 FDA non-promotion gate and external license condition."""
    # Case 1: Zero defect, but NO license -> CLOSED_RESIDUAL (never authorized)
    rec1, dec1, token1 = Layer8FDA.evaluate(
        base_problem, ExactRational(0, 1), ExactRational(0, 1), refused_by_or=False
    )
    assert dec1 == FirewallDecision.ROUTE_CLOSED_RESIDUAL
    assert token1 is None

    # Case 2: a license flag is a claim, not a grant: Layer 8 alone never mints a token.
    # (Authorization goes through AuthorityFirewallEngine with a verified AuthorityGrant.)
    claimed = dataclasses.replace(base_problem, fda_license_granted=True)
    rec2, dec2, token2 = Layer8FDA.evaluate(
        claimed, ExactRational(0, 1), ExactRational(0, 1), refused_by_or=False
    )
    assert dec2 != FirewallDecision.PERMIT_AUTHORIZED
    assert token2 is None

    # Case 3: Upstream refusal -> ROUTE_REFUSED
    rec3, dec3, token3 = Layer8FDA.evaluate(
        base_problem, ExactRational(0, 1), ExactRational(0, 1), refused_by_or=True
    )
    assert dec3 == FirewallDecision.ROUTE_REFUSED
    assert token3 is None


def test_layer9_gtla_terminalization_and_disjointness(base_problem):
    """Test Layer 9 GTLA terminalization into pairwise disjoint branches."""
    records = []
    outcome = Layer9GTLA.terminalize(
        problem=base_problem,
        phi1=ExactRational(0, 1),
        gamma2=ExactRational(0, 1),
        dual_witness=None,
        firewall_decision=FirewallDecision.ROUTE_CLOSED_RESIDUAL,
        authority_token=None,
        layer_records=records,
    )

    assert outcome.terminal_kind == TerminalKind.CLOSED_RESIDUAL
    assert outcome.is_closed_residual is True
    assert outcome.is_authorized is False
    assert outcome.is_refused is False
    assert len(outcome.layer_records) == 1
    assert outcome.layer_records[0].layer_id == LayerId.GTLA
