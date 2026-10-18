from __future__ import annotations
"""
Executable Python dual for W8.1 / OBS D5 — partial MAction dual-slot deepen.

Mirrors Lean `004_wave8_partial_maction.lean`:

1. Partial write applies iff tip equals expected base, else refuses.
2. OrderIndependenceAt requires both sequentializations fully succeed and agree.
3. Concurrent tip=0 writes both expecting base 0: each applies alone; both
   sequentializations refuse → orderIndependenceLaw fails (valuable negative).
4. corePartial preserves binary / family meets → coreMeets = survives.
5. Survival matrix: coreMeets=survives; orderIndependence=failsWithCounterexample;
   bareDifferenceNogo + foldStrictBudget still open.

AuthorityEffect: None. Mutation-capable: flip any asserted kill to fail the suite.
Not Wave-8 exit. Not W8.2. Not D5 close (2 residual slots open).
"""


from dataclasses import dataclass
from enum import Enum
from typing import Optional


# ---------------------------------------------------------------------------
# Toy concurrent-edit carrier (dual of Lean Edit / editAct / actSeq)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Edit:
    kind: str  # "id" | "write"
    expected_base: Optional[int] = None

    @staticmethod
    def id() -> "Edit":
        return Edit(kind="id")

    @staticmethod
    def write(expected_base: int) -> "Edit":
        return Edit(kind="write", expected_base=expected_base)


def edit_act(edit: Edit, tip: int) -> Optional[int]:
    """Partial act: write b applies only when tip == b, then advances by one."""
    if edit.kind == "id":
        return tip
    if edit.kind == "write":
        assert edit.expected_base is not None
        if tip == edit.expected_base:
            return tip + 1
        return None
    raise ValueError(f"unknown edit kind: {edit.kind}")


def act_seq(a: Edit, b: Edit, tip: int) -> Optional[int]:
    """Option-bind sequential composition: apply a, then b on the result."""
    mid = edit_act(a, tip)
    if mid is None:
        return None
    return edit_act(b, mid)


def order_independent_at(a: Edit, b: Edit, tip: int) -> bool:
    """Both sequentializations fully succeed and yield the same result."""
    ab = act_seq(a, b, tip)
    ba = act_seq(b, a, tip)
    return ab is not None and ba is not None and ab == ba


def order_independence_law(edits: list[Edit], tips: list[int]) -> bool:
    """
    Naive survival claim: whenever both acts apply individually at tip,
    they are order-independent at tip.
    """
    for a in edits:
        for b in edits:
            for tip in tips:
                if edit_act(a, tip) is not None and edit_act(b, tip) is not None:
                    if not order_independent_at(a, b, tip):
                        return False
    return True


# ---------------------------------------------------------------------------
# Survival matrix dual
# ---------------------------------------------------------------------------


class SurvivalSlot(str, Enum):
    CORE_MEETS = "coreMeets"
    ORDER_INDEPENDENCE = "orderIndependence"
    BARE_DIFFERENCE_NOGO = "bareDifferenceNogo"
    FOLD_STRICT_BUDGET = "foldStrictBudget"


class SurvivalVerdict(str, Enum):
    SURVIVES = "survives"
    FAILS_WITH_COUNTEREXAMPLE = "failsWithCounterexample"
    OPEN_WIREFRAME = "openWireframe"


SURVIVAL_MATRIX: dict[SurvivalSlot, SurvivalVerdict] = {
    SurvivalSlot.CORE_MEETS: SurvivalVerdict.SURVIVES,
    SurvivalSlot.ORDER_INDEPENDENCE: SurvivalVerdict.FAILS_WITH_COUNTEREXAMPLE,
    SurvivalSlot.BARE_DIFFERENCE_NOGO: SurvivalVerdict.OPEN_WIREFRAME,
    SurvivalSlot.FOLD_STRICT_BUDGET: SurvivalVerdict.OPEN_WIREFRAME,
}


# ---------------------------------------------------------------------------
# Partial core (dual of Lean corePartial / corePartial_inter)
# ---------------------------------------------------------------------------


def core_partial(
    act,  # Callable[[C, X], Optional[X]]
    contexts: list,
    R,  # Callable[[X, X], bool]
    x,
    y,
) -> bool:
    """
    For every context, if both partial acts apply, results stay R-related.
    Refusal on either side is vacuous for that context.
    """
    for c in contexts:
        ox = act(c, x)
        oy = act(c, y)
        if ox is not None and oy is not None:
            if not R(ox, oy):
                return False
    return True


def inter_rel(R, S):
    return lambda a, b: R(a, b) and S(a, b)


def i_inter_rel(family: list):
    return lambda a, b: all(R(a, b) for R in family)


# ---------------------------------------------------------------------------
# Concrete concurrent toy: tip=0, both writes expect base 0
# ---------------------------------------------------------------------------

WRITE_A = Edit.write(0)
WRITE_B = Edit.write(0)
TIP0 = 0


