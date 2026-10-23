"""The five minimal demos, the Newton-Leibniz tape and the CREDIT tape.

Every diagnostic is measured on a declared complex (``automaton.measure``);
every tape is replayed through the step and control laws. Unlawful variants are
kept next to the lawful ones as falsifiers. Run ``python demos.py`` from this
directory to print each tape, its verdict and its receipt head.

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Dict, List, Optional, Tuple

import cochain
from automaton import REFUSED, State, Step, TapeRun, Witness, measure, run_tape
from descent import DescentProjector

UNDECLARED = State("undeclared", (), 0, 0)
F = Fraction


def _hold(state: State, letter: str, witness: Witness = Witness()) -> Step:
    return Step(letter, state, witness)


def _zero(state: State) -> State:
    return State(state.carrier, tuple(F(0) for _ in state.residual), 0, 0, state.adequate)


def _refuse(state: State, reason: str) -> Step:
    return Step("M", state, Witness(reason=reason))


@dataclass(frozen=True)
class Demo:
    name: str
    lawful: bool
    run: TapeRun
    note: str

    @property
    def letters(self) -> str:
        return self.run.letters


def _demo(name: str, initial: State, steps: List[Step], note: str) -> Demo:
    run = run_tape(initial, steps)
    return Demo(name, run.lawful, run, note)


# -- carriers -----------------------------------------------------------------

TWO_TRIANGLES = cochain.Complex(
    ("a", "b", "c", "d"),
    (("a", "b"), ("b", "c"), ("a", "c"), ("b", "d"), ("d", "c")),
    (((0, 1), (1, 1), (2, -1)), ((3, 1), (4, 1), (1, -1))),
)
FILLED_TRIANGLE = cochain.Complex(
    ("a", "b", "c"),
    (("a", "b"), ("b", "c"), ("c", "a")),
    (((0, 1), (1, 1), (2, 1)),),
)
HOLLOW_TRIANGLE = cochain.Complex(("a", "b", "c"), (("a", "b"), ("b", "c"), ("c", "a")))
SQUARE = cochain.Complex(("a", "b", "c", "d"), (("a", "b"), ("b", "c"), ("c", "d"), ("d", "a")))
SQUARE_PLUS_SPUR = cochain.Complex(
    ("a", "b", "c", "d", "e"),
    (("a", "b"), ("b", "c"), ("c", "d"), ("d", "a"), ("a", "e")),
)
SQUARE_FILLED = cochain.Complex(
    ("a", "b", "c", "d"),
    (("a", "b"), ("b", "c"), ("c", "d"), ("d", "a")),
    (((0, 1), (1, 1), (2, 1), (3, 1)),),
)


def path(n: int) -> cochain.Complex:
    names = tuple(str(k) for k in range(n + 1))
    return cochain.Complex(names, tuple((names[k], names[k + 1]) for k in range(n)))


# -- demos ----------------------------------------------------------------------


def demo_1_boundary_cancellation() -> List[Demo]:
    exact = measure(TWO_TRIANGLES, (1, 2, 3, 1, 1), "two_triangles")
    open_ = measure(TWO_TRIANGLES, (1, 2, 3, 1, 2), "two_triangles")
    return [
        _demo("demo1_exact_CRET", UNDECLARED,
              [Step("C", exact), _hold(exact, "R"), Step("E", _zero(exact)), _hold(_zero(exact), "T")],
              "An exact defect is registered, repaired to zero and sealed (CheckPassed)."),
        _demo("demo1_open_CRM", UNDECLARED,
              [Step("C", open_), _hold(open_, "R"), _refuse(open_, "REFUSED_OPEN_OBSTRUCTION")],
              "A face defect cannot be cancelled; the tape ends in a typed refusal."),
        _demo("demo1_open_CRET_unlawful", UNDECLARED,
              [Step("C", open_), _hold(open_, "R"), Step("E", _zero(open_)), _hold(_zero(open_), "T")],
              "Falsifier: E off an exact class is refused (ExactRepairFromNonExactClass)."),
    ]


def demo_2_local_green_global_red() -> List[Demo]:
    state = measure(FILLED_TRIANGLE, (1, 1, 1), "filled_triangle")
    return [
        _demo("demo2_CRM", UNDECLARED,
              [Step("C", state), _hold(state, "R"), _refuse(state, "REFUSED_OPEN_OBSTRUCTION")],
              "Every edge is locally consistent, yet d1 x = 3: refused, never sealed."),
        _demo("demo2_CRMT_unlawful", UNDECLARED,
              [Step("C", state), _hold(state, "R"), _refuse(state, "REFUSED_OPEN_OBSTRUCTION"), _hold(state, "T")],
              "Falsifier: T after M still may not seal Gamma2 > 0 (TerminalizedOpenResidual)."),
    ]


def demo_3_stabilized_survivor() -> List[Demo]:
    survivor = measure(SQUARE, (1, 0, 0, 0), "square")
    lifted = measure(SQUARE_PLUS_SPUR, (1, 0, 0, 0, 0), "square_plus_spur")
    filled = measure(SQUARE_FILLED, (1, 0, 0, 0), "square_filled")
    licence = Witness(lift_licence=True)
    return [
        _demo("demo3_CRT_residual_terminal", UNDECLARED,
              [Step("C", survivor), _hold(survivor, "R"), _hold(survivor, "T")],
              "A closed survivor (Phi1 = 1, Gamma2 = 0) is sealed on the residual terminal."),
        _demo("demo3_CRLT_licensed", UNDECLARED,
              [Step("C", survivor), _hold(survivor, "R"), Step("Λ", lifted, licence), _hold(lifted, "T")],
              "A licensed lift adds capacity; the survivor persists (Phi1 still 1) and is sealed."),
        _demo("demo3_CRMT_requires_lift", UNDECLARED,
              [Step("C", survivor), _hold(survivor, "R"), _refuse(survivor, "REFUSED_REQUIRES_LIFT"), _hold(survivor, "T")],
              "Without a licence the lift is refused; T may still close the closed survivor."),
        _demo("demo3_face_lift_then_T_unlawful", UNDECLARED,
              [Step("C", survivor), _hold(survivor, "R"), Step("Λ", filled, licence), _hold(filled, "T")],
              "Falsifier: attaching a face that bounds the cycle turns the survivor into Gamma2 = 1."),
        _demo("demo3_unlicensed_lift_unlawful", UNDECLARED,
              [Step("C", survivor), _hold(survivor, "R"), Step("Λ", lifted)],
              "Falsifier: a lift trigger is not a lift licence (UnlicensedLift)."),
    ]


def demo_4_detector_collapse() -> List[Demo]:
    blind = State("square_blind_detector", (1, 0, 0, 0), 0, 0, adequate=False)
    seen = measure(SQUARE_PLUS_SPUR, (1, 0, 0, 0, 0), "square_adequate_detector")
    return [
        _demo("demo4_CM", UNDECLARED,
              [Step("C", blind), _refuse(blind, "REFUSED_DETECTOR_INADEQUATE")],
              "A constant detector reports zero; the tape refuses instead of sealing a false green."),
        _demo("demo4_CMT_unlawful", UNDECLARED,
              [Step("C", blind), _refuse(blind, "REFUSED_DETECTOR_INADEQUATE"), _hold(blind, "T")],
              "Falsifier: a blind detector may not seal (BlindDetector)."),
        _demo("demo4_CLT_detector_lift", UNDECLARED,
              [Step("C", blind), Step("Λ", seen, Witness(lift_licence=True)), _hold(seen, "T")],
              "A licensed detector lift re-measures Phi1 = 1 and seals the survivor honestly."),
    ]


def demo_5_descent_with_loss() -> List[Demo]:
    vector = (F(1), F(2), F(3, 2), F(1, 4))
    fine = measure(path(4), vector, "path4")
    receipt = DescentProjector(2).descend(list(vector))
    coarse = measure(path(2), receipt.coarse_vector, "path2")
    ledger = Witness(loss_ledger=True)
    return [
        _demo("demo5_DIT", fine,
              [Step("D", coarse, ledger), _hold(coarse, "I", Witness(receipt=True)), _hold(coarse, "T")],
              f"Descent books loss {receipt.loss_scalar}; the coarse state is sealed."),
        _demo("demo5_DIT_unlawful", fine,
              [Step("D", coarse), _hold(coarse, "I", Witness(receipt=True)), _hold(coarse, "T")],
              "Falsifier: D without a loss ledger (MissingLossLedger)."),
        _demo("demo5_MT_refusal_record", fine,
              [_refuse(fine, "REFUSED_MISSING_LOSS_LEDGER"), _hold(fine, "T")],
              "The lawful record of the refused descent: M, then T on the unchanged state."),
    ]


def newton_leibniz() -> Tuple[Demo, Dict[str, Fraction]]:
    """Integral of f(x) = x on [0, 10] with 10 left-endpoint steps, exactly."""
    n = 10
    grid = path(n)
    left = [F(k) for k in range(n)]
    primitive = {str(k): F(k * k, 2) for k in range(n + 1)}
    exact_increments = grid.d0(primitive)
    defect = tuple(e - m for e, m in zip(exact_increments, left))
    state = measure(grid, defect, "grid_0_10")
    repaired = _zero(state)
    demo = _demo("newton_leibniz_CREIT", UNDECLARED,
                 [Step("C", state), _hold(state, "R"), Step("E", repaired),
                  _hold(repaired, "I", Witness(receipt=True)), _hold(repaired, "T")],
                 "Left sum 45 plus exact correction 5 telescopes to F(10) - F(0) = 50.")
    numbers = {
        "left_sum": sum(left, F(0)),
        "defect": sum(defect, F(0)),
        "integral": sum(exact_increments, F(0)),
        "telescoped": primitive[str(n)] - primitive["0"],
    }
    return demo, numbers


def credit(initial_defect: Tuple[int, ...] = (1, 2, -3), ledger: bool = True) -> Demo:
    """C·R·E·D·I·T on the hollow triangle, descending to its first edge."""
    declared = measure(HOLLOW_TRIANGLE, initial_defect, "hollow_triangle")
    repaired = _zero(declared)
    coarse = measure(path(1), (0,), "edge_ab")
    return _demo("credit", UNDECLARED,
                 [Step("C", declared), _hold(declared, "R"), Step("E", repaired),
                  Step("D", coarse, Witness(loss_ledger=ledger)),
                  _hold(coarse, "I", Witness(receipt=True)), _hold(coarse, "T")],
                 "CREDIT is lawful exactly when each of its six steps is; this one is an exact defect with a booked descent.")


def all_demos() -> List[Demo]:
    demos: List[Demo] = []
    for build in (
        demo_1_boundary_cancellation,
        demo_2_local_green_global_red,
        demo_3_stabilized_survivor,
        demo_4_detector_collapse,
        demo_5_descent_with_loss,
    ):
        demos.extend(build())
    demos.append(newton_leibniz()[0])
    demos.append(credit())
    return demos


def summary(demo: Demo) -> Dict[str, Optional[str]]:
    run = demo.run
    return {
        "name": demo.name,
        "letters": demo.letters,
        "lawful": str(demo.lawful),
        "final_control": run.final_control,
        "halted_at": None if run.halted_at is None else str(run.halted_at),
        "violations": ",".join(run.violations) or None,
        "receipt_head": run.tape.latest_hash,
        "refused_terminal": str(run.final_control == REFUSED),
    }


if __name__ == "__main__":  # pragma: no cover - manual inspection entry point
    for d in all_demos():
        print(summary(d))
    _, nl = newton_leibniz()
    print({k: str(v) for k, v in nl.items()})
