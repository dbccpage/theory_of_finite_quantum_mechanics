# -*- coding: utf-8 -*-
"""
test_pipeline_flow.py: Integration tests verifying end-to-end data flow through all 9 CODA layers.

AuthorityEffect: None.
"""

from __future__ import annotations

from sympy import Matrix, Rational

from coda_application.domain.entities import ProblemInstance, TerminalKind
from coda_application.domain.value_objects import LayerId
from coda_application.tests._authority import granted
from coda_application.application import evaluate_coda_pipeline


def test_end_to_end_pipeline_flow_authorized_case():
    """Verifies complete 9-layer passage resulting in TerminalKind.AUTHORIZED."""
    d0 = Matrix([[-1, 1], [1, -1]])
    d1 = Matrix.zeros(1, 2)
    defect = Matrix([Rational(0), Rational(0)])

    problem = ProblemInstance(
        problem_id="authorized_flow_instance",
        raw_data="sample_data",
        candidate_sieve=("cand_a", "cand_b"),
        coarse_profile=(0, 1),
        fine_profile=(0, 1),
        projection_map={0: 0, 1: 1},
        local_sections={"U0": (Rational(1, 2),)},
        overlaps={("U0", "U0"): True},
        d0=d0,
        d1=d1,
        defect_cochain=defect,
        fda_license_granted=False,
    )

    # Authorization is a grant from an external authority for this evidence, not a flag.
    outcome = granted(problem)

    assert outcome.terminal_kind == TerminalKind.AUTHORIZED
    assert outcome.is_authorized is True
    assert outcome.authority_token is not None
    assert outcome.authority_token.granted_externally is True
    assert outcome.residual_pair.is_exact_zero is True

    # Assert that all 9 layers executed and left an audit record
    executed_layer_ids = [rec.layer_id for rec in outcome.layer_records]
    expected_layer_ids = [
        LayerId.FOC,
        LayerId.MUR,
        LayerId.CS,
        LayerId.CS_Q,
        LayerId.Q,
        LayerId.A,
        LayerId.OR,
        LayerId.FDA,
        LayerId.GTLA,
    ]
    assert executed_layer_ids == expected_layer_ids
    assert all(rec.succeeded for rec in outcome.layer_records)


def test_end_to_end_pipeline_flow_closed_residual_anomalon():
    """Verifies 9-layer passage with non-zero coherent residual resulting in CLOSED_RESIDUAL."""
    d0 = Matrix([[-1, 1], [1, -1]])
    d1 = Matrix.zeros(1, 2)
    # Defect cochain [1, 0]^T is not in im(d0)
    defect = Matrix([Rational(1), Rational(0)])

    problem = ProblemInstance(
        problem_id="anomalon_flow_instance",
        raw_data="sample_data",
        candidate_sieve=("cand_a",),
        coarse_profile=(0, 1),
        fine_profile=(0, 1),
        projection_map={0: 0, 1: 1},
        local_sections={"U0": (Rational(1, 2),)},
        overlaps={("U0", "U0"): True},
        d0=d0,
        d1=d1,
        defect_cochain=defect,
        fda_license_granted=True,  # Even with license, non-zero defect cannot be authorized!
    )

    outcome = evaluate_coda_pipeline(problem)

    assert outcome.terminal_kind == TerminalKind.CLOSED_RESIDUAL
    assert outcome.is_closed_residual is True
    assert outcome.is_authorized is False
    assert outcome.authority_token is None
    assert outcome.residual_pair.phi1.numerator > 0
    assert outcome.residual_pair.gamma2.numerator == 0


def test_end_to_end_pipeline_flow_refused_on_empty_sieve():
    """Verifies 9-layer passage with empty candidate sieve resulting in REFUSED."""
    d0 = Matrix([[-1, 1], [1, -1]])
    d1 = Matrix.zeros(1, 2)
    defect = Matrix([Rational(0), Rational(0)])

    problem = ProblemInstance(
        problem_id="refused_flow_instance",
        raw_data="sample_data",
        candidate_sieve=(),  # Empty sieve triggers OR refusal
        coarse_profile=(0, 1),
        fine_profile=(0, 1),
        projection_map={0: 0, 1: 1},
        local_sections={"U0": (Rational(1, 2),)},
        overlaps={("U0", "U0"): True},
        d0=d0,
        d1=d1,
        defect_cochain=defect,
        fda_license_granted=True,
    )

    outcome = evaluate_coda_pipeline(problem)

    assert outcome.terminal_kind == TerminalKind.REFUSED
    assert outcome.is_refused is True
    assert outcome.is_authorized is False
    assert outcome.authority_token is None
