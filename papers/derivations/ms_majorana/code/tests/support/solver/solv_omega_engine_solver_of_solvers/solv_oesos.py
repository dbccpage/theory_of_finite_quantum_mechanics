"""Cascade Solver of Solvers Engine v0.3 under AuthorityEffect = None.

Implements the hierarchical residual removal loop:
  1. Foundation: Declares finite carrier & initial cochain residual omega.
  2. DDA / Multi-Cycle L1: Removes pure gauge d0*alpha & coexact cycle d1*beta tension.
  3. Homological Cell Attachment (Opt-In): Proposes normal cell generators, verified via d1*d0 = 0 and strict residual reduction.
  4. Window Lift / Obstruction: Elevates carrier degree window or emits typed obstruction.

Exact / CLOSED_NONEXACT / NONCLOSED terminal claims are produced ONLY by the
Gate-11 rational kernel (evaluate_obstruction via classify_network_residual).
Float multi-cycle L1 remains the working residual-reduction engine (diagnostic).

Evaluation stage also emits EvaluationReceipt (OESOS–DDA lifecycle) wrapping the
Gate-11 ObstructionReceipt so downstream Verification/Authorization can consume
it without re-running the kernel.

AuthorityEffect: None.
"""

from __future__ import annotations

import hashlib
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

code_dir = Path(__file__).resolve().parent if "__file__" in locals() else Path(".")
if str(code_dir) not in sys.path:
    sys.path.insert(0, str(code_dir))

try:
    from omega_engine.crates.residuals.network_residual import (
        Network,
        multi_cycle_l1_joint,
        residual_after_gauge_fix,
    )
except ImportError:
    from omega_engine.residuals.network_residual import (
        Network,
        multi_cycle_l1_joint,
    )

try:
    from omega_engine.crates.discrete_deformation_algebra.dda_engine import (
        DDAEngine,
        DDAStepCert,
        FoundationCert,
        TerminationCert,
        TerminationStatus,
        WindowLiftCert,
    )
except ImportError:
    try:
        from omega_engine.crates.discrete_deformation_algebra.base.dda_base_engine import (
            DDAEngine,
            DDAStepCert,
            FoundationCert,
            TerminationCert,
            TerminationStatus,
            WindowLiftCert,
        )
    except ImportError:
        from omega_engine.dda.dda_engine import (
            DDAEngine,
        )



try:
    from omega_engine.crates.functional.phi import solve_phi1_dual_witness
except ImportError:
    solve_phi1_dual_witness = None

try:
    from omega_engine.crates.solver.solv_omega_engine_solver_of_solvers.solv_exact_dual_pricing import (
        ExactDualPricingError,
        ExactDualPricingReceipt,
        price_network_phi1_exact,
    )
except ImportError:
    ExactDualPricingError = None
    ExactDualPricingReceipt = None
    price_network_phi1_exact = None

try:
    from omega_engine.crates.solver.solv_omega_engine_solver_of_solvers.solv_network_to_obstruction import (
        classify_network_residual,
        obstruction_class_to_terminal_status,
    )
    from omega_engine.crates.solver.solv_omega_engine_solver_of_solvers.solv_obstruction_evaluator import (
        ObstructionClass,
        ObstructionReceipt,
    )
except ImportError:
    classify_network_residual = None
    obstruction_class_to_terminal_status = None
    ObstructionClass = None
    ObstructionReceipt = None

try:
    from omega_engine.crates.packet.oesos_dda_lifecycle import EvaluationReceipt
except ImportError:
    EvaluationReceipt = None


