"""Golden tests for omega_homology -- direct port of the Rust integration tests
in crates/omega_homology/src/tests/mod.rs (the faithfulness oracle).

SNF rank tests are omitted: they exercise a separate linear_algebra Smith-Normal-
Form crate, not omega_homology itself. Rank is instead verified via the
H^1 / rank_d0 / rank_d1 assertions below, which use exact Fraction Gaussian
elimination.
"""

import pytest

from omega_engine.crates.homology_theory import (
    Carrier,
    CarrierManifest,
    Chain,
    ChainComplex,
    CertifiedChainMap,
    CochainComplex,
    CoboundaryLawViolation,
    DimensionMismatch,
    NonPositiveWeight,
    NotCycle,
    OrientedSimplex,
    SimplicialComplex,
    TheoremProvenance,
    TriangleMissingEdge,
    BasisId,
    Degree,
    QMatrix,
    graph_carrier,
    hash_weights,
    q,
    try_cycle,
)
from omega_engine.crates.homology_theory.finite_directed_graph import (
    DirectedGraphBuilder,
    TheoremProvenance as GraphProv,
)


def prov():
    return TheoremProvenance.new("test")


def unit_weights(n):
    return [q(1)] * n


def make_graph(num_nodes, edges):
    return DirectedGraphBuilder.from_anonymous(num_nodes, edges, GraphProv("test"))


def test_zero_complex_works():
    d0 = QMatrix.zero(0, 0)
    d1 = QMatrix.zero(0, 0)
    Carrier.new(0, 0, 0, d0, d1, [], prov())  # must not raise


def test_single_edge_tree_homology():
    g = make_graph(2, [(0, 1)])
    c = graph_carrier(g, [], unit_weights(1), prov())
    assert c.rank_d0() == 1
    assert c.dim_q1() == 0
    assert c.dim_h1() == 0


def test_triangle_with_filling_h1_zero():
    g = make_graph(3, [(0, 1), (1, 2), (0, 2)])
    c = graph_carrier(g, [(0, 1, 2)], unit_weights(3), prov())
    assert c.dim_h1() == 0


def test_triangle_without_filling_h1_one():
    g = make_graph(3, [(0, 1), (1, 2), (0, 2)])
    c = graph_carrier(g, [], unit_weights(3), prov())
    assert c.dim_h1() == 1


def test_bad_coboundary_relation_rejected():
    d0 = QMatrix.from_row_major(2, 2, [q(1), q(0), q(0), q(1)])
    d1 = QMatrix.from_row_major(1, 2, [q(1), q(1)])
    with pytest.raises(CoboundaryLawViolation):
        CochainComplex.new(2, 2, 1, d0, d1, prov())


def test_dimension_mismatch_rejected():
    d0 = QMatrix.zero(1, 1)
    d1 = QMatrix.zero(1, 2)
    with pytest.raises(DimensionMismatch):
        CochainComplex.new(2, 2, 1, d0, d1, prov())


def test_non_positive_weights_rejected():
    d0 = QMatrix.from_row_major(1, 2, [q(-1), q(1)])
    d1 = QMatrix.zero(0, 1)
    with pytest.raises(NonPositiveWeight):
        Carrier.new(2, 1, 0, d0, d1, [q(0)], prov())


def test_triangle_missing_edge_rejected():
    g = make_graph(3, [(0, 1), (1, 2)])
    with pytest.raises(TriangleMissingEdge):
        graph_carrier(g, [(0, 1, 2)], unit_weights(2), prov())


def test_carrier_manifest_deterministic():
    g = make_graph(3, [(0, 1), (1, 2), (0, 2)])
    c = graph_carrier(g, [], unit_weights(3), prov())
    m1 = CarrierManifest.from_carrier(c)
    m2 = CarrierManifest.from_carrier(c)
    assert m1.carrier_hash == m2.carrier_hash


def test_different_carriers_different_hashes():
    c1 = graph_carrier(
        make_graph(3, [(0, 1), (1, 2), (0, 2)]), [], unit_weights(3), prov()
    )
    c2 = graph_carrier(make_graph(3, [(0, 1), (1, 2)]), [], unit_weights(2), prov())
    m1 = CarrierManifest.from_carrier(c1)
    m2 = CarrierManifest.from_carrier(c2)
    assert m1.carrier_hash != m2.carrier_hash


def test_cycle_checker_accepts_zero_chain():
    d1 = QMatrix.from_row_major(2, 3, [q(1), q(-1), q(0), q(0), q(1), q(-1)])
    d2 = QMatrix.zero(3, 0)
    complex_ = ChainComplex.new(2, 3, 0, d1, d2)
    chain = Chain.zero(Degree.new(1), BasisId.new("test"), 3)
    try_cycle(chain, complex_.boundary_1, complex_.complex_hash())  # ok


def test_cycle_checker_rejects_non_cycle():
    d1 = QMatrix.from_row_major(2, 3, [q(1), q(-1), q(0), q(0), q(1), q(-1)])
    d2 = QMatrix.zero(3, 0)
    complex_ = ChainComplex.new(2, 3, 0, d1, d2)
    chain = Chain.new(Degree.new(1), BasisId.new("test"), [q(1), q(0), q(0)])
    with pytest.raises(NotCycle):
        try_cycle(chain, complex_.boundary_1, complex_.complex_hash())


