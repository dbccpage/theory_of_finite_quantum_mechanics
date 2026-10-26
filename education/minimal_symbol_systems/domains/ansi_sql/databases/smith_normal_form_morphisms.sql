-- Smith Normal Form (SNF) Morphisms and Integral Homology CTE Evaluator
-- AuthorityEffect: None.

-- 1. Base Relational DDL for Integral Boundary Matrices and Transformations
CREATE TABLE IF NOT EXISTS snf_matrix_state (
    matrix_id TEXT NOT NULL,
    step INTEGER NOT NULL,
    row_idx INTEGER NOT NULL,
    col_idx INTEGER NOT NULL,
    val INTEGER NOT NULL,
    PRIMARY KEY (matrix_id, step, row_idx, col_idx)
);

CREATE TABLE IF NOT EXISTS snf_diagonal_factors (
    matrix_id TEXT NOT NULL,
    diag_idx INTEGER NOT NULL,
    factor INTEGER NOT NULL,
    PRIMARY KEY (matrix_id, diag_idx)
);

CREATE TABLE IF NOT EXISTS integral_homology_groups (
    complex_id TEXT NOT NULL,
    dim INTEGER NOT NULL,
    free_rank INTEGER NOT NULL,
    torsion_coefficients_json TEXT NOT NULL,
    PRIMARY KEY (complex_id, dim)
);

-- 2. Parameterized Elementary Operation CTEs:
-- A. Row Linear Combination CTE: Row(r_target) <- Row(r_target) - q * Row(r_src)
/*
INSERT INTO snf_matrix_state (matrix_id, step, row_idx, col_idx, val)
WITH SourceRow AS (
    SELECT col_idx, val AS src_val
    FROM snf_matrix_state
    WHERE matrix_id = :matrix_id AND step = :step AND row_idx = :src_row
)
SELECT 
    :matrix_id,
    :next_step,
    m.row_idx,
    m.col_idx,
    CASE 
        WHEN m.row_idx = :target_row THEN m.val - :q * sr.src_val
        ELSE m.val
    END AS val
FROM snf_matrix_state m
JOIN SourceRow sr ON m.col_idx = sr.col_idx
WHERE m.matrix_id = :matrix_id AND m.step = :step;
*/

-- B. Column Linear Combination CTE: Col(c_target) <- Col(c_target) - q * Col(c_src)
/*
INSERT INTO snf_matrix_state (matrix_id, step, row_idx, col_idx, val)
WITH SourceCol AS (
    SELECT row_idx, val AS src_val
    FROM snf_matrix_state
    WHERE matrix_id = :matrix_id AND step = :step AND col_idx = :src_col
)
SELECT 
    :matrix_id,
    :next_step,
    m.row_idx,
    m.col_idx,
    CASE 
        WHEN m.col_idx = :target_col THEN m.val - :q * sc.src_val
        ELSE m.val
    END AS val
FROM snf_matrix_state m
JOIN SourceCol sc ON m.row_idx = sc.row_idx
WHERE m.matrix_id = :matrix_id AND m.step = :step;
*/

-- C. Row Swap CTE
/*
INSERT INTO snf_matrix_state (matrix_id, step, row_idx, col_idx, val)
SELECT 
    matrix_id,
    :next_step,
    CASE 
        WHEN row_idx = :r1 THEN :r2
        WHEN row_idx = :r2 THEN :r1
        ELSE row_idx
    END AS row_idx,
    col_idx,
    val
FROM snf_matrix_state
WHERE matrix_id = :matrix_id AND step = :step;
*/

-- D. Column Swap CTE
/*
INSERT INTO snf_matrix_state (matrix_id, step, row_idx, col_idx, val)
SELECT 
    matrix_id,
    :next_step,
    row_idx,
    CASE 
        WHEN col_idx = :c1 THEN :c2
        WHEN col_idx = :c2 THEN :c1
        ELSE col_idx
    END AS col_idx,
    val
FROM snf_matrix_state
WHERE matrix_id = :matrix_id AND step = :step;
*/

-- E. Pivot Sign Normalization CTE
/*
INSERT INTO snf_matrix_state (matrix_id, step, row_idx, col_idx, val)
SELECT 
    matrix_id,
    :next_step,
    row_idx,
    col_idx,
    CASE WHEN row_idx = :curr_diag THEN -val ELSE val END AS val
FROM snf_matrix_state
WHERE matrix_id = :matrix_id AND step = :step;
*/

-- 3. Invariant Factor & Torsion Classification Query
-- Elementary divisors d_i > 1 represent integral torsion summands Z / d_i Z.
SELECT 
    matrix_id,
    diag_idx,
    val AS invariant_factor,
    CASE 
        WHEN val = 1 THEN 'Trivial Quotient (Z / 1Z = 0)'
        WHEN val > 1 THEN 'Torsion Subgroup (Z / ' || val || 'Z)'
        ELSE 'Kernel Zero Divisor'
    END AS algebraic_structure
FROM snf_matrix_state
WHERE row_idx = col_idx AND val > 0
ORDER BY diag_idx ASC;
