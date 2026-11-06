-- Non-Abelian Anyon Fusion, Braiding & Topological Compiling Schema
-- AuthorityEffect: None.
-- Dialect: ANSI SQL / SQLite 3 compatible

-- 1. Anyon Species & Model Configurations
CREATE TABLE IF NOT EXISTS AnyonSpecies (
    species_id INTEGER PRIMARY KEY AUTOINCREMENT,
    model TEXT NOT NULL CHECK (model IN ('FIBONACCI', 'ISING')),
    label TEXT NOT NULL,
    qdim REAL NOT NULL,
    topological_spin REAL NOT NULL,
    UNIQUE (model, label)
);

-- 2. Fusion Multiplicity Tensor N^{ab}_c
CREATE TABLE IF NOT EXISTS AnyonFusionRules (
    model TEXT NOT NULL CHECK (model IN ('FIBONACCI', 'ISING')),
    a TEXT NOT NULL,
    b TEXT NOT NULL,
    c TEXT NOT NULL,
    multiplicity INTEGER NOT NULL CHECK (multiplicity >= 0),
    PRIMARY KEY (model, a, b, c)
);

-- 3. 6j F-Symbols (Associators) F^{abc;d}_{e,f}
CREATE TABLE IF NOT EXISTS AnyonFSymbols (
    model TEXT NOT NULL CHECK (model IN ('FIBONACCI', 'ISING')),
    a TEXT NOT NULL,
    b TEXT NOT NULL,
    c TEXT NOT NULL,
    d TEXT NOT NULL,
    e TEXT NOT NULL,
    f TEXT NOT NULL,
    val REAL NOT NULL,
    PRIMARY KEY (model, a, b, c, d, e, f)
);

-- 4. Braiding R-Matrices R^{ab}_c
CREATE TABLE IF NOT EXISTS AnyonRMatrices (
    model TEXT NOT NULL CHECK (model IN ('FIBONACCI', 'ISING')),
    a TEXT NOT NULL,
    b TEXT NOT NULL,
    c TEXT NOT NULL,
    val_re REAL NOT NULL,
    val_im REAL NOT NULL,
    phase_rad REAL NOT NULL,
    PRIMARY KEY (model, a, b, c)
);

-- 5. Topological Gate Compiling Records
CREATE TABLE IF NOT EXISTS CompiledBraidWords (
    compilation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    model TEXT NOT NULL,
    target_gate TEXT NOT NULL,
    braid_word TEXT NOT NULL,
    word_length INTEGER NOT NULL,
    approximation_error REAL NOT NULL,
    is_unitary INTEGER NOT NULL CHECK (is_unitary IN (0, 1)),
    terminal_route TEXT NOT NULL CHECK (terminal_route IN ('Repair', 'SplitBrainRefusal', 'ClosureFailure'))
);

-- 6. Matrix Entries for Compiled Braid Unitaries
CREATE TABLE IF NOT EXISTS BraidMatrixEntries (
    compilation_id INTEGER NOT NULL,
    row_idx INTEGER NOT NULL CHECK (row_idx IN (0, 1)),
    col_idx INTEGER NOT NULL CHECK (col_idx IN (0, 1)),
    val_re REAL NOT NULL,
    val_im REAL NOT NULL,
    PRIMARY KEY (compilation_id, row_idx, col_idx),
    FOREIGN KEY (compilation_id) REFERENCES CompiledBraidWords(compilation_id)
);

-- ----------------------------------------------------------------------------
-- CTE Views: Fusion Associativity, Pentagon & Hexagon Consistency, Gate Audits
-- ----------------------------------------------------------------------------

-- View 1: Fusion Tensor Associativity Audit
-- Computes LHS = ∑_e N^{ab}_e * N^{ec}_d vs RHS = ∑_f N^{bc}_f * N^{af}_d
CREATE VIEW IF NOT EXISTS ViewFusionAssociativityAudit AS
WITH LHS AS (
    SELECT
        r1.model,
        r1.a,
        r1.b,
        r2.b AS c,
        r2.c AS d,
        SUM(r1.multiplicity * r2.multiplicity) AS lhs_channels
    FROM AnyonFusionRules r1
    JOIN AnyonFusionRules r2
      ON r1.model = r2.model
     AND r1.c = r2.a
    GROUP BY r1.model, r1.a, r1.b, r2.b, r2.c
),
RHS AS (
    SELECT
        r2.model,
        r2.a,
        r1.a AS b,
        r1.b AS c,
        r2.c AS d,
        SUM(r1.multiplicity * r2.multiplicity) AS rhs_channels
    FROM AnyonFusionRules r1
    JOIN AnyonFusionRules r2
      ON r1.model = r2.model
     AND r1.c = r2.b
    GROUP BY r2.model, r2.a, r1.a, r1.b, r2.c
)
SELECT
    l.model,
    l.a,
    l.b,
    l.c,
    l.d,
    l.lhs_channels,
    COALESCE(r.rhs_channels, 0) AS rhs_channels,
    ABS(l.lhs_channels - COALESCE(r.rhs_channels, 0)) AS channel_defect,
    CASE
        WHEN l.lhs_channels = COALESCE(r.rhs_channels, 0) THEN 'ASSOCIATIVE'
        ELSE 'ASSOCIATIVITY_BREACH'
    END AS associativity_status
