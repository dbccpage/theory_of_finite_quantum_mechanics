"""The §23 driver and the worked demos."""

from fractions import Fraction as F

import automaton as A
import demos
import fsm
from automaton import State


def test_driver_never_seals_open_or_blind_states_and_repairs_only_exact_ones():
    for klass, letters in fsm.DRIVER_LETTERS.items():
        if klass in (A.ACTIVE, fsm.INADEQUATE):
            assert "T" not in letters
        if "E" in letters:
            assert klass == A.EXACT
        if "Λ" in letters:
            assert klass in (A.CLOSED, fsm.INADEQUATE)


def test_admissible_respects_control():
    exact = State("p", (F(1),), 0, 0)
    blind = State("p", (F(1),), 0, 0, adequate=False)
    assert fsm.admissible(exact, A.TERMINALIZED) == ()
    assert fsm.admissible(exact, A.REFUSED) == ("T",)
    assert fsm.admissible(exact, A.OPEN_CONTROL) == ("E", "T", "I")
    assert fsm.driver_class(blind) == fsm.INADEQUATE
    assert set(fsm.DRIVERS) == {"autopoietic", "refusal", "self_examination", "allopoietic"}


EXPECTED = {
    "demo1_exact_CRET": (True, A.TERMINALIZED, ()),
    "demo1_open_CRM": (True, A.REFUSED, ()),
    "demo1_open_CRET_unlawful": (False, A.OPEN_CONTROL, ("ExactRepairFromNonExactClass",)),
    "demo2_CRM": (True, A.REFUSED, ()),
    "demo2_CRMT_unlawful": (False, A.REFUSED, ("TerminalizedOpenResidual",)),
    "demo3_CRT_residual_terminal": (True, A.TERMINALIZED, ()),
    "demo3_CRLT_licensed": (True, A.TERMINALIZED, ()),
    "demo3_CRMT_requires_lift": (True, A.TERMINALIZED, ()),
    "demo3_face_lift_then_T_unlawful": (False, A.OPEN_CONTROL, ("TerminalizedOpenResidual",)),
    "demo3_unlicensed_lift_unlawful": (False, A.OPEN_CONTROL, ("UnlicensedLift",)),
    "demo4_CM": (True, A.REFUSED, ()),
    "demo4_CMT_unlawful": (False, A.REFUSED, ("BlindDetector",)),
    "demo4_CLT_detector_lift": (True, A.TERMINALIZED, ()),
    "demo5_DIT": (True, A.TERMINALIZED, ()),
    "demo5_DIT_unlawful": (False, A.OPEN_CONTROL, ("MissingLossLedger",)),
    "demo5_MT_refusal_record": (True, A.TERMINALIZED, ()),
    "newton_leibniz_CREIT": (True, A.TERMINALIZED, ()),
    "credit": (True, A.TERMINALIZED, ()),
}


def test_every_demo_reaches_its_stated_verdict():
    results = {d.name: d for d in demos.all_demos()}
    assert set(results) == set(EXPECTED)
    for name, (lawful, control, violations) in EXPECTED.items():
        run = results[name].run
        assert (run.lawful, run.final_control, run.violations) == (lawful, control, violations), name
        assert run.tape.verify_integrity()
        summary = demos.summary(results[name])
        assert summary["receipt_head"] == run.tape.latest_hash


def test_lifts_do_not_dissolve_a_survivor():
    lawful = {d.name: d for d in demos.demo_3_stabilized_survivor()}["demo3_CRLT_licensed"]
    assert lawful.run.final_state.phi == 1 and lawful.run.final_state.gamma == 0


def test_newton_leibniz_is_exact():
    demo, numbers = demos.newton_leibniz()
    assert numbers == {"left_sum": F(45), "defect": F(5), "integral": F(50), "telescoped": F(50)}
    assert demo.lawful
    # Pinned replay head: any change to the receipt format or the laws must be deliberate.
    assert demo.run.tape.latest_hash == "0f17b5d15b14de1179ef3a7b3c4fa08d4031368253b0702d40f233ba8612312c"


def test_credit_needs_an_exact_start_and_a_booked_descent():
    assert demos.credit().lawful
    assert demos.credit().run.tape.latest_hash == "cc6c764943b5843b73b131aca397f2bf82b459e4d84bdae5308ae43cb9af15e7"
    closed = demos.credit(initial_defect=(1, 1, 1))
    assert not closed.lawful and closed.run.violations == ("ExactRepairFromNonExactClass",)
    unbooked = demos.credit(ledger=False)
    assert not unbooked.lawful and unbooked.run.violations == ("MissingLossLedger",)
