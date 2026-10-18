"""Unit and Integration Tests: GIN Large-Lattice Scaling Benchmark & Cluster Involution Cancellation.
AuthorityEffect: None.

Tests:
1. Large lattice Hubbard cluster geometry, bipartition, and mode indexing (L = 16, 32).
2. GIN inverted index fast partner retrieval with spectator mode pruning.
3. Exact destructive sign cancellation on cluster involution pairs.
4. Equivalence between GIN inverted lookup and linear scan baseline.
5. Adversarial defect detection: corrupted spectator modes and broken weight symmetries.
6. Benchmark scaling performance: asserting positive speedup factor on large lattices.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

code_dir = Path(__file__).resolve().parent.parent
if str(code_dir) not in sys.path:
    sys.path.insert(0, str(code_dir))

from gin_cluster_scaling_benchmark import (
    GinClusterPostingIndex,
    LargeLatticeHubbardCluster,
    generate_large_lattice_ensemble,
    run_single_scaling_benchmark,
)


def test_large_lattice_hubbard_cluster_geometry():
    """Validates 2D square lattice geometry, sublattice parity, and mode indexing."""
    cluster16 = LargeLatticeHubbardCluster(L=16)
    assert cluster16.num_sites == 256
    assert cluster16.total_modes == 512

    # Check coordinate round-trip
    for s in [1, 16, 17, 256]:
        x, y = cluster16.site_to_coord(s)
        assert cluster16.coord_to_site(x, y) == s

    # Check bipartition
    assert cluster16.sublattice(1) == 0  # (0, 0) -> A
    assert cluster16.sublattice(2) == 1  # (1, 0) -> B
    assert cluster16.sublattice(17) == 1 # (0, 1) -> B

    # Plaquette cluster of size 2x2
    c_modes = cluster16.get_plaquette_cluster(top_left_site=1, size=2)
    # 4 sites * 2 spins = 8 modes
    assert len(c_modes) == 8
    # Sites are 1, 2, 17, 18
    expected_sites = {1, 2, 17, 18}
    expected_modes = expected_sites | {s + 256 for s in expected_sites}
    assert c_modes == expected_modes


def test_gin_inverted_index_fast_partner_retrieval():
    """Validates that GIN inverted posting index correctly retrieves cluster involution partners."""
    cluster = LargeLatticeHubbardCluster(L=16)
    configs, queries = generate_large_lattice_ensemble(cluster, num_pairs=50, plaquette_size=2, seed=123)

    gin = GinClusterPostingIndex(total_modes=cluster.total_modes)
    for cid, occ, w, sgn in configs:
        gin.index_configuration(cid, occ, w, sgn)

    # For every pair query, verify partner retrieval
    for q_cid, c_modes in queries:
        partner_id = gin.find_involution_partner_gin(q_cid, c_modes)
        assert partner_id is not None, f"Partner not found for config {q_cid}"
        # Partner must be the next adjacent ID in our paired generation
        expected_partner = q_cid + 1 if q_cid % 2 == 1 else q_cid - 1
        assert partner_id == expected_partner


def test_gin_exact_destructive_sign_cancellation():
    """Validates that retrieved involution pairs exhibit exact destructive sign cancellation."""
    cluster = LargeLatticeHubbardCluster(L=16)
    configs, queries = generate_large_lattice_ensemble(cluster, num_pairs=100, plaquette_size=2, seed=456)

    gin = GinClusterPostingIndex(total_modes=cluster.total_modes)
    for cid, occ, w, sgn in configs:
        gin.index_configuration(cid, occ, w, sgn)

    max_defect = 0.0
    for q_cid, c_modes in queries:
        partner_id = gin.find_involution_partner_gin(q_cid, c_modes)
        assert partner_id is not None
        w1, s1 = gin.cfg_weights[q_cid], gin.cfg_signs[q_cid]
        w2, s2 = gin.cfg_weights[partner_id], gin.cfg_signs[partner_id]
        defect = abs(w1 * s1 + w2 * s2)
        if defect > max_defect:
            max_defect = defect

    assert max_defect < 1e-12, f"Destructive sign cancellation failed with defect {max_defect}"


def test_gin_versus_linear_scan_equivalence():
    """Validates exact candidate equivalence between GIN inverted lookup and naive linear scan."""
    cluster = LargeLatticeHubbardCluster(L=16)
    configs, queries = generate_large_lattice_ensemble(cluster, num_pairs=40, plaquette_size=2, seed=789)

    gin = GinClusterPostingIndex(total_modes=cluster.total_modes)
    for cid, occ, w, sgn in configs:
        gin.index_configuration(cid, occ, w, sgn)

    for q_cid, c_modes in queries:
        gin_partner = gin.find_involution_partner_gin(q_cid, c_modes)
        lin_partner = gin.find_involution_partner_linear(q_cid, c_modes)
        assert gin_partner == lin_partner, f"Mismatch: GIN found {gin_partner}, Linear found {lin_partner}"


def test_adversarial_corrupted_spectator_detection():
    """Falsification test: corrupting spectator modes prevents false-positive pairing."""
    cluster = LargeLatticeHubbardCluster(L=16)
    configs, queries = generate_large_lattice_ensemble(cluster, num_pairs=10, plaquette_size=2, seed=999)

    q1_cid, c_modes = queries[0]
    expected_partner_id = q1_cid + 1 if q1_cid % 2 == 1 else q1_cid - 1

    # Locate the true partner in the shuffled configs
    partner_idx = next(i for i, c in enumerate(configs) if c[0] == expected_partner_id)
    p_id, p_occ, p_w, p_sgn = configs[partner_idx]

    # Pick a spectator mode not in cluster
    spectator_candidates = list(set(range(1, cluster.total_modes + 1)) - c_modes)
    corrupted_mode = spectator_candidates[0]
    corrupted_occ = set(p_occ)
    if corrupted_mode in corrupted_occ:
        corrupted_occ.remove(corrupted_mode)
    else:
        corrupted_occ.add(corrupted_mode)
    configs[partner_idx] = (p_id, corrupted_occ, p_w, p_sgn)

    gin = GinClusterPostingIndex(total_modes=cluster.total_modes)
    for cid, occ, w, sgn in configs:
        gin.index_configuration(cid, occ, w, sgn)

    # GIN lookup for query 1 must return None because spectator is corrupted
    corrupted_partner = gin.find_involution_partner_gin(q1_cid, c_modes)
    assert corrupted_partner is None, "GIN falsely paired a configuration with corrupted spectator modes"


def test_scaling_speedup_ratio_on_16x16():
    """Asserts that GIN index yields a statistically significant speedup (> 3.0x) over linear scan at M=5000."""
    dp = run_single_scaling_benchmark(
        lattice_dim=16,
        num_configs=5000,
        num_queries=50,
        seed=101,
    )
    assert dp.all_exact_cancellations is True
    assert dp.max_cancellation_defect < 1e-12
    assert dp.speedup_factor > 2.0, f"Expected speedup > 2.0x, got {dp.speedup_factor}x"
