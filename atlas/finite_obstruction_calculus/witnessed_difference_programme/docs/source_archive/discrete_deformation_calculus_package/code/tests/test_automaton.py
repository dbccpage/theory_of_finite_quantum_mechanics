"""Tape automaton: every law fires, the paper laws refine the engine laws, and the
tape-level results hold exhaustively on a 32-state abstraction.

The exhaustive checks are computed fixtures over this abstraction. The general
statements are the Lean theorems in ``lean4/Ddc/Theorems.lean``.
"""

from fractions import Fraction as F
from itertools import product

import automaton as A
import pytest
from automaton import State, Step, Witness, run_tape
from typed_refusal import M_REASONS

CARRIERS = ("p", "q")
STATES = [
    State(c, (F(r),), F(phi), F(gamma), adequate)
    for c, r, phi, gamma, adequate in product(CARRIERS, (0, 1), (0, 1), (0, 1), (True, False))
]
WITNESSES = [
    Witness(receipt, ledger, licence, reason)
    for receipt, ledger, licence, reason in product(
        (False, True), (False, True), (False, True), (None, "REFUSED_INVALID_WITNESS")
    )
]
PRICED = ("D", "Λ")


def lawful(letter, before, after, witness):
    return not A.step_violations(letter, before, after, witness)


def moved(state, **changes):
    fields = dict(
        carrier=state.carrier, residual=state.residual, phi=state.phi, gamma=state.gamma, adequate=state.adequate
    )
    fields.update(changes)
    return State(**fields)


EXACT = State("p", (F(1),), 0, 0)
CLOSED = State("p", (F(1),), 1, 0)
OPEN = State("p", (F(1),), 1, 1)
BLIND = State("p", (F(1),), 0, 0, adequate=False)


@pytest.mark.parametrize(
    "letter,before,after,witness,code",
    [
        ("E", EXACT, moved(EXACT, carrier="q", residual=(F(0),)), Witness(), "FixedCarrierOpChangedCarrier"),
        ("E", CLOSED, moved(CLOSED, residual=(F(0),), phi=0), Witness(), "ExactRepairFromNonExactClass"),
        ("E", EXACT, moved(EXACT, residual=(F(0),), gamma=1), Witness(), "ExactRepairLeftResidual"),
        ("E", EXACT, EXACT, Witness(), "ExactRepairLeftDefect"),
        ("E", BLIND, moved(BLIND, residual=(F(0),)), Witness(), "BlindDetector"),
        ("R", CLOSED, moved(CLOSED, carrier="q"), Witness(), "FixedCarrierOpChangedCarrier"),
        ("R", CLOSED, moved(CLOSED, phi=0), Witness(), "ResidualProjectionChangedMass"),
        ("R", OPEN, moved(OPEN, gamma=0), Witness(), "ResidualProjectionChangedClosure"),
        ("R", moved(CLOSED, adequate=False), moved(CLOSED, adequate=False), Witness(), "BlindDetector"),
        ("C", EXACT, EXACT, Witness(), "CarrierUnchangedUnderRestructure"),
        ("C", OPEN, moved(OPEN, carrier="q", gamma=0), Witness(), "ContextExposureLoweredObstruction"),
        ("C", CLOSED, moved(CLOSED, carrier="q", phi=0), Witness(), "ContextExposureLoweredObstruction"),
        ("I", EXACT, EXACT, Witness(), "MissingReceipt"),
        ("I", EXACT, moved(EXACT, residual=(F(0),)), Witness(receipt=True), "InertOpMutatedState"),
        ("Λ", CLOSED, CLOSED, Witness(lift_licence=True), "CarrierUnchangedUnderRestructure"),
        ("Λ", CLOSED, moved(CLOSED, carrier="q"), Witness(), "UnlicensedLift"),
        ("Λ", OPEN, moved(OPEN, carrier="q"), Witness(lift_licence=True), "LiftWithoutTrigger"),
        ("Λ", EXACT, moved(EXACT, carrier="q"), Witness(lift_licence=True), "LiftWithoutTrigger"),
        ("D", EXACT, EXACT, Witness(loss_ledger=True), "CarrierUnchangedUnderRestructure"),
        ("D", EXACT, moved(EXACT, carrier="q"), Witness(), "MissingLossLedger"),
        ("M", EXACT, EXACT, Witness(), "MissingRefusalReason"),
        ("M", EXACT, EXACT, Witness(reason="NOT_A_REASON"), "MissingRefusalReason"),
        ("M", EXACT, moved(EXACT, phi=1), Witness(reason="REFUSED_INVALID_WITNESS"), "InertOpMutatedState"),
        ("T", OPEN, OPEN, Witness(), "TerminalizedOpenResidual"),
        ("T", BLIND, BLIND, Witness(), "BlindDetector"),
        ("T", EXACT, moved(EXACT, residual=(F(0),)), Witness(), "InertOpMutatedState"),
        ("X", EXACT, EXACT, Witness(), "UnknownLetter"),
    ],
)
def test_each_law_fires_on_its_own_violation(letter, before, after, witness, code):
    assert code in A.step_violations(letter, before, after, witness)


