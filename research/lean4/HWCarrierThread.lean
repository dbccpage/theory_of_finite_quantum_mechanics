


import HWKernel
import H000FinitePresentedCarrier
import H002ReportDynamics
import H004FreeLinearization
import H008PhaseBlindPresentation
import H009PhaseFiber
import H010InterferenceNonDescent
import H014TensorCompositionBoundary

namespace FableHilbertWalk20260819.HWCarrierThread

open FableHilbertWalk20260819.HWKernel
open FableHilbertWalk20260819.H000
  (boolFixture PresentedCarrier sameReport sameReport_iff)
open FableHilbertWalk20260819.H002 (pushforward)
open FableHilbertWalk20260819.H004 (Vec)
open FableHilbertWalk20260819.H008 (psi1 psi2 phaseBlind equal_weights)
open FableHilbertWalk20260819.H009 (relative_phase_in_fiber phasePD)
open FableHilbertWalk20260819.H010 (mix_separates no_descent_through_fiber readout)

def reports : PresentedCarrier (Bool × Bool) Bool :=
  boolFixture

theorem reports_are_the_bool_labels :
    reports.enumQ.elems = enumBool.elems :=
  rfl

#print axioms reports_are_the_bool_labels

theorem superposition_is_the_phase_blind_fiber :
    GrokPdNight20260814.Core.ZeroRel (phasePD Bool) psi1 psi2 ∧
      psi1 ≠ psi2 :=
  relative_phase_in_fiber

#print axioms superposition_is_the_phase_blind_fiber

theorem mixing_leftover_on_these_reports :
    (¬ ∀ q : Bool, readout psi1 q = readout psi2 q) ∧
      ¬ ∃ f : (Bool → Int) → (Bool → Int),
        ∀ v : Vec GaussInt Bool, readout v = f (phaseBlind v) :=
  ⟨mix_separates, no_descent_through_fiber⟩

#print axioms mixing_leftover_on_these_reports

theorem entanglement_needs_a_tensor_host :
    ¬ ∃ u v : Bool → Int,
      ∀ p : Bool × Bool,
        FableHilbertWalk20260819.H014.bell p =
          FableHilbertWalk20260819.H014.tensor u v p :=
  FableHilbertWalk20260819.H014.bell_not_product

#print axioms entanglement_needs_a_tensor_host


def alongPres {X Q : Type} (C : PresentedCarrier X Q)
    (v : Vec GaussInt Q) : Vec GaussInt X :=
  fun x => v (C.pres x)

theorem of_mem_filter {α : Type} (p : α → Bool) {a : α} :
    ∀ {l : List α}, a ∈ l.filter p → p a = true := by
  intro l ha
  induction l with
  | nil => cases ha
  | cons b t ih =>
      rw [List.filter_cons] at ha
      by_cases hp : p b = true
      · rw [if_pos hp] at ha
        rcases List.mem_cons.mp ha with rfl | ht
        · exact hp
        · exact ih ht
      · rw [if_neg hp] at ha
        exact ih ha

#print axioms of_mem_filter

theorem same_report_same_amplitude {X Q : Type}
    (C : PresentedCarrier X Q) (v : Vec GaussInt Q) {x y : X}
    (h : sameReport C x y) :
    alongPres C v x = alongPres C v y := by
  have hp : C.pres x = C.pres y := (sameReport_iff C x y).mp h
  unfold alongPres
  rw [hp]

#print axioms same_report_same_amplitude

theorem phaseBlind_alongPres {X Q : Type}
    (C : PresentedCarrier X Q) (v : Vec GaussInt Q) (x : X) :
    phaseBlind (alongPres C v) x = phaseBlind v (C.pres x) :=
  rfl

#print axioms phaseBlind_alongPres

theorem push_alongPres_eq_fiber_sum {X Q : Type} [DecidableEq Q]
    (C : PresentedCarrier X Q) (v : Vec GaussInt Q) (q : Q) :
    pushforward C.enumX C.pres (phaseBlind (alongPres C v)) q =
      rsum intPack
        ((C.enumX.elems.filter (fun x => C.pres x == q)).map
          (fun _ => phaseBlind v q)) := by
  unfold pushforward
  apply congrArg
  apply map_congr_mem
  intro x hx
  have hp : (C.pres x == q) = true :=
    of_mem_filter (fun y => C.pres y == q) hx
  have heq : C.pres x = q := beq_iff_eq.mp hp
  rw [phaseBlind_alongPres, heq]

#print axioms push_alongPres_eq_fiber_sum

theorem boolFixture_fiber (q : Bool) :
    boolFixture.enumX.elems.filter
        (fun x => boolFixture.pres x == q) =
      [(q, false), (q, true)] := by
  cases q <;> decide

#print axioms boolFixture_fiber

theorem rsum_two_const (c : Int) :
    rsum intPack [c, c] = 2 * c := by
  simp only [rsum, intPack]
  rw [Int.add_zero]
  exact (Int.two_mul c).symm

#print axioms rsum_two_const

theorem push_alongPres_scale_two
    (v : Vec GaussInt Bool) (q : Bool) :
    pushforward boolFixture.enumX boolFixture.pres
      (phaseBlind (alongPres boolFixture v)) q =
      2 * phaseBlind v q := by
  rw [push_alongPres_eq_fiber_sum boolFixture v q, boolFixture_fiber]
  exact rsum_two_const (phaseBlind v q)

#print axioms push_alongPres_scale_two

theorem one_carrier_through_mixing_leftover :
    (∀ (v : Vec GaussInt Bool) (x y : Bool × Bool),
      sameReport boolFixture x y →
        alongPres boolFixture v x = alongPres boolFixture v y) ∧
    (∀ (v : Vec GaussInt Bool) (q : Bool),
      pushforward boolFixture.enumX boolFixture.pres
        (phaseBlind (alongPres boolFixture v)) q =
        2 * phaseBlind v q) ∧
    (∀ q : Bool, phaseBlind psi1 q = phaseBlind psi2 q) ∧
    (¬ ∀ q : Bool, readout psi1 q = readout psi2 q) ∧
    (¬ ∃ f : (Bool → Int) → (Bool → Int),
      ∀ v : Vec GaussInt Bool, readout v = f (phaseBlind v)) :=
  ⟨fun v _ _ h => same_report_same_amplitude boolFixture v h,
    push_alongPres_scale_two,
    equal_weights, mix_separates, no_descent_through_fiber⟩

#print axioms one_carrier_through_mixing_leftover

end FableHilbertWalk20260819.HWCarrierThread

private def l5aProvenance : String :=
  "Origin: lean4/HWCarrierThread.lean Claim: reports_are_the_bool_labels AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
