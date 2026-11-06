-- ========================================================================
-- kitaev_honeycomb_schema.sql
-- 2D Honeycomb Kitaev Spin Liquid Relational Schema & Auditing CTE Views
-- AuthorityEffect: None
-- ========================================================================

-- 1. Honeycomb Lattice Metadata
CREATE TABLE IF NOT EXISTS HoneycombLattice (
    lattice_id TEXT PRIMARY KEY,
    lx INT NOT NULL,
    ly INT NOT NULL,
    boundary_condition TEXT NOT NULL, -- 'TORUS' or 'OPEN'
    jx REAL NOT NULL,
    jy REAL NOT NULL,
    jz REAL NOT NULL,
    kappa REAL NOT NULL
);

-- 2. Honeycomb Sites (A/B Sublattice Bipartition)
CREATE TABLE IF NOT EXISTS HoneycombSites (
    lattice_id TEXT NOT NULL,
    site_id INT NOT NULL,
    coord_x INT NOT NULL,
    coord_y INT NOT NULL,
    sublattice TEXT NOT NULL, -- 'A' or 'B'
    PRIMARY KEY (lattice_id, site_id),
    FOREIGN KEY (lattice_id) REFERENCES HoneycombLattice(lattice_id)
);

-- 3. Honeycomb Links (x, y, z Directed Gauge Bonds)
CREATE TABLE IF NOT EXISTS HoneycombLinks (
    lattice_id TEXT NOT NULL,
    link_id TEXT NOT NULL,
    site_u INT NOT NULL,
    site_v INT NOT NULL,
    bond_dir TEXT NOT NULL, -- 'X', 'Y', 'Z'
    gauge_u INT NOT NULL,   -- +1 or -1
    PRIMARY KEY (lattice_id, link_id),
    FOREIGN KEY (lattice_id) REFERENCES HoneycombLattice(lattice_id)
);

-- 4. Hexagonal Plaquettes
CREATE TABLE IF NOT EXISTS HoneycombPlaquettes (
    lattice_id TEXT NOT NULL,
    plaquette_id TEXT NOT NULL,
    center_x REAL NOT NULL,
    center_y REAL NOT NULL,
    flux_wp INT NOT NULL,      -- +1 (vortex-free) or -1 (vortex excitation)
    vortex_charge INT NOT NULL, -- 0 or 1
    PRIMARY KEY (lattice_id, plaquette_id),
    FOREIGN KEY (lattice_id) REFERENCES HoneycombLattice(lattice_id)
);

-- 5. Plaquette Boundary Links (6 directed links per hexagon)
CREATE TABLE IF NOT EXISTS PlaquetteBoundaryLinks (
    lattice_id TEXT NOT NULL,
    plaquette_id TEXT NOT NULL,
    link_id TEXT NOT NULL,
    link_order INT NOT NULL,
    orientation INT NOT NULL, -- +1 or -1
    PRIMARY KEY (lattice_id, plaquette_id, link_id)
);

-- 6. Majorana Matter States & Fermion Parity Evolution
CREATE TABLE IF NOT EXISTS MajoranaMatterStates (
    state_id TEXT PRIMARY KEY,
    lattice_id TEXT NOT NULL,
    time_step INT NOT NULL,
    fermion_parity INT NOT NULL,      -- +1 or -1
    gauge_projector_valid INT NOT NULL, -- 1 if D_j = 1 for all j, else 0
    FOREIGN KEY (lattice_id) REFERENCES HoneycombLattice(lattice_id)
);

-- 7. Vortex Braiding Trajectories
CREATE TABLE IF NOT EXISTS VortexBraidingTrajectories (
    traj_id TEXT PRIMARY KEY,
    lattice_id TEXT NOT NULL,
    vortex_a_id TEXT NOT NULL,
    vortex_b_id TEXT NOT NULL,
    winding_number REAL NOT NULL,
    enclosed_parity INT NOT NULL,     -- 0 (vacuum) or 1 (fermion)
    berry_phase_rad REAL NOT NULL,
    measured_phase_rad REAL NOT NULL,
    phase_residual REAL NOT NULL,
    terminal_route TEXT NOT NULL,
    FOREIGN KEY (lattice_id) REFERENCES HoneycombLattice(lattice_id)
);

-- 8. Honeycomb GIN Index Postings (Inverted Index Mapping Modes to Plaquettes)
CREATE TABLE IF NOT EXISTS HoneycombGinPostings (
    posting_id INTEGER PRIMARY KEY AUTOINCREMENT,
    lattice_id TEXT NOT NULL,
    mode_type TEXT NOT NULL, -- 'LINK_GAUGE' or 'SITE_MATTER'
    mode_id TEXT NOT NULL,
    incident_plaquette_id TEXT NOT NULL,
    incident_link_id TEXT NOT NULL
);

-- ========================================================================
-- AUDITING CTE VIEWS
-- ========================================================================

