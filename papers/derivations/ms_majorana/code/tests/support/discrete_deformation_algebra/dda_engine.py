"""3-Algorithm Execution Engine (Foundation, DDA Step, Window Lift & Termination).

Implements finite, certificate-bearing repair, deformation, and degree-window lifting
under AuthorityEffect = None.
"""

import hashlib
from dataclasses import field
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple
try:
    from omega_engine.crates.functional import phi1, gamma2, xi
except ImportError:
    phi1 = None
    gamma2 = None
    xi = None

from omega_engine.crates.pipeline.certified_pipeline import FingerprintedBag
from omega_engine.crates.residuals.network_residual import (
    Network,
    curl,
    detect_tetrahedra,
    multi_cycle_l1_joint,
    residual_after_gauge_fix,
)



class TerminationStatus(Enum):
    """Execution termination status."""
    SOLVED = "SOLVED"
    AUTHORIZATION_EXHAUSTED = "AUTHORIZATION_EXHAUSTED"
    TYPED_OBSTRUCTION = "TYPED_OBSTRUCTION"


@dataclass
class FoundationCert:
    """Algorithm 1: Foundation Certificate fingerprinting carrier, observer, and initial residuals."""
    carrier_hash: str
    observer_name: str
    phi1: float
    gamma2: float
    chi: float
    authority_effect: str = "None"

    def is_valid(self) -> bool:
        return len(self.carrier_hash) == 64 and self.authority_effect == "None"


@dataclass
class DDAStepCert:
    """Algorithm 2: DDA Step Certificate tracking single licensed repair moves."""
    before_hash: str
    after_hash: str
    move_type: str
    delta_phi1: float
    delta_gamma2: float
    loss_ledger: Dict[str, float] = field(default_factory=dict)
    authority_effect: str = "None"

    def is_valid(self) -> bool:
        return len(self.before_hash) == 64 and len(self.after_hash) == 64 and self.authority_effect == "None"


@dataclass
class WindowLiftCert:
    """Algorithm 3: Window Lift Certificate tracking degree transition C^k -> C^{k+1}."""
    from_degree: int
    to_degree: int
    num_higher_cells: int
    lifted_residuals: Tuple[float, float, float]
    trigger_curvature_mass: float = 0.0
    lift_kind: str = "tetrahedra"
    authority_effect: str = "None"

    @property
    def num_tetrahedra(self) -> int:
        """Backward-compatible alias for degree 1->2 tetrahedra count."""
        return self.num_higher_cells

    def is_valid(self) -> bool:
        return self.to_degree == self.from_degree + 1 and self.authority_effect == "None"


@dataclass
class TerminationCert:
    """Algorithm 3: Terminal Obstruction / Solved Certificate."""
    status: TerminationStatus
    final_residual: Tuple[float, float, float]
    degree_window: int
    total_steps: int
    algebraic_class_id: str = "exact"
    authority_effect: str = "None"


