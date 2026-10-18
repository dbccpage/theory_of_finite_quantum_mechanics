/-
  HWFullThread -- one PresentedCarrier through H000-H016, or a
  precise obstruction. AuthorityEffect: None. Candidate only.

  STACK item: one presented carrier through the whole walk, not
  only through mixing leftover. Re-architecture.

  What this module does
    A typed implication about one H000 PresentedCarrier: the
    parametric rungs (mass along the presentation, free module,
    admitted form, permutation isometry, phase-blind equivariance,
    along-presentation amplitudes) hold of that carrier. On the
    H000 fixture the Bool witnesses for mixing leftover, operators,
    Born pairing, collapse, dilations, and the missing half-step
    are restated about that same carrier. H017 remains a
    conjunction of fixtures; this is the implication about one
    object.

  Precise obstruction
    H014's correlation vector is not a report of this carrier: it
    splits a same-report fiber, so it is not an along-presentation
    lift of any report-level integer vector. The report end has
    two labels; the tensor host has four. The missing extra is a
    second presented carrier whose presentation is the identity on
    the product of two report sets. Complexification (H007) and
    the circle selector (H011) do not consume a PresentedCarrier;
    they stay pack-level and selector-pack imports.

  Nonclaim boundary
    Not combining-system uniqueness. Not Gleason. Not M_n(C).
    Not a replacement of H017 by a derivation of quantum mechanics.

  AuthorityEffect: None
  Origin: papers/core/finite_quantum_mechanics.md
  Scope Fence: What this file does not claim: Pure formal mechanization without physical simulation.
-/

import HWKernel
import H000FinitePresentedCarrier
import H001ProbabilitySimplex
import H002ReportDynamics
import H003ReversibilityGate
import H004FreeLinearization
import H005InnerProductAdmission
import H006PermutationUnitary
import H008PhaseBlindPresentation
import H010InterferenceNonDescent
import H012OperatorAlgebraShadow
import H013BornPairingBoundary
import H014TensorCompositionBoundary
import H015IrreversibleFork
import H016ContinuousDynamicsFork
import HWThread
import HWCarrierThread

namespace FableHilbertWalk20260819.HWFullThread

open FableHilbertWalk20260819.HWKernel
open FableHilbertWalk20260819.H000
  (PresentedCarrier boolFixture sameReport sameReport_iff
    presented_carrier_replays presented_carrier_separates)
open FableHilbertWalk20260819.H001 (ScaledProb)
open FableHilbertWalk20260819.H002 (pushforward pushforward_mass)
open FableHilbertWalk20260819.H003 (Reversible)
open FableHilbertWalk20260819.H004 (Vec delta basis_expansion)
open FableHilbertWalk20260819.H005 (sesq delta_orthonormal)
open FableHilbertWalk20260819.H006 (permU permutation_isometry)
open FableHilbertWalk20260819.H008 (phaseBlind psi1 psi2 equal_weights)
open FableHilbertWalk20260819.H010 (readout mix_separates no_descent_through_fiber)
open FableHilbertWalk20260819.HWCarrierThread
  (alongPres same_report_same_amplitude)

/-! ## General implication: one presented carrier, parametric rungs. -/

/-- Pushing carrier weights along the presentation preserves mass;
    the free module, admitted form, permutation isometry, and
    phase-blind equivariance live on the report end; amplitudes
    lifted along the presentation are constant on same-report
    fibers. This is an implication about C, not a conjunction of
    separate fixtures. -/
theorem parametric_thread {X Q : Type} [DecidableEq Q]
    (C : PresentedCarrier X Q) {τ : Q → Q} (R : Reversible τ) :
    (∀ w : X → Int,
      rsum intPack (C.enumQ.elems.map (pushforward C.enumX C.pres w)) =
        rsum intPack (C.enumX.elems.map w)) ∧
    (∀ (v : Vec Int Q) (x : Q),
      rsum intPack (C.enumQ.elems.map
        (fun q => intPack.mul (v q) (delta intPack q x))) = v x) ∧
    (∀ a b : Q,
      sesq intPack C.enumQ (delta intPack a) (delta intPack b) =
        if (a == b) = true then intPack.one else intPack.zero) ∧
    (∀ u v : Vec Int Q,
      sesq intPack C.enumQ (permU intPack R u) (permU intPack R v) =
        sesq intPack C.enumQ u v) ∧
    (∀ (v : Vec GaussInt Q) (q : Q),
      phaseBlind (permU gaussPack R v) q =
        pushforward C.enumQ τ (phaseBlind v) q) ∧
    (∀ (v : Vec GaussInt Q) (x y : X),
      sameReport C x y → alongPres C v x = alongPres C v y) :=
  ⟨fun w => pushforward_mass C.enumX C.enumQ C.pres w,
    fun v x => basis_expansion intPack C.enumQ v x,
    fun a b => delta_orthonormal intPack C.enumQ a b,
    fun u v => permutation_isometry intPack C.enumQ R u v,
    fun v q =>
      FableHilbertWalk20260819.HWThread.phaseBlind_intertwines C.enumQ R v q,
    fun v _ _ h => same_report_same_amplitude C v h⟩

