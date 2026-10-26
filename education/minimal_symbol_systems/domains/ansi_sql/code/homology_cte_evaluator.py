"""
General k-Simplicial Homology CTE Evaluator: Exact Rational Homology via SQL Gaussian Elimination
AuthorityEffect: None.
"""

import json
import sqlite3
from typing import Any, Dict, List


class HomologyCTEEvaluator:
    """
    Evaluates boundary operators, Stokes nilpotence (d_{k-1} ∘ d_k = 0), and computes
    rational homology groups H_k = Z_k / B_k and Betti numbers via SQL CTE Bareiss Gaussian elimination.
    """

    def __init__(self, in_memory: bool = True):
        self.conn = sqlite3.connect(":memory:" if in_memory else "homology.db")
        self.conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self):
        c = self.conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS complex_simplices (
                dim INTEGER NOT NULL,
                simplex_id TEXT PRIMARY KEY,
                vertices_json TEXT NOT NULL
            );
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS boundary_entries (
                dim INTEGER NOT NULL,
                face_id TEXT NOT NULL,
                simplex_id TEXT NOT NULL,
                weight INTEGER NOT NULL,
                PRIMARY KEY (dim, face_id, simplex_id)
            );
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS matrix_state (
                matrix_id TEXT NOT NULL,
                step INTEGER NOT NULL,
                row_idx INTEGER NOT NULL,
                col_idx INTEGER NOT NULL,
                val INTEGER NOT NULL,
                PRIMARY KEY (matrix_id, step, row_idx, col_idx)
            );
        """)
        self.conn.commit()

    def clear(self):
        c = self.conn.cursor()
        c.execute("DELETE FROM complex_simplices;")
        c.execute("DELETE FROM boundary_entries;")
        c.execute("DELETE FROM matrix_state;")
        self.conn.commit()

    def add_simplex(self, dim: int, simplex_id: str, vertices: List[str]):
        """Registers a k-simplex with an ordered list of vertices."""
        c = self.conn.cursor()
        c.execute(
            """
            INSERT OR REPLACE INTO complex_simplices (dim, simplex_id, vertices_json)
            VALUES (?, ?, ?);
        """,
            (dim, simplex_id, json.dumps(vertices)),
        )
        self.conn.commit()

    def build_boundaries(self):
        """
        Populates boundary_entries for each simplex using simplicial boundary formula:
        \\partial_k [v_0, ..., v_k] = \\sum_{i=0}^k (-1)^i [v_0, ..., \\hat{v}_i, ..., v_k].
        """
        c = self.conn.cursor()
        c.execute("DELETE FROM boundary_entries;")
        c.execute(
            "SELECT dim, simplex_id, vertices_json FROM complex_simplices WHERE dim > 0 ORDER BY dim ASC;"
        )
        rows = c.fetchall()
        for r in rows:
            dim = r["dim"]
            s_id = r["simplex_id"]
            verts = json.loads(r["vertices_json"])
            k = len(verts)
            for i in range(k):
                face_verts = verts[:i] + verts[i + 1 :]
                face_id = "-".join(face_verts)
                sign = 1 if i % 2 == 0 else -1
                c.execute(
                    """
                    INSERT OR REPLACE INTO boundary_entries (dim, face_id, simplex_id, weight)
                    VALUES (?, ?, ?, ?);
                """,
                    (dim, face_id, s_id, sign),
                )
        self.conn.commit()

    def verify_nilpotence(self, k: int) -> Dict[str, Any]:
        """
        Verifies via SQL CTE that d_{k-1} ∘ d_k = 0 identically.
        Returns a dictionary with non-zero count, details, and boolean verification.
        """
        sql = """
        WITH RECURSIVE
        BoundaryProductCTE AS (
            SELECT
                prev.face_id AS codimension_2_face,
                curr.simplex_id AS parent_k_simplex,
                SUM(prev.weight * curr.weight) AS net_incidence_weight,
                COUNT(*) AS contributing_paths
            FROM boundary_entries curr
            JOIN boundary_entries prev
              ON curr.face_id = prev.simplex_id
             AND prev.dim = curr.dim - 1
            WHERE curr.dim = :k
            GROUP BY prev.face_id, curr.simplex_id
        )
        SELECT
            codimension_2_face,
            parent_k_simplex,
            net_incidence_weight,
            contributing_paths
        FROM BoundaryProductCTE
        WHERE net_incidence_weight != 0;
        """
        c = self.conn.cursor()
        c.execute(sql, {"k": k})
        rows = c.fetchall()
        discrepancies = [dict(r) for r in rows]
        return {
            "dim": k,
            "nilpotence_holds": len(discrepancies) == 0,
            "violations_count": len(discrepancies),
            "violations": discrepancies,
        }

    def compute_boundary_rank(self, dim: int) -> int:
        """
        Computes rank(d_dim) using ANSI SQL CTE Bareiss fraction-free Gaussian elimination.
        Division is guaranteed exact over integers by Sylvester's determinant identity.
        """
        c = self.conn.cursor()
        c.execute(
            "SELECT DISTINCT face_id FROM boundary_entries WHERE dim = ? ORDER BY face_id;", (dim,)
        )
        rows = [r[0] for r in c.fetchall()]
        c.execute(
            "SELECT DISTINCT simplex_id FROM boundary_entries WHERE dim = ? ORDER BY simplex_id;",
            (dim,),
        )
        cols = [r[0] for r in c.fetchall()]

        R, C = len(rows), len(cols)
        if R == 0 or C == 0:
            return 0

        row_map = {name: i for i, name in enumerate(rows)}
        col_map = {name: j for j, name in enumerate(cols)}

        matrix_id = f"d_{dim}"
        c.execute("DELETE FROM matrix_state WHERE matrix_id = ?;", (matrix_id,))

        grid = [[0] * C for _ in range(R)]
        c.execute("SELECT face_id, simplex_id, weight FROM boundary_entries WHERE dim = ?;", (dim,))
        for f_id, s_id, w in c.fetchall():
            grid[row_map[f_id]][col_map[s_id]] = w

        for r in range(R):
            for col in range(C):
                c.execute(
                    "INSERT INTO matrix_state VALUES (?, 0, ?, ?, ?);",
                    (matrix_id, r, col, grid[r][col]),
                )
        self.conn.commit()

        step = 0
        curr_row = 0
        prev_pivot = 1

        for col in range(C):
            if curr_row >= R:
                break
            c.execute(
                """
                SELECT row_idx, val FROM matrix_state
                WHERE matrix_id = ? AND step = ? AND col_idx = ? AND row_idx >= ? AND val != 0
                ORDER BY row_idx ASC LIMIT 1;
            """,
                (matrix_id, step, col, curr_row),
            )
            piv = c.fetchone()
            if not piv:
                continue
            piv_row, piv_val = piv

            next_step = step + 1
            cte_sql = """
            INSERT INTO matrix_state (matrix_id, step, row_idx, col_idx, val)
            WITH SwappedState AS (
                SELECT
                    CASE
                        WHEN row_idx = :curr_row THEN :piv_row
                        WHEN row_idx = :piv_row THEN :curr_row
                        ELSE row_idx
                    END AS row_idx,
                    col_idx,
                    val
                FROM matrix_state
                WHERE matrix_id = :matrix_id AND step = :step
            ),
            PivotVal AS (
                SELECT val AS p_val FROM SwappedState
                WHERE row_idx = :curr_row AND col_idx = :col
            ),
            PivotRow AS (
                SELECT col_idx, val AS p_row_val FROM SwappedState
                WHERE row_idx = :curr_row
            ),
            LeadCol AS (
                SELECT row_idx, val AS lead_val FROM SwappedState
                WHERE col_idx = :col
            )
            SELECT
                :matrix_id,
                :next_step,
                s.row_idx,
                s.col_idx,
                CASE
                    WHEN s.row_idx <= :curr_row THEN s.val
                    ELSE (pv.p_val * s.val - lc.lead_val * pr.p_row_val) / :prev_pivot
                END AS val
            FROM SwappedState s
            JOIN PivotRow pr ON s.col_idx = pr.col_idx
            JOIN LeadCol lc ON s.row_idx = lc.row_idx
            CROSS JOIN PivotVal pv;
            """
            c.execute(
                cte_sql,
                {
                    "matrix_id": matrix_id,
                    "step": step,
                    "next_step": next_step,
                    "curr_row": curr_row,
                    "piv_row": piv_row,
                    "col": col,
                    "prev_pivot": prev_pivot,
                },
            )
            self.conn.commit()
            prev_pivot = piv_val
            curr_row += 1
            step = next_step

        c.execute(
            """
            SELECT COUNT(DISTINCT row_idx) FROM matrix_state
            WHERE matrix_id = ? AND step = ? AND val != 0;
        """,
            (matrix_id, step),
        )
        return c.fetchone()[0]

    def compute_homology(self, max_dim: int) -> Dict[str, Any]:
        """
        Computes f-vector, boundary ranks, Betti numbers beta_k, and Euler characteristic.
        Verifies Euler-Poincare identity: sum (-1)^k n_k = sum (-1)^k beta_k.
        """
        c = self.conn.cursor()
        f_vector = []
        for d in range(max_dim + 1):
            c.execute("SELECT COUNT(*) FROM complex_simplices WHERE dim = ?;", (d,))
            f_vector.append(c.fetchone()[0])

        ranks = {}
        for d in range(1, max_dim + 2):
            ranks[d] = self.compute_boundary_rank(d)

        # beta_k = n_k - rank(d_k) - rank(d_{k+1})
        betti_numbers = []
        for k in range(max_dim + 1):
            n_k = f_vector[k]
            rank_curr = ranks.get(k, 0)
            rank_next = ranks.get(k + 1, 0)
            dim_Z_k = n_k - rank_curr
            dim_B_k = rank_next
            beta_k = dim_Z_k - dim_B_k
            betti_numbers.append(beta_k)

        # Euler characteristic from f-vector and Betti numbers
        euler_f = sum((-1) ** k * f_vector[k] for k in range(max_dim + 1))
        euler_beta = sum((-1) ** k * betti_numbers[k] for k in range(max_dim + 1))

        return {
            "max_dim": max_dim,
            "f_vector": f_vector,
            "boundary_ranks": ranks,
            "betti_numbers": betti_numbers,
            "euler_characteristic_f": euler_f,
            "euler_characteristic_betti": euler_beta,
            "euler_poincare_verified": (euler_f == euler_beta),
        }

    def close(self):
        self.conn.close()
