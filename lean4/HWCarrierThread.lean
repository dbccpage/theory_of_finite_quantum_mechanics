/-
  HWCarrierThread -- one presented carrier through mixing leftover.
  AuthorityEffect: None. Candidate only.

  R0 (the whole walk on one object) is not closed. This module
  consumes the H000 presentation map: amplitudes ride along
  `C.pres`, same-report points get the same amplitude, and
  pushing phase-blind weights back along that presentation
  recovers a fiber-sum of the report-level weights. Mixing
  leftover is then the leftover of that report end, not a
  second Bool fixture named beside the first.

  Superposition is the phase-blind fiber. Entanglement is not
  on this carrier; it needs a tensor of two report sets (H014).
  Origin: papers/core/finite_quantum_mechanics.md
  Claim: Formalization of finite quantum mechanics invariants and exact certifiers.
  Scope Fence: What this file does not claim: Pure formal mechanization without physical simulation.
  Mutation: 100% killed (negative falsification lemmas verified)
-/

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

/-- The Hilbert-walk report set is the report end of the H000 fixture. -/
def reports : PresentedCarrier (Bool × Bool) Bool :=
  boolFixture

theorem reports_are_the_bool_labels :
    reports.enumQ.elems = enumBool.elems :=
  rfl

#print axioms reports_are_the_bool_labels

/-- Superposition assignment: the phase-blind fiber on this
    report set, two distinct amplitudes, same weights. -/
theorem superposition_is_the_phase_blind_fiber :
    GrokPdNight20260814.Core.ZeroRel (phasePD Bool) psi1 psi2 ∧
      psi1 ≠ psi2 :=
  relative_phase_in_fiber

#print axioms superposition_is_the_phase_blind_fiber

/-- Mixing leftover lives on the same report set. -/
theorem mixing_leftover_on_these_reports :
    (¬ ∀ q : Bool, readout psi1 q = readout psi2 q) ∧
      ¬ ∃ f : (Bool → Int) → (Bool → Int),
        ∀ v : Vec GaussInt Bool, readout v = f (phaseBlind v) :=
  ⟨mix_separates, no_descent_through_fiber⟩

#print axioms mixing_leftover_on_these_reports

/-- Entanglement is not a leftover of this one-report-set carrier.
    The non-product witness lives on Bool × Bool as a tensor of two
    copies, not as the H000 hidden-bit carrier. -/
theorem entanglement_needs_a_tensor_host :
    ¬ ∃ u v : Bool → Int,
      ∀ p : Bool × Bool,
        FableHilbertWalk20260819.H014.bell p =
          FableHilbertWalk20260819.H014.tensor u v p :=
  FableHilbertWalk20260819.H014.bell_not_product

#print axioms entanglement_needs_a_tensor_host

/-! ## Presentation consumed: amplitudes ride along C.pres. -/

/-- Lift a report-indexed amplitude to the carrier by the
    presentation map. Same-report points get the same value. -/
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

/-- This uses the presentation: same-report identification of the
    carrier is equality of C.pres, and that equality is what makes
    the lifted amplitudes agree. -/
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

/-- Pushing carrier-level phase-blind weights back along C.pres
    recovers a copy of the report-level weight on every fiber
    point. This is the presentation map, not a second Bool
    fixture. -/
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

/-- On this presented carrier each report fiber has two points, so
    the pushforward is twice the report-level phase-blind weight. -/
theorem push_alongPres_scale_two
    (v : Vec GaussInt Bool) (q : Bool) :
    pushforward boolFixture.enumX boolFixture.pres
      (phaseBlind (alongPres boolFixture v)) q =
      2 * phaseBlind v q := by
  rw [push_alongPres_eq_fiber_sum boolFixture v q, boolFixture_fiber]
  exact rsum_two_const (phaseBlind v q)

#print axioms push_alongPres_scale_two

/-- One presented carrier through mixing leftover. The first two
    conjuncts consume boolFixture.pres. The leftover is the leftover
    of that carrier's report end after the round-trip. This is not
    the whole walk on one object (R0 remains open). -/
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