def _stable_sha256(payload: Dict[str, Any]) -> str:
    raw = json.dumps(payload, sort_keys=True, default=str).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


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
    algebraic_class_id: Optional[str] = None
    admitted_complex_verified: bool = True
    dual_witness_status: str = "unavailable"
    authority_effect: str = "None"
    obstruction_class: Optional[str] = None
    evidence_sha256: Optional[str] = None
    evaluation_receipt: Optional[Any] = None
    arithmetic_mode: str = "diagnostic_float"
    exact_phi_k: Optional[str] = None
    exact_dual_value: Optional[str] = None
    exact_gap: Optional[str] = None
    exact_degree: Optional[int] = None
    diagnostic_residual_mass: Optional[float] = None
    exact_dual_receipt: Optional[Any] = None
    estate_wide_phi_k_theorem: str = "REFUSED"
    normhood_from_attainment_alone: str = "REFUSED"

    def is_solved(self) -> bool:
        """Honest: Exact* status AND residual mass coherent (no size-only green)."""
        if self.terminal_status not in (
            "Exact",
            "ExactCellAttached",
            "MODEL_CHANGED_SOLVED",
        ):
            return False
        return self.final_residual_size < 1e-6

    def is_exact_dual_certified(self) -> bool:
        """True only when the rational dual rail reported zero gap."""
        if not (
            self.is_certified
            and self.arithmetic_mode == "Q"
            and self.dual_witness_status == "certified_exact"
            and self.exact_gap is not None
        ):
            return False
        if self.exact_dual_receipt is not None:
            return bool(self.exact_dual_receipt.is_certified)
        try:
            from fractions import Fraction

            return Fraction(self.exact_gap) == 0
        except Exception:
            return self.exact_gap in ("0", "0/1")

    def as_evidence_dict(self) -> Dict[str, Any]:
        """Serialize cascade evidence with exact dual honesty fields.

        Float residual mass stays diagnostic; Q dual zero-gap is separate.
        Never mints AuthorityEffect. Continuum / Pontryagin dual remain OPEN/REFUSED.
        """
        return {
            "carrier_nodes": self.carrier_nodes,
            "carrier_edges": self.carrier_edges,
            "initial_residual_size": self.initial_residual_size,
            "final_residual_size": self.final_residual_size,
            "diagnostic_residual_mass": self.diagnostic_residual_mass,
            "stages_executed": list(self.stages_executed),
            "degree_window_reached": self.degree_window_reached,
            "terminal_status": self.terminal_status,
            "final_residual_triple": list(self.final_residual_triple),
            "is_certified": self.is_certified,
            "is_exact_dual_certified": self.is_exact_dual_certified(),
            "is_solved": self.is_solved(),
            "duality_gap": self.duality_gap,
            "dual_witness_status": self.dual_witness_status,
            "arithmetic_mode": self.arithmetic_mode,
            "exact_phi_k": self.exact_phi_k,
            "exact_dual_value": self.exact_dual_value,
            "exact_gap": self.exact_gap,
            "exact_degree": self.exact_degree,
            "obstruction_class": self.obstruction_class,
            "evidence_sha256": self.evidence_sha256,
            "attached_cells": [list(c) for c in self.attached_cells],
            "lift_history": list(self.lift_history),
            "admitted_complex_verified": self.admitted_complex_verified,
            "algebraic_class_id": self.algebraic_class_id,
            "authority_effect": self.authority_effect or "None",
            "estate_wide_phi_k_theorem": self.estate_wide_phi_k_theorem or "REFUSED",
            "normhood_from_attainment_alone": self.normhood_from_attainment_alone
            or "REFUSED",
            "spine_fence": {
                "wdw_form": "Omega_hat Psi = r (residual-form only)",
                "coda_cs_coda_q": "shared residual pricing language only; not object identity",
                "pontryagin_dual_pi_programme": "STAGED_HOST",
                "finite_declared_quotient_norm": "AVAILABLE",
                "continuum_superspace_wdw": "REFUSED",
                "float_as_exact": "REFUSED",
                "holy_land_rec_full": "REFUSED_WITHOUT_EVIDENCE",
                "estate_wide_phi_k_theorem": self.estate_wide_phi_k_theorem or "REFUSED",
                "normhood_from_attainment_alone": self.normhood_from_attainment_alone
                or "REFUSED",
            },
        }


@dataclass
class DeformationReceipt:
    """Receipt emitted by stage_hpl_deformation under AuthorityEffect: None."""

    contraction_side_conditions_valid: bool
    perturbation_norm: float
    transferred_differential_norm: float
    invertibility_status: str
    loss_ledger: Dict[str, Any] = field(default_factory=dict)
    authority_effect: str = "None"


@dataclass
class FiniteHilbertReceipt:
    """Receipt emitted by stage_hilbert_residual_lift under AuthorityEffect: None."""

    hilbert_dim: int
    projector_exact_norm: float
    projector_closed_nonexact_norm: float
    projector_nonclosed_norm: float
    truncation_leakage_L_P: float
    is_leakage_free: bool
    oracle_needed_status: str
    authority_effect: str = "None"


