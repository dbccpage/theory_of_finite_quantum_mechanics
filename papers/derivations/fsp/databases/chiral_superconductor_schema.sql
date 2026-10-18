-- ========================================================================
-- chiral_superconductor_schema.sql
-- 3D Chiral Topological Superconductor Relational Schema & Auditing CTE Views
-- AuthorityEffect: None
-- ========================================================================

-- 1. Lattice Metadata
CREATE TABLE IF NOT EXISTS WeylSuperconductorLattice (
    lattice_id TEXT PRIMARY KEY,
    lx INT NOT NULL,
    ly INT NOT NULL,
    lz INT NOT NULL,
    k0 REAL NOT NULL,          -- Weyl node separation along kz
    delta_0 REAL NOT NULL,     -- Superconducting pairing amplitude
    mu REAL NOT NULL,          -- Chemical potential
    phs_symmetric INT NOT NULL DEFAULT 1 -- 1 if particle-hole symmetry holds, else 0
);

-- 2. Bulk Weyl Nodes (Monopoles of Berry Curvature)
CREATE TABLE IF NOT EXISTS WeylBulkNodes (
    lattice_id TEXT NOT NULL,
    node_id TEXT NOT NULL,
    kx REAL NOT NULL,
    ky REAL NOT NULL,
    kz REAL NOT NULL,
    chirality INT NOT NULL,       -- +1 (right-handed) or -1 (left-handed)
    monopole_charge INT NOT NULL, -- +1 or -1
    PRIMARY KEY (lattice_id, node_id),
    FOREIGN KEY (lattice_id) REFERENCES WeylSuperconductorLattice(lattice_id)
);

-- 3. Kz Slice 2D Topological Invariants (Chern Slices)
CREATE TABLE IF NOT EXISTS KzSliceTopologicalInvariants (
    lattice_id TEXT NOT NULL,
    slice_id TEXT NOT NULL,
    kz_index INT NOT NULL,
    kz_val REAL NOT NULL,
    chern_number INT NOT NULL,    -- 1 if between -k0 and +k0, else 0
    bulk_gap REAL NOT NULL,
    PRIMARY KEY (lattice_id, slice_id),
    FOREIGN KEY (lattice_id) REFERENCES WeylSuperconductorLattice(lattice_id)
);

-- 4. Surface Majorana Fermi Arcs
CREATE TABLE IF NOT EXISTS SurfaceMajoranaFermiArcs (
    lattice_id TEXT NOT NULL,
    arc_id TEXT NOT NULL,
    node_start_id TEXT NOT NULL,
    node_end_id TEXT NOT NULL,
    surface_orientation TEXT NOT NULL, -- 'TOP' (z=lz-1) or 'BOTTOM' (z=0)
    arc_length REAL NOT NULL,
    is_self_conjugate INT NOT NULL DEFAULT 1, -- 1 if Majorana self-conjugate at E=0
    spectral_residual REAL NOT NULL DEFAULT 0.0,
    PRIMARY KEY (lattice_id, arc_id),
    FOREIGN KEY (lattice_id) REFERENCES WeylSuperconductorLattice(lattice_id)
);

-- 5. Surface-Bulk Spectral Flow & Callan-Harvey Anomaly Inflow Trajectory
CREATE TABLE IF NOT EXISTS SurfaceBulkSpectralFlowTrajectory (
    step_id TEXT PRIMARY KEY,
    lattice_id TEXT NOT NULL,
    time_step INT NOT NULL,
    flux_theta REAL NOT NULL,
    bulk_pumped_charge INT NOT NULL,
    surface_pumped_charge INT NOT NULL,
    net_anomaly INT NOT NULL,
    FOREIGN KEY (lattice_id) REFERENCES WeylSuperconductorLattice(lattice_id)
);

-- 6. GIN Index Postings (Inverted Index Mapping Modes to Slices, Nodes, and Arcs)
CREATE TABLE IF NOT EXISTS ChiralSuperconductorGinPostings (
    posting_id INTEGER PRIMARY KEY AUTOINCREMENT,
    lattice_id TEXT NOT NULL,
    mode_type TEXT NOT NULL, -- 'KZ_TOPOLOGICAL_SLICE', 'BULK_NODE', 'SURFACE_MAJORANA_ARC'
    mode_id TEXT NOT NULL,
    target_id TEXT NOT NULL
);

-- ========================================================================
-- AUDITING CTE VIEWS
-- ========================================================================

-- View 1: Chiral Anomaly Cancellation Audit (Nielsen-Ninomiya sum C_i = 0)
CREATE VIEW IF NOT EXISTS ViewChiralAnomalyCancellationAudit AS
WITH NodeSummary AS (
    SELECT
        lattice_id,
        COUNT(node_id) AS total_nodes,
        SUM(chirality) AS net_chirality,
        SUM(CASE WHEN chirality = 1 THEN 1 ELSE 0 END) AS right_handed_nodes,
        SUM(CASE WHEN chirality = -1 THEN 1 ELSE 0 END) AS left_handed_nodes
    FROM WeylBulkNodes
    GROUP BY lattice_id
)
SELECT
    lattice_id,
    total_nodes,
    right_handed_nodes,
    left_handed_nodes,
    net_chirality,
    CASE
        WHEN net_chirality = 0 AND total_nodes >= 2 THEN 'ANOMALY_CANCELLED_VALID'
        ELSE 'CHIRAL_ANOMALY_DEFECT'
    END AS anomaly_status
