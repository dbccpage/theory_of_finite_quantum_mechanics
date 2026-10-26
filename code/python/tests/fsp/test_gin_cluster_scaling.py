"""Unit and Integration Tests: GIN Large-Lattice Scaling Benchmark & Cluster Involution Cancellation.
AuthorityEffect: None.

Tests:
1. Large lattice Hubbard cluster geometry, bipartition, and mode indexing (L = 16, 32).
2. GIN inverted index fast partner retrieval with spectator mode pruning.
3. Exact destructive sign cancellation on cluster involution pairs.
4. Equivalence between GIN inverted lookup and linear scan baseline.
5. Adversarial defect detection: corrupted spectator modes and broken weight symmetries.
6. Benchmark timings are observations; deterministic candidate work checks pruning.
"""

from __future__ import annotations

import sys
import math
from pathlib import Path

import pytest

code_dir = Path(__file__).resolve().parent.parent
if str(code_dir) not in sys.path:
    sys.path.insert(0, str(code_dir))

from src.fsp.gin_cluster_scaling_benchmark import (
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

    for s in [1, 16, 17, 256]:
        x, y = cluster16.site_to_coord(s)
        assert cluster16.coord_to_site(x, y) == s

    assert cluster16.sublattice(1) == 0
    assert cluster16.sublattice(2) == 1
    assert cluster16.sublattice(17) == 1

    c_modes = cluster16.get_plaquette_cluster(top_left_site=1, size=2)
    assert len(c_modes) == 8
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

    for q_cid, c_modes in queries:
        partner_id = gin.find_involution_partner_gin(q_cid, c_modes)
        assert partner_id is not None, f"Partner not found for config {q_cid}"
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

    partner_idx = next(i for i, c in enumerate(configs) if c[0] == expected_partner_id)
    p_id, p_occ, p_w, p_sgn = configs[partner_idx]

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

    corrupted_partner = gin.find_involution_partner_gin(q1_cid, c_modes)
    assert corrupted_partner is None, "GIN falsely paired a configuration with corrupted spectator modes"


def test_scaling_speedup_ratio_on_16x16(record_property):
    """Record host timing without treating a one-shot ratio as a statistical claim."""
    dp = run_single_scaling_benchmark(
        lattice_dim=16,
        num_configs=5000,
        num_queries=50,
        seed=101,
    )
    assert dp.all_exact_cancellations is True
    assert dp.max_cancellation_defect < 1e-12
    assert math.isfinite(dp.speedup_factor) and dp.speedup_factor > 0
    record_property("observed_speedup", dp.speedup_factor)


def test_singleton_still_must_satisfy_remaining_required_modes():
    gin = GinClusterPostingIndex(total_modes=2)
    for cid, occupied in [(1, {1}), (2, {2}), (3, {2})]:
        gin.index_configuration(cid, occupied, 1.0, 1)
    assert gin.query_by_modes({1, 2}, set()) == set()


def test_postings_prune_candidate_comparisons_on_declared_ensemble():
    class CountedConfigurations(dict):
        reads = 0
        def __getitem__(self, key):
            self.reads += 1
            return super().__getitem__(key)

    cluster = LargeLatticeHubbardCluster(L=16)
    configs, queries = generate_large_lattice_ensemble(cluster, num_pairs=2500, seed=101)
    gin = GinClusterPostingIndex(total_modes=cluster.total_modes)
    for cid, occupied, weight, sign in configs:
        gin.index_configuration(cid, occupied, weight, sign)
    gin.cfg_modes = CountedConfigurations(gin.cfg_modes)
    indexed, linear = 0, 0
    for cid, modes in queries[:50]:
        gin.cfg_modes.reads = 0
        partner = gin.find_involution_partner_gin(cid, modes)
        indexed += gin.cfg_modes.reads
        gin.cfg_modes.reads = 0
        baseline = gin.find_involution_partner_linear(cid, modes)
        linear += gin.cfg_modes.reads
        assert partner == baseline == cid + 1
    # A deterministic regression budget for this seeded ensemble, not an
    # asymptotic complexity theorem or a wall-clock speed guarantee.
    assert indexed <= 100
    assert linear > 10 * indexed