FROM LHS l
LEFT JOIN RHS r
  ON l.model = r.model
 AND l.a = r.a
 AND l.b = r.b
 AND l.c = r.c
 AND l.d = r.d;

-- View 2: F-matrix involution audit (not a pentagon equation)
-- Evaluates the F-matrix involution / orthogonality property F^2 = Id
-- For Fibonacci and Ising anyons: ∑_k F_{i,k} F_{k,j} = δ_{i,j}
CREATE VIEW IF NOT EXISTS ViewFMatrixInvolutionAudit AS
WITH FProduct AS (
    SELECT
        f1.model,
        f1.a, f1.b, f1.c, f1.d,
        f1.e AS i,
        f2.f AS j,
        SUM(f1.val * f2.val) AS mat_product
    FROM AnyonFSymbols f1
    JOIN AnyonFSymbols f2
      ON f1.model = f2.model
     AND f1.a = f2.a AND f1.b = f2.b AND f1.c = f2.c AND f1.d = f2.d
     AND f1.f = f2.e
    GROUP BY f1.model, f1.a, f1.b, f1.c, f1.d, f1.e, f2.f
)
SELECT
    model,
    a, b, c, d,
    i, j,
    mat_product,
    CASE WHEN i = j THEN 1.0 ELSE 0.0 END AS identity_val,
    ABS(mat_product - (CASE WHEN i = j THEN 1.0 ELSE 0.0 END)) AS involution_residual,
    CASE
        WHEN ABS(mat_product - (CASE WHEN i = j THEN 1.0 ELSE 0.0 END)) < 1e-10 THEN 'INVOLUTION_CONSISTENT'
        ELSE 'INVOLUTION_VIOLATION'
    END AS status
FROM FProduct;

-- Full hexagon certification is not implemented.

-- View 4: Braid Matrix Unitarity Audit
-- Evaluates U^† U = Id for all compiled braid words:
-- ∑_k (U_{k, i})^* U_{k, j} = δ_{i, j}
CREATE VIEW IF NOT EXISTS ViewBraidUnitarityAudit AS
WITH UnitaryProducts AS (
    SELECT
        m1.compilation_id,
        m1.col_idx AS i,
        m2.col_idx AS j,
        -- (m1_re - i m1_im) * (m2_re + i m2_im)
        SUM(m1.val_re * m2.val_re + m1.val_im * m2.val_im) AS prod_re,
        SUM(m1.val_re * m2.val_im - m1.val_im * m2.val_re) AS prod_im
    FROM BraidMatrixEntries m1
    JOIN BraidMatrixEntries m2
      ON m1.compilation_id = m2.compilation_id
     AND m1.row_idx = m2.row_idx
    GROUP BY m1.compilation_id, m1.col_idx, m2.col_idx
)
SELECT
    p.compilation_id,
    w.target_gate,
    w.braid_word,
    MAX(CASE WHEN p.i = p.j THEN ABS(p.prod_re - 1.0) + ABS(p.prod_im)
             ELSE ABS(p.prod_re) + ABS(p.prod_im) END) AS max_unitarity_defect,
    CASE
        WHEN MAX(CASE WHEN p.i = p.j THEN ABS(p.prod_re - 1.0) + ABS(p.prod_im)
                      ELSE ABS(p.prod_re) + ABS(p.prod_im) END) < 1e-9 THEN 1
        ELSE 0
    END AS is_strictly_unitary
FROM UnitaryProducts p
JOIN CompiledBraidWords w ON p.compilation_id = w.compilation_id
GROUP BY p.compilation_id, w.target_gate, w.braid_word;

-- View 5: Topological Quantum Compiling Audit
-- Evaluates gate compilation fidelity and assigns BQNF terminal routing
CREATE VIEW IF NOT EXISTS ViewTopologicalCompilingAudit AS
SELECT
    w.compilation_id,
    w.model,
    w.target_gate,
    w.braid_word,
    w.word_length,
    w.approximation_error,
    u.is_strictly_unitary,
    (1.0 - w.approximation_error) AS compilation_fidelity,
    CASE
        WHEN w.terminal_route = 'ClosureFailure' THEN 'ClosureFailure'
        WHEN u.is_strictly_unitary = 1 AND w.approximation_error <= 0.05 THEN 'Repair'
        ELSE 'SplitBrainRefusal'
    END AS terminal_route,
    CASE
        WHEN w.terminal_route = 'ClosureFailure' THEN 'INVALID_BRAID_CLOSURE_FAILURE'
        WHEN u.is_strictly_unitary = 1 AND w.approximation_error <= 0.05 THEN 'TOPOLOGICAL_COMPILATION_CERTIFIED'
        ELSE 'COMPILATION_DEFECT'
    END AS compilation_status
FROM CompiledBraidWords w
JOIN ViewBraidUnitarityAudit u ON w.compilation_id = u.compilation_id;