FROM NodeSummary;

-- View 2: Surface-Bulk Spectral Flow & Fermi Arc Count Audit
CREATE VIEW IF NOT EXISTS ViewSurfaceBulkSpectralFlowAudit AS
WITH ArcCounts AS (
    SELECT
        lattice_id,
        COUNT(arc_id) AS recorded_arcs,
        SUM(CASE WHEN surface_orientation = 'TOP' THEN 1 ELSE 0 END) AS top_surface_arcs,
        SUM(CASE WHEN surface_orientation = 'BOTTOM' THEN 1 ELSE 0 END) AS bottom_surface_arcs
    FROM SurfaceMajoranaFermiArcs
    GROUP BY lattice_id
),
ExpectedArcs AS (
    SELECT
        n.lattice_id,
        -- Net topological charge difference yields 2 Fermi arcs on slab (1 top, 1 bottom)
        (MAX(n.chirality) - MIN(n.chirality)) AS expected_total_arcs
    FROM WeylBulkNodes n
    GROUP BY n.lattice_id
)
SELECT
    e.lattice_id,
    COALESCE(a.recorded_arcs, 0) AS recorded_arcs,
    COALESCE(a.top_surface_arcs, 0) AS top_surface_arcs,
    COALESCE(a.bottom_surface_arcs, 0) AS bottom_surface_arcs,
    e.expected_total_arcs,
    CASE
        WHEN COALESCE(a.recorded_arcs, 0) = e.expected_total_arcs AND e.expected_total_arcs = 2
        THEN 'BULK_BOUNDARY_MATCH'
        ELSE 'BULK_BOUNDARY_DISCREPANCY'
    END AS bulk_boundary_status
FROM ExpectedArcs e
LEFT JOIN ArcCounts a ON e.lattice_id = a.lattice_id;

-- View 3: Majorana Surface Fermi Arc Self-Conjugacy Audit
CREATE VIEW IF NOT EXISTS ViewMajoranaFermiArcAudit AS
SELECT
    arc_id,
    lattice_id,
    surface_orientation,
    arc_length,
    is_self_conjugate,
    spectral_residual,
    CASE
        WHEN is_self_conjugate = 1 AND spectral_residual <= 1e-4
        THEN 'MAJORANA_SELF_CONJUGATE_VALID'
        ELSE 'MAJORANA_SYMMETRY_DEFECT'
    END AS majorana_status
FROM SurfaceMajoranaFermiArcs;

-- View 4: Callan-Harvey Anomaly Inflow Conservation Audit
CREATE VIEW IF NOT EXISTS ViewSurfaceAnomalyInflowAudit AS
SELECT
    step_id,
    lattice_id,
    time_step,
    flux_theta,
    bulk_pumped_charge,
    surface_pumped_charge,
    net_anomaly,
    CASE
        WHEN net_anomaly = 0 THEN 'ANOMALY_INFLOW_CONSERVED'
        ELSE 'INFLOW_LEAKAGE_DEFECT'
    END AS inflow_verdict
FROM SurfaceBulkSpectralFlowTrajectory;

-- View 5: Chiral Superconductor Terminal Routing Audit (BQNF Synthesis)
CREATE VIEW IF NOT EXISTS ViewChiralSuperconductorTerminalRoutingAudit AS
WITH LatticeHealth AS (
    SELECT
        l.lattice_id,
        l.phs_symmetric,
        COALESCE(a.net_chirality, 0) AS net_chirality,
        CASE
            WHEN b.bulk_boundary_status = 'BULK_BOUNDARY_MATCH' THEN 0
            ELSE 1
        END AS arc_discrepancy,
        COALESCE(MAX(ABS(t.net_anomaly)), 0) AS max_inflow_anomaly,
        COALESCE(MIN(m.is_self_conjugate), 1) AS min_majorana_conjugate
    FROM WeylSuperconductorLattice l
    LEFT JOIN ViewChiralAnomalyCancellationAudit a ON l.lattice_id = a.lattice_id
    LEFT JOIN ViewSurfaceBulkSpectralFlowAudit b ON l.lattice_id = b.lattice_id
    LEFT JOIN SurfaceBulkSpectralFlowTrajectory t ON l.lattice_id = t.lattice_id
    LEFT JOIN SurfaceMajoranaFermiArcs m ON l.lattice_id = m.lattice_id
    GROUP BY l.lattice_id, l.phs_symmetric, a.net_chirality, b.bulk_boundary_status
)
SELECT
    lattice_id,
    phs_symmetric,
    net_chirality,
    arc_discrepancy,
    max_inflow_anomaly,
    CASE
        WHEN phs_symmetric = 0 OR min_majorana_conjugate = 0 THEN 'CLOSURE_FAILURE'
        WHEN net_chirality != 0 OR arc_discrepancy != 0 OR max_inflow_anomaly != 0 THEN 'SPLIT_BRAIN_REFUSAL'
        ELSE 'REPAIR'
    END AS terminal_route
FROM LatticeHealth;
