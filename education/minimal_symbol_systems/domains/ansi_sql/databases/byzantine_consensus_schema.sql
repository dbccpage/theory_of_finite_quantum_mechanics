-- Byzantine Fault-Tolerant (BFT) Consensus Cochains & CTE Log-Auditing Schema
-- AuthorityEffect: None
-- Dialect: ANSI SQL / SQLite 3 compatible

CREATE TABLE IF NOT EXISTS PbftNodes (
    node_id INTEGER PRIMARY KEY,
    is_byzantine INTEGER NOT NULL CHECK (is_byzantine IN (0, 1)),
    public_key TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS PbftMessageLog (
    msg_id INTEGER PRIMARY KEY AUTOINCREMENT,
    phase TEXT NOT NULL CHECK (phase IN ('pre_prepare', 'prepare', 'commit', 'checkpoint')),
    view_id INTEGER NOT NULL,
    seq_num INTEGER NOT NULL,
    digest TEXT NOT NULL,
    sender_node_id INTEGER NOT NULL,
    signature TEXT NOT NULL,
    is_corrupt INTEGER NOT NULL DEFAULT 0 CHECK (is_corrupt IN (0, 1)),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_node_id) REFERENCES PbftNodes(node_id)
);

CREATE TABLE IF NOT EXISTS PbftStateSnapshots (
    seq_num INTEGER PRIMARY KEY,
    state_digest TEXT NOT NULL,
    accumulated_val INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS PbftCheckpoints (
    checkpoint_id INTEGER PRIMARY KEY AUTOINCREMENT,
    seq_num INTEGER NOT NULL,
    state_digest TEXT NOT NULL,
    matching_signatures_count INTEGER NOT NULL,
    is_stable INTEGER NOT NULL DEFAULT 0 CHECK (is_stable IN (0, 1)),
    compaction_disposition TEXT NOT NULL CHECK (compaction_disposition IN ('ExactCompaction', 'EquivocationRefusal', 'CorruptedDigestRefusal', 'QuorumDefect'))
);

-- CTE View: Byzantine Equivocation Audit
-- Identifies any node that signed two distinct digests for the same (phase, view_id, seq_num)
CREATE VIEW IF NOT EXISTS ViewEquivocationAudit AS
WITH EquivocatingNodes AS (
    SELECT 
        m1.sender_node_id,
        m1.phase,
        m1.view_id,
        m1.seq_num,
        m1.digest AS digest_1,
        m2.digest AS digest_2,
        m1.msg_id AS msg_id_1,
        m2.msg_id AS msg_id_2
    FROM PbftMessageLog m1
    JOIN PbftMessageLog m2 
      ON m1.sender_node_id = m2.sender_node_id
     AND m1.phase = m2.phase
     AND m1.view_id = m2.view_id
     AND m1.seq_num = m2.seq_num
     AND m1.digest != m2.digest
     AND m1.msg_id < m2.msg_id
)
SELECT 
    sender_node_id AS equivocating_node_id,
    phase,
    view_id,
    seq_num,
    digest_1,
    digest_2,
    COUNT(*) OVER () AS total_equivocations
FROM EquivocatingNodes;

-- CTE View: Quorum Certificates
-- Tallies distinct non-corrupted signatures per (phase, view_id, seq_num, digest)
CREATE VIEW IF NOT EXISTS ViewQuorumCertificates AS
WITH SignatureCounts AS (
    SELECT 
        phase,
        view_id,
        seq_num,
        digest,
        COUNT(DISTINCT sender_node_id) AS distinct_signatures
    FROM PbftMessageLog
    WHERE is_corrupt = 0
    GROUP BY phase, view_id, seq_num, digest
)
SELECT 
    phase,
    view_id,
    seq_num,
    digest,
    distinct_signatures,
    CASE 
        WHEN distinct_signatures >= 3 THEN 1 -- In 4-node cluster (f=1), quorum threshold 2f+1 = 3
        ELSE 0 
    END AS has_valid_quorum
FROM SignatureCounts;

-- CTE View: Checkpoint Log Compaction Audit
-- Evaluates stable checkpoints against application state snapshots and audits log entries eligible for O(1) truncation
CREATE VIEW IF NOT EXISTS ViewCheckpointLogCompactionAudit AS
WITH StableCheckpoints AS (
    SELECT 
        cp.seq_num AS stable_seq,
        cp.state_digest AS cp_digest,
        snap.state_digest AS actual_digest,
        cp.matching_signatures_count,
        CASE 
            WHEN cp.state_digest = snap.state_digest AND cp.matching_signatures_count >= 3 THEN 1
            ELSE 0 
        END AS is_compaction_eligible
    FROM PbftCheckpoints cp
    JOIN PbftStateSnapshots snap ON cp.seq_num = snap.seq_num
),
TruncatableLog AS (
    SELECT 
        sc.stable_seq,
        COUNT(msg.msg_id) AS truncatable_messages_count
    FROM StableCheckpoints sc
    JOIN PbftMessageLog msg ON msg.seq_num <= sc.stable_seq
    WHERE sc.is_compaction_eligible = 1
    GROUP BY sc.stable_seq
)
SELECT 
    sc.stable_seq,
    sc.cp_digest,
    sc.matching_signatures_count,
    sc.is_compaction_eligible,
    COALESCE(tl.truncatable_messages_count, 0) AS truncatable_messages_count
FROM StableCheckpoints sc
LEFT JOIN TruncatableLog tl ON sc.stable_seq = tl.stable_seq;

-- CTE View: Corrupted Message Audit
CREATE VIEW IF NOT EXISTS ViewCorruptedMessageAudit AS
SELECT 
    msg_id,
    phase,
    sender_node_id,
    digest,
    signature,
    is_corrupt
FROM PbftMessageLog
WHERE is_corrupt = 1;
