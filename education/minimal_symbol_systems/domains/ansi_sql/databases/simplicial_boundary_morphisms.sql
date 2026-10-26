-- Simplicial Boundary Morphisms and CTE Evaluator
-- AuthorityEffect: None.

-- 1. Base DDL Tables
CREATE TABLE IF NOT EXISTS simplices (
    simplex_id TEXT PRIMARY KEY,
    dim INTEGER NOT NULL,
    v0 TEXT NOT NULL,
    v1 TEXT,
    v2 TEXT
);

CREATE TABLE IF NOT EXISTS boundary_cache (
    parent_id TEXT NOT NULL,
    child_id TEXT NOT NULL,
    child_dim INTEGER NOT NULL,
    signed_weight INTEGER NOT NULL,
    PRIMARY KEY (parent_id, child_id)
);

-- 2. Master CTE: Simplicial Boundary Nilpotence (d_1 ∘ d_2 = 0)
WITH RECURSIVE
-- Step 1: d_2 boundary of 2-simplices into 1-chains (edges)
BoundaryEdges AS (
    SELECT 
        simplex_id AS parent_id,
        v1 || '->' || v2 AS edge_id,
        v1 AS src,
        v2 AS dst,
        1 AS edge_weight
    FROM simplices
    WHERE dim = 2
    
    UNION ALL
    
    SELECT 
        simplex_id AS parent_id,
        v0 || '->' || v2 AS edge_id,
        v0 AS src,
        v2 AS dst,
        -1 AS edge_weight
    FROM simplices
    WHERE dim = 2
    
    UNION ALL
    
    SELECT 
        simplex_id AS parent_id,
        v0 || '->' || v1 AS edge_id,
        v0 AS src,
        v1 AS dst,
        1 AS edge_weight
    FROM simplices
    WHERE dim = 2
),
-- Step 2: d_1 boundary of 1-chains into 0-chains (vertices)
BoundaryVertices AS (
    -- Target endpoint (+1 * edge_weight)
    SELECT 
        parent_id,
        edge_id,
        dst AS vertex,
        edge_weight * 1 AS vertex_weight
    FROM BoundaryEdges
    
    UNION ALL
    
    -- Source endpoint (-1 * edge_weight)
    SELECT 
        parent_id,
        edge_id,
        src AS vertex,
        edge_weight * (-1) AS vertex_weight
    FROM BoundaryEdges
),
-- Step 3: Accumulation and Nilpotence Verification (d^2 = 0)
BoundaryNilpotenceEvaluation AS (
    SELECT 
        parent_id,
        vertex,
        SUM(vertex_weight) AS net_multiplicity,
        COUNT(*) AS term_count
    FROM BoundaryVertices
    GROUP BY parent_id, vertex
),
-- Step 4: Window Quotient Partitioning
QuotientPartitions AS (
    SELECT 
        parent_id,
        edge_id,
        src,
        dst,
        edge_weight,
        COUNT(*) OVER (PARTITION BY CASE WHEN src < dst THEN src || '<->' || dst ELSE dst || '<->' || src END) AS undirected_multiplicity
    FROM BoundaryEdges
)
SELECT 
    b.parent_id,
    b.vertex,
    b.net_multiplicity,
    CASE WHEN b.net_multiplicity = 0 THEN 1 ELSE 0 END AS stokes_nilpotence_verified
FROM BoundaryNilpotenceEvaluation b;
