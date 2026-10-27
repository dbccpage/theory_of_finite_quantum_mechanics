







import HWKernel
import Core
import ReversibilityGate
import FreeLinearization
import InnerProductAdmission
import PermutationUnitary
import HilbertWalkPhaseBlindPresentation
import PhaseFiber
import InterferenceNonDescent
import BornPairingBoundary
import TensorCompositionBoundary
import IrreversibleFork
import ContinuousDynamicsFork

namespace HilbertWalk.FiniteHilbertBoundary

open ProjectionFiber.Core (ZeroRel)
open HilbertWalk.HWKernel
open HilbertWalk.ReversibilityGate
open HilbertWalk.FreeLinearization
open HilbertWalk.InnerProductAdmission
open HilbertWalk.PermutationUnitary
open HilbertWalk.PhaseBlindPresentation
open HilbertWalk.PhaseFiber
open HilbertWalk.InterferenceNonDescent
open HilbertWalk.BornPairingBoundary
open HilbertWalk.TensorCompositionBoundary
open HilbertWalk.IrreversibleFork
open HilbertWalk.ContinuousDynamicsFork

structure ImportLedger where
  permutation_isometry_envelope_flag : Bool
  phase_fiber_nonempty : Bool
  interference_non_descent : Bool
  complex_phase_selected : Bool
  born_uniqueness : Bool
  tensor_composition_forced : Bool
  channels_canonical : Bool
  continuum_dynamics : Bool

def walkLedger : ImportLedger where
  permutation_isometry_envelope_flag := true
  phase_fiber_nonempty := true
  interference_non_descent := true
  complex_phase_selected := false
  born_uniqueness := false
  tensor_composition_forced := false
  channels_canonical := false
  continuum_dynamics := false

def AllDischarged (L : ImportLedger) : Bool :=
  L.permutation_isometry_envelope_flag && L.phase_fiber_nonempty &&
    L.interference_non_descent && L.complex_phase_selected &&
    L.born_uniqueness && L.tensor_composition_forced &&
    L.channels_canonical && L.continuum_dynamics

theorem import_ledger_gate :
    AllDischarged walkLedger = false ∧
      (walkLedger.permutation_isometry_envelope_flag &&
        walkLedger.phase_fiber_nonempty &&
        walkLedger.interference_non_descent) = true :=
  ⟨rfl, rfl⟩

#print axioms import_ledger_gate

theorem finite_hilbert_boundary :
    (∀ {K Q : Type} (P : StarRingPack K) [DecidableEq Q]
      (E : Enum Q) {τ : Q → Q} (R : Reversible τ) (u v : Vec K Q),
      sesq P E (permU P R u) (permU P R v) = sesq P E u v) ∧
    (ZeroRel (phasePD Bool) psi1 psi2 ∧ psi1 ≠ psi2) ∧
    (¬(∀ q : Bool, readout psi1 q = readout psi2 q)) ∧
    (¬ ∃ f : (Bool → Int) → (Bool → Int),
      ∀ v : Vec GaussInt Bool, readout v = f (phaseBlind v)) ∧
    (¬ ∃ f : (Bool → Int) → (Bool → Int),
      ∀ v : Vec Int Bool, iReadout v = f (iWeights v)) ∧
    (∀ q : Bool, 0 ≤ quartic psi21 q) ∧
    (¬(∀ q : Bool, phaseBlind psi21 q = quartic psi21 q)) ∧
    (¬ ∃ u v : Bool → Int,
      ∀ p : Bool × Bool, bell p = tensor u v p) ∧
    (∀ w : Sum Bool Bool → Int, sumJoin (sumSplit w) = w) ∧
    (¬ ∃ U : Vec Int Bool → Vec Int Bool,
      (∀ u v : Vec Int Bool,
        sesq intPack enumBool (U u) (U v) =
          sesq intPack enumBool u v) ∧
      U (delta intPack false) = delta intPack false ∧
      U (delta intPack true) = delta intPack false) ∧
    ((∀ a b : Bool, (dil1 (a, b)).1 = (dil2 (a, b)).1) ∧
      ¬(∀ a b : Bool, dil1 (a, b) = dil2 (a, b))) ∧
    (¬ ∃ σ : Bool → Bool, ∀ q : Bool, σ (σ q) = toggle q) ∧
    (∀ (v : Vec GaussInt Bool) (q : Bool),
      sqrtSwap (sqrtSwap v) q = scale4 (ampSwap v) q) ∧
    (¬(∀ v : Vec GaussInt Bool, ∀ q : Bool,
      sqrtSwap v q = sqrtSwapNeg v q)) := by
  refine ⟨?_, relative_phase_in_fiber, mix_separates,
    no_descent_through_fiber, int_no_descent, quartic_rival.1,
    quartic_rival.2.2.2, bell_not_product,
    sum_component_embedding_surjective,
    collapse_no_isometry, ⟨same_reduction, dilations_distinct⟩,
    no_report_half_step,
    fun v q => sqrtSwap_squares_to_scaled_swap v q,
    interpolant_not_unique⟩
  intro K Q P inst E τ R u v
  exact permutation_isometry P E R u v

#print axioms finite_hilbert_boundary

end HilbertWalk.FiniteHilbertBoundary

private def l5aProvenance : String :=
  "Origin: lean4/FiniteHilbertBoundary.lean Claim: import_ledger_gate AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
