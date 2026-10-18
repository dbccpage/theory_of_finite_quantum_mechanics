"""Tests for wired engine: CanContinue_n, AdapterContract, DDA tape FSM,
6 anti-cheat laws, budget, LGGR gate.

Each test fires at least one real predicate — no vacuous pass.
"""

import sys
import pathlib
import pytest

_code_dir = str(pathlib.Path(__file__).resolve().parents[2] / "code")
if _code_dir not in sys.path:
    sys.path.insert(0, _code_dir)

from omega_engine.crates.runtime.rt_wired import WE
from omega_engine.crates.type.wired import CC, AC, AX, V, TP, BG, LG, L



class TestCC:
    def test_all_true(self):
        c = CC(o=True, w=True, c=True, a=True, d=True, m=True, k=True, b=True, g=False)
        assert c.v()

    def test_no_obligation(self):
        c = CC(o=False, w=True)
        assert not c.v()

    def test_no_witness(self):
        c = CC(o=True, w=False)
        assert not c.v()

    def test_coda_la_refusal(self):
        c = CC(o=True, w=True, g=True)
        assert not c.v()

    def test_no_budget(self):
        c = CC(o=True, w=True, b=False)
        assert not c.v()

    def test_adapter_unsound(self):
        c = CC(o=True, w=True, a=False)
        assert not c.v()

    def test_skeleton_broken(self):
        c = CC(o=True, w=True, k=False)
        assert not c.v()

    def test_detector_inadequate(self):
        c = CC(o=True, w=True, d=False)
        assert not c.v()

    def test_no_minimal_lift(self):
        c = CC(o=True, w=True, m=False)
        assert not c.v()



class TestAC:
    def test_clean_adapter(self):
        a = AC(s="C0", t="C1")
        assert a.ok
        assert not a.d

    def test_adapter_debt(self):
        a = AC(s="C0", t="C1", ll=["lost_op_1"])
        assert a.d

    def test_unsound_adapter(self):
        a = AC(s="C0", t="C1", ok=False)
        assert not a.ok



class TestAX:
    def test_no_violations_on_same_degree(self):
        ax = AX(dw=1, sk="sk0")
        vv = ax.chk(
            new_deg=1, has_ndim_obl=False, has_same_carrier_repair=False,
            r_hash="r1", sk_hash="sk0", det_revalidated=True,
            claims_above_n0=False, n0_resolved=True,
        )
        assert vv == []

    def test_degree_laundering(self):
        ax = AX(dw=1)
        vv = ax.chk(
            new_deg=2, has_ndim_obl=False, has_same_carrier_repair=False,
            r_hash="r1", sk_hash="sk0", det_revalidated=True,
            claims_above_n0=False, n0_resolved=True,
        )
        assert V.DEG in vv

    def test_lift_laundering(self):
        ax = AX(dw=1)
        vv = ax.chk(
            new_deg=2, has_ndim_obl=True, has_same_carrier_repair=True,
            r_hash="r1", sk_hash="sk0", det_revalidated=True,
            claims_above_n0=False, n0_resolved=True,
        )
        assert V.LIFT in vv

    def test_anomalon_evasion(self):
        ax = AX(dw=1)
        ax.fp.add("r_seen")
        vv = ax.chk(
            new_deg=1, has_ndim_obl=False, has_same_carrier_repair=False,
            r_hash="r_seen", sk_hash="sk0", det_revalidated=True,
            claims_above_n0=False, n0_resolved=True,
        )
        assert V.ANOM in vv

    def test_skeleton_destruction(self):
        ax = AX(dw=1, sk="sk_old")
        vv = ax.chk(
            new_deg=1, has_ndim_obl=False, has_same_carrier_repair=False,
            r_hash="r1", sk_hash="sk_new", det_revalidated=True,
            claims_above_n0=False, n0_resolved=True,
        )
        assert V.SKEL in vv

    def test_detector_revalidation_skip(self):
        ax = AX(dw=1)
        vv = ax.chk(
            new_deg=2, has_ndim_obl=True, has_same_carrier_repair=False,
            r_hash="r1", sk_hash="sk0", det_revalidated=False,
            claims_above_n0=False, n0_resolved=True,
        )
        assert V.DET in vv

    def test_first_unresolved_dishonesty(self):
        ax = AX(dw=1, n0=1)
        vv = ax.chk(
            new_deg=1, has_ndim_obl=False, has_same_carrier_repair=False,
            r_hash="r1", sk_hash="sk0", det_revalidated=True,
            claims_above_n0=True, n0_resolved=False,
        )
        assert V.FUDH in vv



class TestTP:
    def test_write_and_done(self):
        tp = TP()
        tp.w("C", "r0")
        assert tp.t == ["C"]
        assert not tp.done
        tp.w("T", "r1")
        assert tp.done

    def test_hash_chain(self):
        tp = TP()
        h0 = tp.h
        h1 = tp.w("C", "r0")
        assert h1 != h0
        h2 = tp.w("R", "r1")
        assert h2 != h1



