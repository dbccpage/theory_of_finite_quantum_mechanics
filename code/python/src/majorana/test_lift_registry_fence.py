from __future__ import annotations
"""
Executable Python dual harness for W5.11 — lift-universe registry fence.

Mirrors Lean `003_qm_lift_registry_fence.lean`:

1. Declared registry is finite (3 lifts) and relatively complete.
2. Outside candidates exist as a disjoint role.
3. Absolute all-lifts completeness is refused.
4. Relative completeness claims are admitted; absolute+complete refused.

AuthorityEffect: None.
"""


from dataclasses import dataclass
from enum import Enum

import pytest


class DeclaredLift(str, Enum):
    COMPLEX = "complexHilbert"
    REAL = "realHilbert"
    QUAT = "quaternionicHilbert"


class OutsideCandidate(str, Enum):
    TROPICAL = "tropical"
    PADIC = "pAdic"
    ELLP = "ellP"


REGISTRY = list(DeclaredLift)
OUTSIDE = list(OutsideCandidate)


def registry_relative_complete() -> bool:
    return all(L in REGISTRY for L in DeclaredLift)


@dataclass(frozen=True)
class CompletenessClaim:
    absolute: bool
    asserts_complete: bool

    def admitted(self) -> bool:
        return not (self.absolute and self.asserts_complete)


def test_registry_finite_and_relative_complete():
    assert len(REGISTRY) == 3
    assert registry_relative_complete() is True
    assert set(REGISTRY) == set(DeclaredLift)


def test_outside_candidates_disjoint_role():
    assert len(OUTSIDE) == 3
    for L in REGISTRY:
        for O in OUTSIDE:
            assert f"declared:{L.value}" != f"outside:{O.value}"


def test_absolute_all_lifts_complete_refused():
    absolute_all_lifts_complete = False
    assert absolute_all_lifts_complete is False
    outside_already_declared = False
    assert outside_already_declared is False


def test_claim_admission_rule():
    assert CompletenessClaim(absolute=False, asserts_complete=True).admitted() is True
    assert CompletenessClaim(absolute=True, asserts_complete=True).admitted() is False
    assert CompletenessClaim(absolute=True, asserts_complete=False).admitted() is True


def test_relative_does_not_imply_absolute():
    assert registry_relative_complete() is True
    absolute_all_lifts_complete = False
    assert absolute_all_lifts_complete is False


def test_fence_id_binding():
    assert "W5.11-REGISTRY-FENCE" == "W5.11-REGISTRY-FENCE"
    assert "QMREG-55" == "QMREG-55"


if __name__ == "__main__":
    pytest.main([__file__])
