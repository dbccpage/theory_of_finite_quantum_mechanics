"""Unit tests for residual drop metrics (residual_drop.py).

Tests:
1. l1_float and l1_rational norm computations.
2. mass_from_magnitudes and mass_from_ids with negative magnitude refusal.
3. set_delta birth-death set difference accounting.
4. Discrete obstruction-id residual drop:
   - Partial elimination (residual remains Open).
   - Full elimination without dual witness (residual becomes Closed).
   - Full elimination with dual witness (residual becomes Exact).
   - Cost penalty on efficiency.
   - Illegal proposal handling (efficiency = -inf, legal = False).
5. Ledger active map bridge (ObstructionLedger magnitudes).
6. Gate11 exact rational coboundary scoring (score_coboundary_rational).
7. Efficiency ranking (rank_by_efficiency).
"""

from __future__ import annotations

from fractions import Fraction as Q
import math
import pytest

from omega_engine_pfp.domain import (
    AUTHORITY_EFFECT,
    REFUSAL_EXACT_WITHOUT_DUAL,
    REFUSAL_ILLEGAL_PROPOSAL,
    REFUSAL_NEGATIVE_MAGNITUDE,
    ResidualDropV1,
    l1_float,
    l1_rational,
    magnitudes_from_ledger_active,
    mass_from_ids,
    mass_from_magnitudes,
    rank_by_efficiency,
    residual_after_coboundary,
    residual_colour_from_mass,
    residual_drop_from_ids,
    residual_drop_from_ledger_maps,
    residual_drop_l1,
    residual_drop_mass,
    score_coboundary_rational,
    set_delta,
)


def test_norms_and_mass_computations() -> None:
    # l1_float
    assert l1_float([-1.5, 2.0, -0.5]) == 4.0

    # l1_rational
    rats = [Q(-3, 2), Q(2, 1), Q(-1, 2)]
    assert l1_rational(rats) == Q(4, 1)

    # mass_from_magnitudes
    mags = {"OBS-1": 1.5, "OBS-2": 2.5}
    assert mass_from_magnitudes(mags) == 4.0

    # negative magnitude raises ValueError
    with pytest.raises(ValueError, match=REFUSAL_NEGATIVE_MAGNITUDE):
        mass_from_magnitudes({"OBS-1": -1.0})

    # mass_from_ids
    ids = ["OBS-1", "OBS-2", "OBS-1"]  # duplicate
    assert mass_from_ids(ids, unit=1.0) == 2.0
    assert mass_from_ids(ids, unit=2.5) == 5.0


def test_set_delta_birth_death_accounting() -> None:
    before = ("OBS-01", "OBS-02", "OBS-03")
    after = ("OBS-02", "OBS-04")

    eliminated, opened, retained = set_delta(before, after)
    assert eliminated == ("OBS-01", "OBS-03")
    assert opened == ("OBS-04",)
    assert retained == ("OBS-02",)


def test_discrete_residual_drop_open_closed_exact() -> None:
    before = ("OBS-01", "OBS-02", "OBS-03")

    # 1. Partial elimination -> residual colour Open
    after_partial = ("OBS-03",)
    res_partial = residual_drop_from_ids(before, after_partial, cost=1.0)
    assert res_partial.omega_mass == 3.0
    assert res_partial.residual_mass == 1.0
    assert res_partial.delta == 2.0
    assert res_partial.relative_drop == pytest.approx(2.0 / 3.0)
    # efficiency = 2.0 / (1 + 1.0) = 1.0
    assert res_partial.efficiency == 1.0
    assert res_partial.residual_colour == "Open"
    assert res_partial.eliminated_ids == ("OBS-01", "OBS-02")
    assert res_partial.authority_effect == "None"

    # 2. Full elimination without dual witness -> residual colour Closed (NOT Exact)
    after_empty: tuple[str, ...] = ()
    res_closed = residual_drop_from_ids(before, after_empty, dual_witness_present=False)
    assert res_closed.residual_mass == 0.0
    assert res_closed.delta == 3.0
    assert res_closed.residual_colour == "Closed"
    assert not res_closed.dual_witness_present

    # 3. Full elimination WITH dual witness -> residual colour Exact
    res_exact = residual_drop_from_ids(before, after_empty, dual_witness_present=True)
    assert res_exact.residual_mass == 0.0
    assert res_exact.residual_colour == "Exact"
    assert res_exact.dual_witness_present


