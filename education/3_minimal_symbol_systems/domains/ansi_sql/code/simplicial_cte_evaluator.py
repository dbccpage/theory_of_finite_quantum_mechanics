"""
Simplicial CTE Evaluator: Relational Execution of Boundary Operators and Stokes Nilpotence
AuthorityEffect: None.
"""

import sqlite3
from typing import Any, Dict, List, Optional, Tuple


class SimplicialCTEEvaluator:
    def __init__(self, in_memory: bool = True):
        self.conn = sqlite3.connect(":memory:" if in_memory else "simplicial.db")
        self.conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS simplices (
                simplex_id TEXT PRIMARY KEY,
                dim INTEGER NOT NULL,
                v0 TEXT NOT NULL,
                v1 TEXT,
                v2 TEXT
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS boundary_faces (
                parent_id TEXT NOT NULL,
                face_id TEXT NOT NULL,
                face_dim INTEGER NOT NULL,
                signed_weight INTEGER NOT NULL,
                PRIMARY KEY (parent_id, face_id)
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS lattice_vertices (
                vertex_id TEXT PRIMARY KEY,
                dual_area REAL NOT NULL DEFAULT 1.0,
                phi_val REAL NOT NULL DEFAULT 0.0
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS lattice_edges (
                edge_id TEXT PRIMARY KEY,
                src TEXT NOT NULL,
                dst TEXT NOT NULL,
                length REAL NOT NULL DEFAULT 1.0,
                dual_length REAL NOT NULL DEFAULT 1.0,
                hodge_star1 REAL NOT NULL DEFAULT 1.0
            );
        """)
        self.conn.commit()

    def add_lattice_vertex(self, vertex_id: str, dual_area: float = 1.0, phi_val: float = 0.0):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT OR REPLACE INTO lattice_vertices (vertex_id, dual_area, phi_val)
            VALUES (?, ?, ?);
        """,
            (vertex_id, dual_area, phi_val),
        )
        self.conn.commit()

    def add_lattice_edge(
        self,
        edge_id: str,
        src: str,
        dst: str,
        length: float = 1.0,
        dual_length: float = 1.0,
        hodge_star1: Optional[float] = None,
    ):
        star1 = (dual_length / length) if hodge_star1 is None else hodge_star1
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT OR REPLACE INTO lattice_edges (edge_id, src, dst, length, dual_length, hodge_star1)
            VALUES (?, ?, ?, ?, ?, ?);
        """,
            (edge_id, src, dst, length, dual_length, star1),
        )
        self.conn.commit()

    def set_0form_values(self, form0_map: Dict[str, float]):
        cursor = self.conn.cursor()
        for vid, val in form0_map.items():
            cursor.execute(
                """
                INSERT INTO lattice_vertices (vertex_id, dual_area, phi_val)
                VALUES (?, 1.0, ?)
                ON CONFLICT(vertex_id) DO UPDATE SET phi_val = excluded.phi_val;
            """,
                (vid, val),
            )
        self.conn.commit()

    def add_triangle(self, simplex_id: str, v0: str, v1: str, v2: str):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT OR REPLACE INTO simplices (simplex_id, dim, v0, v1, v2)
            VALUES (?, 2, ?, ?, ?);
        """,
            (simplex_id, v0, v1, v2),
        )
        # Ensure vertices exist in lattice_vertices
        for v in (v0, v1, v2):
            cursor.execute(
                """
                INSERT OR IGNORE INTO lattice_vertices (vertex_id, dual_area, phi_val)
                VALUES (?, 1.0, 0.0);
            """,
                (v,),
            )
        # Ensure edges exist in lattice_edges only if no edge connects them
        default_edges = [
            (f"{v0}->{v1}", v0, v1),
            (f"{v1}->{v2}", v1, v2),
            (f"{v0}->{v2}", v0, v2),
        ]
        for eid, src, dst in default_edges:
            cursor.execute(
                """
                SELECT 1 FROM lattice_edges
                WHERE (src = ? AND dst = ?) OR (src = ? AND dst = ?);
            """,
                (src, dst, dst, src),
            )
            if cursor.fetchone() is None:
                cursor.execute(
                    """
                    INSERT INTO lattice_edges (edge_id, src, dst, length, dual_length, hodge_star1)
                    VALUES (?, ?, ?, 1.0, 1.0, 1.0);
                """,
                    (eid, src, dst),
                )
        self.conn.commit()

    def evaluate_boundaries_and_nilpotence(self) -> Dict[str, Any]:
        """
        Executes the CTE evaluating d_1 ∘ d_2 and checking that every vertex multiplicity sums to 0.
        """
        sql = """
        WITH RECURSIVE
        BoundaryEdges AS (
            SELECT
                simplex_id AS parent_id,
                v1 || '->' || v2 AS edge_id,
                v1 AS src,
                v2 AS dst,
                1 AS edge_weight
            FROM simplices
            WHERE dim = 2

            UNION ALL

            SELECT
                simplex_id AS parent_id,
                v0 || '->' || v2 AS edge_id,
                v0 AS src,
                v2 AS dst,
                -1 AS edge_weight
            FROM simplices
            WHERE dim = 2

            UNION ALL

            SELECT
                simplex_id AS parent_id,
                v0 || '->' || v1 AS edge_id,
                v0 AS src,
                v1 AS dst,
                1 AS edge_weight
            FROM simplices
            WHERE dim = 2
        ),
        BoundaryVertices AS (
            SELECT
                parent_id,
                edge_id,
                dst AS vertex,
                edge_weight * 1 AS vertex_weight
            FROM BoundaryEdges

            UNION ALL

            SELECT
                parent_id,
                edge_id,
                src AS vertex,
                edge_weight * (-1) AS vertex_weight
            FROM BoundaryEdges
        ),
        BoundaryNilpotenceEvaluation AS (
            SELECT
                parent_id,
                vertex,
                SUM(vertex_weight) AS net_multiplicity,
                COUNT(*) AS term_count
            FROM BoundaryVertices
            GROUP BY parent_id, vertex
        )
        SELECT
            parent_id,
            vertex,
            net_multiplicity,
            term_count,
            CASE WHEN net_multiplicity = 0 THEN 1 ELSE 0 END AS nilpotence_verified
        FROM BoundaryNilpotenceEvaluation;
        """
        cursor = self.conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()

        all_zero = True
        results = []
        for r in rows:
            results.append(
                {
                    "parent_id": r["parent_id"],
                    "vertex": r["vertex"],
                    "net_multiplicity": r["net_multiplicity"],
                    "term_count": r["term_count"],
                    "nilpotence_verified": bool(r["nilpotence_verified"]),
                }
            )
            if r["net_multiplicity"] != 0:
                all_zero = False

        return {
            "evaluations": results,
            "stokes_nilpotence_holds": all_zero and len(results) > 0,
            "total_vertex_evaluations": len(results),
        }

    def compute_window_quotient_orbits(self) -> List[Dict[str, Any]]:
        """
        Executes window function OVER (PARTITION BY ...) grouping edges by geometric orbit.
        """
        sql = """
        WITH BoundaryEdges AS (
            SELECT
                simplex_id AS parent_id,
                v1 || '->' || v2 AS edge_id,
                v1 AS src,
                v2 AS dst,
                1 AS edge_weight
            FROM simplices
            WHERE dim = 2

            UNION ALL

            SELECT
                simplex_id AS parent_id,
                v0 || '->' || v2 AS edge_id,
                v0 AS src,
                v2 AS dst,
                -1 AS edge_weight
            FROM simplices
            WHERE dim = 2

            UNION ALL

            SELECT
                simplex_id AS parent_id,
                v0 || '->' || v1 AS edge_id,
                v0 AS src,
                v1 AS dst,
                1 AS edge_weight
            FROM simplices
            WHERE dim = 2
        )
        SELECT
            parent_id,
            edge_id,
            src,
            dst,
            edge_weight,
            COUNT(*) OVER (
                PARTITION BY CASE WHEN src < dst THEN src || '<->' || dst ELSE dst || '<->' || src END
            ) AS orbit_multiplicity,
            CASE WHEN src < dst THEN src || '<->' || dst ELSE dst || '<->' || src END AS geometric_orbit_id
        FROM BoundaryEdges;
        """
        cursor = self.conn.cursor()
        cursor.execute(sql)
        return [dict(r) for r in cursor.fetchall()]

    def evaluate_bounded_degree_homology_cte(
        self, max_degree: int, target_simplex_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Executes bounded-degree recursive simplicial homology boundary descent:
        C_2 -> C_1 -> C_0 bounded by max_degree depth limit.
        Matches Scenario 4 Steps 08/09 fuel semantics.
        Optionally filters to target_simplex_id if specified.
        """
        cursor = self.conn.cursor()

        # Count triangles first
        if target_simplex_id is not None:
            cursor.execute(
                "SELECT COUNT(*) AS tri_count FROM simplices WHERE dim = 2 AND simplex_id = ?;",
                (target_simplex_id,),
            )
        else:
            cursor.execute("SELECT COUNT(*) AS tri_count FROM simplices WHERE dim = 2;")
        tri_count = cursor.fetchone()["tri_count"]
        if tri_count == 0:
            return {
                "max_degree": max_degree,
                "steps_taken": 0,
                "fuel_remaining": max_degree,
                "terminal_dim": 0,
                "status": "HALTED",
                "nilpotence_certified": True,
                "edge_count": 0,
                "vertex_evaluations": [],
            }

        sql = """
        WITH RECURSIVE HomologyBoundaryDescent(
            step, dim, parent_id, element_id, src, dst, weight
        ) AS (
            SELECT
                0 AS step,
                2 AS dim,
                simplex_id AS parent_id,
                simplex_id AS element_id,
                v0 AS src,
                v1 AS dst,
                1 AS weight
            FROM simplices
            WHERE dim = 2 AND (? IS NULL OR simplex_id = ?)

            UNION ALL

            SELECT
                1 AS step,
                1 AS dim,
                s.simplex_id AS parent_id,
                CASE e.edge_idx
                    WHEN 0 THEN s.v1 || '->' || s.v2
                    WHEN 1 THEN s.v0 || '->' || s.v2
                    WHEN 2 THEN s.v0 || '->' || s.v1
                END AS element_id,
                CASE e.edge_idx
                    WHEN 0 THEN s.v1
                    WHEN 1 THEN s.v0
                    WHEN 2 THEN s.v0
                END AS src,
                CASE e.edge_idx
                    WHEN 0 THEN s.v2
                    WHEN 1 THEN s.v2
                    WHEN 2 THEN s.v1
                END AS dst,
                CASE e.edge_idx
                    WHEN 0 THEN 1
                    WHEN 1 THEN -1
                    WHEN 2 THEN 1
                END AS weight
            FROM HomologyBoundaryDescent h
            JOIN simplices s ON h.element_id = s.simplex_id AND h.dim = 2
            CROSS JOIN (SELECT 0 AS edge_idx UNION ALL SELECT 1 UNION ALL SELECT 2) e
            WHERE h.step < ?

            UNION ALL

            SELECT
                2 AS step,
                0 AS dim,
                h.parent_id,
                CASE v.v_idx
                    WHEN 0 THEN h.dst
                    WHEN 1 THEN h.src
                END AS element_id,
                '' AS src,
                '' AS dst,
                CASE v.v_idx
                    WHEN 0 THEN h.weight * 1
                    WHEN 1 THEN h.weight * (-1)
                END AS weight
            FROM HomologyBoundaryDescent h
            CROSS JOIN (SELECT 0 AS v_idx UNION ALL SELECT 1) v
            WHERE h.dim = 1 AND h.step < ?
        )
        SELECT step, dim, parent_id, element_id, src, dst, weight
        FROM HomologyBoundaryDescent
        ORDER BY step, parent_id, element_id;
        """
        cursor.execute(sql, (target_simplex_id, target_simplex_id, max_degree, max_degree))
        rows = [dict(r) for r in cursor.fetchall()]

        max((r["step"] for r in rows), default=0)
        terminal_dim = min((r["dim"] for r in rows), default=2)

        edge_rows = [r for r in rows if r["dim"] == 1]
        vertex_rows = [r for r in rows if r["dim"] == 0]

        if terminal_dim == 0:
            # Reached degree 0 (vertices) -> boundary sequence terminated normally
            status = "HALTED"
            steps_taken = 2
            fuel_remaining = max_degree - 2

            # Evaluate Stokes nilpotence at degree 0
            nilpotence_map: Dict[Tuple[str, str], int] = {}
            for vr in vertex_rows:
                key = (vr["parent_id"], vr["element_id"])
                nilpotence_map[key] = nilpotence_map.get(key, 0) + vr["weight"]

            nilpotence_certified = len(nilpotence_map) > 0 and all(
                w == 0 for w in nilpotence_map.values()
            )
            vertex_evals = [
                {"parent_id": pid, "vertex": v, "net_multiplicity": net}
                for (pid, v), net in nilpotence_map.items()
            ]
        elif terminal_dim == 1:
            # Stopped at edges (dim 1) due to max_degree = 1
            status = "OUT_OF_FUEL"
            steps_taken = 1
            fuel_remaining = 0
            nilpotence_certified = False
            vertex_evals = []
        else:
            # Stopped at triangles (dim 2) due to max_degree = 0
            status = "OUT_OF_FUEL"
            steps_taken = 0
            fuel_remaining = 0
            nilpotence_certified = False
            vertex_evals = []

        return {
            "max_degree": max_degree,
            "steps_taken": steps_taken,
            "fuel_remaining": fuel_remaining,
            "terminal_dim": terminal_dim,
            "status": status,
            "nilpotence_certified": nilpotence_certified,
            "edge_count": len(edge_rows),
            "vertex_evaluations": vertex_evals,
        }

    def evaluate_derham_hodge_cte(
        self,
        max_fuel: int,
        form0_map: Optional[Dict[str, float]] = None,
    ) -> Dict[str, Any]:
        """
        Executes Discrete Exterior Calculus (DEC) de Rham differential forms and Hodge star evaluation:
        Stage 0 (0-forms) -> Stage 1 (1-forms d0 φ & de Rham nilpotence) -> Stage 2 (dual Hodge star ⋆_1 & Laplacian Δ_0).
        Bounded by max_fuel limit.
        """
        cursor = self.conn.cursor()
        if form0_map:
            self.set_0form_values(form0_map)

        cursor.execute("SELECT COUNT(*) AS v_count FROM lattice_vertices;")
        v_count = cursor.fetchone()["v_count"]
        if v_count == 0:
            return {
                "max_fuel": max_fuel,
                "steps_taken": 0,
                "fuel_remaining": max_fuel,
                "terminal_stage": 0,
                "status": "HALTED" if max_fuel >= 2 else "OUT_OF_FUEL",
                "laplacian_closed": max_fuel >= 2,
                "hodge_dual_closed": max_fuel >= 2,
                "nilpotence_certified": True,
                "form0": {},
                "form1": {},
                "laplacian": {},
            }

        # SQL CTE to evaluate the fuel-bounded stages
        sql = """
        WITH RECURSIVE FuelCounter(step) AS (
            SELECT 0
            UNION ALL
            SELECT step + 1 FROM FuelCounter WHERE step < ?
        ),
        Form0_CTE AS (
            SELECT vertex_id, phi_val, dual_area
            FROM lattice_vertices
        ),
        Form1_CTE AS (
            SELECT
                e.edge_id,
                e.src,
                e.dst,
                (v_dst.phi_val - v_src.phi_val) AS d0_val,
                e.hodge_star1,
                e.hodge_star1 * (v_dst.phi_val - v_src.phi_val) AS star1_d0_val
            FROM lattice_edges e
            JOIN lattice_vertices v_src ON e.src = v_src.vertex_id
            JOIN lattice_vertices v_dst ON e.dst = v_dst.vertex_id
            WHERE EXISTS (SELECT 1 FROM FuelCounter WHERE step >= 1)
        ),
        Laplacian_CTE AS (
            SELECT
                v.vertex_id,
                COALESCE(
                    SUM(
                        CASE
                            WHEN e.src = v.vertex_id THEN e.hodge_star1 * (v.phi_val - v_nbr_dst.phi_val)
                            WHEN e.dst = v.vertex_id THEN e.hodge_star1 * (v.phi_val - v_nbr_src.phi_val)
                            ELSE 0.0
                        END
                    ) / NULLIF(v.dual_area, 0.0),
                    0.0
                ) AS laplacian_val
            FROM lattice_vertices v
            LEFT JOIN lattice_edges e ON e.src = v.vertex_id OR e.dst = v.vertex_id
            LEFT JOIN lattice_vertices v_nbr_dst ON e.dst = v_nbr_dst.vertex_id AND e.src = v.vertex_id
            LEFT JOIN lattice_vertices v_nbr_src ON e.src = v_nbr_src.vertex_id AND e.dst = v.vertex_id
            WHERE EXISTS (SELECT 1 FROM FuelCounter WHERE step >= 2)
            GROUP BY v.vertex_id
        )
        SELECT
            (SELECT COUNT(*) FROM Form0_CTE) AS f0_count,
            (SELECT COUNT(*) FROM Form1_CTE) AS f1_count,
            (SELECT COUNT(*) FROM Laplacian_CTE) AS lap_count;
        """
        cursor.execute(sql, (max_fuel,))
        _ = cursor.fetchone()

        cursor.execute(
            "SELECT vertex_id, phi_val, dual_area FROM lattice_vertices ORDER BY vertex_id;"
        )
        form0_dict = {row["vertex_id"]: float(row["phi_val"]) for row in cursor.fetchall()}

        if max_fuel >= 1:
            sql_f1 = """
            SELECT
                e.edge_id, e.src, e.dst,
                (v_dst.phi_val - v_src.phi_val) AS d0_val,
                e.hodge_star1 * (v_dst.phi_val - v_src.phi_val) AS star1_d0_val
            FROM lattice_edges e
            JOIN lattice_vertices v_src ON e.src = v_src.vertex_id
            JOIN lattice_vertices v_dst ON e.dst = v_dst.vertex_id
            ORDER BY e.edge_id;
            """
            cursor.execute(sql_f1)
            form1_dict = {
                row["edge_id"]: {
                    "src": row["src"],
                    "dst": row["dst"],
                    "d0": float(row["d0_val"]),
                    "star1_d0": float(row["star1_d0_val"]),
                }
                for row in cursor.fetchall()
            }

            sql_nilp = """
            SELECT
                s.simplex_id,
                (
                    (v2.phi_val - v1.phi_val)
                    - (v2.phi_val - v0.phi_val)
                    + (v1.phi_val - v0.phi_val)
                ) AS nilpotence_defect
            FROM simplices s
            JOIN lattice_vertices v0 ON s.v0 = v0.vertex_id
            JOIN lattice_vertices v1 ON s.v1 = v1.vertex_id
            JOIN lattice_vertices v2 ON s.v2 = v2.vertex_id
            WHERE s.dim = 2;
            """
            cursor.execute(sql_nilp)
            nilp_rows = cursor.fetchall()
            nilpotence_certified = len(nilp_rows) == 0 or all(
                abs(r["nilpotence_defect"]) < 1e-12 for r in nilp_rows
            )
        else:
            form1_dict = {}
            nilpotence_certified = False

        if max_fuel >= 2:
            sql_lap = """
            SELECT
                v.vertex_id,
                COALESCE(
                    SUM(
                        CASE
                            WHEN e.src = v.vertex_id THEN e.hodge_star1 * (v.phi_val - v_nbr_dst.phi_val)
                            WHEN e.dst = v.vertex_id THEN e.hodge_star1 * (v.phi_val - v_nbr_src.phi_val)
                            ELSE 0.0
                        END
                    ) / NULLIF(v.dual_area, 0.0),
                    0.0
                ) AS laplacian_val
            FROM lattice_vertices v
            LEFT JOIN lattice_edges e ON e.src = v.vertex_id OR e.dst = v.vertex_id
            LEFT JOIN lattice_vertices v_nbr_dst ON e.dst = v_nbr_dst.vertex_id AND e.src = v.vertex_id
            LEFT JOIN lattice_vertices v_nbr_src ON e.src = v_nbr_src.vertex_id AND e.dst = v.vertex_id
            GROUP BY v.vertex_id
            ORDER BY v.vertex_id;
            """
            cursor.execute(sql_lap)
            laplacian_dict = {
                row["vertex_id"]: float(row["laplacian_val"]) for row in cursor.fetchall()
            }
            status = "HALTED"
            terminal_stage = 2
            steps_taken = 2
            fuel_remaining = max_fuel - 2
            laplacian_closed = True
            hodge_dual_closed = True
        elif max_fuel == 1:
            laplacian_dict = {}
            status = "OUT_OF_FUEL"
            terminal_stage = 1
            steps_taken = 1
            fuel_remaining = 0
            laplacian_closed = False
            hodge_dual_closed = False
        else:
            laplacian_dict = {}
            status = "OUT_OF_FUEL"
            terminal_stage = 0
            steps_taken = 0
            fuel_remaining = 0
            laplacian_closed = False
            hodge_dual_closed = False

        return {
            "max_fuel": max_fuel,
            "steps_taken": steps_taken,
            "fuel_remaining": fuel_remaining,
            "terminal_stage": terminal_stage,
            "status": status,
            "laplacian_closed": laplacian_closed,
            "hodge_dual_closed": hodge_dual_closed,
            "nilpotence_certified": nilpotence_certified,
            "form0": form0_dict,
            "form1": form1_dict,
            "laplacian": laplacian_dict,
        }

    def close(self):
        self.conn.close()
