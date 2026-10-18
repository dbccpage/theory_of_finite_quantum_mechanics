"""test_su2_cluster_benchmark_4d.py — Unit Tests for Multi-Turn PFP Cluster Sweeps on L=8.

AuthorityEffect: None.
Reference: sealed-derivation-v1 (3100c4e), Paper 011, gemini_000.md.
"""

from __future__ import annotations

from fractions import Fraction
import sys
from pathlib import Path
import pytest

# Ensure code directory is in sys.path
code_dir = Path(__file__).resolve().parent.parent.parent
if str(code_dir) not in sys.path:
    sys.path.insert(0, str(code_dir))

from src.fsp.su2_link_holonomy_4d import Lattice4DCoord
from src.fsp.su2_cluster_benchmark_4d import (
    L8ClusterBenchmarkReceipt,
    SU2ClusterBenchmarkRunner,
)


class TestL8ClusterBenchmarkReceipt:
    """Test suite for L8ClusterBenchmarkReceipt value object."""

    def test_receipt_equality_and_rejection(self):
        r1 = L8ClusterBenchmarkReceipt(
            benchmark_id="bm_test",
            lattice_dims=(2, 2, 2, 2),
            total_sites=16,
            total_links=64,
            num_rounds=2,
            num_proposals=4,
            num_accepted=2,
            acceptance_rate=Fraction(1, 1),
            initial_action=Fraction(10, 1),
            final_action=Fraction(8, 1),
            action_descent=Fraction(2, 1),
            involution_pairing_certified=True,
            unitarity_certified=True,
            authority_effect="None",
        )
        r2 = L8ClusterBenchmarkReceipt(
            benchmark_id="bm_test",
            lattice_dims=(2, 2, 2, 2),
            total_sites=16,
            total_links=64,
            num_rounds=2,
            num_proposals=4,
            num_accepted=2,
            acceptance_rate=Fraction(1, 1),
            initial_action=Fraction(10, 1),
            final_action=Fraction(8, 1),
            action_descent=Fraction(2, 1),
            involution_pairing_certified=True,
            unitarity_certified=True,
            authority_effect="None",
        )
        assert r1 == r2
        assert r1 != "not_a_receipt"
        assert r1 != 42

        # Check digest is valid hex SHA-256
        digest = r1.canonical_digest()
        assert isinstance(digest, str)
        assert len(digest) == 64


class TestSU2ClusterBenchmarkRunner:
    """Test suite for SU2ClusterBenchmarkRunner."""

    def test_runner_initialization_and_validation(self):
        runner = SU2ClusterBenchmarkRunner(lattice_dim=2)
        assert runner.dims == (2, 2, 2, 2)
        assert runner.lattice.volume == 16
        assert runner.lattice.num_links == 64

        with pytest.raises(ValueError, match="lattice_dim must be an integer >= 2"):
            SU2ClusterBenchmarkRunner(lattice_dim=1)
        with pytest.raises(ValueError, match="lattice_dim must be an integer >= 2"):
            SU2ClusterBenchmarkRunner(lattice_dim=True)

    def test_cluster_generation(self):
        runner = SU2ClusterBenchmarkRunner(lattice_dim=4)
        base = Lattice4DCoord(3, 3, 3, 3, runner.dims)
        cluster = runner.generate_cluster_sites(base, cluster_size=2)
        # 2^4 = 16 sites
        assert len(cluster) == 16
        # Verify periodic boundary wrapping
        assert any(c.x0 == 0 for c in cluster)
        assert any(c.x1 == 0 for c in cluster)

    def test_run_benchmark_validation(self):
        runner = SU2ClusterBenchmarkRunner(lattice_dim=2)
        with pytest.raises(ValueError, match="num_rounds must be positive"):
            runner.run_benchmark(num_rounds=0)
        with pytest.raises(ValueError, match="random_threshold must be in"):
            runner.run_benchmark(num_rounds=1, random_threshold=Fraction(-1, 2))
        with pytest.raises(ValueError, match="random_threshold must be in"):
            runner.run_benchmark(num_rounds=1, random_threshold=Fraction(3, 2))

    def test_run_benchmark_execution_and_receipt(self):
        runner = SU2ClusterBenchmarkRunner(lattice_dim=2)
        receipt = runner.run_benchmark(
            num_rounds=3,
            cluster_size=2,
            random_threshold=Fraction(1, 1),  # deterministic accept
        )
        assert receipt.benchmark_id == "bm_l8_2x2x2x2"
        assert receipt.total_sites == 16
        assert receipt.total_links == 64
        assert receipt.num_rounds == 3
        assert receipt.num_proposals > 0
        assert receipt.num_accepted >= 0
        assert receipt.involution_pairing_certified is True
        assert receipt.unitarity_certified is True
        assert receipt.authority_effect == "None"

    def test_l8_lattice_dimensions_and_structure(self):
        # Test L=8 initialization and cluster structure (V=4096 sites, 16384 links)
        runner = SU2ClusterBenchmarkRunner(lattice_dim=8)
        assert runner.dims == (8, 8, 8, 8)
        assert runner.lattice.volume == 4096
        assert runner.lattice.num_links == 16384

        base = Lattice4DCoord(0, 0, 0, 0, runner.dims)
        cluster = runner.generate_cluster_sites(base, cluster_size=2)
        assert len(cluster) == 16

    def test_run_benchmark_l3_multiturn(self):
        # L=3 lattice: V = 81 sites, 324 links - fast and comprehensive multi-turn benchmark
        runner = SU2ClusterBenchmarkRunner(lattice_dim=3)
        receipt = runner.run_benchmark(
            num_rounds=2,
            cluster_size=1,
            random_threshold=Fraction(1, 2),
        )
        assert receipt.total_sites == 81
        assert receipt.total_links == 324
        assert receipt.num_rounds == 2
        assert receipt.involution_pairing_certified is True
        assert receipt.unitarity_certified is True
