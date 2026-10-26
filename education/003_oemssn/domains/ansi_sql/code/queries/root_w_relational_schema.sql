-- DDL: Root W Relational Bedrock Schema
-- AuthorityEffect: None

CREATE TABLE IF NOT EXISTS carrier_elements (
    element_id TEXT PRIMARY KEY,
    admitted_step INTEGER NOT NULL,
    metadata TEXT
);

CREATE TABLE IF NOT EXISTS difference_relations (
    src TEXT NOT NULL,
    dst TEXT NOT NULL,
    admitted_step INTEGER NOT NULL,
    PRIMARY KEY (src, dst),
    FOREIGN KEY (src) REFERENCES carrier_elements(element_id),
    FOREIGN KEY (dst) REFERENCES carrier_elements(element_id),
    CONSTRAINT chk_irreflexive CHECK (src <> dst)
);

-- Transposition View: sigma(u, v) = (v, u)
CREATE VIEW IF NOT EXISTS view_transposed_relations AS
SELECT 
    dst AS src,
    src AS dst,
    admitted_step,
    'transposed' AS relation_type
FROM difference_relations;

-- 1-Chain Boundary Evaluation View on Original vs Transposed Relations
CREATE VIEW IF NOT EXISTS view_boundary_sign_inversion AS
WITH OriginalBoundary AS (
    SELECT vertex, SUM(weight) AS weight
    FROM (
        SELECT src AS vertex, -1 AS weight FROM difference_relations
        UNION ALL
        SELECT dst AS vertex, 1 AS weight FROM difference_relations
    )
    GROUP BY vertex
),
TransposedBoundary AS (
    SELECT vertex, SUM(weight) AS weight
    FROM (
        SELECT src AS vertex, -1 AS weight FROM view_transposed_relations
        UNION ALL
        SELECT dst AS vertex, 1 AS weight FROM view_transposed_relations
    )
    GROUP BY vertex
)
SELECT 
    o.vertex,
    o.weight AS orig_weight,
    t.weight AS trans_weight,
    (o.weight + t.weight) AS net_sum
FROM OriginalBoundary o
JOIN TransposedBoundary t ON o.vertex = t.vertex;

