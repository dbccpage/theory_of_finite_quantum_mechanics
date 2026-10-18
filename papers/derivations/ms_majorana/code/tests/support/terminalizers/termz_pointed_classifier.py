"""Pointed Obstruction Classifier & Obstruction Status Terminalizer for Python."""

from enum import Enum


class ObstructionStatus(str, Enum):
    ExactRepair = "ExactRepair"
    StabilizedSurvivor = "StabilizedSurvivor"
    OpenObstruction = "OpenObstruction"


def terminalize(phi: int, gamma: int) -> ObstructionStatus:
    """`phi == 0 -> ExactRepair | gamma == 0 -> StabilizedSurvivor | else -> OpenObstruction`."""
    if phi == 0:
        return ObstructionStatus.ExactRepair
    elif gamma == 0:
        return ObstructionStatus.StabilizedSurvivor
    else:
        return ObstructionStatus.OpenObstruction


class PointedObstructionClassifier:
    @staticmethod
    def terminalize(phi: int, gamma: int) -> ObstructionStatus:
        return terminalize(phi, gamma)
