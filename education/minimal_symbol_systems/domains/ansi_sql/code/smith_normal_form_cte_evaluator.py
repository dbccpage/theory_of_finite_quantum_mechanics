"""
Smith Normal Form CTE Evaluator: Integral Homology and Torsion Coefficient Evaluation
AuthorityEffect: None.
"""

import sqlite3
from typing import Any, Dict, List, Tuple


class SmithNormalFormCTEEvaluator:
    """
    Evaluates boundary matrices over Z using relational ANSI SQL CTE elementary operations
    to compute canonical Smith Normal Form (SNF) invariant factors and integral homology groups:
    H_k(K; Z) ≅ Z^{beta_k} ⊕ ⨁_i (Z / d_i Z).
    """

    def __init__(self, in_memory: bool = True):
        self.conn = sqlite3.connect(":memory:" if in_memory else "snf.db")
        self.conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self):
        c = self.conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS snf_matrix_state (
                matrix_id TEXT NOT NULL,
                step INTEGER NOT NULL,
                row_idx INTEGER NOT NULL,
                col_idx INTEGER NOT NULL,
                val INTEGER NOT NULL,
                PRIMARY KEY (matrix_id, step, row_idx, col_idx)
            );
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS snf_diagonal_factors (
                matrix_id TEXT NOT NULL,
                diag_idx INTEGER NOT NULL,
                factor INTEGER NOT NULL,
                PRIMARY KEY (matrix_id, diag_idx)
            );
        """)
        self.conn.commit()

    def clear(self):
        c = self.conn.cursor()
        c.execute("DELETE FROM snf_matrix_state;")
        c.execute("DELETE FROM snf_diagonal_factors;")
        self.conn.commit()

    def load_matrix(self, matrix_id: str, grid: List[List[int]]) -> Tuple[int, int]:
        """Loads an integer matrix grid into snf_matrix_state at step 0."""
        R = len(grid)
        C = len(grid[0]) if R > 0 else 0
        c = self.conn.cursor()
        c.execute("DELETE FROM snf_matrix_state WHERE matrix_id = ?;", (matrix_id,))
        for r in range(R):
            for col in range(C):
                c.execute(
                    "INSERT INTO snf_matrix_state VALUES (?, 0, ?, ?, ?);",
                    (matrix_id, r, col, grid[r][col]),
                )
        self.conn.commit()
        return R, C

    def compute_snf(self, matrix_id: str, R: int, C: int) -> Dict[str, Any]:
        """
        Executes Smith Normal Form reduction over Z using relational SQL CTE elementary operations:
        - Row and column swaps
        - Row and column linear combinations (Euclidean reduction)
        - Pivot sign normalizations
        - Invariant factor divisibility pass (d_i | d_{i+1})
        """
        c = self.conn.cursor()
        step = 0
        curr_diag = 0
        limit_diag = min(R, C)

        while curr_diag < limit_diag:
            # 1. Find pivot with smallest non-zero absolute value in submatrix [curr_diag..R-1, curr_diag..C-1]
            c.execute(
                """
                SELECT row_idx, col_idx, val FROM snf_matrix_state
                WHERE matrix_id = ? AND step = ? AND row_idx >= ? AND col_idx >= ? AND val != 0
                ORDER BY ABS(val) ASC LIMIT 1;
            """,
                (matrix_id, step, curr_diag, curr_diag),
            )
            piv = c.fetchone()
            if not piv:
                break
            piv_r, piv_c, _piv_val = piv["row_idx"], piv["col_idx"], piv["val"]

            # Row swap CTE if piv_r != curr_diag
            if piv_r != curr_diag:
                next_step = step + 1
                c.execute(
                    """
                    INSERT INTO snf_matrix_state (matrix_id, step, row_idx, col_idx, val)
                    SELECT matrix_id, :next_step,
                        CASE
                            WHEN row_idx = :curr THEN :piv_r
                            WHEN row_idx = :piv_r THEN :curr
                            ELSE row_idx
                        END AS row_idx,
                        col_idx, val
                    FROM snf_matrix_state
                    WHERE matrix_id = :matrix_id AND step = :step;
                """,
                    {
                        "matrix_id": matrix_id,
                        "step": step,
                        "next_step": next_step,
                        "curr": curr_diag,
                        "piv_r": piv_r,
                    },
                )
                self.conn.commit()
                step = next_step

            # Col swap CTE if piv_c != curr_diag
            if piv_c != curr_diag:
                next_step = step + 1
                c.execute(
                    """
                    INSERT INTO snf_matrix_state (matrix_id, step, row_idx, col_idx, val)
                    SELECT matrix_id, :next_step,
                        row_idx,
                        CASE
                            WHEN col_idx = :curr THEN :piv_c
                            WHEN col_idx = :piv_c THEN :curr
                            ELSE col_idx
                        END AS col_idx, val
                    FROM snf_matrix_state
                    WHERE matrix_id = :matrix_id AND step = :step;
                """,
                    {
                        "matrix_id": matrix_id,
                        "step": step,
                        "next_step": next_step,
                        "curr": curr_diag,
                        "piv_c": piv_c,
                    },
                )
                self.conn.commit()
                step = next_step

            # Read current pivot value
            c.execute(
                """
                SELECT val FROM snf_matrix_state
                WHERE matrix_id = ? AND step = ? AND row_idx = ? AND col_idx = ?;
            """,
                (matrix_id, step, curr_diag, curr_diag),
            )
            curr_val = c.fetchone()["val"]

            # 2. Check and eliminate row and column
            cleared = True

            # Eliminate other rows in curr_diag column
            c.execute(
                """
                SELECT row_idx, val FROM snf_matrix_state
                WHERE matrix_id = ? AND step = ? AND col_idx = ? AND row_idx > ? AND val != 0;
            """,
                (matrix_id, step, curr_diag, curr_diag),
            )
            other_rows = c.fetchall()
            for row_cand in other_rows:
                r_idx, val = row_cand["row_idx"], row_cand["val"]
                q = val // curr_val
                if q != 0:
                    next_step = step + 1
                    c.execute(
                        """
                        INSERT INTO snf_matrix_state (matrix_id, step, row_idx, col_idx, val)
                        WITH SourceRow AS (
                            SELECT col_idx, val AS src_val FROM snf_matrix_state
                            WHERE matrix_id = :matrix_id AND step = :step AND row_idx = :src_row
                        )
                        SELECT :matrix_id, :next_step, m.row_idx, m.col_idx,
                            CASE
                                WHEN m.row_idx = :target_row THEN m.val - :q * sr.src_val
                                ELSE m.val
                            END AS val
                        FROM snf_matrix_state m
                        JOIN SourceRow sr ON m.col_idx = sr.col_idx
                        WHERE m.matrix_id = :matrix_id AND m.step = :step;
                    """,
                        {
                            "matrix_id": matrix_id,
                            "step": step,
                            "next_step": next_step,
                            "src_row": curr_diag,
                            "target_row": r_idx,
                            "q": q,
                        },
                    )
                    self.conn.commit()
                    step = next_step
                    if val - q * curr_val != 0:
                        cleared = False
                        break
            if not cleared:
                continue

            # Eliminate other cols in curr_diag row
            c.execute(
                """
                SELECT col_idx, val FROM snf_matrix_state
                WHERE matrix_id = ? AND step = ? AND row_idx = ? AND col_idx > ? AND val != 0;
            """,
                (matrix_id, step, curr_diag, curr_diag),
            )
            other_cols = c.fetchall()
            for col_cand in other_cols:
                c_idx, val = col_cand["col_idx"], col_cand["val"]
                q = val // curr_val
                if q != 0:
                    next_step = step + 1
                    c.execute(
                        """
                        INSERT INTO snf_matrix_state (matrix_id, step, row_idx, col_idx, val)
                        WITH SourceCol AS (
                            SELECT row_idx, val AS src_val FROM snf_matrix_state
                            WHERE matrix_id = :matrix_id AND step = :step AND col_idx = :src_col
                        )
                        SELECT :matrix_id, :next_step, m.row_idx, m.col_idx,
                            CASE
                                WHEN m.col_idx = :target_col THEN m.val - :q * sc.src_val
                                ELSE m.val
                            END AS val
                        FROM snf_matrix_state m
                        JOIN SourceCol sc ON m.row_idx = sc.row_idx
                        WHERE m.matrix_id = :matrix_id AND m.step = :step;
                    """,
                        {
                            "matrix_id": matrix_id,
                            "step": step,
                            "next_step": next_step,
                            "src_col": curr_diag,
                            "target_col": c_idx,
                            "q": q,
                        },
                    )
                    self.conn.commit()
                    step = next_step
                    if val - q * curr_val != 0:
                        cleared = False
                        break
            if not cleared:
                continue

            # Normalize sign of pivot if negative
            c.execute(
                """
                SELECT val FROM snf_matrix_state
                WHERE matrix_id = ? AND step = ? AND row_idx = ? AND col_idx = ?;
            """,
                (matrix_id, step, curr_diag, curr_diag),
            )
            p_val = c.fetchone()["val"]
            if p_val < 0:
                next_step = step + 1
                c.execute(
                    """
                    INSERT INTO snf_matrix_state (matrix_id, step, row_idx, col_idx, val)
                    SELECT matrix_id, :next_step, row_idx, col_idx,
                        CASE WHEN row_idx = :curr THEN -val ELSE val END AS val
                    FROM snf_matrix_state
                    WHERE matrix_id = :matrix_id AND step = :step;
                """,
                    {
                        "matrix_id": matrix_id,
                        "step": step,
                        "next_step": next_step,
                        "curr": curr_diag,
                    },
                )
                self.conn.commit()
                step = next_step
                curr_val = -p_val

            # Check divisibility condition with any previously established diagonal entries
            found_indivisible = False
            for prev_d in range(curr_diag):
                c.execute(
                    """
                    SELECT val FROM snf_matrix_state
                    WHERE matrix_id = ? AND step = ? AND row_idx = ? AND col_idx = ?;
                """,
                    (matrix_id, step, prev_d, prev_d),
                )
                d_prev = c.fetchone()["val"]
                if d_prev != 0 and curr_val % d_prev != 0:
                    # Add row curr_diag to row prev_d
                    next_step = step + 1
                    c.execute(
                        """
                        INSERT INTO snf_matrix_state (matrix_id, step, row_idx, col_idx, val)
                        WITH SourceRow AS (
                            SELECT col_idx, val AS src_val FROM snf_matrix_state
                            WHERE matrix_id = :matrix_id AND step = :step AND row_idx = :src_row
                        )
                        SELECT :matrix_id, :next_step, m.row_idx, m.col_idx,
                            CASE
                                WHEN m.row_idx = :target_row THEN m.val + sr.src_val
                                ELSE m.val
                            END AS val
                        FROM snf_matrix_state m
                        JOIN SourceRow sr ON m.col_idx = sr.col_idx
                        WHERE m.matrix_id = :matrix_id AND m.step = :step;
                    """,
                        {
                            "matrix_id": matrix_id,
                            "step": step,
                            "next_step": next_step,
                            "src_row": curr_diag,
                            "target_row": prev_d,
                        },
                    )
                    self.conn.commit()
                    step = next_step
                    curr_diag = prev_d
                    found_indivisible = True
                    break
            if found_indivisible:
                continue

            curr_diag += 1

        # Extract diagonal elements
        c.execute(
            """
            SELECT row_idx, val FROM snf_matrix_state
            WHERE matrix_id = ? AND step = ? AND row_idx = col_idx AND val != 0
            ORDER BY row_idx ASC;
        """,
            (matrix_id, step),
        )
        diag = [r["val"] for r in c.fetchall()]

        # Record in snf_diagonal_factors
        c.execute("DELETE FROM snf_diagonal_factors WHERE matrix_id = ?;", (matrix_id,))
        for idx, factor in enumerate(diag):
            c.execute(
                "INSERT INTO snf_diagonal_factors VALUES (?, ?, ?);", (matrix_id, idx, factor)
            )
        self.conn.commit()

        torsion = [d for d in diag if d > 1]
        return {
            "matrix_id": matrix_id,
            "rank": len(diag),
            "diagonal_factors": diag,
            "torsion_coefficients": torsion,
            "total_cte_steps": step,
        }

    def close(self):
        self.conn.close()