@dataclass
class NormalizedContraction:
    """Represents a normalized chain contraction (i, r, h) between complexes C and D.

    Inclusions i: D -> C, retraction r: C -> D, homotopy h: End^-1(C).
    Side conditions:
        1. r * i = 1_D
        2. 1_C - i * r = d * h + h * d
        3. h * i = 0
        4. r * h = 0
        5. h * h = 0
    """

    i_map: np.ndarray
    r_map: np.ndarray
    h_map: np.ndarray
    d_C: np.ndarray
    d_D: np.ndarray

    def verify_side_conditions(self, tol: float = 1e-6) -> bool:
        dim_D = self.r_map.shape[0]
        dim_C = self.h_map.shape[0]
        eye_D = np.eye(dim_D)
        eye_C = np.eye(dim_C)

        if not np.allclose(self.r_map @ self.i_map, eye_D, atol=tol):
            return False

        lhs = eye_C - (self.i_map @ self.r_map)
        rhs = (self.d_C @ self.h_map) + (self.h_map @ self.d_C)
        if not np.allclose(lhs, rhs, atol=tol):
            return False

        if not np.allclose(self.h_map @ self.i_map, 0.0, atol=tol):
            return False

        if not np.allclose(self.r_map @ self.h_map, 0.0, atol=tol):
            return False

        if not np.allclose(self.h_map @ self.h_map, 0.0, atol=tol):
            return False

        return True


