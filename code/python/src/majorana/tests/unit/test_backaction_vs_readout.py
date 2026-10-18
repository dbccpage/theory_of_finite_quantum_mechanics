from __future__ import annotations
"""
Executable Python dual harness for W6.17 (measurement back-action vs readout).

Mirrors Lean `003_qm_backaction_vs_readout.lean`:

1. Readout = outcome mass; back-action = sector update (role-distinct, coupled).
2. Pure states undisturbed on matching outcome; mixed states disturbed.
3. Universal non-disturbing projective readout underivable / refuted on FinL1.
4. Soft/gentle half-kill toy under lift host: smaller disturbance than projective;
   still not universal nondisturbing; full POVM catalogue OPEN.
5. Soft hierarchy + face decoupling: quarter < half < projective; soft post-total
   ≠ readout mass; soft density readout mass bind.

AuthorityEffect: None. Mutation-capable.
"""


from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class BitWeight:
    w0: int
    w1: int

    @property
    def total(self) -> int:
        return self.w0 + self.w1

    @property
    def is_mixed(self) -> bool:
        return self.w0 > 0 and self.w1 > 0


class Outcome(str, Enum):
    O0 = "o0"
    O1 = "o1"


def readout(w: BitWeight, o: Outcome) -> int:
    return w.w0 if o is Outcome.O0 else w.w1


def back_action(w: BitWeight, o: Outcome) -> BitWeight:
    if o is Outcome.O0:
        return BitWeight(w.w0, 0)
    return BitWeight(0, w.w1)


PURE0 = BitWeight(1, 0)
PURE1 = BitWeight(0, 1)
FAIR = BitWeight(1, 1)
PRIOR31 = BitWeight(3, 1)


def test_readout_matches_sectors():
    assert readout(PRIOR31, Outcome.O0) == 3
    assert readout(PRIOR31, Outcome.O1) == 1


def test_readout_eq_post_total():
    for w in (PURE0, FAIR, PRIOR31):
        for o in (Outcome.O0, Outcome.O1):
            assert readout(w, o) == back_action(w, o).total


def test_pure_undisturbed_on_matching_outcome():
    assert back_action(PURE0, Outcome.O0) == PURE0
    assert back_action(PURE1, Outcome.O1) == PURE1


def test_mixed_disturbed():
    assert FAIR.is_mixed
    assert back_action(FAIR, Outcome.O0) != FAIR
    assert back_action(FAIR, Outcome.O1) != FAIR
    assert back_action(PRIOR31, Outcome.O1) == BitWeight(0, 1)
    assert back_action(PRIOR31, Outcome.O1) != PRIOR31


def test_readout_same_mass_pure_vs_fair_o0():
    assert readout(PURE0, Outcome.O0) == 1
    assert readout(FAIR, Outcome.O0) == 1
    assert back_action(PURE0, Outcome.O0) == PURE0
    assert back_action(FAIR, Outcome.O0) != FAIR


def test_no_universal_nondisturbing_projective():
    assert any(back_action(w, o) != w for w in (FAIR, PRIOR31) for o in Outcome)


class ImportStatus(str, Enum):
    DERIVED = "derived"
    UNDERIVABLE = "underivable"
    CONDITIONAL_IMPORT = "conditionalImport"


READOUT_STATUS = ImportStatus.DERIVED
BACKACTION_CLASSICAL = ImportStatus.DERIVED
NONDISTURBING_FROM_FINL1 = ImportStatus.UNDERIVABLE
GENTLE_UNDER_LIFT = ImportStatus.CONDITIONAL_IMPORT


def test_import_status_packaging():
    assert READOUT_STATUS is ImportStatus.DERIVED
    assert BACKACTION_CLASSICAL is ImportStatus.DERIVED
    assert NONDISTURBING_FROM_FINL1 is ImportStatus.UNDERIVABLE
    assert GENTLE_UNDER_LIFT is ImportStatus.CONDITIONAL_IMPORT


def test_backaction_vs_readout_package():
    assert readout(FAIR, Outcome.O0) == 1
    assert back_action(FAIR, Outcome.O0) != FAIR
    assert back_action(PURE0, Outcome.O0) == PURE0
    assert READOUT_STATUS is ImportStatus.DERIVED
    assert BACKACTION_CLASSICAL is ImportStatus.DERIVED
    assert NONDISTURBING_FROM_FINL1 is ImportStatus.UNDERIVABLE
    assert GENTLE_UNDER_LIFT is ImportStatus.CONDITIONAL_IMPORT




def disturbance(prior: BitWeight, post: BitWeight) -> int:
    return abs(prior.w0 - post.w0) + abs(prior.w1 - post.w1)


