/-
  H010 -- interference non-descent. AuthorityEffect: None. Candidate
  only. Not PROVEN. Kind: LIFT RUNG (obstruction).

  Claim identifier: HW-H010
  Source-paper contact: QM_061 C3-C5 (the (1,1)/(1,-1) witness,
  replayed exactly at integer scale), QM_121 interference rung,
  QM_208 (audited as proposal). Work order hard obligations 2, 3, 4;
  mutation gate G6.

  Target proposition
    A mixing presentation (unnormalized Hadamard, integer entries,
    normalization disclosed as total-weight doubling) separates two
    vectors that the phase-blind presentation identifies. Therefore
    NO function of the phase-blind report reproduces the mixed
    readout: the mixed observable does not descend through the
    phase quotient. Phase is operationally visible after a change
    of presentation.

  Imports added at this rung
    The mixing map itself (a declared second presentation) and its
    normalization convention (entries 1, 1, 1, -1; total weight
    doubles -- disclosed, and proved for the witnesses).

  Theorem or counterexample
    mix_separates: readout distinguishes psi1 from psi2 (ob. 3).
    equal_weights (H008): phase-blind identifies them (ob. 2).
    no_descent_through_fiber: no f with readout = f o phaseBlind
    (ob. 4, the non-factorization theorem, exact statement).
    mutation_phase_removed: replacing psi2's phase by +1 kills the
    separation (G6 mutation 1).
    mutation_diagonal_readout: without mixing, the readout descends
    -- phase stays invisible to diagonal measurement (the work
    order's countermodel for this rung, G6 mutation 2).
    int_realization: the whole witness runs over Int -- interference
    non-descent does NOT select i, C, or U(1) (feeds H011).

  Nonclaim boundary
    No claim that every physical interference experiment is
    represented. No claim that complex amplitudes are unique or
    necessary (int_realization proves the opposite for this
    witness). No probability interpretation of the weights.

  AuthorityEffect: None
-/

import HWKernel
import H004FreeLinearization
import H008PhaseBlindPresentation
import H009PhaseFiber

namespace FableHilbertWalk20260819.H010

open FableHilbertWalk20260819.HWKernel
open FableHilbertWalk20260819.H004
open FableHilbertWalk20260819.H008
open FableHilbertWalk20260819.H009

/-- Unnormalized Hadamard mixing: integer entries, no scaling
    convention smuggled. -/
def mix (v : Vec GaussInt Bool) : Vec GaussInt Bool :=
  fun q =>
    if q then GaussInt.gadd (v false) (GaussInt.gneg (v true))
    else GaussInt.gadd (v false) (v true)

/-- Readout: mixed presentation followed by the phase-blind map. -/
def readout (v : Vec GaussInt Bool) : Bool → Int :=
  phaseBlind (mix v)

/-! ## Obligation 3: the mixing map separates the witnesses. -/

theorem mix_psi1 : ∀ q : Bool, readout psi1 q = if q then 0 else 4 := by
  decide

theorem mix_psi2 : ∀ q : Bool, readout psi2 q = if q then 4 else 0 := by
  decide

theorem mix_separates : ¬(∀ q : Bool, readout psi1 q = readout psi2 q) := by
  decide

#print axioms mix_separates

/-- Normalization disclosure: total weight doubles under the
    unnormalized mixing, checked on both witnesses. -/
theorem mix_doubles_total :
    totalWeight enumBool (mix psi1) = 2 * totalWeight enumBool psi1 ∧
      totalWeight enumBool (mix psi2) = 2 * totalWeight enumBool psi2 := by
  refine ⟨by decide, by decide⟩

#print axioms mix_doubles_total

/-! ## Obligation 4: the non-factorization theorem, exactly stated:
    no function of the phase-blind report reproduces the mixed
    readout. -/

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

/-! ## G6 mutation 1: remove the distinguishing phase. The witness
    collapses: the test fails when its data is neutralized. The
    mutant is defined LITERALLY (not as an alias of psi1), so the
    statements below are checks on independent definitions, not
    self-comparisons. -/

/-- psi2 with its relative phase stripped: (1, +1), written out. -/
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

/-! ## G6 mutation 2: drop the mixing. Without the mixing map the
    witnesses provably do not separate -- phase invisible to
    diagonal measurement. (Descent of the unmixed readout through
    the fiber holds definitionally, recorded below for contrast
    with no_descent_through_fiber; the statement that can FAIL,
    and therefore carries the mutation-sensitivity content, is
    diagonal_blind_on_witnesses.) -/

theorem mutation_diagonal_readout :
    ∃ f : (Bool → Int) → (Bool → Int),
      ∀ v : Vec GaussInt Bool, phaseBlind v = f (phaseBlind v) :=
  ⟨id, fun _ => rfl⟩

#print axioms mutation_diagonal_readout

theorem diagonal_blind_on_witnesses :
    ∀ q : Bool, phaseBlind psi1 q = phaseBlind psi2 q :=
  equal_weights

#print axioms diagonal_blind_on_witnesses

/-! ## Rival carrier: the entire witness runs over Int. Non-descent
    does not select i, C, or U(1). Feeds H011. -/

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

/-- H010 punchline: the phase-blind quotient does not carry the
    mixed observable (with both mutations failing as they must),
    and the obstruction already lives over the integers. -/
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
