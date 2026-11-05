# -*- coding: utf-8 -*-
"""
Bridge to Rust crates in omega_engine/crates_rs.
Transports exact inputs to the packaged native solver and functional evaluator.

AuthorityEffect: None.
"""

from __future__ import annotations

from pathlib import Path
import tomllib
from typing import Any, Dict, List, Optional, Tuple

from sympy import Matrix, Rational

from coda_application.infrastructure.native_functional_adapter import NativeFunctionalEvaluator
from coda_application.domain.intake import exact, matrix_rows
from coda_application.domain.l1_quotient import solve_l1_quotient


class RustCrateBridge:
    """Interface to omega_engine/crates_rs cargo workspace."""

    @staticmethod
    def _default_workspace() -> Optional[Path]:
        return next(
            (p / "omega_engine" / "crates_rs" for p in Path(__file__).resolve().parents
             if (p / "omega_engine" / "crates_rs" / "Cargo.toml").is_file()),
            None,
        )

    def __init__(self, workspace_path: Optional[Path] = None):
        if workspace_path is None:
            # An extracted paper need not contain the separate native workspace.
            self.workspace_path = self._default_workspace()
        else:
            self.workspace_path = Path(workspace_path)

    def is_workspace_available(self) -> bool:
        """Checks if crates_rs Cargo.toml exists."""
        return self.workspace_path is not None and (self.workspace_path / "Cargo.toml").is_file()

    def get_available_crates(self) -> List[str]:
        """Lists registered member crates in omega_engine/crates_rs."""
        if self.workspace_path is None:
            return []
        cargo_toml = self.workspace_path / "Cargo.toml"
        if not cargo_toml.exists():
            return []

        manifest = tomllib.loads(cargo_toml.read_text(encoding="utf-8"))
        workspace = manifest.get("workspace", {})
        excluded = workspace.get("exclude", [])
        crates = set()
        for pattern in workspace.get("members", []):
            for member in self.workspace_path.glob(pattern):
                relative = member.relative_to(self.workspace_path)
                if any(relative.match(pattern) for pattern in excluded):
                    continue
                crate_manifest = member / "Cargo.toml"
                if crate_manifest.is_file():
                    package = tomllib.loads(crate_manifest.read_text(encoding="utf-8")).get("package", {})
                    if isinstance(package.get("name"), str):
                        crates.add(package["name"])
        return sorted(crates)

    def solve_phi1_l1_via_rust(
        self,
        boundary_matrix: Matrix,
        cochain: Matrix,
    ) -> Optional[Dict[str, Any]]:
        """
        Evaluate Phi_1 through the native adapter and retain the serialized input.

        The solver proposes a certificate; omega_functional checks it. Missing
        executables or non-exact entries raise an error before a value is returned.
        """
        rows, (m, k) = matrix_rows(boundary_matrix, "boundary_matrix")
        if cochain.cols != 1 or cochain.rows != m:
            raise ValueError(f"cochain shape {cochain.shape} does not match the boundary's {m} rows")
        x = [exact(cochain[r, 0], f"cochain[{r}]") for r in range(m)]
        cert = solve_l1_quotient(rows, k, x, evaluator=NativeFunctionalEvaluator())
        payload = {
            "d_rows": m,
            "d_cols": k,
            "d_nonzeros": sorted([i, j, v.numerator, v.denominator] for i, row in enumerate(rows) for j, v in row.items()),
            "cochain_entries": [[v.numerator, v.denominator] for v in x],
        }
        return {
            "status": "NATIVE_CERTIFICATE_VERIFIED",
            "crate": "omega_functional",
            "target": "evaluate_wdp_functionals",
            "rust_workspace_present": self.is_workspace_available(),
            "phi1": [cert.distance.numerator, cert.distance.denominator],
            "solver_method": cert.method,
            "payload_dim": (m, k),
            "payload": payload,
        }

    @staticmethod
    def generate_high_dim_graph_instance(
        num_vertices: int = 1000,
        chord_interval: int = 10,
        licensed: bool = False,
    ) -> Any:
        """
        Generates a high-dimensional graph ProblemInstance (num_vertices >= 10).
        Topology: an oriented cycle plus chordal bypass edges i -> i + chord_interval.
        A chord that would start and end at the same vertex (chord_interval a multiple of
        num_vertices) is omitted, so every row is an incidence row with one -1 and one +1.
        ``licensed`` sets the problem's license *claim*, which never authorizes by itself.
        """
        if type(num_vertices) is not int or num_vertices < 10:
            raise ValueError("num_vertices must be at least 10 for high-dimensional testing")

        if type(chord_interval) is not int or chord_interval < 0:
            raise ValueError("chord_interval must be a nonnegative integer")
        if type(licensed) is not bool:
            raise ValueError("licensed must be a Boolean claim")

        from coda_application.domain.entities import ProblemInstance

        v = num_vertices
        edges: List[Tuple[int, int]] = [(i, (i + 1) % v) for i in range(v)]
        if chord_interval > 0 and chord_interval % v != 0:
            for i in range(0, v, chord_interval):
                edges.append((i, (i + chord_interval) % v))

        e = len(edges)
        d0 = Matrix.zeros(e, v)
        for idx, (src, tgt) in enumerate(edges):
            d0[idx, src] = -1
            d0[idx, tgt] = 1

        d1 = Matrix.zeros(1, e)

        # Defect: unit flux on the primary cycle edges, 0 on chordal edges
        defect = Matrix([Rational(1) if i < v else Rational(0) for i in range(e)])

        return ProblemInstance(
            problem_id=f"graph_v{v}_e{e}",
            raw_data=f"declared_cycle_fixture_dim_{v}",
            candidate_sieve=(f"cand_graph_{v}",),
            coarse_profile=(0, 1),
            fine_profile=(0, 1),
            projection_map={0: 0, 1: 1},
            local_sections={"U0": (Rational(1, 2),)},
            overlaps={("U0", "U0"): True},
            d0=d0,
            d1=d1,
            defect_cochain=defect,
            fda_license_granted=licensed,
        )