class CascadeSolver:
    """Hierarchical Cascade Solver of Solvers for cochain residual extraction."""

    def __init__(self, network: Network, observer_name: str = "CascadeSolver"):
        self.network = network
        self.observer_name = observer_name
        self.dda_engine = DDAEngine(network, observer_name=observer_name)

    def stage_hpl_deformation(
        self,
        contraction: NormalizedContraction,
        delta: np.ndarray,
        tol: float = 1e-6,
    ) -> Tuple[Optional[np.ndarray], DeformationReceipt]:
        """Stage executing Homological Perturbation Lemma (HPL) transfer delta_D = r (1 + delta h)^-1 delta i.

        The plus sign matches the side condition 1_C - i r = d h + h d checked by
        NormalizedContraction.verify_side_conditions (WDP-CH16-C01).

        Under AuthorityEffect: None.
        Emits DeformationReceipt wrapping side-condition checks, Neumann series transfer, and loss ledger if uninvertible.
        """
        side_ok = contraction.verify_side_conditions(tol=tol)
        delta_norm = float(np.linalg.norm(delta))

        dim_C = contraction.h_map.shape[0]
        eye_C = np.eye(dim_C)
        dh = delta @ contraction.h_map

        eigvals = np.linalg.eigvals(dh)
        spectral_radius = float(np.max(np.abs(eigvals))) if len(eigvals) > 0 else 0.0

        if spectral_radius >= 1.0 - 1e-9:
            receipt = DeformationReceipt(
                contraction_side_conditions_valid=side_ok,
                perturbation_norm=delta_norm,
                transferred_differential_norm=0.0,
                invertibility_status="UNINVERTIBLE_PERTURBATION",
                loss_ledger={
                    "spectral_radius": spectral_radius,
                    "reason": "Neumann series (1 + delta*h)^-1 divergent (spectral radius >= 1.0)",
                    "AuthorityEffect": "None",
                },
                authority_effect="None",
            )
            return None, receipt

        try:
            inv_matrix = np.linalg.inv(eye_C + dh)
        except np.linalg.LinAlgError:
            receipt = DeformationReceipt(
                contraction_side_conditions_valid=side_ok,
                perturbation_norm=delta_norm,
                transferred_differential_norm=0.0,
                invertibility_status="UNINVERTIBLE_PERTURBATION",
                loss_ledger={
                    "reason": "Matrix (1 + delta*h) is singular",
                    "AuthorityEffect": "None",
                },
                authority_effect="None",
            )
            return None, receipt

        delta_D = contraction.r_map @ inv_matrix @ delta @ contraction.i_map
        delta_D_norm = float(np.linalg.norm(delta_D))

        receipt = DeformationReceipt(
            contraction_side_conditions_valid=side_ok,
            perturbation_norm=delta_norm,
            transferred_differential_norm=delta_D_norm,
            invertibility_status="INVERTIBLE",
            loss_ledger={},
            authority_effect="None",
        )
        return delta_D, receipt

    def stage_hilbert_residual_lift(
        self,
        Q: np.ndarray,
        constraint_A: np.ndarray,
        state_psi: np.ndarray,
        oracle_packet: Optional[Dict[str, Any]] = None,
        tol: float = 1e-6,
    ) -> Tuple[Dict[str, Any], FiniteHilbertReceipt]:
        r"""Stage executing Finite Hilbert-Complex Obstruction Layer & Leakage Check.

        Under AuthorityEffect: None.
        1. Nilpotent Q (Q^2 = 0), Laplacian Delta_Q = Q Q^\dagger + Q^\dagger Q.
        2. Gate-11 Trichotomy Projectors (P_exact, P_closed_nonexact, P_nonclosed).
        3. Subspace Truncation Leakage L_P = P A^\dagger (1 - P) A P.
        4. OracleNeeded refusal: Refuses Born uniqueness or continuum claims if un-certified.
        """
        dim = Q.shape[0]
        state_norm = float(np.linalg.norm(state_psi))
        if state_norm > 1e-12:
            psi_norm = state_psi / state_norm
        else:
            psi_norm = state_psi

        Q_adj = Q.conj().T
        Delta_Q = (Q @ Q_adj) + (Q_adj @ Q)

        evals, evecs = np.linalg.eigh(Delta_Q)

        harmonic_mask = np.abs(evals) < tol
        if np.any(harmonic_mask):
            V_harm = evecs[:, harmonic_mask]
            P_closed_nonexact = V_harm @ V_harm.conj().T
        else:
            P_closed_nonexact = np.zeros((dim, dim))

        evals_qq, evecs_qq = np.linalg.eigh(Q @ Q_adj)
        exact_mask = evals_qq > tol
        if np.any(exact_mask):
            V_exact = evecs_qq[:, exact_mask]
            P_exact = V_exact @ V_exact.conj().T
        else:
            P_exact = np.zeros((dim, dim))

        P_nonclosed = np.eye(dim) - (P_exact + P_closed_nonexact)

        norm_exact = float(np.linalg.norm(P_exact @ psi_norm))
        norm_cne = float(np.linalg.norm(P_closed_nonexact @ psi_norm))
        norm_nc = float(np.linalg.norm(P_nonclosed @ psi_norm))

        P_active = P_exact + P_closed_nonexact
        A_adj = constraint_A.conj().T
        eye = np.eye(dim)

        L_P_op = P_active @ A_adj @ (eye - P_active) @ constraint_A @ P_active
        leakage_norm = float(np.linalg.norm(L_P_op))
        is_leakage_free = leakage_norm <= tol

        requires_oracle = False
        oracle_status = "SATISFIED"
        if oracle_packet is not None:
            claims_born = oracle_packet.get("claims_born_uniqueness", False)
            claims_continuum = oracle_packet.get("claims_continuum_limit", False)
            has_witness = oracle_packet.get("import_witness_certified", False)
            if (claims_born or claims_continuum) and not has_witness:
                requires_oracle = True
                oracle_status = "REFUSED_ORACLE_NEEDED"

        receipt = FiniteHilbertReceipt(
            hilbert_dim=dim,
            projector_exact_norm=norm_exact,
            projector_closed_nonexact_norm=norm_cne,
            projector_nonclosed_norm=norm_nc,
            truncation_leakage_L_P=leakage_norm,
            is_leakage_free=is_leakage_free,
            oracle_needed_status=oracle_status,
            authority_effect="None",
        )

        lift_result = {
            "psi_exact": P_exact @ psi_norm,
            "psi_closed_nonexact": P_closed_nonexact @ psi_norm,
            "psi_nonclosed": P_nonclosed @ psi_norm,
            "L_P_operator": L_P_op,
            "is_refused": requires_oracle,
        }

        return lift_result, receipt


    def build_admitted_complex(self, net: Optional[Network] = None) -> Any:
        """Build exact SymPy d0 and d1 matrices and verify d1 * d0 = 0 via AdmittedComplexV1."""
        from omega_engine.crates.homology_theory.cochain_presentation import AdmittedComplexV1
        from sympy import Matrix

        target_net = net if net is not None else self.network
        nodes = sorted(list(target_net.nodes))
        edges = list(target_net.edges)
        faces = list(target_net.faces) if target_net.faces else []

        if not nodes or not edges:
            return None

        node_map = {n: i for i, n in enumerate(nodes)}
        edge_map = {e: i for i, e in enumerate(edges)}

        d0_matrix = Matrix.zeros(len(edges), len(nodes))
        for e_idx, (u, v) in enumerate(edges):
            d0_matrix[e_idx, node_map[v]] = 1
            d0_matrix[e_idx, node_map[u]] = -1

        if not faces:
            return None
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

            cand_faces = tuple(list(existing_faces) + [face_candidate])
            cand_net = Network(
                nodes=self.network.nodes,
                edges=self.network.edges,
                faces=cand_faces,
                tetrahedra=self.network.tetrahedra,
            )

            try:
                admitted = self.build_admitted_complex(net=cand_net)
                if admitted is None:
                    continue
            except Exception:
                continue

            res_after = multi_cycle_l1_joint(cand_net, residual_edges)
            phi_after = float(res_after["residual_size"])
            if phi_after >= phi_before and phi_before > 1e-6:
                continue

            self.network = cand_net
            self.dda_engine.network = cand_net
            return True, face_candidate

        return False, None

    def _get_exact_dual_cert(
        self, cochain: Dict[Tuple[Any, Any], float]
    ) -> Tuple[bool, Optional[float], str, Optional[Any]]:
        """Prefer FW-8 exact dual rail (Q, zero gap). Float LP is diagnostic only.

        Returns (is_certified, duality_gap_float, dual_witness_status, exact_receipt).
        ``is_certified`` is True only for arithmetic_mode Q with exact gap 0.

        Edge residual always admits Φ₁ pricing, independent of ``degree_window``
        (window lifts do not drop the exact dual rail).
        """
        if price_network_phi1_exact is not None:
            try:
                exact_rcpt = price_network_phi1_exact(self.network, cochain)
                gap_f = float(exact_rcpt.exact_gap)
                return (
                    exact_rcpt.is_certified,
                    gap_f,
                    exact_rcpt.dual_witness_status,
                    exact_rcpt,
                )
            except Exception:
                pass

        if solve_phi1_dual_witness is None:
            return False, None, "unavailable", None

        try:
            edges = list(self.network.edges)
            nodes = sorted(list(self.network.nodes))
            cochain_vec = np.array([cochain.get(e, 0.0) for e in edges], dtype=float)

            res = solve_phi1_dual_witness(nodes, edges, cochain_vec)
            ok_float = bool(res.get("is_certified", False))
            status = "float_diagnostic_certified" if ok_float else "float_diagnostic_uncertified"
            return False, res.get("duality_gap"), status, None
        except Exception:
            return False, None, "error", None

    def _get_dual_witness_cert(
        self, cochain: Dict[Tuple[Any, Any], float]
    ) -> Tuple[bool, Optional[float], str]:
        """Backward-compatible triple; prefer exact rail via _get_exact_dual_cert."""
        ok, gap, status, _ = self._get_exact_dual_cert(cochain)
        return ok, gap, status

    def _dual_fields_for_receipt(
        self, cochain: Dict[Tuple[Any, Any], float], diagnostic_mass: float
    ) -> Dict[str, Any]:
        """Build dual-related SolverCascadeReceipt kwargs with float/exact split.

        Always stamps estate-wide / normhood-from-attainment refuse fields so
        dual zero-gap cannot be misread as a quotient-norm theorem seal when
        consumers read live receipt attributes (not only as_evidence_dict).
        """
        is_cert, gap, dual_st, exact_rcpt = self._get_exact_dual_cert(cochain)
        fields: Dict[str, Any] = {
            "is_certified": is_cert,
            "duality_gap": gap,
            "dual_witness_status": dual_st,
            "diagnostic_residual_mass": float(diagnostic_mass),
            "exact_dual_receipt": exact_rcpt,
            "estate_wide_phi_k_theorem": "REFUSED",
            "normhood_from_attainment_alone": "REFUSED",
        }
        if exact_rcpt is not None:
            fields["arithmetic_mode"] = "Q"
            fields["exact_phi_k"] = str(exact_rcpt.phi_k)
            fields["exact_dual_value"] = str(exact_rcpt.dual_value)
            fields["exact_gap"] = str(exact_rcpt.exact_gap)
            fields["exact_degree"] = int(exact_rcpt.degree)
            if hasattr(exact_rcpt, "as_cascade_fields"):
                casc = exact_rcpt.as_cascade_fields()
                fields["estate_wide_phi_k_theorem"] = casc.get(
                    "estate_wide_phi_k_theorem", "REFUSED"
                )
                fields["normhood_from_attainment_alone"] = casc.get(
                    "normhood_from_attainment_alone", "REFUSED"
                )
        else:
            fields["arithmetic_mode"] = "diagnostic_float"
            fields["exact_phi_k"] = None
            fields["exact_dual_value"] = None
            fields["exact_gap"] = None
            fields["exact_degree"] = None
            fields["is_certified"] = False
        return fields

    def _synthetic_candidate_digest(
        self, residual: Dict[Tuple[Any, Any], float]
    ) -> str:
        """Stable forensic digest of topology + residual when no CandidatePacket supplied."""
        faces = list(self.network.faces) if self.network.faces else []
        residual_payload = {
            f"{u}->{v}": str(val)
            for (u, v), val in sorted(
                residual.items(),
                key=lambda kv: (str(kv[0][0]), str(kv[0][1])),
            )
        }
        return _stable_sha256({
            "nodes": sorted((str(n) for n in self.network.nodes)),
            "edges": [(str(u), str(v)) for u, v in self.network.edges],
            "faces": [tuple(str(x) for x in f) for f in faces],
            "residual": residual_payload,
            "evaluator": self.observer_name,
        })

    def _gate11_classify(
        self, residual: Dict[Tuple[Any, Any], float]
    ) -> Tuple[str, Optional[str], Optional[str], bool, Optional[Any]]:
        """Force Exact / CLOSED_NONEXACT / NONCLOSED through the rational kernel.

        Returns (terminal_status, obstruction_class, evidence_sha256,
                 independently_verifiable, obstruction_receipt).
        Float residual is converted to Fraction inside classify_network_residual.
        AuthorityEffect remains None.
        """
        if classify_network_residual is None or obstruction_class_to_terminal_status is None:
            return "TYPED_OBSTRUCTION", None, None, False, None
        try:
            receipt = classify_network_residual(self.network, residual)
            status = obstruction_class_to_terminal_status(receipt.classification)
            oclass = (
                receipt.classification.value
                if hasattr(receipt.classification, "value")
                else str(receipt.classification)
            )
            return (
                status,
                oclass,
                receipt.evidence_sha256,
                receipt.independently_verifiable,
                receipt,
            )
        except Exception:
            return "TYPED_OBSTRUCTION", None, None, False, None

    def _make_evaluation_receipt(
        self,
        residual: Dict[Tuple[Any, Any], float],
        obstruction: Any,
        *,
        candidate_digest: Optional[str] = None,
    ) -> Optional[Any]:
        """Wrap Gate-11 ObstructionReceipt as EvaluationReceipt (evaluation stage only).

        Does not issue licenses, run verification, or touch HostExecutor.
        AuthorityEffect remains None.
        """
        if EvaluationReceipt is None or obstruction is None:
            return None
        if candidate_digest is None:
            candidate_digest = self._synthetic_candidate_digest(residual)
        return EvaluationReceipt(
            candidate_digest=candidate_digest,
            obstruction=obstruction,
            evaluator_id=f"{self.observer_name}.gate11",
        )

    def _classify_and_evaluate(
        self,
        residual: Dict[Tuple[Any, Any], float],
        *,
        candidate_digest: Optional[str] = None,
    ) -> Tuple[str, Optional[str], Optional[str], Optional[Any]]:
        """Single Gate-11 + EvaluationReceipt emission used by every terminal exit."""
        status, oclass, evid, _, obstruction = self._gate11_classify(residual)
        eval_receipt = self._make_evaluation_receipt(
            residual, obstruction, candidate_digest=candidate_digest
        )
        return status, oclass, evid, eval_receipt

    def solve(
        self,
        edge_values: Dict[Tuple[Any, Any], float],
        max_lifts: int = 1,
        tol: float = 1e-6,
        enable_cell_attachment: bool = False,
        candidate_digest: Optional[str] = None,
    ) -> SolverCascadeReceipt:
        """Executes the cascade under AuthorityEffect: None.

        Residual reduction uses float L1 / DDA (diagnostic).
        Terminal Exact claims are produced only by Gate-11 evaluate_obstruction.
        Evaluation stage also emits EvaluationReceipt wrapping the Gate-11 receipt.

        Optional candidate_digest binds the EvaluationReceipt to an upstream
        CandidatePacket; when omitted a stable topology+residual digest is used.
        """
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
            dual_kw = self._dual_fields_for_receipt(
                self.dda_engine.current_edge_values, initial_size
            )
            stages.append("ExactDualPricing")
            status, oclass, evid, eval_receipt = self._classify_and_evaluate(
                self.dda_engine.current_edge_values, candidate_digest=candidate_digest
            )
            if status != "Exact":
                status = status if status else "CLOSED_NONEXACT"
            return SolverCascadeReceipt(
                carrier_nodes=len(self.network.nodes),
                carrier_edges=len(self.network.edges),
                initial_residual_size=initial_size,
                final_residual_size=initial_size,
                stages_executed=stages,
                degree_window_reached=1,
                terminal_status=status,
                final_residual_triple=(foundation.phi1, foundation.gamma2, foundation.chi),
                attached_cells=attached_cells,
                lift_history=lift_history,
                admitted_complex_verified=admitted_ok,
                authority_effect="None",
                obstruction_class=oclass,
                evidence_sha256=evid,
                evaluation_receipt=eval_receipt,
                **dual_kw,
            )

        cert_gauge, (phi1_g, gamma2_g, chi_g) = self.dda_engine.step_dda(move_type="exact_d0")
        stages.append("ExactLocalGaugeFix")

        if phi1_g < tol and gamma2_g < tol:
            dual_kw = self._dual_fields_for_receipt(
                self.dda_engine.current_edge_values, phi1_g
            )
            stages.append("ExactDualPricing")
            status, oclass, evid, eval_receipt = self._classify_and_evaluate(
                self.dda_engine.current_edge_values, candidate_digest=candidate_digest
            )
            if status != "Exact":
                status = status if status else "CLOSED_NONEXACT"
            return SolverCascadeReceipt(
                carrier_nodes=len(self.network.nodes),
                carrier_edges=len(self.network.edges),
                initial_residual_size=initial_size,
                final_residual_size=phi1_g,
                stages_executed=stages,
                degree_window_reached=1,
                terminal_status=status,
                final_residual_triple=(phi1_g, gamma2_g, chi_g),
                attached_cells=attached_cells,
                lift_history=lift_history,
                admitted_complex_verified=admitted_ok,
                authority_effect="None",
                obstruction_class=oclass,
                evidence_sha256=evid,
                evaluation_receipt=eval_receipt,
                **dual_kw,
            )

        cert_multi, (phi1_m, gamma2_m, chi_m) = self.dda_engine.step_dda(move_type="multi_cycle_l1")
        stages.append("MultiCycleL1Descent")

        if phi1_m < tol and gamma2_m < tol:
            dual_kw = self._dual_fields_for_receipt(
                self.dda_engine.current_edge_values, phi1_m
            )
            stages.append("ExactDualPricing")
            status, oclass, evid, eval_receipt = self._classify_and_evaluate(
                self.dda_engine.current_edge_values, candidate_digest=candidate_digest
            )
            if status != "Exact":
                status = status if status else "CLOSED_NONEXACT"
            return SolverCascadeReceipt(
                carrier_nodes=len(self.network.nodes),
                carrier_edges=len(self.network.edges),
                initial_residual_size=initial_size,
                final_residual_size=phi1_m,
                stages_executed=stages,
                degree_window_reached=1,
                terminal_status=status,
                final_residual_triple=(phi1_m, gamma2_m, chi_m),
                attached_cells=attached_cells,
                lift_history=lift_history,
                admitted_complex_verified=admitted_ok,
                authority_effect="None",
                obstruction_class=oclass,
                evidence_sha256=evid,
                evaluation_receipt=eval_receipt,
                **dual_kw,
            )

        if enable_cell_attachment and (phi1_m > tol or gamma2_m > tol):
            attached, cell_added = self.attach_normal_cell(self.dda_engine.current_edge_values)
            if attached and cell_added:
                stages.append("HomologicalCellAttachment")
                attached_cells.append(cell_added)
                cert_post, (phi1_post, gamma2_post, chi_post) = self.dda_engine.step_dda(move_type="multi_cycle_l1")
                if phi1_post < tol and gamma2_post < tol:
                    dual_kw = self._dual_fields_for_receipt(
                        self.dda_engine.current_edge_values, phi1_post
                    )
                    stages.append("ExactDualPricing")
                    status, oclass, evid, eval_receipt = self._classify_and_evaluate(
                        self.dda_engine.current_edge_values, candidate_digest=candidate_digest
                    )
                    if status == "Exact":
                        status = "MODEL_CHANGED_SOLVED"
                    else:
                        status = status if status else "CLOSED_NONEXACT"
                    return SolverCascadeReceipt(
                        carrier_nodes=len(self.network.nodes),
                        carrier_edges=len(self.network.edges),
                        initial_residual_size=initial_size,
                        final_residual_size=phi1_post,
                        stages_executed=stages,
                        degree_window_reached=self.dda_engine.degree_window,
                        terminal_status=status,
                        final_residual_triple=(phi1_post, gamma2_post, chi_post),
                        attached_cells=attached_cells,
                        lift_history=lift_history,
                        admitted_complex_verified=admitted_ok,
                        authority_effect="None",
                        obstruction_class=oclass,
                        evidence_sha256=evid,
                        evaluation_receipt=eval_receipt,
                        **dual_kw,
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

        dual_kw = self._dual_fields_for_receipt(
            self.dda_engine.current_edge_values, float(phi1_m)
        )
        stages.append("ExactDualPricing")
        status_str, oclass, evid, eval_receipt = self._classify_and_evaluate(
            self.dda_engine.current_edge_values, candidate_digest=candidate_digest
        )

        final_triple = (phi1_m, gamma2_m, chi_m)
        if hasattr(term_cert, "final_residual") and term_cert.final_residual is not None:
            final_triple = tuple(term_cert.final_residual)
        elif hasattr(term_cert, "lifted_residuals") and term_cert.lifted_residuals is not None:
            final_triple = tuple(term_cert.lifted_residuals)
        final_size = float(final_triple[0])

        if status_str == "Exact" and final_size >= tol:
            status_str = "TYPED_OBSTRUCTION"

        return SolverCascadeReceipt(
            carrier_nodes=len(self.network.nodes),
            carrier_edges=len(self.network.edges),
            initial_residual_size=initial_size,
            final_residual_size=final_size,
            stages_executed=stages,
            degree_window_reached=self.dda_engine.degree_window,
            terminal_status=status_str,
            final_residual_triple=final_triple,
            attached_cells=attached_cells,
            lift_history=lift_history,
            algebraic_class_id=getattr(term_cert, "algebraic_class_id", None),
            admitted_complex_verified=admitted_ok,
            authority_effect="None",
            obstruction_class=oclass,
            evidence_sha256=evid,
            evaluation_receipt=eval_receipt,
            **dual_kw,
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
    print(f"Obstruction Class:     {receipt.obstruction_class}")
    print(f"Evidence SHA256:       {receipt.evidence_sha256}")
    if receipt.evaluation_receipt is not None:
        print(f"Evaluation digest:     {receipt.evaluation_receipt.digest()}")
        print(f"Eval classification:   {receipt.evaluation_receipt.classification}")
        print(f"Evaluator id:          {receipt.evaluation_receipt.evaluator_id}")
    print(f"Dual Certified:        {receipt.is_certified} (duality gap: {receipt.duality_gap})")
    print(f"Dual witness status:   {receipt.dual_witness_status}")
    print(f"Arithmetic mode:       {receipt.arithmetic_mode}")
    print(f"Exact Phi_k / gap:     {receipt.exact_phi_k} / {receipt.exact_gap}")
    print(f"Exact dual certified:  {receipt.is_exact_dual_certified()}")
    print(f"Attached Cells:        {receipt.attached_cells}")
    print(f"AuthorityEffect:       {receipt.authority_effect}")
    fence = receipt.as_evidence_dict().get("spine_fence", {})
    print(f"Spine fence:           float_as_exact={fence.get('float_as_exact')}; "
          f"estate_wide_phi_k={fence.get('estate_wide_phi_k_theorem')}; "
          f"pontryagin_pi={fence.get('pontryagin_dual_pi_programme')}; "
          f"continuum_wdw={fence.get('continuum_superspace_wdw')}")