#print axioms parametric_thread

/-! ## Obstruction: a fiber-splitting function is not a report. -/

/-- Report-level integer data, pulled back along the presentation,
    cannot separate same-report points. -/
theorem along_report_constant {X Q : Type}
    (C : PresentedCarrier X Q) (v : Q → Int) {x y : X}
    (h : sameReport C x y) :
    v (C.pres x) = v (C.pres y) := by
  have hp : C.pres x = C.pres y := (sameReport_iff C x y).mp h
  rw [hp]

#print axioms along_report_constant

/-- If a carrier function splits a same-report fiber, it is not
    an along-presentation lift of any report-level vector. -/
theorem not_along_if_fiber_splits {X Q : Type}
    (C : PresentedCarrier X Q) (f : X → Int) {x y : X}
    (hsame : sameReport C x y) (hsplit : f x ≠ f y) :
    ¬ ∃ v : Q → Int, ∀ z : X, v (C.pres z) = f z := by
  intro h
  rcases h with ⟨v, hv⟩
  have hconst : v (C.pres x) = v (C.pres y) :=
    along_report_constant C v hsame
  have hx : v (C.pres x) = f x := hv x
  have hy : v (C.pres y) = f y := hv y
  rw [hx, hy] at hconst
  exact hsplit hconst

#print axioms not_along_if_fiber_splits

theorem bell_splits_a_fiber :
    sameReport boolFixture (false, false) (false, true) ∧
      FableHilbertWalk20260819.H014.bell (false, false) ≠
        FableHilbertWalk20260819.H014.bell (false, true) :=
  ⟨presented_carrier_replays, by decide⟩

#print axioms bell_splits_a_fiber

/-- The H014 correlation vector is not a report of the H000
    presented carrier. -/
theorem bell_not_along_presentation :
    ¬ ∃ v : Bool → Int, ∀ p : Bool × Bool,
      v (boolFixture.pres p) = FableHilbertWalk20260819.H014.bell p :=
  not_along_if_fiber_splits boolFixture
    FableHilbertWalk20260819.H014.bell
    presented_carrier_replays (by decide)

#print axioms bell_not_along_presentation

theorem this_report_end_has_two_labels :
    boolFixture.enumQ.elems.length = 2 :=
  rfl

#print axioms this_report_end_has_two_labels

theorem tensor_host_has_four_labels :
    enumBoolProd.elems.length = 4 :=
  rfl

#print axioms tensor_host_has_four_labels

/-- Two labels are not four: this report end is not the tensor host. -/
theorem this_report_end_is_not_the_tensor_host :
    boolFixture.enumQ.elems.length ≠ enumBoolProd.elems.length := by
  decide

#print axioms this_report_end_is_not_the_tensor_host

/-- The missing extra that would make the correlation vector a
    report: identity presentation on the product of two report sets. -/
def productHost : PresentedCarrier (Bool × Bool) (Bool × Bool) where
  pres := id
  enumX := enumBoolProd
  enumQ := enumBoolProd

theorem bell_is_a_report_of_the_product_host (p : Bool × Bool) :
    FableHilbertWalk20260819.H014.bell (productHost.pres p) =
      FableHilbertWalk20260819.H014.bell p :=
  rfl

#print axioms bell_is_a_report_of_the_product_host

/-! ## H015 dilations live on this carrier and preserve presentation. -/

theorem dilations_preserve_this_presentation (x : Bool × Bool) :
    boolFixture.pres (FableHilbertWalk20260819.H015.dil1 x) =
      boolFixture.pres x ∧
    boolFixture.pres (FableHilbertWalk20260819.H015.dil2 x) =
      boolFixture.pres x :=
  ⟨rfl, rfl⟩

#print axioms dilations_preserve_this_presentation

/-! ## Typed implication: from this presented carrier, the walk. -/

/-- From one presented carrier equal to the H000 fixture, the
    report-end walk through H016, and the H014 obstruction.
    H007 and H011 are not conjuncts: they do not consume C. -/
