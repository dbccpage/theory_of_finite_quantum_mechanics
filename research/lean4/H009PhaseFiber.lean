






import HWKernel
import Core
import H004FreeLinearization
import H008PhaseBlindPresentation

namespace FableHilbertWalk20260819.H009

open FableHilbertWalk20260819.HWKernel
open FableHilbertWalk20260819.H004
open FableHilbertWalk20260819.H008
open GrokPdNight20260814.Core

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


theorem global_phase_in_fiber {Q : Type} (v : Vec GaussInt Q) :
    ZeroRel (phasePD Q) (fun x => GaussInt.gmul GaussInt.gi (v x)) v := by
  show phaseBlind (fun x => GaussInt.gmul GaussInt.gi (v x)) = phaseBlind v
  funext q
  exact global_phase_blind v q

#print axioms global_phase_in_fiber


theorem relative_phase_in_fiber :
    ZeroRel (phasePD Bool) psi1 psi2 ∧ psi1 ≠ psi2 := by
  constructor
  · show phaseBlind psi1 = phaseBlind psi2
    funext q
    exact equal_weights q
  · intro h
    exact distinct_vectors (fun q => congrFun h q)

#print axioms relative_phase_in_fiber


def units : List GaussInt :=
  [GaussInt.gone, GaussInt.gi,
    GaussInt.gneg GaussInt.gone,
    GaussInt.gneg GaussInt.gi]

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

private def l5aProvenance : String :=
  "Origin: lean4/H009PhaseFiber.lean Claim: phasePD_zeroRel_iff AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
