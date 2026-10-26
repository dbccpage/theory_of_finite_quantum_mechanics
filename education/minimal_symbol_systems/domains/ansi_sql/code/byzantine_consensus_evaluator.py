"""
Byzantine Fault-Tolerant (BFT) Consensus Cochain & Log-Auditing Evaluator
AuthorityEffect: None.

Implements PBFT 3-phase consensus simulation, checkpoint log compaction,
and relational CTE log-auditing for Byzantine equivocation, message corruption,
and quorum certification.
"""

from __future__ import annotations

import hashlib
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional


@dataclass(frozen=True)
class PbftConsensusAuditReceipt:
    view_id: int
    seq_num: int
    digest: str
    has_quorum_prepare: bool
    has_quorum_commit: bool
    is_committed: bool
    equivocating_nodes: Sequence[int]
    corrupted_messages_count: int
    is_equivocation_detected: bool
    bft_disposition: str


@dataclass(frozen=True)
class CheckpointCompactionReceipt:
    checkpoint_seq: int
    state_digest: str
    matching_signatures_count: int
    is_compaction_eligible: bool
    truncated_messages_count: int
    remaining_log_count: int
    compaction_disposition: str


class ByzantineConsensusEvaluator:
    """Evaluator executing PBFT consensus and ANSI SQL CTE log-auditing."""

    def __init__(self, in_memory: bool = True, db_path: Optional[str] = None):
        if in_memory:
            self.conn = sqlite3.connect(":memory:")
        else:
            self.conn = sqlite3.connect(db_path or "byzantine_consensus.db")
        self.cur = self.conn.cursor()
        self._init_schema()
        self.N = 4
        self.f = 1
        self.primary_id = 0

    def _init_schema(self) -> None:
        schema_path = (
            Path(__file__).resolve().parent.parent / "databases" / "byzantine_consensus_schema.sql"
        )
        if not schema_path.exists():
            schema_path = Path(__file__).resolve().parent / "byzantine_consensus_schema.sql"
        if schema_path.exists():
            with open(schema_path, "r", encoding="utf-8") as f:
                self.conn.executescript(f.read())
        self.conn.commit()

    def close(self) -> None:
        self.conn.close()

    def init_cluster(
        self, n: int = 4, f: int = 1, byzantine_node_ids: Optional[List[int]] = None
    ) -> None:
        """Initializes N nodes with at most f Byzantine nodes."""
        self.N = n
        self.f = f
        byz_set = set(byzantine_node_ids or [])

        self.cur.execute("DELETE FROM PbftNodes")
        for node_id in range(n):
            is_byz = 1 if node_id in byz_set else 0
            pub_key = f"pk_node_{node_id}"
            self.cur.execute(
                "INSERT INTO PbftNodes (node_id, is_byzantine, public_key) VALUES (?, ?, ?)",
                (node_id, is_byz, pub_key),
            )
        self.conn.commit()

    @staticmethod
    def compute_digest(data_str: str) -> str:
        """Deterministic digest."""
        return hashlib.sha256(data_str.encode("utf-8")).hexdigest()[:16]

    def execute_consensus_round(
        self,
        view_id: int,
        seq_num: int,
        request_val: int,
        inject_equivocation: bool = False,
        byzantine_silent: bool = False,
        byzantine_corrupt: bool = False,
    ) -> PbftConsensusAuditReceipt:
        """Executes a 3-phase consensus round with optional fault injection."""
        base_digest = self.compute_digest(f"REQ:{view_id}:{seq_num}:{request_val}")
        alt_digest = self.compute_digest(f"FORGED:{view_id}:{seq_num}:{request_val}")

        # Query which nodes are Byzantine
        self.cur.execute("SELECT node_id FROM PbftNodes WHERE is_byzantine = 1")
        byz_nodes = {row[0] for row in self.cur.fetchall()}

        # 1. Pre-Prepare phase by primary
        self.cur.execute(
            """INSERT INTO PbftMessageLog
               (phase, view_id, seq_num, digest, sender_node_id, signature, is_corrupt)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                "pre_prepare",
                view_id,
                seq_num,
                base_digest,
                self.primary_id,
                f"sig_{self.primary_id}",
                0,
            ),
        )

        if inject_equivocation and self.primary_id in byz_nodes:
            # Primary double-signs conflicting digest
            self.cur.execute(
                """INSERT INTO PbftMessageLog
                   (phase, view_id, seq_num, digest, sender_node_id, signature, is_corrupt)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (
                    "pre_prepare",
                    view_id,
                    seq_num,
                    alt_digest,
                    self.primary_id,
                    f"sig_{self.primary_id}",
                    0,
                ),
            )

        # 2. Prepare phase
        for node_id in range(self.N):
            if node_id in byz_nodes and byzantine_silent:
                continue  # Silent node drops message

            is_corrupt = 0
            dig = base_digest
            if node_id in byz_nodes:
                if inject_equivocation:
                    # Byzantine replica broadcasts conflicting digest
                    dig = alt_digest
                elif byzantine_corrupt:
                    is_corrupt = 1
                    dig = "corrupted_hash"

            self.cur.execute(
                """INSERT INTO PbftMessageLog
                   (phase, view_id, seq_num, digest, sender_node_id, signature, is_corrupt)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                ("prepare", view_id, seq_num, dig, node_id, f"sig_{node_id}", is_corrupt),
            )

        # Check if prepare quorum achieved: 2f + 1 = 3
        quorum_thresh = 2 * self.f + 1
        self.cur.execute(
            """SELECT COUNT(DISTINCT sender_node_id) FROM PbftMessageLog
               WHERE phase = 'prepare' AND view_id = ? AND seq_num = ? AND digest = ? AND is_corrupt = 0""",
            (view_id, seq_num, base_digest),
        )
        prep_count = self.cur.fetchone()[0]
        has_quorum_prep = prep_count >= quorum_thresh

        # 3. Commit phase
        has_quorum_commit = False
        if has_quorum_prep:
            for node_id in range(self.N):
                if node_id in byz_nodes and byzantine_silent:
                    continue
                is_corrupt = 0
                dig = base_digest
                if node_id in byz_nodes and byzantine_corrupt:
                    is_corrupt = 1
                    dig = "corrupted_commit"

                self.cur.execute(
                    """INSERT INTO PbftMessageLog
                       (phase, view_id, seq_num, digest, sender_node_id, signature, is_corrupt)
                       VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    ("commit", view_id, seq_num, dig, node_id, f"sig_{node_id}", is_corrupt),
                )

            self.cur.execute(
                """SELECT COUNT(DISTINCT sender_node_id) FROM PbftMessageLog
                   WHERE phase = 'commit' AND view_id = ? AND seq_num = ? AND digest = ? AND is_corrupt = 0""",
                (view_id, seq_num, base_digest),
            )
            commit_count = self.cur.fetchone()[0]
            has_quorum_commit = commit_count >= quorum_thresh

        is_committed = has_quorum_commit
        if is_committed:
            # Apply state update into PbftStateSnapshots
            self.cur.execute("SELECT MAX(accumulated_val) FROM PbftStateSnapshots")
            prev_row = self.cur.fetchone()
            prev_val = prev_row[0] if prev_row and prev_row[0] is not None else 0
            new_val = prev_val + request_val
            state_dig = self.compute_digest(f"STATE:{seq_num}:{new_val}")
            self.cur.execute(
                "INSERT OR REPLACE INTO PbftStateSnapshots (seq_num, state_digest, accumulated_val) VALUES (?, ?, ?)",
                (seq_num, state_dig, new_val),
            )

        self.conn.commit()

        # Audit equivocations using CTE view
        equiv_nodes = self.audit_equivocations()
        is_equiv = len(equiv_nodes) > 0

        # Determine disposition matching Lean 4
        if is_equiv:
            disposition = "EquivocationRefusal"
        elif not is_committed:
            disposition = "QuorumDefect"
        else:
            disposition = "ExactCompaction"

        # Count corrupt messages
        self.cur.execute("SELECT COUNT(*) FROM ViewCorruptedMessageAudit")
        corrupt_count = self.cur.fetchone()[0]

        return PbftConsensusAuditReceipt(
            view_id=view_id,
            seq_num=seq_num,
            digest=base_digest,
            has_quorum_prepare=has_quorum_prep,
            has_quorum_commit=has_quorum_commit,
            is_committed=is_committed,
            equivocating_nodes=equiv_nodes,
            corrupted_messages_count=corrupt_count,
            is_equivocation_detected=is_equiv,
            bft_disposition=disposition,
        )

    def audit_equivocations(self) -> List[int]:
        """Queries ViewEquivocationAudit to find equivocating nodes."""
        self.cur.execute("SELECT DISTINCT equivocating_node_id FROM ViewEquivocationAudit")
        return [row[0] for row in self.cur.fetchall()]

    def create_checkpoint(
        self,
        seq_num: int,
        inject_forged_digest: bool = False,
        missing_signatures: int = 0,
    ) -> CheckpointCompactionReceipt:
        """Emits a checkpoint certificate and audits log compaction via CTE."""
        # Retrieve true state digest
        self.cur.execute(
            "SELECT state_digest FROM PbftStateSnapshots WHERE seq_num = ?", (seq_num,)
        )
        row = self.cur.fetchone()
        true_digest = row[0] if row else "unknown_state"

        cp_digest = "forged_state_digest" if inject_forged_digest else true_digest

        # Quorum threshold: 2f + 1 = 3 out of 4
        signatures_count = max(0, self.N - missing_signatures)
        quorum_thresh = 2 * self.f + 1

        is_stable = 1 if (signatures_count >= quorum_thresh and not inject_forged_digest) else 0

        if inject_forged_digest:
            disposition = "CorruptedDigestRefusal"
        elif signatures_count < quorum_thresh:
            disposition = "QuorumDefect"
        else:
            disposition = "ExactCompaction"

        self.cur.execute(
            """INSERT INTO PbftCheckpoints
               (seq_num, state_digest, matching_signatures_count, is_stable, compaction_disposition)
               VALUES (?, ?, ?, ?, ?)""",
            (seq_num, cp_digest, signatures_count, is_stable, disposition),
        )
        self.conn.commit()

        # Query ViewCheckpointLogCompactionAudit
        self.cur.execute(
            """SELECT matching_signatures_count, is_compaction_eligible, truncatable_messages_count
               FROM ViewCheckpointLogCompactionAudit WHERE stable_seq = ?""",
            (seq_num,),
        )
        audit_row = self.cur.fetchone()
        if audit_row:
            matching_sigs, is_eligible, truncatable_count = audit_row
        else:
            matching_sigs = signatures_count
            is_eligible = 0

        # Perform log compaction if eligible
        truncated_count = 0
        if is_eligible == 1:
            truncated_count = self.truncate_log_to_checkpoint(seq_num)

        self.cur.execute("SELECT COUNT(*) FROM PbftMessageLog")
        remaining_count = self.cur.fetchone()[0]

        return CheckpointCompactionReceipt(
            checkpoint_seq=seq_num,
            state_digest=cp_digest,
            matching_signatures_count=matching_sigs,
            is_compaction_eligible=bool(is_eligible),
            truncated_messages_count=truncated_count,
            remaining_log_count=remaining_count,
            compaction_disposition=disposition,
        )

    def truncate_log_to_checkpoint(self, seq_num: int) -> int:
        """Truncates / garbage-collects log entries with seq_num <= target in O(1)."""
        self.cur.execute("SELECT COUNT(*) FROM PbftMessageLog WHERE seq_num <= ?", (seq_num,))
        count = self.cur.fetchone()[0]
        self.cur.execute("DELETE FROM PbftMessageLog WHERE seq_num <= ?", (seq_num,))
        self.conn.commit()
        return count


__all__ = [
    "ByzantineConsensusEvaluator",
    "CheckpointCompactionReceipt",
    "PbftConsensusAuditReceipt",
]