class TestBG:
    def test_bounded_ops(self):
        bg = BG(bt=3.0, dc=1.0)
        assert bg.mx == 3
        assert bg.spend()
        assert bg.spend()
        assert bg.spend()
        assert not bg.spend()

    def test_zero_budget(self):
        bg = BG(bt=0.0, dc=1.0)
        assert not bg.ok



class TestLG:
    def test_all_pass(self):
        lg = LG(gr=True, ga=True, gt=True, ge=True)
        assert lg.el

    def test_missing_rep(self):
        lg = LG(gr=False, ga=True, gt=True, ge=True)
        assert not lg.el

    def test_missing_auth(self):
        lg = LG(gr=True, ga=False, gt=True, ge=True)
        assert not lg.el

    def test_missing_time(self):
        lg = LG(gr=True, ga=True, gt=False, ge=True)
        assert not lg.el

    def test_missing_eval(self):
        lg = LG(gr=True, ga=True, gt=True, ge=False)
        assert not lg.el



class TestWE:
    def test_happy_path_solve(self):
        """Foundation -> E step -> terminal SOLVED."""
        w = WE(bt=10.0, dc=1.0)
        w.fnd(p1=1.0, g2=0.5)
        s, vv = w.stp(
            letter="E", dp1=-1.0, dg2=-0.5,
            r_hash="r1", sk_hash="sk0",
        )
        assert s == "OK"
        assert vv == []
        assert w.phi1 == pytest.approx(0.0)
        assert w.gm2 == pytest.approx(0.0)
        result = w.trm()
        assert result == "SOLVED"
        assert w.tape[-1] == "T"

    def test_budget_halt(self):
        """Budget exhaustion halts via CanContinue_n (budget is one of 9 conjuncts)."""
        w = WE(bt=1.0, dc=1.0)
        w.fnd(p1=5.0, g2=1.0)
        w.stp(letter="E", dp1=-1.0, dg2=0.0, r_hash="r1", sk_hash="sk0")
        s, _ = w.stp(letter="E", dp1=-1.0, dg2=0.0, r_hash="r2", sk_hash="sk0")
        assert s == "HALT_CC"

    def test_anticheats_fire(self):
        """Degree laundering without n+1 obligation halts."""
        w = WE(bt=100.0, dc=1.0)
        w.fnd(p1=5.0, g2=1.0)
        s, vv = w.stp(
            letter="D", dp1=0.0, dg2=0.0,
            r_hash="r1", sk_hash="sk0",
            has_ndim_obl=False,
        )
        assert s == "HALT_AX"
        assert V.DEG in vv

    def test_adapter_debt_recorded(self):
        """Adapter with debt records loss ledger entry."""
        w = WE(bt=100.0, dc=1.0)
        w.ac = AC(s="C0", t="C1", ll=["lost_witness"])
        w.fnd(p1=1.0, g2=0.0)
        w.stp(letter="E", dp1=-1.0, dg2=0.0, r_hash="r1", sk_hash="sk0")
        assert len(w.ll) > 0

    def test_cc_fails_no_obligation(self):
        """CanContinue_n fails on missing obligation."""
        w = WE(bt=100.0, dc=1.0)
        w.fnd(p1=1.0, g2=0.0)
        s, _ = w.stp(
            letter="E", dp1=-1.0, dg2=0.0,
            r_hash="r1", sk_hash="sk0",
            has_obl=False,
        )
        assert s == "HALT_CC"

    def test_typed_obstruction_terminal(self):
        """Non-zero residual with sufficient budget -> TYPED_OBS."""
        w = WE(bt=10.0, dc=1.0)
        w.fnd(p1=5.0, g2=1.0)
        w.stp(letter="E", dp1=-1.0, dg2=-0.5, r_hash="r1", sk_hash="sk0")
        result = w.trm()
        assert result == "TYPED_OBS"
        assert "I" in w.tape
        assert w.tape[-1] == "T"

    def test_lggr_gate(self):
        w = WE()
        assert not w.lggr(True, True, True, False)
        assert w.lggr(True, True, True, True)

    def test_anomalon_evasion_fires(self):
        """Same residual hash repeated -> ANOM violation."""
        w = WE(bt=100.0, dc=1.0)
        w.fnd(p1=5.0, g2=1.0)
        w.stp(letter="E", dp1=-1.0, dg2=0.0, r_hash="r1", sk_hash="sk0")
        s, vv = w.stp(letter="E", dp1=-1.0, dg2=0.0, r_hash="r1", sk_hash="sk0")
        assert s == "HALT_AX"
        assert V.ANOM in vv

    def test_full_autopoietic_tape(self):
        """Full C·R·E·I·T tape sequence."""
        w = WE(bt=100.0, dc=1.0)
        w.fnd(p1=1.0, g2=0.0)
        w.stp(letter="E", dp1=-1.0, dg2=0.0, r_hash="r1", sk_hash="sk0")
        w.trm()
        assert w.tape[0] == "C"
        assert w.tape[1] == "R"
        assert "E" in w.tape
        assert w.tape[-1] == "T"




