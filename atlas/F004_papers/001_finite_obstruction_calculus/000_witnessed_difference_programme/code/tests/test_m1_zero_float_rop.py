"""Milestone 1 (M1) Exact-Arithmetic and ROP Monad Verification Suite.

# Executable finite evidence; AuthorityEffect: None.
# Enforces exact Gaussian rational arithmetic, strict ROP monads,
# Value Object type isolation, and native Rust dual-witness verification.
"""

from fractions import Fraction
import pytest

from witnessed_difference.outcomes import Accepted, RefusalCode, Refused
from witnessed_difference.ports import (
    DigestReceipt,
    GenesisDescentRequest,
    GenesisDescentResult,
    L1Solution,
    ObstructionSolveRequest,
    QuotientCertificate,
    QuotientVerificationReceipt,
    WdpObstructionSolution,
)
from witnessed_difference.projective import GaussianRational
from witnessed_difference.quantum import (
    PhaseBlindReadout,
    U1Connection,
    edge_phase,
    fixed_scale_phase,
    gauge_transform,
    holonomy,
    make_connection,
    to_gaussian_rational,
)
from witnessed_difference.rop import Err, Ok, Refusal, Result
from native_wdp import solve_native_genesis_descent, solve_native_obstruction


# ---------------------------------------------------------------------------
# 1. Exact Gaussian Rational Unit Phase Tests
# ---------------------------------------------------------------------------

def test_gaussian_rational_exact_arithmetic():
    """Verify Gaussian rational algebraic operations over Q(i) with zero floats."""
    z1 = GaussianRational(Fraction(3, 5), Fraction(4, 5))
    z2 = GaussianRational(Fraction(5, 13), Fraction(12, 13))

    assert z1.norm_squared() == Fraction(1, 1)
    assert z2.norm_squared() == Fraction(1, 1)

    # Product of unit Gaussian rationals is unit Gaussian rational
    prod = z1 * z2
    assert prod.norm_squared() == Fraction(1, 1)
    assert prod.real == Fraction(3, 5) * Fraction(5, 13) - Fraction(4, 5) * Fraction(12, 13)
    assert prod.imag == Fraction(3, 5) * Fraction(12, 13) + Fraction(4, 5) * Fraction(5, 13)

    # Subtraction and addition
    diff = z1 - z2
    assert diff.real == Fraction(3, 5) - Fraction(5, 13)
    assert diff.imag == Fraction(4, 5) - Fraction(12, 13)

    # Conjugate via both .conjugate() and .conj()
    conj_z1 = z1.conjugate()
    assert conj_z1 == z1.conj()
    assert conj_z1.real == Fraction(3, 5)
    assert conj_z1.imag == Fraction(-4, 5)
    assert (z1 * conj_z1).real == Fraction(1, 1)
    assert (z1 * conj_z1).imag == Fraction(0, 1)

    # Reject float initialization
    with pytest.raises(TypeError, match="must not be bool or float"):
        GaussianRational(0.6, 0.8)  # type: ignore[arg-type]


def test_gaussian_rational_rejects_cross_type_equality():
    """Equality stays inside GaussianRational so a set cannot mix ints and phases."""
    one = GaussianRational(1)
    assert one != 1
    assert one != Fraction(1)
    assert one != (1 + 0j)
    assert 1 != one
    twin = GaussianRational(Fraction(1), Fraction(0))
    assert one == twin
    assert hash(one) == hash(twin)
    assert len({one, twin}) == 1


