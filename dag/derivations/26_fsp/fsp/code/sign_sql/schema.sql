-- ============================================================================
-- schema.sql — "the SQL of the Fermion Sign Problem"
--
-- A literal relational encoding of the void-to-Troyer-Wiese walk, through to
-- the Wheeler-DeWitt equation as a boundary row.
--
-- AuthorityEffect: None.  This schema DIAGNOSES and ILLUSTRATES; it authorizes
-- nothing and proves nothing.  Honesty fences, load-bearing:
--   * The toy instance seeded on top of this schema ILLUSTRATES the structure
--     of the sign problem (signed cancellation vs. re-presentation); it does
--     NOT simulate physics.  No Hamiltonian, no amplitude, no continuum limit.
--   * The Wheeler-DeWitt row is a DECLARED boundary object, citing the house
--     DeWitt superspace case study (PP/021, PO-021): constraint-level problem
--     mathematics, not root ontology.  It is stored with standing
--     'declared_boundary' precisely so a query can SHOW it is declared, not
--     derived.
--   * The pricing discipline is load-bearing: every admission row carries a
--     priced/derived flag.  priced = 0 means the sealed sources license it
--     (sealed-derivation-v1 @ 3100c4e); priced = 1 means it is a PURCHASE the
--     sources do not license (the walk's imports #1..#6 and the asymptotic
--     frame).  The audit query (q4) exists to make smuggling impossible.
--   * NP-hardness statements (Cook-Levin, Troyer-Wiese) are EXTERNAL
--     LITERATURE rows, never derivations.  Nothing in this database is a
--     hardness proof.
-- ============================================================================

PRAGMA foreign_keys = ON;

-- ----------------------------------------------------------------------------
-- rungs: the levels of the walk, void (0) to Troyer-Wiese (7) to the
-- Wheeler-DeWitt boundary row (8).  A rung is a stage of admitted structure.
-- The parent chain makes the walk a literal path a recursive CTE can climb.
-- ----------------------------------------------------------------------------
CREATE TABLE rungs (
    rung_id        INTEGER PRIMARY KEY,          -- ordinal of the rung: 0 = void, 8 = WDW boundary
    parent_rung_id INTEGER REFERENCES rungs(rung_id),
                                                 -- the previous rung; NULL only at the void.
                                                 -- This column IS the walk: q4 recurses over it.
    name           TEXT NOT NULL UNIQUE,         -- short machine name of the stage
    standing       TEXT NOT NULL CHECK (standing IN
                     ('licensed',                -- fully licensed by sealed-derivation-v1 @ 3100c4e
                      'mixed',                   -- licensed core + at least one priced import
                      'priced',                  -- reachable only by purchase (priced imports)
                      'external',                -- anchored in external literature, not derivation
                      'declared_boundary')),     -- declared, not derived: a boundary row only
    claim_type     TEXT NOT NULL,                -- house claim palette for the rung's strongest claim
                                                 -- (PROVEN-MECHANIZED / FINITE COMPUTATION /
                                                 --  CONDITIONAL / OPEN / external literature / DECLARED)
    lay_sentence   TEXT NOT NULL,                -- the one plain-words sentence for a lay reader
    source         TEXT NOT NULL                 -- citation: sealed tag + file + theorem names,
                                                 -- or external literature, or the PP/021 case study
);

-- ----------------------------------------------------------------------------
-- carriers: the finite carriers each rung actually stands on.  size is NULL
-- when the carrier is unbounded or refused (the continuum superspace of the
-- WDW row is REFUSED as a carrier per PP/021 — it appears here only so the
-- refusal is a row, not an omission).
-- ----------------------------------------------------------------------------
CREATE TABLE carriers (
    carrier_id  INTEGER PRIMARY KEY,             -- surrogate key
    rung_id     INTEGER NOT NULL REFERENCES rungs(rung_id),
                                                 -- the rung this carrier belongs to
    name        TEXT NOT NULL,                   -- carrier name (e.g. the oriented two-point carrier)
    size        INTEGER,                         -- element count; NULL = unbounded or refused
    description TEXT NOT NULL                    -- what the carrier is, in plain words, with fences
);

