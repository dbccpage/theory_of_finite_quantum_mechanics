-- Schema for Primitive Difference Tower and Survivor Witness Ledger
-- AuthorityEffect: None.

CREATE TABLE IF NOT EXISTS survivor_witnesses (
    witness_id TEXT PRIMARY KEY,
    stage_id INTEGER NOT NULL,
    x_locus TEXT NOT NULL,
    y_locus TEXT NOT NULL,
    demand_type TEXT NOT NULL,
    qx_observation TEXT NOT NULL,
    qy_observation TEXT NOT NULL,
    reason TEXT NOT NULL,
    is_retained BOOLEAN NOT NULL DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS genesis_stages (
    stage_num INTEGER PRIMARY KEY,
    category_name TEXT NOT NULL,
    carrier_type TEXT NOT NULL,
    boundary_formula TEXT,
    degrees_of_freedom INTEGER NOT NULL,
    status TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS simplicial_chains (
    chain_id TEXT PRIMARY KEY,
    dimension INTEGER NOT NULL,
    simplex_label TEXT NOT NULL,
    boundary_representation TEXT NOT NULL,
    stokes_verified BOOLEAN NOT NULL DEFAULT 1
);
