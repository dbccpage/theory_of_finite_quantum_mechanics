-- Bareiss Fraction-Free Integer Determinant via Relational State Transitions
-- AuthorityEffect: None

CREATE TABLE IF NOT EXISTS bareiss_matrix_state (
    matrix_id TEXT NOT NULL,
    step INTEGER NOT NULL,
    row_idx INTEGER NOT NULL,
    col_idx INTEGER NOT NULL,
    val INTEGER NOT NULL,
    PRIMARY KEY (matrix_id, step, row_idx, col_idx)
);

CREATE TABLE IF NOT EXISTS bareiss_pivots (
    matrix_id TEXT NOT NULL,
    step INTEGER NOT NULL,
    pivot_val INTEGER NOT NULL,
    sign_multiplier INTEGER NOT NULL,
    PRIMARY KEY (matrix_id, step)
);