def soft_back_action(w: BitWeight, o: Outcome) -> BitWeight:
    """Half-kill soft update: floor-halve the unmeasured sector mass."""
    if o is Outcome.O0:
        return BitWeight(w.w0, w.w1 // 2)
    return BitWeight(w.w0 // 2, w.w1)


PRIOR42 = BitWeight(4, 2)


def soft_gentle_requires_lift_host(host: str) -> bool:
    if host == "finL1Classical":
        return False
    if host == "complexHilbertLift":
        return True
    raise ValueError(host)


def test_soft_gentler_than_projective_prior42():
    proj = back_action(PRIOR42, Outcome.O0)
    soft = soft_back_action(PRIOR42, Outcome.O0)
    assert proj == BitWeight(4, 0)
    assert soft == BitWeight(4, 1)
    assert disturbance(PRIOR42, soft) == 1
    assert disturbance(PRIOR42, proj) == 2
    assert disturbance(PRIOR42, soft) < disturbance(PRIOR42, proj)


def test_soft_still_disturbs_and_not_universal_nondisturbing():
    assert soft_back_action(PRIOR42, Outcome.O0) != PRIOR42
    assert any(
        soft_back_action(w, o) != w for w in (PRIOR42, PRIOR31, FAIR) for o in Outcome
    )


def test_soft_gentle_host_fence():
    assert soft_gentle_requires_lift_host("finL1Classical") is False
    assert soft_gentle_requires_lift_host("complexHilbertLift") is True


def test_soft_gentle_instrument_package():
    assert disturbance(PRIOR42, soft_back_action(PRIOR42, Outcome.O0)) == 1
    assert disturbance(PRIOR42, back_action(PRIOR42, Outcome.O0)) == 2
    assert soft_back_action(PRIOR42, Outcome.O0) != PRIOR42
    assert soft_gentle_requires_lift_host("complexHilbertLift") is True
    assert soft_gentle_requires_lift_host("finL1Classical") is False
    soft_gentle_activation = "activatedToyMech"
    full_povm_catalogue_open = True
    assert soft_gentle_activation == "activatedToyMech"
    assert full_povm_catalogue_open is True
    assert GENTLE_UNDER_LIFT is ImportStatus.CONDITIONAL_IMPORT




def soft_quarter_back_action(w: BitWeight, o: Outcome) -> BitWeight:
    """Quarter-kill soft update: keep 3/4 of unmeasured sector mass."""
    if o is Outcome.O0:
        return BitWeight(w.w0, (3 * w.w1) // 4)
    return BitWeight((3 * w.w0) // 4, w.w1)


PRIOR84 = BitWeight(8, 4)
SOFT_EFFECT0 = (2, 1, 1, 2)
SOFT_EFFECT1 = (2, -1, -1, 2)
RHO_PLUS = (1, 1, 1, 1)


def soft_density_readout(
    e: tuple[int, int, int, int], rho: tuple[int, int, int, int]
) -> int:
    e00, e01, e10, e11 = e
    r00, r01, r10, r11 = rho
    return e00 * r00 + e01 * r10 + e10 * r01 + e11 * r11


def test_soft_disturbance_hierarchy_prior84():
    q = soft_quarter_back_action(PRIOR84, Outcome.O0)
    h = soft_back_action(PRIOR84, Outcome.O0)
    p = back_action(PRIOR84, Outcome.O0)
    assert q == BitWeight(8, 3)
    assert h == BitWeight(8, 2)
    assert p == BitWeight(8, 0)
    assert disturbance(PRIOR84, q) == 1
    assert disturbance(PRIOR84, h) == 2
    assert disturbance(PRIOR84, p) == 4
    assert disturbance(PRIOR84, q) < disturbance(PRIOR84, h) < disturbance(PRIOR84, p)


def test_soft_breaks_total_coupling_prior42():
    soft_post = soft_back_action(PRIOR42, Outcome.O0)
    proj_post = back_action(PRIOR42, Outcome.O0)
    assert readout(PRIOR42, Outcome.O0) == 4
    assert soft_post.total == 5
    assert readout(PRIOR42, Outcome.O0) != soft_post.total
    assert readout(PRIOR42, Outcome.O0) == proj_post.total


def test_soft_density_readout_resolution():
    m0 = soft_density_readout(SOFT_EFFECT0, RHO_PLUS)
    m1 = soft_density_readout(SOFT_EFFECT1, RHO_PLUS)
    assert m0 == 6 and m1 == 2 and m0 + m1 == 8
    assert SOFT_EFFECT0[1] != 0


def test_soft_gentle_hierarchy_package():
    assert disturbance(PRIOR84, soft_quarter_back_action(PRIOR84, Outcome.O0)) == 1
    assert disturbance(PRIOR84, soft_back_action(PRIOR84, Outcome.O0)) == 2
    assert disturbance(PRIOR84, back_action(PRIOR84, Outcome.O0)) == 4
    assert readout(PRIOR42, Outcome.O0) != soft_back_action(PRIOR42, Outcome.O0).total
    assert (
        soft_density_readout(SOFT_EFFECT0, RHO_PLUS)
        + soft_density_readout(SOFT_EFFECT1, RHO_PLUS)
        == 8
    )
    assert soft_gentle_requires_lift_host("complexHilbertLift") is True
    full_povm_catalogue_open = True
    assert full_povm_catalogue_open is True
