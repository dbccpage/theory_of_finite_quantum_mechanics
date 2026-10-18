






import HWKernel
import H004FreeLinearization
import H008PhaseBlindPresentation
import H009PhaseFiber

namespace FableHilbertWalk20260819.H010

open FableHilbertWalk20260819.HWKernel
open FableHilbertWalk20260819.H004
open FableHilbertWalk20260819.H008
open FableHilbertWalk20260819.H009

def mix (v : Vec GaussInt Bool) : Vec GaussInt Bool :=
  fun q =>
    if q then GaussInt.gadd (v false) (GaussInt.gneg (v true))
    else GaussInt.gadd (v false) (v true)

def readout (v : Vec GaussInt Bool) : Bool → Int :=
  phaseBlind (mix v)


theorem mix_psi1 : ∀ q : Bool, readout psi1 q = if q then 0 else 4 := by
  decide

theorem mix_psi2 : ∀ q : Bool, readout psi2 q = if q then 4 else 0 := by
  decide

theorem mix_separates : ¬(∀ q : Bool, readout psi1 q = readout psi2 q) := by
  decide

#print axioms mix_separates

theorem mix_doubles_total :
    totalWeight enumBool (mix psi1) = 2 * totalWeight enumBool psi1 ∧
      totalWeight enumBool (mix psi2) = 2 * totalWeight enumBool psi2 := by
  refine ⟨by decide, by decide⟩

#print axioms mix_doubles_total


theorem no_descent_through_fiber :
    ¬ ∃ f : (Bool → Int) → (Bool → Int),
      ∀ v : Vec GaussInt Bool, readout v = f (phaseBlind v) := by
  intro h
  rcases h with ⟨f, hf⟩
  have hw : phaseBlind psi1 = phaseBlind psi2 := by
    funext q
    exact equal_weights q
  have h1 : readout psi1 = f (phaseBlind psi1) := hf psi1
  have h2 : readout psi2 = f (phaseBlind psi2) := hf psi2
  rw [hw] at h1
  exact mix_separates (fun q => congrFun (h1.trans h2.symm) q)

#print axioms no_descent_through_fiber


def psi2_mutated : Vec GaussInt Bool :=
  fun q => if q then GaussInt.gone else GaussInt.gone

theorem mutant_is_phase_stripped :
    ∀ q : Bool, psi2_mutated q = psi1 q := by
  intro q; cases q <;> rfl

theorem mutation_phase_removed :
    (∀ q : Bool, phaseBlind psi1 q = phaseBlind psi2_mutated q) ∧
      (∀ q : Bool, readout psi1 q = readout psi2_mutated q) := by
  refine ⟨fun q => by cases q <;> rfl, fun q => by cases q <;> rfl⟩

#print axioms mutation_phase_removed


theorem mutation_diagonal_readout :
    ∃ f : (Bool → Int) → (Bool → Int),
      ∀ v : Vec GaussInt Bool, phaseBlind v = f (phaseBlind v) :=
  ⟨id, fun _ => rfl⟩

#print axioms mutation_diagonal_readout

theorem diagonal_blind_on_witnesses :
    ∀ q : Bool, phaseBlind psi1 q = phaseBlind psi2 q :=
  equal_weights

#print axioms diagonal_blind_on_witnesses


def iPsi1 : Vec Int Bool := fun _ => 1

def iPsi2 : Vec Int Bool := fun q => if q then -1 else 1

def iWeights (v : Vec Int Bool) : Bool → Int :=
  fun q => v q * v q

def iMix (v : Vec Int Bool) : Vec Int Bool :=
  fun q => if q then v false - v true else v false + v true

def iReadout (v : Vec Int Bool) : Bool → Int :=
  iWeights (iMix v)

theorem int_realization :
    (∀ q : Bool, iWeights iPsi1 q = iWeights iPsi2 q) ∧
      ¬(∀ q : Bool, iReadout iPsi1 q = iReadout iPsi2 q) := by
  refine ⟨by decide, by decide⟩

#print axioms int_realization

theorem int_no_descent :
    ¬ ∃ f : (Bool → Int) → (Bool → Int),
      ∀ v : Vec Int Bool, iReadout v = f (iWeights v) := by
  intro h
  rcases h with ⟨f, hf⟩
  have hw : iWeights iPsi1 = iWeights iPsi2 := by
    funext q
    exact int_realization.1 q
  have h1 : iReadout iPsi1 = f (iWeights iPsi1) := hf iPsi1
  have h2 : iReadout iPsi2 = f (iWeights iPsi2) := hf iPsi2
  rw [hw] at h1
  exact int_realization.2 (fun q => congrFun (h1.trans h2.symm) q)

#print axioms int_no_descent

theorem interference_non_descent :
    (∀ q : Bool, phaseBlind psi1 q = phaseBlind psi2 q) ∧
      ¬(∀ q : Bool, readout psi1 q = readout psi2 q) ∧
      (¬ ∃ f : (Bool → Int) → (Bool → Int),
        ∀ v : Vec GaussInt Bool, readout v = f (phaseBlind v)) ∧
      (∀ q : Bool, readout psi1 q = readout psi2_mutated q) ∧
      (¬ ∃ f : (Bool → Int) → (Bool → Int),
        ∀ v : Vec Int Bool, iReadout v = f (iWeights v)) :=
  ⟨equal_weights, mix_separates, no_descent_through_fiber,
    mutation_phase_removed.2, int_no_descent⟩

#print axioms interference_non_descent

end FableHilbertWalk20260819.H010

private def l5aProvenance : String :=
  "Origin: lean4/H010InterferenceNonDescent.lean Claim: mix_psi1 AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