def test_float_components_do_not_certify_a_unit_phase():
    """A decimal float and a nonzero rational norm gap cannot certify a unit phase."""
    assert to_gaussian_rational(complex(0.6, 0.8)) is None
    assert to_gaussian_rational(True) is None
    assert to_gaussian_rational(False) is None
    assert to_gaussian_rational((1,)) is None
    assert to_gaussian_rational(1j) == GaussianRational(0, 1)
    pair = to_gaussian_rational((Fraction(3, 5), Fraction(4, 5)))
    assert pair == GaussianRational(Fraction(3, 5), Fraction(4, 5))
    near = GaussianRational(1, Fraction(1, 10**9))
    refused = make_connection(("a", "b"), (("a", "b", near),))
    assert isinstance(refused, Refused)
    admitted = make_connection(
        ("a", "b"),
        (("a", "b", near),),
        tolerance=Fraction(1, 10**12),
    )
    assert isinstance(admitted, Refused)
    zero = fixed_scale_phase(0, 1)
    assert isinstance(zero, Accepted) and zero.value == GaussianRational(1, 0)
    fraction_zero = fixed_scale_phase(Fraction(0), 1)
    assert isinstance(fraction_zero, Accepted) and fraction_zero.value == GaussianRational(1, 0)
    tiny = fixed_scale_phase(Fraction(1, 10**400), 1)
    assert isinstance(tiny, Refused) and tiny.code is RefusalCode.NOT_EXACT
    negative_tiny = fixed_scale_phase(Fraction(-1, 10**400), 1)
    assert isinstance(negative_tiny, Refused) and negative_tiny.code is RefusalCode.NOT_EXACT
    huge_scale = fixed_scale_phase(0, Fraction(10**400))
    assert isinstance(huge_scale, Accepted) and huge_scale.value == GaussianRational(1, 0)
    tiny_scale = fixed_scale_phase(Fraction(0), Fraction(1, 10**400))
    assert isinstance(tiny_scale, Accepted) and tiny_scale.value == GaussianRational(1, 0)
    angle = fixed_scale_phase(1, 1)
    assert isinstance(angle, Refused) and angle.code is RefusalCode.NOT_EXACT
    with pytest.raises(TypeError):
        _ = GaussianRational(1) - complex(0.6, 0.8)
    integer_shift = GaussianRational(1) - complex(1, 0)
    assert integer_shift == GaussianRational(0)


def test_u1_connection_and_gauge_transform_exact():
    """Verify U(1) connections over exact Gaussian rationals with non-unit rejection."""
    # Pythagorean triples yield exact unit Gaussian rationals
    p1 = GaussianRational(Fraction(3, 5), Fraction(4, 5))
    p2 = GaussianRational(Fraction(0, 1), Fraction(1, 1))
    p3 = GaussianRational(Fraction(-3, 5), Fraction(4, 5))

    vertices = ("v0", "v1", "v2")
    phases = (
        ("v0", "v1", p1),
        ("v1", "v2", p2),
        ("v2", "v0", p3),
    )
    conn_res = make_connection(vertices, phases)
    assert isinstance(conn_res, Accepted)
    conn = conn_res.value
    assert isinstance(conn, U1Connection)

    # Edge phase check
    ep = edge_phase(conn, "v0", "v1")
    assert isinstance(ep, Accepted) and ep.value == p1
    ep_rev = edge_phase(conn, "v1", "v0")
    assert isinstance(ep_rev, Accepted) and ep_rev.value == p1.conjugate()

    # Holonomy on 3-cycle
    cycle = ("v0", "v1", "v2", "v0")
    h_res = holonomy(conn, cycle)
    assert isinstance(h_res, Accepted)
    h = h_res.value
    expected_h = p1 * p2 * p3
    assert h == expected_h
    assert h.norm_squared() == Fraction(1, 1)

    # Gauge transformation by exact unit phases
    gauge = {
        "v0": GaussianRational(Fraction(1, 1), Fraction(0, 1)),
        "v1": GaussianRational(Fraction(0, 1), Fraction(1, 1)),
        "v2": GaussianRational(Fraction(4, 5), Fraction(-3, 5)),
    }
    trans_res = gauge_transform(conn, gauge)
    assert isinstance(trans_res, Accepted)
    near_unit = GaussianRational(1, Fraction(1, 10**9))
    admitted = make_connection(
        ("v0", "v1"),
        (("v0", "v1", near_unit),),
        tolerance=Fraction(1, 10**12),
    )
    assert isinstance(admitted, Refused)
    transformed = trans_res.value

    # Gauge invariance of cycle holonomy
    h_transformed_res = holonomy(transformed, cycle)
    assert isinstance(h_transformed_res, Accepted)
    assert h_transformed_res.value == h

    # Non-unit phase must be refused
    non_unit = GaussianRational(Fraction(1, 2), Fraction(1, 2))
    bad_phases = (("v0", "v1", non_unit),)
    bad_res = make_connection(vertices, bad_phases)
    assert isinstance(bad_res, Refused)


