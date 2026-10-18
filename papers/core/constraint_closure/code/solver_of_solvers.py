"""Cascade Solver of Solvers Engine v0.2 under AuthorityEffect = None.

Implements the 3-algorithm hierarchical residual removal loop:
  1. Foundation: Declares finite carrier & initial cochain residual omega.
  2. DDA / Multi-Cycle L1: Removes pure gauge d0*alpha & coexact cycle d1*beta tension.
  3. Homological Cell Attachment (Opt-In): Proposes normal cell generators, verified via d1*d0 = 0 and strict residual reduction.
  4. Window Lift / Obstruction: Elevates carrier degree window C^k -> C^{k+1} or emits TYPED_OBSTRUCTION with dual witness receipts.

AuthorityEffect: None.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import numpy as np

code_dir = Path(__file__).resolve().parent if "__file__" in locals() else Path(".")
if str(code_dir) not in sys.path:
    sys.path.insert(0, str(code_dir))

try:
    from universe_anomalonica.coda.network_residual import Network, residual_after_gauge_fix, multi_cycle_l1_joint
except ImportError:
    from network_residual import Network, residual_after_gauge_fix, multi_cycle_l1_joint

try:
    from discrete_descent_engine import (
        DDAEngine,
        FoundationCert,
        DDAStepCert,
        WindowLiftCert,
        TerminationCert,
        TerminationStatus,
    )
except ImportError:
    try:
        from universe_anomalonica.coda.dda_engine import (
            DDAEngine,
            FoundationCert,
            DDAStepCert,
            WindowLiftCert,
            TerminationCert,
            TerminationStatus,
        )
    except ImportError:
        from dda_engine import (
            DDAEngine,
            FoundationCert,
            DDAStepCert,
            WindowLiftCert,
            TerminationCert,
            TerminationStatus,
        )


try:
    from universe_anomalonica.omega_engine.functional import solve_phi1_dual_witness
except ImportError:
    try:
        from codaq.phi1_lp import solve_phi1_dual_witness
    except ImportError:
        solve_phi1_dual_witness = None


@dataclass
class SolverCascadeReceipt:
    """Receipt tracking the hierarchical cascade solver execution."""

    carrier_nodes: int
    carrier_edges: int
    initial_residual_size: float
    final_residual_size: float
    stages_executed: List[str]
    degree_window_reached: int
    terminal_status: str
    final_residual_triple: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    is_certified: bool = False
    duality_gap: Optional[float] = None
    attached_cells: List[Tuple[Any, ...]] = field(default_factory=list)
    lift_history: List[Dict[str, Any]] = field(default_factory=list)
    prior_degree_obligations: Dict[int, Any] = field(default_factory=dict)
    algebraic_class_id: Optional[str] = None
    admitted_complex_verified: bool = True
    authority_effect: str = "None"

    def is_solved(self) -> bool:
        if not self.admitted_complex_verified:
            return False
        if self.terminal_status not in ("Exact", "ExactCellAttached"):
            return False
        if self.final_residual_size > 1e-8:
            return False
        if any(abs(x) > 1e-8 for x in self.final_residual_triple):
            return False
        if self.prior_degree_obligations:
            for deg, obl in self.prior_degree_obligations.items():
                if isinstance(obl, (tuple, list)):
                    if any(abs(x) > 1e-8 for x in obl):
                        return False
                elif isinstance(obl, (int, float)):
                    if abs(obl) > 1e-8:
                        return False
        return True


class CascadeSolver:
    """Hierarchical Cascade Solver of Solvers for cochain residual extraction."""

    def __init__(self, network: Network, observer_name: str = "CascadeSolver"):
        self.network = network
        self.observer_name = observer_name
        self.dda_engine = DDAEngine(network, observer_name=observer_name)

    def build_admitted_complex(self) -> Any:
        """Build exact SymPy d0 and d1 matrices and verify d1 * d0 = 0 via AdmittedComplexV1."""
        from cochain_presentation import AdmittedComplexV1
        from sympy import Matrix

        nodes = sorted(list(self.network.nodes))
        edges = list(self.network.edges)
        faces = list(self.network.faces) if self.network.faces else []

        if not nodes or not edges:
            return None

        node_map = {n: i for i, n in enumerate(nodes)}
        edge_map = {e: i for i, e in enumerate(edges)}

        d0_matrix = Matrix.zeros(len(edges), len(nodes))
        for e_idx, (u, v) in enumerate(edges):
            d0_matrix[e_idx, node_map[v]] = 1
            d0_matrix[e_idx, node_map[u]] = -1

        if not faces:
            d1_matrix = Matrix.zeros(1, len(edges))
        else:
            d1_matrix = Matrix.zeros(len(faces), len(edges))
            for f_idx, (u, v, w) in enumerate(faces):
                for (e_u, e_v), sign in [((u, v), 1), ((v, w), 1), ((u, w), -1)]:
                    if (e_u, e_v) in edge_map:
                        d1_matrix[f_idx, edge_map[(e_u, e_v)]] += sign
                    elif (e_v, e_u) in edge_map:
                        d1_matrix[f_idx, edge_map[(e_v, e_u)]] -= sign

        return AdmittedComplexV1(d0=d0_matrix, d1=d1_matrix)

    def attach_normal_cell(
        self, residual_edges: Dict[Tuple[Any, Any], float]
    ) -> Tuple[bool, Optional[Tuple[Any, ...]]]:
        """Attaches a 2-cell face along the principal normal leakage vector.

        Opt-in cell attachment: candidate cell is accepted ONLY if d1 * d0 = 0 is verified
        and the residual quotient mass strictly decreases. Otherwise, changes are rolled back.
        Returns (success_flag, attached_cell_tuple).
        """
        active_edges = [(e, val) for e, val in residual_edges.items() if abs(val) > 1e-6]
        if not active_edges:
            return False, None

        active_edges.sort(key=lambda item: abs(item[1]), reverse=True)
        existing_faces = set(self.network.faces) if self.network.faces else set()

        res_before = multi_cycle_l1_joint(self.network, residual_edges)
        phi_before = float(res_before["residual_size"])

        candidates: List[Tuple[Any, ...]] = []

        edge_nodes = set()
        for (u, v), _ in active_edges:
            edge_nodes.add(u)
            edge_nodes.add(v)

        if len(edge_nodes) >= 3:
            cycle_nodes = sorted(list(edge_nodes))[:3]
            candidates.append((cycle_nodes[0], cycle_nodes[1], cycle_nodes[2]))

        for (u, v), _ in active_edges:
            for w in self.network.nodes:
                if w != u and w != v:
                    cand = tuple(sorted([u, v, w]))
                    if cand not in candidates:
                        candidates.append(cand)

        for face_candidate in candidates:
            if face_candidate in existing_faces or (face_candidate[1], face_candidate[0], face_candidate[2]) in existing_faces:
                continue

            if self.network.faces is None:
                self.network.faces = []

            self.network.faces.append(face_candidate)

            try:
                admitted = self.build_admitted_complex()
                if admitted is None:
                    self.network.faces.pop()
                    continue
            except Exception:
                self.network.faces.pop()
                continue

            res_after = multi_cycle_l1_joint(self.network, residual_edges)
            phi_after = float(res_after["residual_size"])
            if phi_after >= phi_before and phi_before > 1e-6:
                self.network.faces.pop()
                continue

            return True, face_candidate

        return False, None

    def _get_dual_witness_cert(
        self, cochain: Dict[Tuple[Any, Any], float]
    ) -> Tuple[bool, Optional[float]]:
        """Resolves primal-dual L1 gauge certificate if solver is available."""
        if solve_phi1_dual_witness is None or self.dda_engine.degree_window != 1:
            return False, None

        try:
            edges = list(self.network.edges)
            nodes = sorted(list(self.network.nodes))
            cochain_vec = np.array([cochain.get(e, 0.0) for e in edges], dtype=float)

            res = solve_phi1_dual_witness(nodes, edges, cochain_vec)
            return bool(res.get("is_certified", False)), res.get("duality_gap")
        except Exception:
            return False, None

    def solve(
        self,
        edge_values: Dict[Tuple[Any, Any], float],
        max_lifts: int = 1,
        tol: float = 1e-6,
        enable_cell_attachment: bool = False,
    ) -> SolverCascadeReceipt:
        """Executes the 3-algorithm cascade solver loop under AuthorityEffect: None."""
        stages: List[str] = []
        attached_cells: List[Tuple[Any, ...]] = []
        lift_history: List[Dict[str, Any]] = []

        foundation = self.dda_engine.run_foundation(edge_values)
        stages.append("Foundation")
        initial_size = foundation.phi1

        admitted_ok = True
        try:
            adm = self.build_admitted_complex()
            admitted_ok = adm is not None
        except Exception:
            admitted_ok = False

        if initial_size < tol and foundation.gamma2 < tol:
            is_cert, gap = self._get_dual_witness_cert(self.dda_engine.current_edge_values)
            return SolverCascadeReceipt(
                carrier_nodes=len(self.network.nodes),
                carrier_edges=len(self.network.edges),
                initial_residual_size=initial_size,
                final_residual_size=initial_size,
                stages_executed=stages,
                degree_window_reached=1,
                terminal_status="Exact",
                final_residual_triple=(foundation.phi1, foundation.gamma2, foundation.chi),
                is_certified=is_cert,
                duality_gap=gap,
                attached_cells=attached_cells,
                lift_history=lift_history,
                admitted_complex_verified=admitted_ok,
                authority_effect="None",
            )

        cert_gauge, (phi1_g, gamma2_g, chi_g) = self.dda_engine.step_dda(move_type="exact_d0")
        stages.append("ExactLocalGaugeFix")

        if phi1_g < tol and gamma2_g < tol:
            is_cert, gap = self._get_dual_witness_cert(self.dda_engine.current_edge_values)
            return SolverCascadeReceipt(
                carrier_nodes=len(self.network.nodes),
                carrier_edges=len(self.network.edges),
                initial_residual_size=initial_size,
                final_residual_size=phi1_g,
                stages_executed=stages,
                degree_window_reached=1,
                terminal_status="Exact",
                final_residual_triple=(phi1_g, gamma2_g, chi_g),
                is_certified=is_cert,
                duality_gap=gap,
                attached_cells=attached_cells,
                lift_history=lift_history,
                admitted_complex_verified=admitted_ok,
                authority_effect="None",
            )

        cert_multi, (phi1_m, gamma2_m, chi_m) = self.dda_engine.step_dda(move_type="multi_cycle_l1")
        stages.append("MultiCycleL1Descent")

        if phi1_m < tol and gamma2_m < tol:
            is_cert, gap = self._get_dual_witness_cert(self.dda_engine.current_edge_values)
            return SolverCascadeReceipt(
                carrier_nodes=len(self.network.nodes),
                carrier_edges=len(self.network.edges),
                initial_residual_size=initial_size,
                final_residual_size=phi1_m,
                stages_executed=stages,
                degree_window_reached=1,
                terminal_status="Exact",
                final_residual_triple=(phi1_m, gamma2_m, chi_m),
                is_certified=is_cert,
                duality_gap=gap,
                attached_cells=attached_cells,
                lift_history=lift_history,
                admitted_complex_verified=admitted_ok,
                authority_effect="None",
            )

        if enable_cell_attachment and (phi1_m > tol or gamma2_m > tol):
            attached, cell_added = self.attach_normal_cell(self.dda_engine.current_edge_values)
            if attached and cell_added:
                stages.append("HomologicalCellAttachment")
                attached_cells.append(cell_added)
                cert_post, (phi1_post, gamma2_post, chi_post) = self.dda_engine.step_dda(move_type="multi_cycle_l1")
                if phi1_post < tol and gamma2_post < tol:
                    is_cert, gap = self._get_dual_witness_cert(self.dda_engine.current_edge_values)
                    return SolverCascadeReceipt(
                        carrier_nodes=len(self.network.nodes),
                        carrier_edges=len(self.network.edges),
                        initial_residual_size=initial_size,
                        final_residual_size=phi1_post,
                        stages_executed=stages,
                        degree_window_reached=self.dda_engine.degree_window,
                        terminal_status="ExactCellAttached",
                        final_residual_triple=(phi1_post, gamma2_post, chi_post),
                        is_certified=is_cert,
                        duality_gap=gap,
                        attached_cells=attached_cells,
                        lift_history=lift_history,
                        admitted_complex_verified=admitted_ok,
                        authority_effect="None",
                    )
                else:
                    phi1_m, gamma2_m, chi_m = phi1_post, gamma2_post, chi_post

        stages.append("WindowLiftEvaluation")
        term_cert = self.dda_engine.lift_or_terminate((phi1_m, gamma2_m, chi_m), tol=tol, max_lifts=max_lifts)

        if self.dda_engine.lift_history:
            for lift_cert in self.dda_engine.lift_history:
                lift_history.append({
                    "from_degree": lift_cert.from_degree,
                    "to_degree": lift_cert.to_degree,
                    "num_higher_cells": lift_cert.num_higher_cells,
                    "lift_kind": lift_cert.lift_kind,
                    "trigger_curvature_mass": lift_cert.trigger_curvature_mass,
                })

        status_map = {
            TerminationStatus.SOLVED: "Exact",
            TerminationStatus.TYPED_OBSTRUCTION: "TYPED_OBSTRUCTION",
            TerminationStatus.AUTHORIZATION_EXHAUSTED: "AUTHORIZATION_EXHAUSTED",
        }
        status_str = status_map.get(term_cert.status, "TYPED_OBSTRUCTION")
        if gamma2_m < tol and status_str == "TYPED_OBSTRUCTION":
            status_str = "ClosedResidual"

        is_cert, gap = self._get_dual_witness_cert(self.dda_engine.current_edge_values)

        return SolverCascadeReceipt(
            carrier_nodes=len(self.network.nodes),
            carrier_edges=len(self.network.edges),
            initial_residual_size=initial_size,
            final_residual_size=phi1_m,
            stages_executed=stages,
            degree_window_reached=self.dda_engine.degree_window,
            terminal_status=status_str,
            final_residual_triple=(phi1_m, gamma2_m, chi_m),
            is_certified=is_cert,
            duality_gap=gap,
            attached_cells=attached_cells,
            lift_history=lift_history,
            prior_degree_obligations=dict(getattr(self.dda_engine, "prior_degree_obligations", {})),
            algebraic_class_id=term_cert.algebraic_class_id,
            admitted_complex_verified=admitted_ok,
            authority_effect="None",
        )


if __name__ == "__main__":
    net = Network(
        nodes=[0, 1, 2, 3],
        edges=[(0, 1), (1, 2), (2, 0), (1, 3), (3, 0)],
        faces=[(0, 1, 2), (0, 1, 3)],
    )

    omega = {(0, 1): 3.0, (1, 2): 2.0, (2, 0): 2.0, (1, 3): 1.0, (3, 0): 1.0}
    solver = CascadeSolver(net)
    receipt = solver.solve(omega)

    print("=== Cascade Solver of Solvers Receipt ===")
    print(f"Carrier Nodes/Edges: {receipt.carrier_nodes}/{receipt.carrier_edges}")
    print(f"Initial Residual Phi1: {receipt.initial_residual_size:.6f}")
    print(f"Final Residual Phi1:   {receipt.final_residual_size:.6f}")
    print(f"Stages Executed:       {' -> '.join(receipt.stages_executed)}")
    print(f"Degree Window Reached: C^{receipt.degree_window_reached}")
    print(f"Terminal Status:       {receipt.terminal_status}")
    print(f"Dual Certified:        {receipt.is_certified} (duality gap: {receipt.duality_gap})")
    print(f"Attached Cells:        {receipt.attached_cells}")
    print(f"AuthorityEffect:       {receipt.authority_effect}")
