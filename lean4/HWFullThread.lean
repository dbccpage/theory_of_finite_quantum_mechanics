





import HWKernel
import FinitePresentedCarrier
import ProbabilitySimplex
import ReportDynamics
import ReversibilityGate
import FreeLinearization
import InnerProductAdmission
import PermutationUnitary
import HilbertWalkPhaseBlindPresentation
import InterferenceNonDescent
import OperatorAlgebraShadow
import BornPairingBoundary
import TensorCompositionBoundary
import IrreversibleFork
import ContinuousDynamicsFork
import HWThread
import HWCarrierThread

namespace HilbertWalk.HWFullThread

open HilbertWalk.HWKernel
open HilbertWalk.FinitePresentedCarrier
  (PresentedCarrier boolFixture sameReport sameReport_iff
    presented_carrier_replays presented_carrier_separates)
open HilbertWalk.ProbabilitySimplex (ScaledProb)
open HilbertWalk.ReportDynamics (pushforward pushforward_mass)
open HilbertWalk.ReversibilityGate (Reversible)
open HilbertWalk.FreeLinearization (Vec delta basis_expansion)
open HilbertWalk.InnerProductAdmission (sesq delta_orthonormal)
open HilbertWalk.PermutationUnitary (permU permutation_isometry)
open HilbertWalk.PhaseBlindPresentation (phaseBlind psi1 psi2 equal_weights)
open HilbertWalk.InterferenceNonDescent (readout mix_separates no_descent_through_fiber)
open HilbertWalk.HWCarrierThread
  (alongPres same_report_same_amplitude)


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
      HilbertWalk.HWThread.phaseBlind_intertwines C.enumQ R v q,
    fun v _ _ h => same_report_same_amplitude C v h⟩

#print axioms parametric_thread


theorem along_report_constant {X Q : Type}
    (C : PresentedCarrier X Q) (v : Q → Int) {x y : X}
    (h : sameReport C x y) :
    v (C.pres x) = v (C.pres y) := by
  have hp : C.pres x = C.pres y := (sameReport_iff C x y).mp h
  rw [hp]

#print axioms along_report_constant

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
      HilbertWalk.TensorCompositionBoundary.bell (false, false) ≠
        HilbertWalk.TensorCompositionBoundary.bell (false, true) :=
  ⟨presented_carrier_replays, by decide⟩

#print axioms bell_splits_a_fiber

theorem bell_not_along_presentation :
    ¬ ∃ v : Bool → Int, ∀ p : Bool × Bool,
      v (boolFixture.pres p) = HilbertWalk.TensorCompositionBoundary.bell p :=
  not_along_if_fiber_splits boolFixture
    HilbertWalk.TensorCompositionBoundary.bell
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

theorem this_report_end_is_not_the_tensor_host :
    boolFixture.enumQ.elems.length ≠ enumBoolProd.elems.length := by
  decide

#print axioms this_report_end_is_not_the_tensor_host

def productHost : PresentedCarrier (Bool × Bool) (Bool × Bool) where
  pres := id
  enumX := enumBoolProd
  enumQ := enumBoolProd

theorem bell_is_a_report_of_the_product_host (p : Bool × Bool) :
    HilbertWalk.TensorCompositionBoundary.bell (productHost.pres p) =
      HilbertWalk.TensorCompositionBoundary.bell p :=
  rfl

#print axioms bell_is_a_report_of_the_product_host


theorem dilations_preserve_this_presentation (x : Bool × Bool) :
    boolFixture.pres (HilbertWalk.IrreversibleFork.dil1 x) =
      boolFixture.pres x ∧
    boolFixture.pres (HilbertWalk.IrreversibleFork.dil2 x) =
      boolFixture.pres x :=
  ⟨rfl, rfl⟩

#print axioms dilations_preserve_this_presentation


