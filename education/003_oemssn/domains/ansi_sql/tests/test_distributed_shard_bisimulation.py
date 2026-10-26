"""
Pytest Suite for Distributed Shard Bisimulation:
Cross-Shard Boundary Relvars (Distributed 5NF) & Consensus Cochain Reconciliation
AuthorityEffect: None.
"""

import sys
from pathlib import Path

# Ensure 9_ansi_sql/code is on path
code_dir = Path(__file__).resolve().parent.parent / "code"
if str(code_dir) not in sys.path:
    sys.path.insert(0, str(code_dir))

from distributed_bisimulation_bridge import DistributedBisimulationBridge


def test_lean4_distributed_sharding_core_compilation():
    """Validates that lean4/distributed_sharding_core.lean elaborates cleanly with 0 errors."""
    bridge = DistributedBisimulationBridge()
    assert bridge.verify_lean_compilation() is True


def test_distributed_join_losslessness_with_boundary():
    """
    Validates Distributed 5NF join losslessness:
    When cross-shard boundary relvar is enforced, reconstruction is exact and zero spurious tuples are synthesized.
    """
    bridge = DistributedBisimulationBridge()
    cert = bridge.verify_distributed_5nf_join_losslessness()
    assert cert.is_bisimilar is True
    assert cert.discrepancy_count == 0
    assert cert.details["is_lossless"] is True
    assert cert.details["lossless_joined_count"] == 3


def test_distributed_5nf_spurious_tuple_synthesis():
    """
    Validates Distributed 5NF failure mode:
    When cross-shard boundary constraints are dropped, spurious cross-shard tuples are synthesized.
    """
    bridge = DistributedBisimulationBridge()
    cert = bridge.verify_distributed_5nf_spurious_synthesis()
    assert cert.is_bisimilar is True
    assert cert.discrepancy_count > 0
    assert cert.details["is_lossless"] is False


def test_network_partition_commutative_cochain_repair():
    """
    Validates consensus cochain reconciliation for commutative concurrent writes:
    Disjoint key insertions during network partition heal via exact coboundary potential (Repair).
    """
    bridge = DistributedBisimulationBridge()
    cert = bridge.verify_consensus_cochain_commutative_heal()
    assert cert.is_bisimilar is True
    assert cert.terminal_route == "Repair"
    assert cert.details["commutative_repairs"] == 2
    assert cert.details["conflicts_reconciled"] == 0


def test_network_partition_conflicting_cochain_reconciliation():
    """
    Validates consensus cochain reconciliation for conflicting concurrent writes:
    Concurrent divergent updates to the same key during partition detect a non-trivial 1-cycle
    and trigger consensus conflict resolution (ReconcileConflict).
    """
    bridge = DistributedBisimulationBridge()
    cert = bridge.verify_consensus_cochain_conflict_reconciliation()
    assert cert.is_bisimilar is True
    assert cert.terminal_route == "ReconcileConflict"
    assert cert.details["conflicts_reconciled"] == 1


def test_split_brain_minority_partition_refusal():
    """
    Validates split-brain prevention:
    Mutations on an isolated shard lacking majority quorum are refused (SplitBrainRefusal).
    """
    bridge = DistributedBisimulationBridge()
    cert = bridge.verify_split_brain_refusal()
    assert cert.is_bisimilar is True
    assert cert.terminal_route == "SplitBrainRefusal"


def test_full_distributed_bisimulation_bridge_suite():
    """
    End-to-end bisimulation test: executes all checks and verifies complete bijection
    between Lean 4 formal certificates and SQL multi-shard evaluator outputs.
    """
    bridge = DistributedBisimulationBridge()
    c1 = bridge.verify_distributed_5nf_join_losslessness()
    c2 = bridge.verify_distributed_5nf_spurious_synthesis()
    c3 = bridge.verify_consensus_cochain_commutative_heal()
    c4 = bridge.verify_consensus_cochain_conflict_reconciliation()
    c5 = bridge.verify_split_brain_refusal()

    assert all(
        [c1.is_bisimilar, c2.is_bisimilar, c3.is_bisimilar, c4.is_bisimilar, c5.is_bisimilar]
    )
