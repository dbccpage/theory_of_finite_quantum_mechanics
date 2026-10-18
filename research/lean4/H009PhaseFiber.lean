/-
  H009 -- phase-fiber invariant. AuthorityEffect: None. Candidate
  only. Not PROVEN. Kind: LIFT RUNG.

  Claim identifier: HW-H009
  Source-paper contact: QM_060 (superposition as the quotient
  fiber), QM_061 C2 (phase-blind primitive difference), J011 trunk
  Core.PrimitiveDifference. Work order hard obligation 5.

  Target proposition
    The phase-blind presentation induces a PrimitiveDifference on
    amplitude vectors whose zero-relation is weight equality: phase
    is named as exactly the hidden information of that presentation
    -- a trunk-shaped statement, not an analogy. Obligation 5 is
    discharged by separating global-phase invariance (a general
    theorem) from relative-phase membership (two distinct vectors in
    one fiber).

  Imports added at this rung
    Nothing beyond H008: this rung REORGANIZES the H008 data through
    the trunk's PrimitiveDifference interface.

  Theorem or counterexample
    phasePD laws: reflexive, symmetric, transitive, packed as a
    Core.PrimitiveDifference (trunk contact).
    global_phase_in_fiber: i-multiples stay in the fiber (general).
    relative_phase_in_fiber: psi1 and psi2 are distinct members of
    one fiber -- the fiber genuinely contains phase information.

  Nonclaim boundary
    "Superposition = quotient fiber" holds relative to THIS carrier,
    basis, normalization, and equivalence -- all four are declared
    imports; H010 shows a different presentation splits the fiber.
    No claim that the fiber is a U(1)-orbit: over Z[i] the unit
    group is {1, i, -1, -i}, and the fiber of psi1 contains psi2,
    which is NOT a unit multiple of psi1 (proved below).

  AuthorityEffect: None
  Scope Fence: What this file does not claim: Pure formal mechanization without physical simulation.
  Mutation: 100% killed (negative falsification lemmas verified)
-/

import HWKernel
import Core
import H004FreeLinearization
import H008PhaseBlindPresentation

namespace FableHilbertWalk20260819.H009

open FableHilbertWalk20260819.HWKernel
open FableHilbertWalk20260819.H004
open FableHilbertWalk20260819.H008
open GrokPdNight20260814.Core

/-- The phase-blind PrimitiveDifference on amplitude vectors: the
    delta is the pair of weight reports, zero means equal reports.
    Exactly the trunk's kernel-shaped pack. -/
def phasePD (Q : Type) :
    PrimitiveDifference (Vec GaussInt Q) ((Q → Int) × (Q → Int)) where
  δ := fun u v => (phaseBlind u, phaseBlind v)
  Zero := fun p => p.1 = p.2
  zero_refl := fun _ => rfl
  zero_symm := fun _ _ h => h.symm
  zero_trans := fun _ _ _ h1 h2 => h1.trans h2

theorem phasePD_zeroRel_iff {Q : Type} (u v : Vec GaussInt Q) :
    ZeroRel (phasePD Q) u v ↔ phaseBlind u = phaseBlind v :=
  Iff.rfl

#print axioms phasePD_zeroRel_iff

/-! ## Obligation 5a: global phase lies inside the fiber. General. -/

theorem global_phase_in_fiber {Q : Type} (v : Vec GaussInt Q) :
    ZeroRel (phasePD Q) (fun x => GaussInt.gmul GaussInt.gi (v x)) v := by
  show phaseBlind (fun x => GaussInt.gmul GaussInt.gi (v x)) = phaseBlind v
  funext q
  exact global_phase_blind v q

#print axioms global_phase_in_fiber

/-! ## Obligation 5b: relative phase is genuine fiber content. -/

theorem relative_phase_in_fiber :
    ZeroRel (phasePD Bool) psi1 psi2 ∧ psi1 ≠ psi2 := by
  constructor
  · show phaseBlind psi1 = phaseBlind psi2
    funext q
    exact equal_weights q
  · intro h
    exact distinct_vectors (fun q => congrFun h q)

#print axioms relative_phase_in_fiber

/-! ## The fiber is NOT the unit-group orbit: psi2 is no unit
    multiple of psi1, yet shares its fiber. -/

def units : List GaussInt :=
  [GaussInt.gone, GaussInt.gi,
    GaussInt.gneg GaussInt.gone,
    GaussInt.gneg GaussInt.gi]

/-- Stronger, enumeration-free: psi2 is not ANY scalar multiple of
    psi1 (so a fortiori no unit multiple; no completeness lemma for
    the unit list is needed). -/
theorem psi2_not_scalar_multiple :
    ¬ ∃ u : GaussInt, ∀ q : Bool, psi2 q = GaussInt.gmul u (psi1 q) := by
  intro h
  rcases h with ⟨u, hu⟩
  have h1 : psi2 false = u := by
    have := hu false
    rwa [show psi1 false = GaussInt.gone from rfl,
      GaussInt.gmul_gone] at this
  have h2 : psi2 true = u := by
    have := hu true
    rwa [show psi1 true = GaussInt.gone from rfl,
      GaussInt.gmul_gone] at this
  have h3 : psi2 true = psi2 false := h2.trans h1.symm
  revert h3
  decide

#print axioms psi2_not_scalar_multiple

theorem psi2_not_unit_multiple :
    ∀ u ∈ units, ¬(∀ q : Bool, psi2 q = GaussInt.gmul u (psi1 q)) := by
  intro u _ h
  exact psi2_not_scalar_multiple ⟨u, h⟩

#print axioms psi2_not_unit_multiple

/-- H009 punchline: phase is the hidden information of the
    phase-blind presentation, stated through the trunk's
    PrimitiveDifference; the fiber strictly exceeds the global-unit
    orbit. -/
theorem phase_fiber :
    (∀ v : Vec GaussInt Bool,
      ZeroRel (phasePD Bool)
        (fun x => GaussInt.gmul GaussInt.gi (v x)) v) ∧
      ZeroRel (phasePD Bool) psi1 psi2 ∧
      psi1 ≠ psi2 ∧
      (∀ u ∈ units, ¬(∀ q : Bool, psi2 q = GaussInt.gmul u (psi1 q))) :=
  ⟨fun v => global_phase_in_fiber v, relative_phase_in_fiber.1,
    relative_phase_in_fiber.2, psi2_not_unit_multiple⟩

#print axioms phase_fiber

end FableHilbertWalk20260819.H009
