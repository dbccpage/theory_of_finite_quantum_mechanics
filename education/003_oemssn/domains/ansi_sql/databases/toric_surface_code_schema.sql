-- Topological Quantum Error-Correcting Code Cochains & Stabilizer Chains Schema
-- AuthorityEffect: None.
-- Dialect: ANSI SQL / SQLite 3 compatible

-- 1. Lattice Geometry & Cell Complexes
CREATE TABLE IF NOT EXISTS ToricLattice (
    lattice_id INTEGER PRIMARY KEY,
    L_x INTEGER NOT NULL,
    L_y INTEGER NOT NULL,
    topology TEXT NOT NULL CHECK (topology IN ('TORUS', 'PLANAR_SURFACE'))
);

CREATE TABLE IF NOT EXISTS ToricVertices (
    vertex_id INTEGER PRIMARY KEY,
    x INTEGER NOT NULL,
    y INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS ToricEdges (
    edge_id INTEGER PRIMARY KEY,
    orientation TEXT NOT NULL CHECK (orientation IN ('H', 'V')),
    u INTEGER NOT NULL,
    v INTEGER NOT NULL,
    x REAL NOT NULL,
    y REAL NOT NULL,
    FOREIGN KEY (u) REFERENCES ToricVertices(vertex_id),
    FOREIGN KEY (v) REFERENCES ToricVertices(vertex_id)
);

CREATE TABLE IF NOT EXISTS ToricPlaquettes (
    plaquette_id INTEGER PRIMARY KEY,
    x INTEGER NOT NULL,
    y INTEGER NOT NULL
);

-- 2. Boundary Operators: d1 (Edges -> Vertices) and d2 (Plaquettes -> Edges)
CREATE TABLE IF NOT EXISTS ToricBoundary1 (
    edge_id INTEGER NOT NULL,
    vertex_id INTEGER NOT NULL,
    coeff INTEGER NOT NULL DEFAULT 1,
    PRIMARY KEY (edge_id, vertex_id),
    FOREIGN KEY (edge_id) REFERENCES ToricEdges(edge_id),
    FOREIGN KEY (vertex_id) REFERENCES ToricVertices(vertex_id)
);

CREATE TABLE IF NOT EXISTS ToricBoundary2 (
    plaquette_id INTEGER NOT NULL,
    edge_id INTEGER NOT NULL,
    coeff INTEGER NOT NULL DEFAULT 1,
    PRIMARY KEY (plaquette_id, edge_id),
    FOREIGN KEY (plaquette_id) REFERENCES ToricPlaquettes(plaquette_id),
    FOREIGN KEY (edge_id) REFERENCES ToricEdges(edge_id)
);

-- 3. Pauli Error Injections and Syndrome Measurements
CREATE TABLE IF NOT EXISTS ToricPauliErrors (
    round_id INTEGER NOT NULL,
    edge_id INTEGER NOT NULL,
    pauli_type TEXT NOT NULL CHECK (pauli_type IN ('X', 'Z', 'Y')),
    PRIMARY KEY (round_id, edge_id, pauli_type),
    FOREIGN KEY (edge_id) REFERENCES ToricEdges(edge_id)
);

CREATE TABLE IF NOT EXISTS ToricSyndromes (
    round_id INTEGER NOT NULL,
    cell_type TEXT NOT NULL CHECK (cell_type IN ('VERTEX', 'PLAQUETTE')),
    cell_id INTEGER NOT NULL,
    syndrome_val INTEGER NOT NULL CHECK (syndrome_val IN (0, 1)),
    PRIMARY KEY (round_id, cell_type, cell_id)
);

-- 4. Recovery Cochains (Correction Operators applied by decoder)
CREATE TABLE IF NOT EXISTS ToricRecoveryChains (
    round_id INTEGER NOT NULL,
    edge_id INTEGER NOT NULL,
    correction_type TEXT NOT NULL CHECK (correction_type IN ('X', 'Z')),
    PRIMARY KEY (round_id, edge_id, correction_type),
    FOREIGN KEY (edge_id) REFERENCES ToricEdges(edge_id)
);

-- 5. Anyon Worldlines for Topological Braiding
CREATE TABLE IF NOT EXISTS ToricAnyonWorldlines (
    worldline_id INTEGER PRIMARY KEY AUTOINCREMENT,
    braid_run_id INTEGER NOT NULL,
    anyon_id INTEGER NOT NULL,
    anyon_type TEXT NOT NULL CHECK (anyon_type IN ('e', 'm')),
    step_t INTEGER NOT NULL,
    cell_id INTEGER NOT NULL,
    x REAL NOT NULL,
    y REAL NOT NULL
);

-- ----------------------------------------------------------------------------
-- Recursive CTE Views & Relational Auditing Morpisms
-- ----------------------------------------------------------------------------

-- View 1: Chain Complex Boundary Nilpotence (d1 ∘ d2 = 0 mod 2)
-- For every (plaquette, vertex) pair, the number of incident edges traversed must be even.
CREATE VIEW IF NOT EXISTS ViewChainComplexNilpotence AS
SELECT 
    b2.plaquette_id,
    b1.vertex_id,
    COUNT(*) AS incident_path_count,
    (COUNT(*) % 2) AS residual_mod2,
    CASE WHEN (COUNT(*) % 2) = 0 THEN 'NILPOTENT' ELSE 'DEFECT_CYCLE' END AS status
FROM ToricBoundary2 b2
JOIN ToricBoundary1 b1 ON b2.edge_id = b1.edge_id
GROUP BY b2.plaquette_id, b1.vertex_id;

-- View 2: Stabilizer Commutation Audit ([A_s, B_p] = 0)
-- A star stabilizer A_s and plaquette stabilizer B_p commute iff they share an even number of edges.
CREATE VIEW IF NOT EXISTS ViewStabilizerCommutation AS
SELECT 
    v.vertex_id AS star_id,
    p.plaquette_id AS plaquette_id,
    COUNT(b1.edge_id) AS shared_edges_count,
    (COUNT(b1.edge_id) % 2) AS overlap_mod2,
    CASE WHEN (COUNT(b1.edge_id) % 2) = 0 THEN 1 ELSE 0 END AS commutes,
    CASE WHEN (COUNT(b1.edge_id) % 2) = 0 THEN 1 ELSE -1 END AS pauli_commutation_phase
FROM ToricVertices v
CROSS JOIN ToricPlaquettes p
LEFT JOIN ToricBoundary1 b1 ON v.vertex_id = b1.vertex_id
LEFT JOIN ToricBoundary2 b2 ON p.plaquette_id = b2.plaquette_id AND b1.edge_id = b2.edge_id
GROUP BY v.vertex_id, p.plaquette_id;

-- View 3: Relational Syndrome Derivation from Injected Pauli Errors
-- S_X(v) = sum_{e incident to v} (E_Z + E_Y) mod 2
-- S_Z(p) = sum_{e in boundary of p} (E_X + E_Y) mod 2
CREATE VIEW IF NOT EXISTS ViewComputedSyndromes AS
WITH VertexErrors AS (
    SELECT 
        e.round_id,
        'VERTEX' AS cell_type,
        b1.vertex_id AS cell_id,
        (COUNT(*) % 2) AS computed_syndrome
    FROM ToricPauliErrors e
    JOIN ToricBoundary1 b1 ON e.edge_id = b1.edge_id
    WHERE e.pauli_type IN ('Z', 'Y')
    GROUP BY e.round_id, b1.vertex_id
),
PlaquetteErrors AS (
    SELECT 
        e.round_id,
        'PLAQUETTE' AS cell_type,
        b2.plaquette_id AS cell_id,
        (COUNT(*) % 2) AS computed_syndrome
    FROM ToricPauliErrors e
    JOIN ToricBoundary2 b2 ON e.edge_id = b2.edge_id
    WHERE e.pauli_type IN ('X', 'Y')
    GROUP BY e.round_id, b2.plaquette_id
)
SELECT * FROM VertexErrors
UNION ALL
SELECT * FROM PlaquetteErrors;

-- View 4: Syndrome Measurement Discrepancy Audit
-- Compares measured syndromes in ToricSyndromes against mathematically computed ones
CREATE VIEW IF NOT EXISTS ViewSyndromeAudit AS
SELECT 
    cs.round_id,
    cs.cell_type,
    cs.cell_id,
    cs.computed_syndrome,
    COALESCE(ms.syndrome_val, 0) AS measured_syndrome,
    CASE WHEN cs.computed_syndrome = COALESCE(ms.syndrome_val, 0) THEN 'SYNDROME_VERIFIED' ELSE 'SYNDROME_MISMATCH' END AS audit_disposition
FROM ViewComputedSyndromes cs
LEFT JOIN ToricSyndromes ms 
    ON cs.round_id = ms.round_id 
   AND cs.cell_type = ms.cell_type 
   AND cs.cell_id = ms.cell_id;

-- View 5: Anyon Defect Conservation & Even Parity Audit
-- On closed surfaces, total electric (e) and magnetic (m) anyons must be even.
CREATE VIEW IF NOT EXISTS ViewAnyonConservation AS
SELECT 
    round_id,
    SUM(CASE WHEN cell_type = 'VERTEX' AND syndrome_val = 1 THEN 1 ELSE 0 END) AS total_e_anyons,
    SUM(CASE WHEN cell_type = 'PLAQUETTE' AND syndrome_val = 1 THEN 1 ELSE 0 END) AS total_m_anyons,
    (SUM(CASE WHEN cell_type = 'VERTEX' AND syndrome_val = 1 THEN 1 ELSE 0 END) % 2 = 0) AS e_parity_even,
    (SUM(CASE WHEN cell_type = 'PLAQUETTE' AND syndrome_val = 1 THEN 1 ELSE 0 END) % 2 = 0) AS m_parity_even,
    CASE 
        WHEN (SUM(CASE WHEN cell_type = 'VERTEX' AND syndrome_val = 1 THEN 1 ELSE 0 END) % 2 = 0)
         AND (SUM(CASE WHEN cell_type = 'PLAQUETTE' AND syndrome_val = 1 THEN 1 ELSE 0 END) % 2 = 0)
        THEN 'PARITY_CONSERVED'
        ELSE 'CHARGE_LEAKAGE_DEFECT'
    END AS parity_status
FROM ToricSyndromes
GROUP BY round_id;

-- View 6: Anyonic Braiding Berry Phase Audit
-- Computes the topological intersection (winding number) of an electric anyon trajectory
-- on the primal lattice with the dual cut of a magnetic anyon flux.
-- If the electric anyon path winds around the magnetic flux, mutual statistics phase = (-1)^w.
CREATE VIEW IF NOT EXISTS ViewAnyonicBraidingAudit AS
WITH BraidRuns AS (
    SELECT DISTINCT braid_run_id FROM ToricAnyonWorldlines
),
ElectricPathSteps AS (
    SELECT 
        w1.braid_run_id,
        w1.step_t,
        w1.x AS x1, w1.y AS y1,
        w2.x AS x2, w2.y AS y2
    FROM ToricAnyonWorldlines w1
    JOIN ToricAnyonWorldlines w2 
      ON w1.braid_run_id = w2.braid_run_id 
     AND w1.anyon_id = w2.anyon_id 
     AND w1.anyon_type = 'e'
     AND w2.step_t = w1.step_t + 1
),
MagneticFluxCenter AS (
    SELECT 
        braid_run_id,
        x AS m_x,
        y AS m_y
    FROM ToricAnyonWorldlines
    WHERE anyon_type = 'm' AND step_t = 0
),
RayCrossings AS (
    -- Ray casting crossing test: ray from (m_x, m_y) extending horizontally to +infinity
    -- A segment (x1, y1)-(x2, y2) crosses the ray if it straddles m_y and its x-intercept > m_x
    SELECT 
        e.braid_run_id,
        e.step_t,
        CASE 
            WHEN (e.y1 <= m.m_y AND e.y2 > m.m_y) OR (e.y2 <= m.m_y AND e.y1 > m.m_y) THEN
                CASE 
                    WHEN (e.x1 + (m.m_y - e.y1) / NULLIF(e.y2 - e.y1, 0) * (e.x2 - e.x1)) > m.m_x THEN 1
                    ELSE 0
                END
            ELSE 0
        END AS is_crossing
    FROM ElectricPathSteps e
    JOIN MagneticFluxCenter m ON e.braid_run_id = m.braid_run_id
)
SELECT 
    r.braid_run_id,
    SUM(rc.is_crossing) AS winding_number,
    (SUM(rc.is_crossing) % 2) AS winding_mod2,
    CASE WHEN (SUM(rc.is_crossing) % 2) = 1 THEN -1 ELSE 1 END AS topological_berry_phase,
    CASE WHEN (SUM(rc.is_crossing) % 2) = 1 THEN 'NON_TRIVIAL_BRAID_PHASE' ELSE 'TRIVIAL_BRAID_PHASE' END AS braid_classification
FROM BraidRuns r
LEFT JOIN RayCrossings rc ON r.braid_run_id = rc.braid_run_id
GROUP BY r.braid_run_id;

-- View 7: Logical Homology Cycle Audit & Terminal Routing
-- Residual chain R = Error + Recovery mod 2.
-- Computes non-contractible homology windings:
-- W_X = crossing a vertical meridian (e.g. x = 0.5)
-- W_Y = crossing a horizontal parallel (e.g. y = 0.5)
CREATE VIEW IF NOT EXISTS ViewLogicalHomologyAudit AS
WITH ResidualEdges AS (
    SELECT 
        COALESCE(e.round_id, r.round_id) AS round_id,
        COALESCE(e.edge_id, r.edge_id) AS edge_id,
        ((COUNT(e.edge_id) + COUNT(r.edge_id)) % 2) AS in_residual_chain
    FROM ToricPauliErrors e
    FULL OUTER JOIN ToricRecoveryChains r 
        ON e.round_id = r.round_id AND e.edge_id = r.edge_id
    GROUP BY COALESCE(e.round_id, r.round_id), COALESCE(e.edge_id, r.edge_id)
    HAVING in_residual_chain = 1
),
HomologyWindings AS (
    SELECT 
        re.round_id,
        -- Horizontal edges crossing vertical meridian x = 0.5
        SUM(CASE WHEN te.orientation = 'H' AND te.x = 0.5 THEN 1 ELSE 0 END) AS horizontal_meridian_crossings,
        -- Vertical edges crossing horizontal parallel y = 0.5
        SUM(CASE WHEN te.orientation = 'V' AND te.y = 0.5 THEN 1 ELSE 0 END) AS vertical_parallel_crossings
    FROM ResidualEdges re
    JOIN ToricEdges te ON re.edge_id = te.edge_id
    GROUP BY re.round_id
)
SELECT 
    hw.round_id,
    hw.horizontal_meridian_crossings,
    hw.vertical_parallel_crossings,
    (hw.horizontal_meridian_crossings % 2) AS logical_z_flip,
    (hw.vertical_parallel_crossings % 2) AS logical_x_flip,
    CASE 
        WHEN (hw.horizontal_meridian_crossings % 2 = 0) AND (hw.vertical_parallel_crossings % 2 = 0)
        THEN 'Repair'
        ELSE 'SplitBrainRefusal'
    END AS terminal_route,
    CASE 
        WHEN (hw.horizontal_meridian_crossings % 2 = 0) AND (hw.vertical_parallel_crossings % 2 = 0)
        THEN 'EXACT_HOMOLOGICAL_REPAIR'
        ELSE 'LOGICAL_OPERATOR_FAULT'
    END AS qec_recovery_status
FROM HomologyWindings hw;
