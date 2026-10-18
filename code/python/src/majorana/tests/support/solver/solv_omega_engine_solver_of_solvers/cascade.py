"""OesosCascade: compose stages + Prime 002; no residual math in-body.

AuthorityEffect: None. Calls handlers that may use homology/residuals.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from omega_engine.crates.prime.prime_000 import (
    AdmissionDecision,
    AdmissionKind,
    DeclarationPacket,
    admit_declaration,
)
from omega_engine.crates.prime.prime_002 import (
    CanContinueInput,
    CanContinueResult,
    can_continue,
)

from .problem import ObstructionProblem
from .receipt import CascadeReceipt, StageRecord
from .registry import SolverRegistry
from .stage import CascadeStage, StageKind


@dataclass
class OesosCascade:
    """Object-set cascade controller (not Engine, not Pipeline, not math)."""

    registry: SolverRegistry
    stages: List[CascadeStage] = field(default_factory=list)
    authority_effect: str = "None"

    def run(
        self,
        problem: ObstructionProblem,
        declaration: DeclarationPacket,
        continue_input: Optional[CanContinueInput] = None,
        handler_kwargs: Optional[Dict[str, Any]] = None,
    ) -> CascadeReceipt:
        receipt = CascadeReceipt(problem_id=problem.problem_id)
        admission: AdmissionDecision = admit_declaration(declaration)
        if admission.kind != AdmissionKind.ACCEPT_DECLARATION:
            receipt.terminal_status = admission.kind.value
            receipt.record(
                StageRecord(
                    stage="prime_000",
                    solver_id="prime_000",
                    status="REFUSED",
                    residual_mass=float("nan"),
                    detail={"reason": admission.reason, "steps": list(admission.steps)},
                )
            )
            return receipt

        if continue_input is not None:
            cont: CanContinueResult = can_continue(continue_input)
            if not cont.may_continue:
                receipt.terminal_status = cont.reason
                receipt.record(
                    StageRecord(
                        stage="prime_002",
                        solver_id="prime_002",
                        status="HALT",
                        residual_mass=float("nan"),
                        detail={
                            "reason": cont.reason,
                            "anti_cheat": list(cont.anti_cheat_violations),
                        },
                    )
                )
                return receipt

        kwargs = dict(handler_kwargs or {})
        kwargs.setdefault("problem", problem)
        residual_mass = float(kwargs.get("initial_residual_mass", 1.0))

        for stage in self.stages:
            if stage.handler is None:
                solvers = self.registry.solvers_for(problem.residual_class)
                solver_id = stage.solver_id or (solvers[0] if solvers else "none")
                receipt.record(
                    StageRecord(
                        stage=stage.kind.value,
                        solver_id=solver_id,
                        status="DECLARED",
                        residual_mass=residual_mass,
                        detail={"note": "no handler; declared only"},
                    )
                )
                continue
            result = stage.handler(**kwargs)
            if isinstance(result, dict):
                residual_mass = float(result.get("residual_mass", residual_mass))
                status = str(result.get("status", "OK"))
                detail = {k: v for k, v in result.items() if k not in ("residual_mass", "status")}
            else:
                status = "OK"
                detail = {"result": result}
            receipt.record(
                StageRecord(
                    stage=stage.kind.value,
                    solver_id=stage.solver_id,
                    status=status,
                    residual_mass=residual_mass,
                    detail=detail,
                )
            )
            if stage.kind == StageKind.TERMINAL or status in ("SOLVED", "REFUSED", "OBSTRUCTED"):
                receipt.terminal_status = status
                break
        else:
            receipt.terminal_status = "COMPLETED_STAGES"
        return receipt


