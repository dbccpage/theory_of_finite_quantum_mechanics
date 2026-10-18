"""Boundary Closure Terminal Gate for Python."""

import math
from enum import Enum
from typing import Optional
from pydantic import BaseModel


class TerminalBranchVerdict(str, Enum):
    Open = "Open"
    Closed = "Closed"
    Invalid = "Invalid"
    EvidenceInvalid = "EvidenceInvalid"
    ObstructionPresent = "ObstructionPresent"
    NoLiftFound = "NoLiftFound"


class TerminalBranchResult(BaseModel):
    boundary_residual_l1: float
    phi1: Optional[float] = None
    h1_discharged: bool
    evidence_valid: bool
    is_terminal: bool
    verdict: TerminalBranchVerdict


class BoundaryClosureTerminalGate:
    @staticmethod
    def evaluate(
        boundary_residual_l1: float,
        phi1: Optional[float],
        h1_discharged: bool,
        evidence_valid: bool,
        has_higher_cell_injection: bool,
        tolerance: float,
    ) -> TerminalBranchResult:
        if (
            not math.isfinite(boundary_residual_l1)
            or boundary_residual_l1 < 0.0
            or not math.isfinite(tolerance)
            or tolerance <= 0.0
            or (phi1 is not None and (not math.isfinite(phi1) or phi1 < 0.0))
        ):
            return TerminalBranchResult(
                boundary_residual_l1=boundary_residual_l1,
                phi1=phi1,
                h1_discharged=h1_discharged,
                evidence_valid=evidence_valid,
                is_terminal=False,
                verdict=TerminalBranchVerdict.Invalid,
            )

        if phi1 is not None and phi1 > tolerance and not has_higher_cell_injection:
            return TerminalBranchResult(
                boundary_residual_l1=boundary_residual_l1,
                phi1=phi1,
                h1_discharged=h1_discharged,
                evidence_valid=evidence_valid,
                is_terminal=False,
                verdict=TerminalBranchVerdict.NoLiftFound,
            )

        if not evidence_valid:
            return TerminalBranchResult(
                boundary_residual_l1=boundary_residual_l1,
                phi1=phi1,
                h1_discharged=h1_discharged,
                evidence_valid=evidence_valid,
                is_terminal=False,
                verdict=TerminalBranchVerdict.EvidenceInvalid,
            )

        if not h1_discharged:
            return TerminalBranchResult(
                boundary_residual_l1=boundary_residual_l1,
                phi1=phi1,
                h1_discharged=h1_discharged,
                evidence_valid=evidence_valid,
                is_terminal=False,
                verdict=TerminalBranchVerdict.ObstructionPresent,
            )

        is_terminal = boundary_residual_l1 < tolerance

        return TerminalBranchResult(
            boundary_residual_l1=boundary_residual_l1,
            phi1=phi1,
            h1_discharged=h1_discharged,
            evidence_valid=evidence_valid,
            is_terminal=is_terminal,
            verdict=TerminalBranchVerdict.Closed
            if is_terminal
            else TerminalBranchVerdict.Open,
        )