def test_lawful_examples_of_every_letter():
    assert lawful("E", EXACT, moved(EXACT, residual=(F(0),)), Witness())
    assert lawful("R", CLOSED, moved(CLOSED, residual=(F(2),)), Witness())
    assert lawful("C", EXACT, moved(EXACT, carrier="q", phi=1, gamma=1), Witness())
    assert lawful("I", OPEN, OPEN, Witness(receipt=True))
    assert lawful("Λ", CLOSED, moved(CLOSED, carrier="q", phi=0), Witness(lift_licence=True))
    assert lawful("Λ", BLIND, moved(BLIND, carrier="q", adequate=True), Witness(lift_licence=True))
    assert lawful("D", OPEN, moved(OPEN, carrier="q", gamma=0), Witness(loss_ledger=True))
    assert lawful("M", OPEN, OPEN, Witness(reason="REFUSED_OPEN_OBSTRUCTION"))
    assert lawful("T", CLOSED, CLOSED, Witness())


def test_every_reason_in_the_vocabulary_is_admitted_by_M():
    for reason in M_REASONS:
        assert lawful("M", OPEN, OPEN, Witness(reason=reason))
    assert set(A.REASON_FOR.values()) <= set(M_REASONS)


def test_paper_laws_refine_the_engine_laws_on_every_step():
    """Every paper-lawful step passes the engine's verify_step (Lean: paper_refines_engine)."""
    checked = 0
    for letter in A.LETTERS:
        for before, after in product(STATES, STATES):
            engine = A.engine_violations(letter, before, after)
            assert set(engine) <= set(A.ENGINE_CODES)
            for witness in WITNESSES:
                if lawful(letter, before, after, witness):
                    assert engine == ()
                    checked += 1
    assert checked > 0


def test_engine_checks_less_than_the_paper():
    # A class-crossing edit passes the engine but not the paper (residual R-DDC-02).
    after = moved(OPEN, residual=(F(0),), phi=0, gamma=0)
    assert A.engine_violations("E", OPEN, after) == ()
    assert "ExactRepairFromNonExactClass" in A.step_violations("E", OPEN, after, Witness())
    # Scope laundering passes the engine but not the paper (R-DDC-04).
    laundered = moved(OPEN, carrier="q", phi=0, gamma=0)
    assert A.engine_violations("C", OPEN, laundered) == ()
    assert "ContextExposureLoweredObstruction" in A.step_violations("C", OPEN, laundered, Witness())


def test_no_free_decrease():
    """A lawful step that lowers Phi1 or Gamma2 is a D or a Λ (Lean: no_free_decrease)."""
    for letter in A.LETTERS:
        for before, after in product(STATES, STATES):
            if after.phi < before.phi or after.gamma < before.gamma:
                if any(lawful(letter, before, after, w) for w in WITNESSES):
                    assert letter in PRICED, (letter, before, after)


def _successors(control, state):
    for letter in A.LETTERS:
        if A.control_violation(control, letter):
            continue
        for after in STATES:
            if any(lawful(letter, state, after, w) for w in WITNESSES):
                yield letter, A.next_control(control, letter), after


def test_open_obstruction_is_never_sealed_without_a_priced_move():
    """Exhaustive reachability on the abstraction (Lean: open_needs_priced_move)."""
    for start in STATES:
        if start.gamma == 0:
            continue
        frontier = [(A.OPEN_CONTROL, start)]
        seen = set(frontier)
        while frontier:
            control, state = frontier.pop()
            for letter, nxt_control, after in _successors(control, state):
                assert letter != "T", f"sealed {start} without D or Λ"
                if letter in PRICED:
                    continue
                node = (nxt_control, after)
                if node not in seen:
                    seen.add(node)
                    frontier.append(node)