def test_phase_blind_readout_exact():
    """Verify PhaseBlindReadout evaluates exact quadratic norms and relative phases over Q."""
    # (1, 1) state in Q(i)^2
    v1 = (GaussianRational(Fraction(1), Fraction(0)), GaussianRational(Fraction(1), Fraction(0)))
    # Global phase (-1, -1) has identical relative phase
    v_global = (GaussianRational(Fraction(-1), Fraction(0)), GaussianRational(Fraction(-1), Fraction(0)))
    # Non-trivial relative phase (1, -1)
    v_rel = (GaussianRational(Fraction(1), Fraction(0)), GaussianRational(Fraction(-1), Fraction(0)))

    # Exact rational readout of probabilities
    pi1 = PhaseBlindReadout.readout(v1)
    assert pi1 == (Fraction(1, 1), Fraction(1, 1))

    # Phase differentiation across fibers: global phase does not differentiate, relative phase does
    assert PhaseBlindReadout.fiber_relative_phase(v1, v_global) is False
    assert PhaseBlindReadout.fiber_relative_phase(v1, v_rel) is True


# ---------------------------------------------------------------------------
# 2. Exact Value Object Isolation & Type Strictness Tests
# ---------------------------------------------------------------------------

def test_value_object_exact_type_equality():
    """Verify Value Objects enforce exact-type equality type(self) is type(other)."""
    sol1 = L1Solution(
        phi1_value=Fraction(3, 1),
        potential={"v0": Fraction(0), "v1": Fraction(1)},
        residual={("v0", "v1"): Fraction(0)},
        dual={("v0", "v1"): Fraction(1)},
        is_exact=True,
    )
    sol2 = L1Solution(
        phi1_value=Fraction(3, 1),
        potential={"v0": Fraction(0), "v1": Fraction(1)},
        residual={("v0", "v1"): Fraction(0)},
        dual={("v0", "v1"): Fraction(1)},
        is_exact=True,
    )
    assert sol1 == sol2
    assert hash(sol1) == hash(sol2)

    # Subclass or foreign object with identical attributes must NOT equal
    class L1SolutionSubclass(L1Solution):
        pass

    sol_sub = L1SolutionSubclass(
        phi1_value=Fraction(3, 1),
        potential={"v0": Fraction(0), "v1": Fraction(1)},
        residual={("v0", "v1"): Fraction(0)},
        dual={("v0", "v1"): Fraction(1)},
        is_exact=True,
    )
    assert sol1 != sol_sub
    assert sol_sub != sol1

    # GenesisDescentResult exact-type equality
    gen1 = GenesisDescentResult(
        kind="map",
        prefix=(1,),
        certificate="Some(0)",
    )
    gen2 = GenesisDescentResult(
        kind="map",
        prefix=(1,),
        certificate="Some(0)",
    )
    assert gen1 == gen2
    assert hash(gen1) == hash(gen2)

    class GenesisSubclass(GenesisDescentResult):
        pass

    gen_sub = GenesisSubclass(kind="map", prefix=(1,), certificate="Some(0)")
    assert gen1 != gen_sub


# ---------------------------------------------------------------------------
# 3. ROP Monad Result[T, Refusal] Conformance Tests
# ---------------------------------------------------------------------------