def test_simplicial_triangle_face_closure():
    triangle = OrientedSimplex.new([0, 1, 2])
    complex_ = SimplicialComplex.from_maximal_simplices([triangle])
    assert complex_.count(0) == 3
    assert complex_.count(1) == 3
    assert complex_.count(2) == 1
    assert complex_.euler_characteristic() == 1


def test_manifest_records_weights_hash():
    """The manifest is v2 (BLAKE3, framed binary), so it records the v2 weights
    digest -- not the legacy SHA-256 ``hash_weights``, which is still used by
    ``chain_complex`` and is deliberately a different encoding."""
    from omega_engine.crates.homology_theory.hashing import hash_weights_v2

    g = make_graph(3, [(0, 1), (1, 2)])
    c = graph_carrier(g, [], unit_weights(2), prov())
    m = CarrierManifest.from_carrier(c)

    pairs = [(w.numerator, w.denominator) for w in c.weights()]
    assert m.weights_hash == hash_weights_v2(pairs)
    assert m.weights_hash != hash_weights(c.weights()), (
        "v2 must not coincide with the legacy SHA-256 encoding, or the schema "
        "change is not actually in effect"
    )


def test_manifest_records_provenance_hash():
    g = make_graph(2, [(0, 1)])
    c = graph_carrier(g, [], unit_weights(1), prov())
    m = CarrierManifest.from_carrier(c)
    assert not m.provenance_hash.is_zero


def test_triangle_subdivision_preserves_homology():
    d1_c = QMatrix.from_row_major(
        3, 3, [q(-1), q(0), q(1), q(1), q(-1), q(0), q(0), q(1), q(-1)]
    )
    d2_c = QMatrix.zero(3, 0)
    c = ChainComplex.new(3, 3, 0, d1_c, d2_c)

    d1_d = QMatrix.from_row_major(
        4,
        4,
        [
            q(-1),
            q(0),
            q(1),
            q(0),
            q(0),
            q(-1),
            q(0),
            q(1),
            q(0),
            q(1),
            q(-1),
            q(0),
            q(1),
            q(0),
            q(0),
            q(-1),
        ],
    )
    d2_d = QMatrix.zero(4, 0)
    d = ChainComplex.new(4, 4, 0, d1_d, d2_d)

    phi_0 = QMatrix.from_row_major(
        4, 3, [q(1), q(0), q(0), q(0), q(1), q(0), q(0), q(0), q(1), q(0), q(0), q(0)]
    )
    phi_1 = QMatrix.from_row_major(
        4, 3, [q(1), q(0), q(0), q(0), q(1), q(0), q(0), q(0), q(1), q(1), q(0), q(0)]
    )
    phi_2 = QMatrix.zero(0, 0)

    chain_map = CertifiedChainMap.new_checked([phi_0, phi_1, phi_2], c, d)

    z = QMatrix.from_row_major(3, 1, [q(1), q(1), q(1)])
    assert c.boundary_1.matrix.matmul(z).is_zero()  # z is a cycle in C

    phi_z = chain_map.maps()[1].matmul(z)
    assert phi_z.as_flat() == [q(1), q(1), q(1), q(1)]
    assert d.boundary_1.matrix.matmul(phi_z).is_zero()  # image is a cycle in D


# --- PO-D1 discharge: d1 . d0 = 0 per carrier (construction is the proof) ---


def test_pod1_filled_triangle():
    g = make_graph(3, [(0, 1), (1, 2), (0, 2)])
    c = graph_carrier(g, [(0, 1, 2)], unit_weights(3), prov())
    assert (c.c0_dim(), c.c1_dim(), c.c2_dim()) == (3, 3, 1)
    assert c.dim_h1() == 0
    assert c.rank_d0() == 2
    assert c.rank_d1() == 1


def test_pod1_square_graph():
    g = make_graph(4, [(0, 1), (1, 2), (2, 3), (0, 3)])
    c = graph_carrier(g, [], unit_weights(4), prov())
    assert (c.c0_dim(), c.c1_dim(), c.c2_dim()) == (4, 4, 0)
    assert c.dim_h1() == 1
    assert c.rank_d0() == 3


def test_pod1_k4_graph():
    g = make_graph(4, [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)])
    c = graph_carrier(
        g, [(0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)], unit_weights(6), prov()
    )
    assert (c.c0_dim(), c.c1_dim(), c.c2_dim()) == (4, 6, 4)
    assert c.dim_h1() == 0
    assert c.rank_d0() == 3


def test_pod1_linear_path_3_nodes():
    g = make_graph(3, [(0, 1), (1, 2)])
    c = graph_carrier(g, [], unit_weights(2), prov())
    assert (c.c0_dim(), c.c1_dim(), c.c2_dim()) == (3, 2, 0)
    assert c.dim_h1() == 0
    assert c.rank_d0() == 2


def test_pod1_direct_matrix_construction():
    d0 = QMatrix.from_row_major(3, 1, [q(1), q(-1), q(0)])
    d1 = QMatrix.from_row_major(1, 3, [q(1), q(1), q(-1)])
    c = Carrier.new(1, 3, 1, d0, d1, [q(1), q(1), q(1)], prov())
    assert (c.c0_dim(), c.c1_dim(), c.c2_dim()) == (1, 3, 1)