theorem from_one_presented_carrier
    (C : PresentedCarrier (Bool × Bool) Bool)
    (hC : C = boolFixture) :
    sameReport C (false, false) (false, true) ∧
    ¬ sameReport C (false, false) (true, false) ∧
    Nonempty (ScaledProb Bool C.enumQ 1) ∧
    (∀ w : Bool × Bool → Int,
      rsum intPack (C.enumQ.elems.map (pushforward C.enumX C.pres w)) =
        rsum intPack (C.enumX.elems.map w)) ∧
    ¬ Nonempty (Reversible HilbertWalk.ReversibilityGate.collapse) ∧
    (∀ (v : Vec Int Bool) (x : Bool),
      rsum intPack (C.enumQ.elems.map
        (fun q => intPack.mul (v q) (delta intPack q x))) = v x) ∧
    (∀ a b : Bool,
      sesq intPack C.enumQ (delta intPack a) (delta intPack b) =
        if (a == b) = true then intPack.one else intPack.zero) ∧
    (∀ u v : Vec Int Bool,
      sesq intPack C.enumQ
        (permU intPack HilbertWalk.ReversibilityGate.toggleRev u)
        (permU intPack HilbertWalk.ReversibilityGate.toggleRev v) =
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
      HilbertWalk.OperatorAlgebraShadow.mmul
        HilbertWalk.OperatorAlgebraShadow.nMat
        HilbertWalk.OperatorAlgebraShadow.nMat' i j =
      HilbertWalk.OperatorAlgebraShadow.mmul
        HilbertWalk.OperatorAlgebraShadow.nMat'
        HilbertWalk.OperatorAlgebraShadow.nMat i j) ∧
    (HilbertWalk.BornPairingBoundary.pair C.enumQ (phaseBlind psi1)
      (HilbertWalk.BornPairingBoundary.indicator false) = 1) ∧
    (¬ ∃ v : Bool → Int, ∀ p : Bool × Bool,
      v (C.pres p) = HilbertWalk.TensorCompositionBoundary.bell p) ∧
    (C.enumQ.elems.length ≠ enumBoolProd.elems.length) ∧
    (¬ ∃ U : Vec Int Bool → Vec Int Bool,
      (∀ u v : Vec Int Bool,
        sesq intPack C.enumQ (U u) (U v) =
          sesq intPack C.enumQ u v) ∧
      U (delta intPack false) = delta intPack false ∧
      U (delta intPack true) = delta intPack false) ∧
    (∀ x : Bool × Bool,
      C.pres (HilbertWalk.IrreversibleFork.dil1 x) = C.pres x ∧
      C.pres (HilbertWalk.IrreversibleFork.dil2 x) = C.pres x) ∧
    (¬ ∃ σ : Bool → Bool, ∀ q : Bool,
      σ (σ q) = HilbertWalk.ReversibilityGate.toggle q) ∧
    ¬(∀ v : Vec GaussInt Bool, ∀ q : Bool,
      HilbertWalk.ContinuousDynamicsFork.sqrtSwap v q =
        HilbertWalk.ContinuousDynamicsFork.sqrtSwapNeg v q) := by
  subst hC
  refine ⟨presented_carrier_replays, presented_carrier_separates,
    ⟨HilbertWalk.ProbabilitySimplex.pointMass⟩,
    fun w => pushforward_mass boolFixture.enumX boolFixture.enumQ
      boolFixture.pres w,
    HilbertWalk.ReversibilityGate.collapse_not_reversible,
    fun v x => basis_expansion intPack boolFixture.enumQ v x,
    fun a b => delta_orthonormal intPack boolFixture.enumQ a b,
    fun u v => permutation_isometry intPack boolFixture.enumQ
      HilbertWalk.ReversibilityGate.toggleRev u v,
    fun R v q =>
      HilbertWalk.HWThread.phaseBlind_intertwines
        boolFixture.enumQ R v q,
    fun v _ _ h => same_report_same_amplitude boolFixture v h,
    equal_weights, mix_separates, no_descent_through_fiber,
    HilbertWalk.OperatorAlgebraShadow.noncomm_witness,
    HilbertWalk.BornPairingBoundary.pairing_exists.1,
    bell_not_along_presentation,
    this_report_end_is_not_the_tensor_host,
    HilbertWalk.IrreversibleFork.collapse_no_isometry,
    dilations_preserve_this_presentation,
    HilbertWalk.ContinuousDynamicsFork.no_report_half_step,
    HilbertWalk.ContinuousDynamicsFork.interpolant_not_unique⟩

#print axioms from_one_presented_carrier

theorem one_carrier_through_H000_H016 :
    sameReport boolFixture (false, false) (false, true) ∧
      (¬ ∃ v : Bool → Int, ∀ p : Bool × Bool,
        v (boolFixture.pres p) =
          HilbertWalk.TensorCompositionBoundary.bell p) ∧
      ¬ ∃ σ : Bool → Bool, ∀ q : Bool,
        σ (σ q) = HilbertWalk.ReversibilityGate.toggle q :=
  ⟨(from_one_presented_carrier boolFixture rfl).1,
    bell_not_along_presentation,
    HilbertWalk.ContinuousDynamicsFork.no_report_half_step⟩

#print axioms one_carrier_through_H000_H016

end HilbertWalk.HWFullThread

private def l5aProvenance : String :=
  "Origin: lean4/HWFullThread.lean Claim: parametric_thread AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
