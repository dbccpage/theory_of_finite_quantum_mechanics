"""Historical Exploratory Solver Adapter for Gauge, Higgs, and SUSY Ansatz.

Conforms to contract specification:
    urn:omega:math:solver:v1.0.0

AuthorityEffect: None.
Status: Historical exploratory ansatz demonstrating manual scale injection.
"""

from __future__ import annotations

try:
    from universe_anomalonica.omega_engine.solver.solver import (
        BaseSolver,
        SolverCertificate,
        SolverInput,
        SolverOutput,
    )
except ImportError:
    from .solver import (
        BaseSolver,
        SolverCertificate,
        SolverInput,
        SolverOutput,
    )

try:
    from universe_anomalonica.omega_engine.solvers.gauge_higgs_susy_derivation import (
        GaugeHiggsSUSYResult,
        run_full_gauge_higgs_susy_derivation,
    )
except ImportError:
    from gauge_higgs_susy_derivation import (
        GaugeHiggsSUSYResult,
        run_full_gauge_higgs_susy_derivation,
    )
try:
    from universe_anomalonica.omega_engine.type.refusal import Refusal
except ImportError:
    class Refusal:
        def __init__(self, reason: str = ""):
            self.reason = reason


class GaugeHiggsSUSYSolverAdapter(BaseSolver):
    """Historical adapter for Gauge Group, Higgs Field, and SUSY Saturation Scale exploratory ansatz."""

    def __init__(self, solver_id: str = "gauge_higgs_susy_solver"):
        super().__init__(
            solver_id=solver_id,
            category="historical_simplicial_ansatz",
            solver_version="v1.0.0",
        )

    def solve(self, input_data: SolverInput) -> SolverOutput:
        payload = input_data.data or input_data.parameters or {}
        vev_gev = float(payload.get("vev_gev", 246.0))
        res = run_full_gauge_higgs_susy_derivation(vev_gev=vev_gev)

        if isinstance(res, Refusal):
            return SolverOutput(
                problem_id=input_data.problem_id,
                solver_id=self.solver_id,
                status="FAILED",
                residual_mass=1.0,
                residual_vector=[1.0],
                metadata={"error": res.reason},
                authority_effect="None",
            )

        val: GaugeHiggsSUSYResult = res

        output = SolverOutput(
            problem_id=input_data.problem_id,
            solver_id=self.solver_id,
            status="HISTORICAL_ANSATZ_DEMO",
            residual_mass=val.l1_repair_distance,
            residual_vector=[val.l1_repair_distance],
            metadata={
                "derived_gauge_group": val.derived_gauge_group,
                "higgs_vev_gev": val.higgs_derivation.vev_gev,
                "higgs_mass_gev": val.higgs_derivation.higgs_mass_gev,
                "susy_scale_tev": val.susy_scale_tev,
                "note": (
                    "Historical exploratory ansatz demonstrating manual scale injection; "
                    "does not constitute a certified Hodge calculation or physical derivation."
                ),
            },
            certificate=SolverCertificate(
                certificate_type="HISTORICAL_UNVERIFIED_ANSATZ",
                witness_data={
                    "witness_id": val.witness.witness_id,
                    "source_layer": val.witness.source_layer,
                    "target_layer": val.witness.target_layer,
                },
                is_valid=False,
                certificate_hash=val.witness.witness_id,
            ),
            authority_effect="None",
        )
        return output