-- ----------------------------------------------------------------------------
-- admissions: every deliberate addition of structure, with the priced/derived
-- flag.  THE PRICING DISCIPLINE LIVES HERE.  "Admitted" = deliberately added
-- by an explicit, replayable act (sealed model.py: step/replay).  "Priced" =
-- an admission the sealed sources do NOT license; the paper must present it
-- as a purchase, never a derivation.
-- ----------------------------------------------------------------------------
CREATE TABLE admissions (
    admission_id INTEGER PRIMARY KEY,            -- surrogate key; also the seed order within a rung
    rung_id      INTEGER NOT NULL REFERENCES rungs(rung_id),
                                                 -- the rung at which this admission is made
    name         TEXT NOT NULL UNIQUE,           -- what is admitted (machine name)
    kind         TEXT NOT NULL,                  -- rough sort: relation / law / definition / operation /
                                                 -- resource / authority / frame / arithmetic / ...
    priced       INTEGER NOT NULL CHECK (priced IN (0, 1)),
                                                 -- 0 = derived/licensed by the sealed sources;
                                                 -- 1 = PRICED IMPORT (a purchase).  Load-bearing.
    price_tag    TEXT,                           -- the walk's import number ('#1'..'#6') when priced;
                                                 -- NULL for licensed admissions and for the
                                                 -- asymptotic frame (priced but un-numbered: it
                                                 -- rides on imports #3-#5 plus external literature)
    source       TEXT NOT NULL,                  -- what licenses it (sealed citation) or what must
                                                 -- pay for it (fresh proof / external literature)
    description  TEXT NOT NULL                   -- the admission in plain words
);

-- ----------------------------------------------------------------------------
-- systems: a signed-sum object — the THING computed, prior to any choice of
-- how to write it.  The sign problem is a property of a presentation of a
-- system, not of the system (rung 7's reclassification), which is why systems
-- and presentations are separate tables: the schema itself keeps the
-- presentation/internal distinction the sealed discipline demands.
-- ----------------------------------------------------------------------------
CREATE TABLE systems (
    system_id   INTEGER PRIMARY KEY,             -- surrogate key
    name        TEXT NOT NULL UNIQUE,            -- system name
    description TEXT NOT NULL                    -- what it is, with the not-physics fence inline
);

-- ----------------------------------------------------------------------------
-- presentations: basis choices — ways of WRITING a system's sum.  Two
-- presentations of one system can differ in sign-freedom while the net total
-- is untouched; that is the entire point of queries q1-q3.
-- ----------------------------------------------------------------------------
CREATE TABLE presentations (
    presentation_id INTEGER PRIMARY KEY,         -- surrogate key
    system_id       INTEGER NOT NULL REFERENCES systems(system_id),
                                                 -- the system this presentation writes down
    label           TEXT NOT NULL UNIQUE,        -- short label ('A_frustrated', 'B_meron_repaired')
    basis_note      TEXT NOT NULL,               -- what basis/re-presentation move produced it,
                                                 -- naming any witness (e.g. a sign-inverting,
                                                 -- weight-preserving involution) in plain words
    description     TEXT NOT NULL                -- fences and provenance for this presentation
);

-- ----------------------------------------------------------------------------
-- paths: walk configurations of a system — the many things a sum collapses
-- to one total.  Paths belong to the SYSTEM (they are the fibers of the
-- collapse map); their weights belong to a presentation (next table).
-- ----------------------------------------------------------------------------
CREATE TABLE paths (
    path_id     INTEGER PRIMARY KEY,             -- surrogate key
    system_id   INTEGER NOT NULL REFERENCES systems(system_id),
                                                 -- the system whose configuration this is
    label       TEXT NOT NULL,                   -- path label
    description TEXT NOT NULL                    -- what this configuration illustrates
);

-- ----------------------------------------------------------------------------
-- path_weights: SIGNED RATIONAL weights, one per (path, presentation).
-- Stored as integer numerator/denominator because EXACTNESS MATTERS: the
-- cancellation ratio |sum|/L1 must be an exact fraction, not a float that
-- might round a whisper to zero.  Signs live in num; den is strictly positive.
--
-- Exactness fence: SQLite has no rational aggregate.  The queries keep sums
-- exact by requiring a COMMON DENOMINATOR per presentation (checked in-query
-- via COUNT(DISTINCT den) = 1 — the guard column is printed, not assumed).
-- Seeds must honor that; a general exact rational aggregator would be a
-- further purchase this file does not make.
-- ----------------------------------------------------------------------------
CREATE TABLE path_weights (
    path_id         INTEGER NOT NULL REFERENCES paths(path_id),
                                                 -- the path being weighted
    presentation_id INTEGER NOT NULL REFERENCES presentations(presentation_id),
                                                 -- the presentation assigning the weight
    num             INTEGER NOT NULL,            -- signed numerator (the sign lives here)
    den             INTEGER NOT NULL CHECK (den > 0),
                                                 -- positive denominator (exact rational, no floats)
    PRIMARY KEY (path_id, presentation_id)       -- exactly one weight per path per presentation
);

-- ----------------------------------------------------------------------------
-- observers: the declared aggregations over paths — many-to-one collapse maps.
-- A sum is an act of forgetting: it sends many distinct weighted paths to one
-- total, and the total is all a downstream reader gets (rung 6).  The two
-- kinds seeded are the net signed sum and the gross L1 mass; their ratio is
-- the sign-problem severity the queries exhibit.
-- ----------------------------------------------------------------------------
CREATE TABLE observers (
    observer_id INTEGER PRIMARY KEY,             -- surrogate key
    name        TEXT NOT NULL UNIQUE,            -- observer name
    kind        TEXT NOT NULL CHECK (kind IN ('signed_sum', 'l1_sum')),
                                                 -- which aggregation this observer performs:
                                                 -- 'signed_sum' = SUM(num/den) (net, cancellation-blind
                                                 -- to path identity); 'l1_sum' = SUM(|num|/den) (gross)
    description TEXT NOT NULL                    -- what the observation forgets, in plain words
);

-- ----------------------------------------------------------------------------
-- obstructions: what blocks the naive continuation at each rung, each typed
-- and bound to the rung it blocks.  Terminals are plain words (no borrowed
-- enum): what actually happens when the block is hit.
-- ----------------------------------------------------------------------------
CREATE TABLE obstructions (
    obstruction_id   INTEGER PRIMARY KEY,        -- surrogate key
    rung_id          INTEGER NOT NULL REFERENCES rungs(rung_id),
                                                 -- the rung this obstruction blocks
    obstruction_type TEXT NOT NULL,              -- sort of block: inertia / collision / collapse /
                                                 -- unlicensed-structure / authority / complexity /
                                                 -- cancellation / misclassification / no-section
    name             TEXT NOT NULL UNIQUE,       -- obstruction name
    description      TEXT NOT NULL,              -- what exactly is blocked and why, plain words
    terminal         TEXT NOT NULL,              -- what happens at the block (plain words: e.g.
                                                 -- 'loud stop: purchase required before continuing')
    source           TEXT NOT NULL               -- citation grounding the block
);
