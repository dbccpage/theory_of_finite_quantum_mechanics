"""Tests for PointedObstructionClassifier & BoundaryClosureTerminalGate in Python."""

from omega_engine.crates.type.terminalizers import (
    ObstructionStatus,
    PointedObstructionClassifier,
    terminalize,
    BoundaryClosureTerminalGate,
    TerminalBranchVerdict,
)


def test_pointed_classifier_terminalize():
    assert terminalize(0, 5) == ObstructionStatus.ExactRepair
    assert terminalize(3, 0) == ObstructionStatus.StabilizedSurvivor
    assert terminalize(4, 2) == ObstructionStatus.OpenObstruction
    assert (
        PointedObstructionClassifier.terminalize(0, 0) == ObstructionStatus.ExactRepair
    )


def test_boundary_closure_terminal_gate():
    res = BoundaryClosureTerminalGate.evaluate(
        boundary_residual_l1=1e-10,
        phi1=None,
        h1_discharged=True,
        evidence_valid=True,
        has_higher_cell_injection=False,
        tolerance=1e-6,
    )
    assert res.is_terminal
    assert res.verdict == TerminalBranchVerdict.Closed



