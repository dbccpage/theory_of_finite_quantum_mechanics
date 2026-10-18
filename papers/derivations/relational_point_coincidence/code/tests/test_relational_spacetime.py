"""Targeted unit tests for relational spacetime and dressing field exact rational engine."""

from fractions import Fraction

from relational_spacetime import (
    DressingFieldProjection,
    EventTuple,
    ExactRationalDualWitness,
    SpacetimeRelation,
)


def test_point_coincidence_candidate_key():
    """Verify that 4 invariant scalar fields act as a candidate key distinguishing points."""
    attributes = {"phi0", "phi1", "phi2", "phi3", "matter_density", "kretschmann"}

    # Create 3 distinct events with unique scalar field quadruplets
    t1 = EventTuple({
        "phi0": Fraction(1, 1), "phi1": Fraction(0, 1), "phi2": Fraction(0, 1), "phi3": Fraction(0, 1),
        "matter_density": Fraction(10, 1), "kretschmann": Fraction(48, 1)
    })
    t2 = EventTuple({
        "phi0": Fraction(2, 1), "phi1": Fraction(1, 1), "phi2": Fraction(0, 1), "phi3": Fraction(0, 1),
        "matter_density": Fraction(5, 1), "kretschmann": Fraction(12, 1)
    })
    t3 = EventTuple({
        "phi0": Fraction(3, 1), "phi1": Fraction(1, 1), "phi2": Fraction(1, 1), "phi3": Fraction(1, 1),
        "matter_density": Fraction(1, 1), "kretschmann": Fraction(3, 1)
    })

    rel = SpacetimeRelation(attributes, [t1, t2, t3])
    candidate_key = {"phi0", "phi1", "phi2", "phi3"}

    # Candidate key functionally determines all attributes
    assert rel.is_superkey(candidate_key) is True

    # A 3-attribute subset fails to determine the full relation if values collide
    assert rel.check_functional_dependency({"phi1", "phi2", "phi3"}, {"matter_density"}) is True

    # RPCNF compliance check
    res = rel.check_rpcnf(candidate_key, forbidden_coordinates={"t", "x", "y", "z"})
    assert res["is_rpcnf"] is True
    assert len(res["violations"]) == 0


def test_rpcnf_rejects_bare_coordinates():
    """Verify RPCNF rejects relations containing bare coordinates."""
    attributes = {"phi0", "phi1", "phi2", "phi3", "t", "x"}
    t1 = EventTuple({
        "phi0": Fraction(1), "phi1": Fraction(0), "phi2": Fraction(0), "phi3": Fraction(0),
        "t": Fraction(0), "x": Fraction(1)
    })
    rel = SpacetimeRelation(attributes, [t1])
    res = rel.check_rpcnf({"phi0", "phi1", "phi2", "phi3"}, forbidden_coordinates={"t", "x", "y", "z"})
    assert res["is_rpcnf"] is False
    assert any("Forbidden coordinate" in v for v in res["violations"])


def test_heaths_theorem_lossless_observer_join():
    """Verify Heath's Theorem: r = pi_{K union A}(r) bowtie pi_{K union B}(r) is lossless."""
    attributes = {"phi0", "phi1", "phi2", "phi3", "obs_alpha_curr", "obs_beta_temp"}
    t1 = EventTuple({
        "phi0": Fraction(1), "phi1": Fraction(0), "phi2": Fraction(0), "phi3": Fraction(0),
        "obs_alpha_curr": Fraction(100), "obs_beta_temp": Fraction(300)
    })
    t2 = EventTuple({
        "phi0": Fraction(2), "phi1": Fraction(1), "phi2": Fraction(0), "phi3": Fraction(0),
        "obs_alpha_curr": Fraction(200), "obs_beta_temp": Fraction(273)
    })
    rel = SpacetimeRelation(attributes, [t1, t2])
    key = {"phi0", "phi1", "phi2", "phi3"}

    lossless = rel.verify_heaths_theorem(key, {"obs_alpha_curr"}, {"obs_beta_temp"})
    assert lossless is True


def test_dressing_field_method_projection():
    """Verify DFM retraction idempotence and gauge invariance."""
    # Field state: (gauge_parameter theta, physical_amplitude A)
    # Gauge transformation by g in R: (theta + g, A)
    # Dressing field u(theta, A) = -theta (clock or phase dressing)
    def gauge_action(g: Fraction, state: tuple[Fraction, Fraction]) -> tuple[Fraction, Fraction]:
        theta, A = state
        return (theta + g, A)

    def dressing_field(state: tuple[Fraction, Fraction]) -> Fraction:
        theta, _ = state
        return -theta

    dfm = DressingFieldProjection(gauge_action, dressing_field)

    initial_state = (Fraction(3, 4), Fraction(42, 1))
    dressed = dfm.dress(initial_state)
    assert dressed == (Fraction(0), Fraction(42, 1))

    # Idempotence: Pi^2 = Pi
    assert dfm.verify_idempotence(initial_state) is True

    # Gauge invariance: Pi(phi^g) == Pi(phi)
    gauge_shift = Fraction(5, 7)
    assert dfm.verify_gauge_invariance(initial_state, gauge_shift) is True


def test_exact_rational_dual_witness_certification():
    """Verify exact rational dual LP witness certifying cochain obstruction Phi_1([omega]) > 0."""
    # Consider a 3-cycle complex C_1 (triangle with 3 edges, 3 vertices)
    # Vertices: 0, 1, 2
    # Edges: e0 = (0->1), e1 = (1->2), e2 = (2->0)
    # Coboundary D: C^0 -> C^1
    # D alpha = [alpha1 - alpha0, alpha2 - alpha1, alpha0 - alpha2]
    # In matrix form D (3 edges x 3 vertices):
    # row 0: [-1,  1,  0]
    # row 1: [ 0, -1,  1]
    # row 2: [ 1,  0, -1]
    D = [
        [Fraction(-1), Fraction(1), Fraction(0)],
        [Fraction(0), Fraction(-1), Fraction(1)],
        [Fraction(1), Fraction(0), Fraction(-1)],
    ]

    # Let target 1-cochain omega be uniform circulation: [1, 1, 1]
    # Notice sum of rows of D is 0. So for any D alpha, sum(D alpha) = 0.
    # But sum(omega) = 3 != 0. Thus omega is not a coboundary!
    omega = [Fraction(1), Fraction(1), Fraction(1)]

    # Dual witness w in Q^3:
    # We require D^T w = 0, ||w||_infty <= 1.
    # D^T =
    # [-1,  0,  1]
    # [ 1, -1,  0]
    # [ 0,  1, -1]
    # Choose w = [1, 1, 1].
    # Then D^T w = [-1 + 1, 1 - 1, 1 - 1] = [0, 0, 0] (divergence free!)
    # ||w||_infty = 1 <= 1.
    # Dual value <w, omega> = 1*1 + 1*1 + 1*1 = 3.
    w = [Fraction(1), Fraction(1), Fraction(1)]

    cert = ExactRationalDualWitness.verify_dual_witness(D, omega, w, claimed_quotient=Fraction(3))
    assert cert["valid"] is True
    assert cert["dual_value"] == Fraction(3)
    assert cert["is_divergence_free"] is True
    assert cert["inf_norm"] == Fraction(1)
