-- Finite link-sign and plaquette bookkeeping only.

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

CREATE TABLE IF NOT EXISTS HoneycombSites (
    lattice_id TEXT NOT NULL,
    site_id INT NOT NULL,
    coord_x INT NOT NULL,
    coord_y INT NOT NULL,
    sublattice TEXT NOT NULL, -- 'A' or 'B'
    PRIMARY KEY (lattice_id, site_id),
    FOREIGN KEY (lattice_id) REFERENCES HoneycombLattice(lattice_id)
);

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

CREATE TABLE IF NOT EXISTS PlaquetteBoundaryLinks (
    lattice_id TEXT NOT NULL,
    plaquette_id TEXT NOT NULL,
    link_id TEXT NOT NULL,
    link_order INT NOT NULL,
    orientation INT NOT NULL, -- +1 or -1
    PRIMARY KEY (lattice_id, plaquette_id, link_id)
);

CREATE TABLE IF NOT EXISTS HoneycombGinPostings (
    posting_id INTEGER PRIMARY KEY AUTOINCREMENT,
    lattice_id TEXT NOT NULL,
    mode_type TEXT NOT NULL, -- 'LINK_GAUGE' or 'SITE_MATTER'
    mode_id TEXT NOT NULL,
    incident_plaquette_id TEXT NOT NULL,
    incident_link_id TEXT NOT NULL
);

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