def test_rop_monad_semantics():
    """Verify Railway-Oriented Programming Result, Ok, Err, Refusal monadic behavior."""
    ok_val: Result[int, Refusal] = Ok(42)
    assert ok_val.is_ok
    assert not ok_val.is_err
    assert ok_val.unwrap() == 42
    with pytest.raises(Exception):
        ok_val.unwrap_err()

    refusal = Refusal(
        code="WDP_ZERO_DEFECT",
        message="Exact defect zero",
        locus="test_rop_monad",
        details=(("authority_effect", "None"),),
    )
    err_val: Result[int, Refusal] = Err(refusal)
    assert not err_val.is_ok
    assert err_val.is_err
    assert err_val.unwrap_err() == refusal
    with pytest.raises(Exception):
        err_val.unwrap()

    # Ok does not index. The solution value object owns the keys.
    sol = WdpObstructionSolution(
        phi1=Fraction(5, 2),
        potential={"v0": Fraction(0), "v1": Fraction(1)},
        residual={("v0", "v1"): Fraction(1, 2)},
        dual_witness={("v0", "v1"): Fraction(1)},
        is_exact=False,
        authority_effect="None",
        backend="rust",
    )
    wrapped = Ok(sol)
    assert wrapped.value["phi1"] == Fraction(5, 2)
    assert wrapped.value["potential"] == {"v0": Fraction(0), "v1": Fraction(1)}
    assert wrapped.value["residual"] == {("v0", "v1"): Fraction(1, 2)}
    assert wrapped.value["dual"] == {("v0", "v1"): Fraction(1)}
    assert wrapped.value["is_exact"] is False


# ---------------------------------------------------------------------------
# 4. Sovereign Rust Math Delegation & Zero Duality Gap Tests
# ---------------------------------------------------------------------------

def test_solve_native_obstruction_zero_duality_gap():
    """Verify solve_native_obstruction returns Ok[WdpObstructionSolution] with zero gap."""
    vertices = ["a", "b", "c"]
    edges = [("a", "b"), ("b", "c"), ("c", "a")]
    cochain = {
        ("a", "b"): Fraction(1, 1),
        ("b", "c"): Fraction(1, 1),
        ("c", "a"): Fraction(1, 1),
    }

    res_result = solve_native_obstruction(
        vertices=vertices,
        edges=edges,
        cochain=cochain,
        require_native=True,
    )

    assert isinstance(res_result, Ok)
    sol = res_result.unwrap()
    assert isinstance(sol, WdpObstructionSolution)
    assert sol.is_exact is False
    assert sol.authority_effect == "None"

    # Zero duality gap: <h, y> == Phi_1(h)
    # The dual witness y in C_1(K; Q) satisfies d_0^T y = 0 and |y_e| <= 1
    dual = sol.dual_witness
    assert dual is not None
    assert set(dual.keys()) == set(cochain.keys())

    # Check Kirchhoff divergence-free condition at all vertices: sum_{v} y_{uv} - sum_{w} y_{wu} = 0
    divergence = {v: Fraction(0) for v in vertices}
    for (u, v), y_e in dual.items():
        divergence[u] += y_e
        divergence[v] -= y_e
    for v, div in divergence.items():
        assert div == Fraction(0), f"Vertex {v} non-zero divergence: {div}"

    # Check dual feasibility: |y_e| <= 1
    for e, y_e in dual.items():
        assert abs(y_e) <= Fraction(1), f"Dual bound violated on {e}: {y_e} > 1"

    from tests.functional_checks import verify_native
    verify_native(vertices, edges, cochain, sol)


def test_solve_native_genesis_descent_rop_result():
    """Verify solve_native_genesis_descent returns Ok[GenesisDescentResult]."""
    memory_transitions = [[0, 1], [1, 0]]
    memory_initial = 0
    transducer_transitions = [[0, 0]]
    transducer_emit = [[[0], [1]]]
    transducer_initial = 0
    prefix_words = [1]
    final_words = [[]]

    res = solve_native_genesis_descent(
        memory_transitions=memory_transitions,
        memory_initial=memory_initial,
        transducer_transitions=transducer_transitions,
        transducer_emit=transducer_emit,
        transducer_initial=transducer_initial,
        prefix_words=prefix_words,
        final_words=final_words,
        require_native=True,
    )

    assert isinstance(res, Ok)
    cert = res.unwrap()
    assert isinstance(cert, GenesisDescentResult)
    assert cert.kind == "map"
    assert cert.prefix == (1,)
    assert cert.authority_effect == "None"
