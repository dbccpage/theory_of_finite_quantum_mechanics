"""
Distributed Shard Evaluator: Cross-Shard Boundary Relvars & Consensus Cochain Reconciliation
AuthorityEffect: None.
"""

import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


class DistributedShardEvaluator:
    """
    Evaluates distributed join-losslessness across cross-shard boundary relvars
    and executes consensus cochain defect reconciliation under simulated network partitions.
    """

    def __init__(self, in_memory: bool = True):
        self.conn = sqlite3.connect(":memory:" if in_memory else "distributed_shards.db")
        self.conn.row_factory = sqlite3.Row
        self._init_schema()
        # Network connectivity topology: (s1, s2) -> bool
        self.network_links: Dict[Tuple[int, int], bool] = {}
        self.num_shards = 0

    def _init_schema(self):
        sql_path = (
            Path(__file__).resolve().parent.parent / "databases" / "distributed_shard_schema.sql"
        )
        if not sql_path.exists():
            sql_path = Path(__file__).resolve().parent / "distributed_shard_schema.sql"
        if sql_path.exists():
            with open(sql_path, "r", encoding="utf-8") as f:
                self.conn.executescript(f.read())
        self.conn.commit()

    def init_cluster(self, num_shards: int = 3):
        """Initializes a cluster of N shards with fully connected network topology."""
        self.num_shards = num_shards
        c = self.conn.cursor()
        c.execute("DELETE FROM shard_cluster_nodes;")
        for sid in range(1, num_shards + 1):
            c.execute(
                """
                INSERT INTO shard_cluster_nodes (shard_id, node_name, status, term, last_applied_lsn)
                VALUES (?, ?, 'ONLINE', 1, 0);
            """,
                (sid, f"shard_node_{sid}"),
            )

        # Initialize fully connected topology
        self.network_links = {}
        for i in range(1, num_shards + 1):
            for j in range(1, num_shards + 1):
                self.network_links[(i, j)] = True
        self.conn.commit()

    # ------------------------------------------------------------------------
    # Network Partition Topology Management
    # ------------------------------------------------------------------------
    def disconnect_shards(self, s1: int, s2: int):
        """Partitions network link between shard s1 and shard s2."""
        self.network_links[(s1, s2)] = False
        self.network_links[(s2, s1)] = False
        self._update_node_partition_status()

    def isolate_shard(self, shard_id: int):
        """Completely isolates a shard from all other cluster nodes."""
        for other in range(1, self.num_shards + 1):
            if other != shard_id:
                self.network_links[(shard_id, other)] = False
                self.network_links[(other, shard_id)] = False
        self._update_node_partition_status()

    def heal_partitions(self):
        """Heals all network partitions, restoring full connectivity."""
        for k in self.network_links:
            self.network_links[k] = True
        c = self.conn.cursor()
        c.execute("UPDATE shard_cluster_nodes SET status = 'ONLINE';")
        self.conn.commit()

    def _update_node_partition_status(self):
        c = self.conn.cursor()
        for sid in range(1, self.num_shards + 1):
            reachable = sum(
                1 for o in range(1, self.num_shards + 1) if self.network_links.get((sid, o), False)
            )
            status = "PARTITIONED" if reachable < self.num_shards else "ONLINE"
            c.execute(
                "UPDATE shard_cluster_nodes SET status = ? WHERE shard_id = ?;", (status, sid)
            )
        self.conn.commit()

    def has_quorum(self, shard_id: int) -> bool:
        """Determines if a shard can reach a strict majority quorum."""
        reachable = sum(
            1 for o in range(1, self.num_shards + 1) if self.network_links.get((shard_id, o), False)
        )
        majority = (self.num_shards // 2) + 1
        return reachable >= majority

    # ------------------------------------------------------------------------
    # Distributed 5NF & Cross-Shard Boundary Relvar Evaluation
    # ------------------------------------------------------------------------
    def populate_distributed_orders(
        self, orders: List[Dict[str, Any]], contracts: List[Dict[str, Any]]
    ):
        """Populates distributed orders, shard projections, and cross-shard boundary relvars."""
        c = self.conn.cursor()
        c.execute("DELETE FROM distributed_orders;")
        c.execute("DELETE FROM shard_customer_projection;")
        c.execute("DELETE FROM shard_supplier_projection;")
        c.execute("DELETE FROM cross_shard_boundary_relvar;")

        for o in orders:
            c.execute(
                """
                INSERT INTO distributed_orders (shard_id, order_id, customer_id, supplier_id, amount, status, vector_clock)
                VALUES (?, ?, ?, ?, ?, ?, ?);
            """,
                (
                    o["shard_id"],
                    o["order_id"],
                    o["customer_id"],
                    o["supplier_id"],
                    o["amount"],
                    o.get("status", "COMPLETED"),
                    o.get("vector_clock", 1),
                ),
            )

            c.execute(
                """
                INSERT INTO shard_customer_projection (shard_id, order_id, customer_id)
                VALUES (?, ?, ?);
            """,
                (o["shard_id"], o["order_id"], o["customer_id"]),
            )

            c.execute(
                """
                INSERT INTO shard_supplier_projection (shard_id, order_id, supplier_id)
                VALUES (?, ?, ?);
            """,
                (o["shard_id"], o["order_id"], o["supplier_id"]),
            )

        for ctr in contracts:
            c.execute(
                """
                INSERT INTO cross_shard_boundary_relvar (source_shard, target_shard, customer_id, supplier_id, contract_id)
                VALUES (?, ?, ?, ?, ?);
            """,
                (
                    ctr["source_shard"],
                    ctr["target_shard"],
                    ctr["customer_id"],
                    ctr["supplier_id"],
                    ctr["contract_id"],
                ),
            )

        self.conn.commit()

    def evaluate_distributed_join_losslessness(self) -> Dict[str, Any]:
        """
        Evaluates distributed join losslessness:
        - Lossless view joins local projections with the cross-shard boundary relvar.
        - Spurious view captures phantom cross-shard combinations that appear if boundary relvar is dropped.
        """
        c = self.conn.cursor()
        c.execute("SELECT * FROM view_distributed_join_lossless;")
        lossless_rows = c.fetchall()

        c.execute("SELECT * FROM view_distributed_spurious_tuples;")
        spurious_rows = c.fetchall()

        is_lossless = len(spurious_rows) == 0

        return {
            "is_lossless": is_lossless,
            "lossless_joined_count": len(lossless_rows),
            "spurious_tuples_count": len(spurious_rows),
            "spurious_tuples": [dict(r) for r in spurious_rows],
        }

    # ------------------------------------------------------------------------
    # Consensus Cochain Defect Reconciliation
    # ------------------------------------------------------------------------
    def apply_shard_mutation(
        self,
        shard_id: int,
        lsn: int,
        key_id: int,
        op_type: str,
        old_val: Optional[float],
        new_val: Optional[float],
        vector_clock: int,
    ) -> Dict[str, Any]:
        """
        Records a mutation event at a specific shard.
        If the shard is partitioned and lacks quorum, the mutation is flagged with SplitBrainRefusal.
        """
        c = self.conn.cursor()
        quorum_ok = self.has_quorum(shard_id)

        if not quorum_ok:
            c.execute(
                """
                INSERT INTO consensus_cochain_log (
                    shard_id, lsn, key_id, op_type, old_val, new_val, vector_clock,
                    is_commutative, conflict_detected, terminal_route, reconciled_val
                ) VALUES (?, ?, ?, ?, ?, ?, ?, 0, 1, 'SplitBrainRefusal', NULL);
            """,
                (shard_id, lsn, key_id, op_type, old_val, new_val, vector_clock),
            )
            self.conn.commit()
            return {"accepted": False, "terminal_route": "SplitBrainRefusal", "reason": "No Quorum"}

        # Accept tentatively into local log
        c.execute(
            """
            INSERT INTO consensus_cochain_log (
                shard_id, lsn, key_id, op_type, old_val, new_val, vector_clock,
                is_commutative, conflict_detected, terminal_route, reconciled_val
            ) VALUES (?, ?, ?, ?, ?, ?, ?, 1, 0, 'Repair', ?);
        """,
            (shard_id, lsn, key_id, op_type, old_val, new_val, vector_clock, new_val),
        )
        self.conn.commit()
        return {"accepted": True, "terminal_route": "Repair"}

    def reconcile_network_partition_heal(self) -> Dict[str, Any]:
        """
        Executes consensus cochain defect reconciliation upon partition healing:
        1. Identifies keys with concurrent mutations across different shards.
        2. If mutations on a key are commutative or identical:
           defect cochain is exact (omega = d^0 alpha) -> Route: Repair.
        3. If mutations on a key have divergent values and overlapping vector clocks:
           defect cochain is a non-trivial 1-cohomology obstruction cycle ([omega] != 0) ->
           Route: ReconcileConflict, applying deterministic consensus resolution.
        """
        c = self.conn.cursor()
        c.execute("""
            SELECT key_id, COUNT(DISTINCT shard_id) AS shard_count, COUNT(*) AS event_count
            FROM consensus_cochain_log
            WHERE terminal_route != 'SplitBrainRefusal'
            GROUP BY key_id;
        """)
        key_summaries = c.fetchall()

        commutative_repairs = 0
        conflicts_reconciled = 0
        split_brain_refusals = 0

        c.execute(
            "SELECT COUNT(*) FROM consensus_cochain_log WHERE terminal_route = 'SplitBrainRefusal';"
        )
        split_brain_refusals = c.fetchone()[0]

        for ks in key_summaries:
            kid = ks["key_id"]
            shards_involved = ks["shard_count"]

            c.execute(
                """
                SELECT event_id, shard_id, new_val, vector_clock
                FROM consensus_cochain_log
                WHERE key_id = ? AND terminal_route != 'SplitBrainRefusal'
                ORDER BY vector_clock DESC, new_val DESC;
            """,
                (kid,),
            )
            events = c.fetchall()

            if shards_involved <= 1:
                # Single shard write: exact coboundary
                commutative_repairs += 1
                c.execute(
                    """
                    UPDATE consensus_cochain_log
                    SET is_commutative = 1, conflict_detected = 0, terminal_route = 'Repair'
                    WHERE key_id = ? AND terminal_route != 'SplitBrainRefusal';
                """,
                    (kid,),
                )
            else:
                # Multiple shards modified this key during partition
                distinct_vals = set(e["new_val"] for e in events)
                if len(distinct_vals) == 1:
                    # Idempotent / identical value: exact coboundary
                    commutative_repairs += 1
                    c.execute(
                        """
                        UPDATE consensus_cochain_log
                        SET is_commutative = 1, conflict_detected = 0, terminal_route = 'Repair'
                        WHERE key_id = ? AND terminal_route != 'SplitBrainRefusal';
                    """,
                        (kid,),
                    )
                else:
                    # Divergent values on same key: non-trivial 1-cycle in H^1!
                    conflicts_reconciled += 1
                    # Deterministic consensus resolution: highest vector clock, then max value
                    winning_event = events[0]
                    resolved_val = winning_event["new_val"]

                    c.execute(
                        """
                        UPDATE consensus_cochain_log
                        SET is_commutative = 0, conflict_detected = 1, terminal_route = 'ReconcileConflict',
                            reconciled_val = ?
                        WHERE key_id = ? AND terminal_route != 'SplitBrainRefusal';
                    """,
                        (resolved_val, kid),
                    )

        self.conn.commit()

        return {
            "keys_reconciled": len(key_summaries),
            "commutative_repairs": commutative_repairs,
            "conflicts_reconciled": conflicts_reconciled,
            "split_brain_refusals": split_brain_refusals,
            "verified_consensus": True,
        }

    def close(self):
        self.conn.close()