theorem from_one_presented_carrier
    (C : PresentedCarrier (Bool × Bool) Bool)
    (hC : C = boolFixture) :
    sameReport C (false, false) (false, true) ∧
    ¬ sameReport C (false, false) (true, false) ∧
    Nonempty (ScaledProb Bool C.enumQ 1) ∧
    (∀ w : Bool × Bool → Int,
      rsum intPack (C.enumQ.elems.map (pushforward C.enumX C.pres w)) =
        rsum intPack (C.enumX.elems.map w)) ∧
    ¬ Nonempty (Reversible FableHilbertWalk20260819.H003.collapse) ∧
    (∀ (v : Vec Int Bool) (x : Bool),
      rsum intPack (C.enumQ.elems.map
        (fun q => intPack.mul (v q) (delta intPack q x))) = v x) ∧
    (∀ a b : Bool,
      sesq intPack C.enumQ (delta intPack a) (delta intPack b) =
        if (a == b) = true then intPack.one else intPack.zero) ∧
    (∀ u v : Vec Int Bool,
      sesq intPack C.enumQ
        (permU intPack FableHilbertWalk20260819.H003.toggleRev u)
        (permU intPack FableHilbertWalk20260819.H003.toggleRev v) =
      sesq intPack C.enumQ u v) ∧
    (∀ {τ : Bool → Bool} (R : Reversible τ)
      (v : Vec GaussInt Bool) (q : Bool),
      phaseBlind (permU gaussPack R v) q =
        pushforward C.enumQ τ (phaseBlind v) q) ∧
    (∀ (v : Vec GaussInt Bool) (x y : Bool × Bool),
      sameReport C x y → alongPres C v x = alongPres C v y) ∧
    (∀ q : Bool, phaseBlind psi1 q = phaseBlind psi2 q) ∧
    (¬ ∀ q : Bool, readout psi1 q = readout psi2 q) ∧
    (¬ ∃ f : (Bool → Int) → (Bool → Int),
      ∀ v : Vec GaussInt Bool, readout v = f (phaseBlind v)) ∧
    (¬ ∀ i j : Bool,
      FableHilbertWalk20260819.H012.mmul
        FableHilbertWalk20260819.H012.nMat
        FableHilbertWalk20260819.H012.nMat' i j =
      FableHilbertWalk20260819.H012.mmul
        FableHilbertWalk20260819.H012.nMat'
        FableHilbertWalk20260819.H012.nMat i j) ∧
    (FableHilbertWalk20260819.H013.pair C.enumQ (phaseBlind psi1)
      (FableHilbertWalk20260819.H013.indicator false) = 1) ∧
    (¬ ∃ v : Bool → Int, ∀ p : Bool × Bool,
      v (C.pres p) = FableHilbertWalk20260819.H014.bell p) ∧
    (C.enumQ.elems.length ≠ enumBoolProd.elems.length) ∧
    (¬ ∃ U : Vec Int Bool → Vec Int Bool,
      (∀ u v : Vec Int Bool,
        sesq intPack C.enumQ (U u) (U v) =
          sesq intPack C.enumQ u v) ∧
      U (delta intPack false) = delta intPack false ∧
      U (delta intPack true) = delta intPack false) ∧
    (∀ x : Bool × Bool,
      C.pres (FableHilbertWalk20260819.H015.dil1 x) = C.pres x ∧
      C.pres (FableHilbertWalk20260819.H015.dil2 x) = C.pres x) ∧
    (¬ ∃ σ : Bool → Bool, ∀ q : Bool,
      σ (σ q) = FableHilbertWalk20260819.H003.toggle q) ∧
    ¬(∀ v : Vec GaussInt Bool, ∀ q : Bool,
      FableHilbertWalk20260819.H016.sqrtSwap v q =
        FableHilbertWalk20260819.H016.sqrtSwapNeg v q) := by
  subst hC
  refine ⟨presented_carrier_replays, presented_carrier_separates,
    ⟨FableHilbertWalk20260819.H001.pointMass⟩,
    fun w => pushforward_mass boolFixture.enumX boolFixture.enumQ
      boolFixture.pres w,
    FableHilbertWalk20260819.H003.collapse_not_reversible,
    fun v x => basis_expansion intPack boolFixture.enumQ v x,
    fun a b => delta_orthonormal intPack boolFixture.enumQ a b,
    fun u v => permutation_isometry intPack boolFixture.enumQ
      FableHilbertWalk20260819.H003.toggleRev u v,
    fun R v q =>
      FableHilbertWalk20260819.HWThread.phaseBlind_intertwines
        boolFixture.enumQ R v q,
    fun v _ _ h => same_report_same_amplitude boolFixture v h,
    equal_weights, mix_separates, no_descent_through_fiber,
    FableHilbertWalk20260819.H012.noncomm_witness,
    FableHilbertWalk20260819.H013.pairing_exists.1,
    bell_not_along_presentation,
    this_report_end_is_not_the_tensor_host,
    FableHilbertWalk20260819.H015.collapse_no_isometry,
    dilations_preserve_this_presentation,
    FableHilbertWalk20260819.H016.no_report_half_step,
    FableHilbertWalk20260819.H016.interpolant_not_unique⟩

#print axioms from_one_presented_carrier

/-- Punchline: the H000 fixture carries the report-end walk
    through H016, and H014's leftover is not a report of that
    fixture. -/
theorem one_carrier_through_H000_H016 :
    sameReport boolFixture (false, false) (false, true) ∧
      (¬ ∃ v : Bool → Int, ∀ p : Bool × Bool,
        v (boolFixture.pres p) =
          FableHilbertWalk20260819.H014.bell p) ∧
      ¬ ∃ σ : Bool → Bool, ∀ q : Bool,
        σ (σ q) = FableHilbertWalk20260819.H003.toggle q :=
  ⟨(from_one_presented_carrier boolFixture rfl).1,
    bell_not_along_presentation,
    FableHilbertWalk20260819.H016.no_report_half_step⟩

#print axioms one_carrier_through_H000_H016

end FableHilbertWalk20260819.HWFullThread
