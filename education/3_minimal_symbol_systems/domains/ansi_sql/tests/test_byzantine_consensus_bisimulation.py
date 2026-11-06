"""
Pytest Suite for Byzantine Fault-Tolerant (BFT) Consensus Cochains & CTE Log-Auditing
AuthorityEffect: None.
"""

import sys
from pathlib import Path

# Ensure 9_ansi_sql/code is on path
code_dir = Path(__file__).resolve().parent.parent / "code"
if str(code_dir) not in sys.path:
    sys.path.insert(0, str(code_dir))

from byzantine_bisimulation_bridge import ByzantineBisimulationBridge
from byzantine_consensus_evaluator import ByzantineConsensusEvaluator


def test_lean4_byzantine_consensus_core_compilation():
    """Validates that lean4/byzantine_consensus_core.lean elaborates cleanly with 0 errors."""
    bridge = ByzantineBisimulationBridge()
    assert bridge.verify_lean_compilation() is True


def test_quorum_intersection_and_honest_progress():
    """Validates PBFT 3-phase consensus progress with f=1 silent Byzantine replica (2f+1 honest quorum)."""
    bridge = ByzantineBisimulationBridge()
    cert = bridge.verify_quorum_intersection_and_honest_progress()
    assert cert.is_bisimilar is True
    assert cert.discrepancy_count == 0
    assert cert.terminal_route == "ExactCompaction"
    assert cert.details["prepare_quorum"] is True
    assert cert.details["commit_quorum"] is True
    assert cert.details["is_committed"] is True


def test_equivocation_detection_and_refusal():
    """Validates Byzantine equivocation detection: primary double-signing conflicting digests is refused."""
    bridge = ByzantineBisimulationBridge()
    cert = bridge.verify_equivocation_detection_and_refusal()
    assert cert.is_bisimilar is True
    assert cert.terminal_route == "EquivocationRefusal"
    assert cert.details["equivocation_detected"] is True
    assert 0 in cert.details["equivocating_nodes"]


def test_stable_checkpoint_log_compaction():
    """Validates log compaction: stable checkpoint with 2f+1 matching signatures truncates old log in O(1)."""
    bridge = ByzantineBisimulationBridge()
    cert = bridge.verify_stable_checkpoint_log_compaction()
    assert cert.is_bisimilar is True
    assert cert.terminal_route == "ExactCompaction"
    assert cert.details["truncated_messages"] > 0
    assert cert.details["remaining_messages"] == 0


def test_corrupted_checkpoint_digest_refusal():
    """Validates that forged checkpoint state digest is refused without truncating log."""
    bridge = ByzantineBisimulationBridge()
    cert = bridge.verify_corrupted_checkpoint_digest_refusal()
    assert cert.is_bisimilar is True
    assert cert.terminal_route == "CorruptedDigestRefusal"
    assert cert.details["is_compaction_eligible"] is False


def test_corrupted_message_audit():
    """Validates ViewCorruptedMessageAudit identifies messages with corrupted payload hashes."""
    evaluator = ByzantineConsensusEvaluator(in_memory=True)
    evaluator.init_cluster(n=4, f=1, byzantine_node_ids=[1])
    receipt = evaluator.execute_consensus_round(
        view_id=0,
        seq_num=1,
        request_val=99,
        byzantine_corrupt=True,
    )
    assert receipt.corrupted_messages_count > 0
    evaluator.close()


def test_full_byzantine_bisimulation_suite():
    """End-to-end bisimulation test verifying complete bijection between Lean 4 theorems and SQL CTE audits."""
    bridge = ByzantineBisimulationBridge()
    c1 = bridge.verify_quorum_intersection_and_honest_progress()
    c2 = bridge.verify_equivocation_detection_and_refusal()
    c3 = bridge.verify_stable_checkpoint_log_compaction()
    c4 = bridge.verify_corrupted_checkpoint_digest_refusal()

    assert all([c1.is_bisimilar, c2.is_bisimilar, c3.is_bisimilar, c4.is_bisimilar])