-- View 1: Plaquette Vortex Audit (Computes W_p = prod u_e and checks consistency)
CREATE VIEW IF NOT EXISTS ViewPlaquetteVortexAudit AS
WITH PlaquetteProducts AS (
    SELECT
        p.lattice_id,
        p.plaquette_id,
        p.flux_wp AS recorded_wp,
        p.vortex_charge AS recorded_vortex,
        -- Product of 6 link gauge values in {-1, 1}:
        -- A product is -1 iff the count of (-1) values is odd.
        SUM(CASE WHEN l.gauge_u = -1 THEN 1 ELSE 0 END) AS negative_link_count
    FROM HoneycombPlaquettes p
    JOIN PlaquetteBoundaryLinks b
      ON p.lattice_id = b.lattice_id AND p.plaquette_id = b.plaquette_id
    JOIN HoneycombLinks l
      ON b.lattice_id = l.lattice_id AND b.link_id = l.link_id
    GROUP BY p.lattice_id, p.plaquette_id, p.flux_wp, p.vortex_charge
)
SELECT
    lattice_id,
    plaquette_id,
    recorded_wp,
    recorded_vortex,
    CASE WHEN (negative_link_count % 2 = 1) THEN -1 ELSE 1 END AS computed_wp,
    CASE WHEN (negative_link_count % 2 = 1) THEN 1 ELSE 0 END AS computed_vortex,
    CASE
        WHEN (CASE WHEN (negative_link_count % 2 = 1) THEN -1 ELSE 1 END) = recorded_wp
         AND (CASE WHEN (negative_link_count % 2 = 1) THEN 1 ELSE 0 END) = recorded_vortex
        THEN 'FLUX_CONSISTENT'
        ELSE 'FLUX_DISCREPANCY'
    END AS audit_status
FROM PlaquetteProducts;

-- View 2: Total Vortex Flux Audit (Even Parity Conservation on Torus)
CREATE VIEW IF NOT EXISTS ViewTotalVortexFluxAudit AS
WITH LatticeVortexSummary AS (
    SELECT
        l.lattice_id,
        l.boundary_condition,
        COUNT(p.plaquette_id) AS total_plaquettes,
        SUM(p.vortex_charge) AS total_vortices
    FROM HoneycombLattice l
    LEFT JOIN HoneycombPlaquettes p ON l.lattice_id = p.lattice_id
    GROUP BY l.lattice_id, l.boundary_condition
)
SELECT
    lattice_id,
    boundary_condition,
    total_plaquettes,
    total_vortices,
    total_vortices % 2 AS vortex_parity_mod2,
    CASE
        WHEN boundary_condition = 'TORUS' AND (total_vortices % 2 = 0) THEN 'FLUX_PARITY_VALID'
        WHEN boundary_condition = 'TORUS' AND (total_vortices % 2 != 0) THEN 'FLUX_PARITY_ANOMALY'
        ELSE 'OPEN_BOUNDARY_FLUX_PERMITTED'
    END AS parity_audit_verdict
FROM LatticeVortexSummary;

-- View 3: Majorana Fermion Parity Conservation Audit
CREATE VIEW IF NOT EXISTS ViewMajoranaParityConservationAudit AS
WITH OrderedStates AS (
    SELECT
        state_id,
        lattice_id,
        time_step,
        fermion_parity,
        gauge_projector_valid,
        LAG(fermion_parity, 1, fermion_parity) OVER (
            PARTITION BY lattice_id ORDER BY time_step
        ) AS prev_fermion_parity
    FROM MajoranaMatterStates
)
SELECT
    state_id,
    lattice_id,
    time_step,
    fermion_parity,
    prev_fermion_parity,
    gauge_projector_valid,
    (fermion_parity - prev_fermion_parity) AS parity_delta,
    CASE
        WHEN gauge_projector_valid = 0 THEN 'GAUGE_PROJECTOR_DEFECT'
        WHEN (fermion_parity - prev_fermion_parity) = 0 THEN 'PARITY_CONSERVED'
        ELSE 'PARITY_LEAKAGE_DEFECT'
    END AS conservation_verdict
FROM OrderedStates;

-- View 4: Vortex Braiding Audit (Non-Abelian Ising Anyon Berry Phase)
CREATE VIEW IF NOT EXISTS ViewVortexBraidingAudit AS
SELECT
    traj_id,
    lattice_id,
    vortex_a_id,
    vortex_b_id,
    winding_number,
    enclosed_parity,
    berry_phase_rad,
    measured_phase_rad,
    phase_residual,
    CASE
        WHEN phase_residual <= 1e-4 THEN 'ISING_BRAIDING_CERTIFIED'
        ELSE 'BRAIDING_PHASE_DEFECT'
    END AS phase_status,
    terminal_route
FROM VortexBraidingTrajectories;

-- View 5: Honeycomb Terminal Routing Audit (BQNF Synthesis)
CREATE VIEW IF NOT EXISTS ViewHoneycombTerminalRoutingAudit AS
WITH AggregatedLatticeHealth AS (
    SELECT
        l.lattice_id,
        COALESCE(MIN(m.gauge_projector_valid), 1) AS min_projector_valid,
        COALESCE(MAX(ABS(m.fermion_parity - LAG_PARITY.prev_parity)), 0) AS max_parity_delta,
        COALESCE(SUM(p.vortex_charge), 0) AS total_vortices,
        l.boundary_condition
    FROM HoneycombLattice l
    LEFT JOIN MajoranaMatterStates m ON l.lattice_id = m.lattice_id
    LEFT JOIN (
        SELECT
            state_id,
            LAG(fermion_parity, 1, fermion_parity) OVER (
                PARTITION BY lattice_id ORDER BY time_step
            ) AS prev_parity
        FROM MajoranaMatterStates
    ) LAG_PARITY ON m.state_id = LAG_PARITY.state_id
    LEFT JOIN HoneycombPlaquettes p ON l.lattice_id = p.lattice_id
    GROUP BY l.lattice_id, l.boundary_condition
)
SELECT
    lattice_id,
    boundary_condition,
    total_vortices,
    max_parity_delta,
    min_projector_valid,
    CASE
        WHEN min_projector_valid = 0 THEN 'CLOSURE_FAILURE'
        WHEN max_parity_delta != 0 THEN 'SPLIT_BRAIN_REFUSAL'
        WHEN boundary_condition = 'TORUS' AND (total_vortices % 2 != 0) THEN 'SPLIT_BRAIN_REFUSAL'
        ELSE 'REPAIR'
    END AS terminal_route
FROM AggregatedLatticeHealth;