class DDAEngine:
    """3-Algorithm Execution Engine for finite cochain complexes."""

    def __init__(self, network: Network, observer_name: str = "L1_coordinate_wise"):
        self.network = network
        self.observer_name = observer_name
        self.current_edge_values: Dict[Tuple[Any, Any], float] = {}
        self.current_face_values: Dict[Tuple[Any, Any, Any], float] = {}
        self.degree_window: int = 1
        self.foundation_history: List[FoundationCert] = []
        self.step_history: List[DDAStepCert] = []
        self.lift_history: List[WindowLiftCert] = []
        self.termination_history: List[TerminationCert] = []
        self.current_bag: Optional[FingerprintedBag] = None

    def _record_termination(self, cert: TerminationCert) -> TerminationCert:
        self.termination_history.append(cert)
        return cert

    def run_foundation(self, edge_values: Dict[Tuple[Any, Any], float]) -> FoundationCert:
        """Algorithm 1: Foundation step initializing cochains and computing initial residuals."""
        self.current_edge_values = dict(edge_values)

        res_fix = residual_after_gauge_fix(self.network, self.current_edge_values, method="l1")
        phi1 = res_fix["residual_size"]

        curls = curl(self.network, self.current_edge_values)
        gamma2 = float(sum(abs(v) for v in curls.values())) if curls else 0.0

        chi = phi1 if gamma2 < 1e-6 else 0.0


        h = hashlib.sha256()
        h.update(str(self.network.nodes).encode())
        h.update(str(self.network.edges).encode())
        h.update(self.observer_name.encode())
        carrier_hash = h.hexdigest()

        bag_data = {
            f"edge_{u}_{v}": f"{val:.6f}" for (u, v), val in sorted(self.current_edge_values.items())
        }
        self.current_bag = FingerprintedBag(name=f"state_deg_{self.degree_window}", data=bag_data)

        cert = FoundationCert(
            carrier_hash=carrier_hash,
            observer_name=self.observer_name,
            phi1=phi1,
            gamma2=gamma2,
            chi=chi,
            authority_effect="None",
        )
        self.foundation_history.append(cert)
        return cert

    def step_dda(self, move_type: str = "exact_d0") -> Tuple[DDAStepCert, Tuple[float, float, float]]:
        """Algorithm 2: Single DDA repair step (exact d0 gauge fix or coexact curl reduction)."""
        if self.current_bag is None:
            raise RuntimeError("Must call run_foundation before step_dda")

        before_hash = self.current_bag.fingerprint()

        res_before = residual_after_gauge_fix(self.network, self.current_edge_values, method="l1")
        phi1_before = res_before["residual_size"]
        curls_before = curl(self.network, self.current_edge_values)
        gamma2_before = float(sum(abs(v) for v in curls_before.values())) if curls_before else 0.0

        loss_ledger = {}

        if move_type == "exact_d0":
            self.current_edge_values = res_before["residual"]
            loss_ledger["gauge_potentials_removed"] = float(sum(abs(v) for v in res_before["potentials"].values()))
        elif move_type == "coexact_curl":
            if self.network.faces:
                for u, v, w in self.network.faces:
                    face_curl = (
                        self.current_edge_values.get((u, v), 0.0)
                        + self.current_edge_values.get((v, w), 0.0)
                        + self.current_edge_values.get((w, u), 0.0)
                    )
                    adj = face_curl / 3.0
                    if (u, v) in self.current_edge_values:
                        self.current_edge_values[(u, v)] -= adj
                    if (v, w) in self.current_edge_values:
                        self.current_edge_values[(v, w)] -= adj
                    if (w, u) in self.current_edge_values:
                        self.current_edge_values[(w, u)] -= adj
                loss_ledger["curl_mass_canceled"] = float(gamma2_before)
        elif move_type == "multi_cycle_l1":
            res_multi = multi_cycle_l1_joint(self.network, self.current_edge_values)
            self.current_edge_values = res_multi["residual"]
            loss_ledger["gauge_potentials_removed"] = float(sum(abs(v) for v in res_multi["potentials"].values()))
            loss_ledger["cycle_coeffs_removed"] = float(sum(abs(v) for v in res_multi["cycle_coeffs"].values()))

        res_after = residual_after_gauge_fix(self.network, self.current_edge_values, method="l1")
        phi1_after = res_after["residual_size"]
        curls_after = curl(self.network, self.current_edge_values)
        gamma2_after = float(sum(abs(v) for v in curls_after.values())) if curls_after else 0.0
        chi_after = phi1_after if gamma2_after < 1e-6 else 0.0

        bag_data = {
            f"edge_{u}_{v}": f"{val:.6f}" for (u, v), val in sorted(self.current_edge_values.items())
        }
        self.current_bag = FingerprintedBag(name=f"state_deg_{self.degree_window}_step_{len(self.step_history)+1}", data=bag_data)
        after_hash = self.current_bag.fingerprint()

        cert = DDAStepCert(
            before_hash=before_hash,
            after_hash=after_hash,
            move_type=move_type,
            delta_phi1=phi1_after - phi1_before,
            delta_gamma2=gamma2_after - gamma2_before,
            loss_ledger=loss_ledger,
            authority_effect="None",
        )
        self.step_history.append(cert)
        return cert, (phi1_after, gamma2_after, chi_after)

    def lift_or_terminate(
        self,
        current_residuals: Tuple[float, float, float],
        tol: float = 1e-6,
        max_lifts: int = 1,
    ) -> TerminationCert:
        """Algorithm 3: Evaluates degree fixed point and decides whether to lift window or terminate."""
        phi_k, gamma_kp1, chi_k = current_residuals

        if phi_k < tol and gamma_kp1 < tol and chi_k < tol:
            return self._record_termination(TerminationCert(
                status=TerminationStatus.SOLVED,
                final_residual=current_residuals,
                degree_window=self.degree_window,
                total_steps=len(self.step_history),
                algebraic_class_id="exact",
                authority_effect="None",
            ))

        if self.degree_window <= max_lifts:
            from_deg = self.degree_window
            to_deg = from_deg + 1

            if from_deg == 1:
                self.degree_window = to_deg
                tetrahedra = detect_tetrahedra(self.network)
                self.network = Network(
                    nodes=self.network.nodes,
                    edges=self.network.edges,
                    faces=self.network.faces,
                    tetrahedra=tetrahedra,
                )
                self.current_face_values = curl(self.network, self.current_edge_values)

                from omega_engine.crates.discrete_deformation_algebra.degree_generic_residual import residual_triple_for_lift
                lifted_residuals = residual_triple_for_lift(self.network, degree=2, cochain_values=self.current_face_values, method="l1_gauge")

                lift_cert = WindowLiftCert(
                    from_degree=from_deg,
                    to_degree=to_deg,
                    num_higher_cells=len(tetrahedra),
                    lifted_residuals=lifted_residuals,
                    trigger_curvature_mass=gamma_kp1,
                    lift_kind="tetrahedra",
                    authority_effect="None",
                )
                self.lift_history.append(lift_cert)

                bag_data = {
                    f"face_{u}_{v}_{w}": f"{val:.6f}" for (u, v, w), val in sorted(self.current_face_values.items())
                }
                self.current_bag = FingerprintedBag(name=f"state_deg_{self.degree_window}", data=bag_data)

                return self.lift_or_terminate(lifted_residuals, tol=tol, max_lifts=max_lifts)
            else:
                from omega_engine.crates.functional.higher_simplex_assembly import discover_higher_cells_for_lift
                from omega_engine.crates.discrete_deformation_algebra.degree_generic_residual import residual_triple_for_lift

                cells, lift_kind = discover_higher_cells_for_lift(self.network, from_degree=from_deg)
                self.degree_window = to_deg

                if cells:
                    lifted_residuals = residual_triple_for_lift(self.network, degree=to_deg, cochain_values=self.current_face_values, method="l1_gauge")
                    lift_cert = WindowLiftCert(
                        from_degree=from_deg,
                        to_degree=to_deg,
                        num_higher_cells=len(cells),
                        lifted_residuals=lifted_residuals,
                        trigger_curvature_mass=gamma_kp1,
                        lift_kind=lift_kind,
                        authority_effect="None",
                    )
                    self.lift_history.append(lift_cert)

                    bag_data = {
                        f"higher_cell_{i}": str(cell) for i, cell in enumerate(cells)
                    }
                    self.current_bag = FingerprintedBag(name=f"state_deg_{self.degree_window}", data=bag_data)

                    return self.lift_or_terminate(lifted_residuals, tol=tol, max_lifts=max_lifts)
                else:
                    lift_cert = WindowLiftCert(
                        from_degree=from_deg,
                        to_degree=to_deg,
                        num_higher_cells=0,
                        lifted_residuals=current_residuals,
                        trigger_curvature_mass=gamma_kp1,
                        lift_kind="unsupported",
                        authority_effect="None",
                    )
                    self.lift_history.append(lift_cert)

                    alg_class = f"unsupported-lift:C^{from_deg}->C^{to_deg}:curvature_{gamma_kp1:.4f}"
                    return self._record_termination(TerminationCert(
                        status=TerminationStatus.AUTHORIZATION_EXHAUSTED,
                        final_residual=current_residuals,
                        degree_window=self.degree_window,
                        total_steps=len(self.step_history),
                        algebraic_class_id=alg_class,
                        authority_effect="None",
                    ))

        if gamma_kp1 < 1e-6 and chi_k > 1e-6:
            alg_class = f"closed-residual:harmonic_h1_norm_{chi_k:.4f}"
        else:
            alg_class = f"open-obstruction:curvature_gamma_{self.degree_window+1}_{gamma_kp1:.4f}"

        return self._record_termination(TerminationCert(
            status=TerminationStatus.TYPED_OBSTRUCTION,
            final_residual=current_residuals,
            degree_window=self.degree_window,
            total_steps=len(self.step_history),
            algebraic_class_id=alg_class,
            authority_effect="None",
        ))


    def evaluate_majorana_parity_obstruction(self, threshold: float = 1e-4) -> Any:
        """Evaluates GF(2) Majorana parity obstruction on current continuous edge residuals."""
        try:
            from .majorana_cohomology_bridge import evaluate_network_majorana_parity
        except ImportError:
            from omega_engine.crates.majorana.majorana_cohomology_bridge import evaluate_network_majorana_parity

        return evaluate_network_majorana_parity(
            self.network, self.current_edge_values, threshold=threshold
        )




