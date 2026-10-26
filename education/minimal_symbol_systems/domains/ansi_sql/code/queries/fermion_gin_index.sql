-- GIN Index Inverted Posting List Schema for Fermion Sign Resolution
-- Maps orbital modes and boundary bonds to many-body configuration IDs.
-- Exact sign-reversing, weight-preserving involution partners Xi(C) are retrieved
-- via inverted posting list intersections.
-- AuthorityEffect: None

CREATE TABLE IF NOT EXISTS many_body_configurations (
    config_id TEXT PRIMARY KEY,
    weight INTEGER NOT NULL,
    sign INTEGER NOT NULL,
    num_particles INTEGER NOT NULL,
    metadata TEXT
);

CREATE TABLE IF NOT EXISTS orbital_postings (
    orbital_id TEXT NOT NULL,
    config_id TEXT NOT NULL,
    is_occupied INTEGER NOT NULL,
    PRIMARY KEY (orbital_id, config_id),
    FOREIGN KEY (config_id) REFERENCES many_body_configurations(config_id)
);

CREATE TABLE IF NOT EXISTS involution_pairs (
    config_id TEXT NOT NULL,
    partner_id TEXT NOT NULL,
    involution_type TEXT NOT NULL,
    PRIMARY KEY (config_id, partner_id),
    FOREIGN KEY (config_id) REFERENCES many_body_configurations(config_id),
    FOREIGN KEY (partner_id) REFERENCES many_body_configurations(config_id)
);

CREATE VIEW IF NOT EXISTS view_gin_fermion_cancellation AS
SELECT 
    c.config_id,
    p.partner_id,
    c.weight AS config_weight,
    p_cfg.weight AS partner_weight,
    c.sign AS config_sign,
    p_cfg.sign AS partner_sign,
    (c.weight * c.sign + p_cfg.weight * p_cfg.sign) AS net_weight
FROM many_body_configurations c
JOIN involution_pairs p ON c.config_id = p.config_id
JOIN many_body_configurations p_cfg ON p.partner_id = p_cfg.config_id;