def test_illegal_proposal_handling() -> None:
    before = ("OBS-01",)
    after = ()

    res_illegal = residual_drop_from_ids(
        before,
        after,
        legal=False,
        refusal_code="MODEL_OUTPUT_IMPLIES_EXECUTION",
    )
    assert not res_illegal.legal
    assert res_illegal.delta == float("-inf")
    assert res_illegal.efficiency == float("-inf")
    assert res_illegal.refusal_code == "MODEL_OUTPUT_IMPLIES_EXECUTION"


def test_ledger_active_map_bridge() -> None:
    before_ledger = {"OBS-01": 1.5, "OBS-02": 2.5, "OBS-03": 1.0}
    after_ledger = {"OBS-03": 1.0}

    res = residual_drop_from_ledger_maps(before_ledger, after_ledger, cost=0.0)
    assert res.omega_mass == 5.0
    assert res.residual_mass == 1.0
    assert res.delta == 4.0
    assert res.efficiency == 4.0
    assert res.eliminated_ids == ("OBS-01", "OBS-02")


def test_gate11_exact_rational_coboundary_scoring() -> None:
    # Exact cover in rational 1-norm
    omega = (Q(-1, 1), Q(0, 1), Q(1, 1), Q(-1, 1))
    d_alpha = (Q(-1, 1), Q(0, 1), Q(1, 1), Q(-1, 1))

    res_exact = score_coboundary_rational(
        omega,
        d_alpha,
        cost=0.0,
        dual_witness_present=True,
    )
    assert res_exact.omega_mass == 3.0
    assert res_exact.residual_mass == 0.0
    assert res_exact.delta == 3.0
    assert res_exact.residual_colour == "Exact"

    # Partial repair
    d_alpha_partial = (Q(-1, 1), Q(0, 1), Q(0, 1), Q(0, 1))
    res_partial = score_coboundary_rational(
        omega,
        d_alpha_partial,
        cost=1.0,
        dual_witness_present=False,
    )
    assert res_partial.omega_mass == 3.0
    assert res_partial.residual_mass == 2.0
    assert res_partial.delta == 1.0
    # efficiency = 1.0 / (1 + 1.0) = 0.5
    assert res_partial.efficiency == 0.5
    assert res_partial.residual_colour == "Open"


def test_rank_by_efficiency() -> None:
    before = ("OBS-01", "OBS-02", "OBS-03")

    s1 = residual_drop_from_ids(before, ("OBS-01",), cost=0.0)  # delta=2, eff=2.0
    s2 = residual_drop_from_ids(before, (), cost=0.0, dual_witness_present=True)  # delta=3, eff=3.0
    s3 = residual_drop_from_ids(before, ("OBS-01",), cost=3.0)  # delta=2, eff=0.5
    s_illegal = residual_drop_from_ids(before, (), legal=False)

    ranked = rank_by_efficiency([s1, s3, s_illegal, s2])
    assert len(ranked) == 3
    assert ranked[0] == s2
    assert ranked[1] == s1
    assert ranked[2] == s3


def test_residual_drop_to_dict_wire_roundtrip() -> None:
    before = ("OBS-01", "OBS-02")
    after = ("OBS-02",)
    drop = residual_drop_from_ids(before, after, cost=0.5)

    wire = drop.to_dict()
    assert wire["omega_mass"] == 2.0
    assert wire["residual_mass"] == 1.0
    assert wire["delta"] == 1.0
    assert wire["eliminated_ids"] == ["OBS-01"]
    assert wire["authority_effect"] == "None"