def test_write_fresh_advances():
    assert edit_act(Edit.write(0), 0) == 1
    assert edit_act(Edit.write(3), 3) == 4


def test_write_stale_refuses():
    assert edit_act(Edit.write(0), 1) is None
    assert edit_act(Edit.write(2), 5) is None


def test_id_always_applies():
    for tip in range(5):
        assert edit_act(Edit.id(), tip) == tip


def test_concurrent_writes_individually_apply_at_tip0():
    assert edit_act(WRITE_A, TIP0) == 1
    assert edit_act(WRITE_B, TIP0) == 1


def test_concurrent_write_sequentializations_refuse():
    """First advances tip to 1; second on original base refuses — both orders."""
    assert act_seq(WRITE_A, WRITE_B, TIP0) is None
    assert act_seq(WRITE_B, WRITE_A, TIP0) is None


def test_concurrent_writes_not_order_independent_at_tip0():
    assert not order_independent_at(WRITE_A, WRITE_B, TIP0)


def test_order_independence_fails_on_concurrent_write_toy():
    """Dual of Lean `order_independence_fails_on_concurrent_write_toy`."""
    edits = [WRITE_A, WRITE_B, Edit.id(), Edit.write(1)]
    tips = [0, 1, 2]
    assert order_independence_law(edits, tips) is False
    # Explicit counterexample facts
    assert edit_act(WRITE_A, TIP0) is not None
    assert edit_act(WRITE_B, TIP0) is not None
    assert act_seq(WRITE_A, WRITE_B, TIP0) is None


def test_survival_matrix_order_independence_fails():
    assert (
        SURVIVAL_MATRIX[SurvivalSlot.ORDER_INDEPENDENCE]
        == SurvivalVerdict.FAILS_WITH_COUNTEREXAMPLE
    )


def test_survival_matrix_core_meets_survives():
    assert SURVIVAL_MATRIX[SurvivalSlot.CORE_MEETS] == SurvivalVerdict.SURVIVES


def test_core_partial_preserves_binary_meets():
    """Dual of Lean `corePartial_inter` on the concurrent-edit toy."""
    contexts = [Edit.id(), Edit.write(0), Edit.write(1), Edit.write(2)]
    tips = [0, 1, 2, 3]

    def R(a: int, b: int) -> bool:
        return a % 2 == b % 2  # same parity

    def S(a: int, b: int) -> bool:
        return a <= b

    RS = inter_rel(R, S)
    act = lambda c, x: edit_act(c, x)

    for x in tips:
        for y in tips:
            left = core_partial(act, contexts, RS, x, y)
            right = core_partial(act, contexts, R, x, y) and core_partial(
                act, contexts, S, x, y
            )
            assert left == right, f"meet law fail at {(x, y)}: {left} vs {right}"


def test_core_partial_preserves_family_meets():
    """Dual of Lean `corePartial_iInter` on a 3-relation family."""
    contexts = [Edit.id(), Edit.write(0), Edit.write(1)]
    tips = [0, 1, 2]
    family = [
        lambda a, b: a == b,
        lambda a, b: a <= b,
        lambda a, b: (a + b) % 2 == 0,
    ]
    F = i_inter_rel(family)
    act = lambda c, x: edit_act(c, x)

    for x in tips:
        for y in tips:
            left = core_partial(act, contexts, F, x, y)
            right = all(core_partial(act, contexts, R, x, y) for R in family)
            assert left == right, f"family meet fail at {(x, y)}"


def test_survival_matrix_residual_slots_open():
    """Two residual slots remain open after dual-slot adjudication."""
    assert (
        SURVIVAL_MATRIX[SurvivalSlot.BARE_DIFFERENCE_NOGO]
        == SurvivalVerdict.OPEN_WIREFRAME
    )
    assert (
        SURVIVAL_MATRIX[SurvivalSlot.FOLD_STRICT_BUDGET]
        == SurvivalVerdict.OPEN_WIREFRAME
    )


def test_not_wave8_exit():
    """Programme residual: 2 open + 1 fail + 1 survive ⇒ not D5 close / Wave-8 exit."""
    open_count = sum(
        1 for v in SURVIVAL_MATRIX.values() if v == SurvivalVerdict.OPEN_WIREFRAME
    )
    fail_count = sum(
        1
        for v in SURVIVAL_MATRIX.values()
        if v == SurvivalVerdict.FAILS_WITH_COUNTEREXAMPLE
    )
    survive_count = sum(
        1 for v in SURVIVAL_MATRIX.values() if v == SurvivalVerdict.SURVIVES
    )
    assert open_count == 2
    assert fail_count == 1
    assert survive_count == 1
    assert SURVIVAL_MATRIX[SurvivalSlot.ORDER_INDEPENDENCE] != SurvivalVerdict.SURVIVES
    assert SURVIVAL_MATRIX[SurvivalSlot.CORE_MEETS] == SurvivalVerdict.SURVIVES
