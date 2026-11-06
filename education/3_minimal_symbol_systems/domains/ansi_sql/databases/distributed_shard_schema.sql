-- ============================================================================
-- ANSI SQL Distributed Shard Schema:
-- Cross-Shard Boundary Relvars (Distributed 5NF) & Consensus Cochain Log
-- AuthorityEffect: None.
-- ============================================================================

-- Cluster Nodes / Shards Registry
CREATE TABLE IF NOT EXISTS shard_cluster_nodes (
    shard_id INTEGER PRIMARY KEY,
    node_name TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL CHECK (status IN ('ONLINE', 'PARTITIONED', 'HEALING', 'OFFLINE')),
    term INTEGER NOT NULL DEFAULT 1,
    last_applied_lsn INTEGER NOT NULL DEFAULT 0
);

-- Horizontal Partition of Base Distributed Orders Relvar across Shards
CREATE TABLE IF NOT EXISTS distributed_orders (
    shard_id INTEGER NOT NULL,
    order_id INTEGER NOT NULL,
    customer_id INTEGER NOT NULL,
    supplier_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    status TEXT NOT NULL,
    vector_clock INTEGER NOT NULL DEFAULT 1,
    PRIMARY KEY (shard_id, order_id),
    FOREIGN KEY (shard_id) REFERENCES shard_cluster_nodes(shard_id)
);

-- Shard Local Projections (Decomposition into Customer and Supplier views)
CREATE TABLE IF NOT EXISTS shard_customer_projection (
    shard_id INTEGER NOT NULL,
    order_id INTEGER NOT NULL,
    customer_id INTEGER NOT NULL,
    PRIMARY KEY (shard_id, order_id)
);

CREATE TABLE IF NOT EXISTS shard_supplier_projection (
    shard_id INTEGER NOT NULL,
    order_id INTEGER NOT NULL,
    supplier_id INTEGER NOT NULL,
    PRIMARY KEY (shard_id, order_id)
);

-- Cross-Shard Boundary Relvar (∂R):
-- Preserves valid cross-shard contract bindings between customers and suppliers.
-- Required for Distributed 5NF join-losslessness.
CREATE TABLE IF NOT EXISTS cross_shard_boundary_relvar (
    source_shard INTEGER NOT NULL,
    target_shard INTEGER NOT NULL,
    customer_id INTEGER NOT NULL,
    supplier_id INTEGER NOT NULL,
    contract_id INTEGER NOT NULL,
    PRIMARY KEY (customer_id, supplier_id)
);

CREATE INDEX IF NOT EXISTS idx_cross_shard_boundary 
ON cross_shard_boundary_relvar(source_shard, target_shard);

-- Consensus Cochain Log:
-- Records mutation events under distributed CDC and network partitions.
-- Evaluates defect cochains (exact coboundary vs non-trivial conflict cycles).
CREATE TABLE IF NOT EXISTS consensus_cochain_log (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    shard_id INTEGER NOT NULL,
    lsn INTEGER NOT NULL,
    key_id INTEGER NOT NULL,
    op_type TEXT NOT NULL CHECK (op_type IN ('INSERT', 'UPDATE', 'DELETE')),
    old_val REAL,
    new_val REAL,
    vector_clock INTEGER NOT NULL,
    is_commutative INTEGER NOT NULL, -- 1 if disjoint key or commutative CRDT action
    conflict_detected INTEGER NOT NULL, -- 1 if concurrent divergent writes on identical key
    terminal_route TEXT NOT NULL CHECK (terminal_route IN ('Repair', 'ReconcileConflict', 'SplitBrainRefusal')),
    reconciled_val REAL,
    reconciled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ----------------------------------------------------------------------------
-- Distributed 5NF Verification Views
-- ----------------------------------------------------------------------------

-- Lossless Distributed Join View (Enforcing Cross-Shard Boundary Relvar ∂R)
CREATE VIEW IF NOT EXISTS view_distributed_join_lossless AS
SELECT 
    c.shard_id AS customer_shard,
    s.shard_id AS supplier_shard,
    c.order_id,
    c.customer_id,
    s.supplier_id,
    b.contract_id
FROM shard_customer_projection c
JOIN shard_supplier_projection s 
    ON c.order_id = s.order_id
JOIN cross_shard_boundary_relvar b 
    ON c.customer_id = b.customer_id 
   AND s.supplier_id = b.supplier_id;

-- Spurious Cross-Shard Tuples View (Reconstruction WITHOUT Boundary Relvar)
-- If boundary constraints are omitted, Cartesian cross-shard combinations
-- synthesize phantom records not present in the original distributed orders.
CREATE VIEW IF NOT EXISTS view_distributed_spurious_tuples AS
SELECT 
    c.shard_id AS customer_shard,
    s.shard_id AS supplier_shard,
    c.order_id,
    c.customer_id,
    s.supplier_id
FROM shard_customer_projection c
JOIN shard_supplier_projection s 
    ON c.order_id = s.order_id
LEFT JOIN cross_shard_boundary_relvar b 
    ON c.customer_id = b.customer_id 
   AND s.supplier_id = b.supplier_id
WHERE b.contract_id IS NULL;

-- Cochain Reconciliation Summary View
CREATE VIEW IF NOT EXISTS view_cochain_reconciliation_audit AS
SELECT 
    key_id,
    COUNT(DISTINCT shard_id) AS reporting_shards,
    MAX(vector_clock) AS max_vector_clock,
    SUM(conflict_detected) AS total_conflicts,
    MAX(CASE WHEN terminal_route = 'ReconcileConflict' THEN 1 ELSE 0 END) AS requires_consensus,
    COUNT(*) AS total_events
FROM consensus_cochain_log
GROUP BY key_id;