def test_terminal_and_refusal_absorption():
    for letter in A.LETTERS:
        assert A.control_violation(A.TERMINALIZED, letter) == "TerminalAbsorbing"
        blocked = A.control_violation(A.REFUSED, letter)
        assert (blocked is None) == (letter in ("C", "Λ", "T"))
        assert A.control_violation(A.OPEN_CONTROL, letter) is None
    assert A.next_control(A.REFUSED, "C") == A.OPEN_CONTROL
    assert A.next_control(A.OPEN_CONTROL, "M") == A.REFUSED
    assert A.next_control(A.OPEN_CONTROL, "T") == A.TERMINALIZED
    assert A.next_control(A.OPEN_CONTROL, "E") == A.OPEN_CONTROL


def test_run_tape_stops_at_the_first_unlawful_step_and_chains_receipts():
    steps = [
        Step("R", CLOSED),
        Step("M", CLOSED, Witness(reason="REFUSED_REQUIRES_LIFT")),
        Step("T", CLOSED),
        Step("R", CLOSED),
    ]
    run = run_tape(CLOSED, steps)
    assert not run.lawful and run.halted_at == 3
    assert run.violations == ("TerminalAbsorbing",)
    assert run.final_control == A.TERMINALIZED
    entries = run.tape.get_entries()
    assert [e.letter for e in entries] == ["R", "M", "T"]
    assert run.tape.verify_integrity()
    assert all(e.payload["authority_effect"] == "None" for e in entries)
    assert entries[-1].payload["routing_terminal"] == "Residual"
    assert run.authority_effect == "None"


def test_replay_is_deterministic():
    steps = [Step("E", moved(EXACT, residual=(F(0),))), Step("T", moved(EXACT, residual=(F(0),)))]
    first = run_tape(EXACT, steps)
    second = run_tape(EXACT, steps)
    assert first.lawful and first.tape.latest_hash == second.tape.latest_hash
    assert first.tape.get_entries()[-1].payload["routing_terminal"] == "CheckPassed"


def test_lawful_append():
    """Replaying t1 ++ t2 equals replaying t2 from where t1 stopped (Lean: lawful_append)."""
    t1 = [Step("R", CLOSED), Step("M", CLOSED, Witness(reason="REFUSED_REQUIRES_LIFT"))]
    t2 = [Step("Λ", moved(CLOSED, carrier="q"), Witness(lift_licence=True)), Step("T", moved(CLOSED, carrier="q"))]
    whole = run_tape(CLOSED, t1 + t2)
    head = run_tape(CLOSED, t1)
    tail = run_tape(head.final_state, t2, head.final_control)
    assert whole.lawful == (head.lawful and tail.lawful) is True
    assert whole.final_state == tail.final_state and whole.final_control == tail.final_control


def _credit_reachable(start):
    frontier = {(A.OPEN_CONTROL, start)}
    for letter in "CREDIT":
        nxt = set()
        for control, state in frontier:
            if A.control_violation(control, letter):
                continue
            for after in STATES:
                if any(lawful(letter, state, after, w) for w in WITNESSES):
                    nxt.add((A.next_control(control, letter), after))
        frontier = nxt
    return frontier


def test_credit_is_lawful_only_from_an_exact_start():
    """Exhaustive on the abstraction (Lean: credit_starts_exact)."""
    for start in STATES:
        if _credit_reachable(start):
            assert start.phi == 0 and start.gamma == 0
    assert _credit_reachable(State("p", (F(1),), 0, 0))


def test_measure_uses_the_declared_complex():
    import cochain

    square = cochain.Complex(("a", "b", "c", "d"), (("a", "b"), ("b", "c"), ("c", "d"), ("d", "a")))
    state = A.measure(square, (1, 0, 0, 0), "square")
    assert (state.phi, state.gamma, state.cls) == (F(1), F(0), A.CLOSED)
    with pytest.raises(TypeError):
        State("p", (), 0, 0, adequate=1)
    with pytest.raises(ValueError):
        State("p", (), -1, 0)
    for kwargs in ({"receipt": 1}, {"receipt": 0}, {"loss_ledger": 1}, {"lift_licence": 0}):
        with pytest.raises(TypeError):
            Witness(**kwargs)
    assert not A.step_violations("I", EXACT, EXACT, Witness(receipt=True))
