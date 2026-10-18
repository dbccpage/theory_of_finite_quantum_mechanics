






import HWKernel
import H004FreeLinearization
import H005InnerProductAdmission

namespace FableHilbertWalk20260819.H008

open FableHilbertWalk20260819.HWKernel
open FableHilbertWalk20260819.H004
open FableHilbertWalk20260819.H005 (gauss_self_real int_sq_nonneg)

def phaseBlind {Q : Type} (v : Vec GaussInt Q) : Q → Int :=
  fun q => (GaussInt.gmul (GaussInt.gconj (v q)) (v q)).re

def totalWeight {Q : Type} (E : Enum Q) (v : Vec GaussInt Q) : Int :=
  rsum intPack (E.elems.map (phaseBlind v))

theorem weight_nonneg {Q : Type} (v : Vec GaussInt Q) (q : Q) :
    0 ≤ phaseBlind v q :=
  (gauss_self_real (v q)).2

#print axioms weight_nonneg

theorem weight_real {Q : Type} (v : Vec GaussInt Q) (q : Q) :
    (GaussInt.gmul (GaussInt.gconj (v q)) (v q)).im = 0 :=
  (gauss_self_real (v q)).1

#print axioms weight_real


def psi1 : Vec GaussInt Bool :=
  fun q => if q then GaussInt.gone else GaussInt.gone

def psi2 : Vec GaussInt Bool :=
  fun q => if q then GaussInt.gneg GaussInt.gone else GaussInt.gone

theorem equal_weights : ∀ q : Bool, phaseBlind psi1 q = phaseBlind psi2 q := by
  intro q; cases q <;> rfl

theorem distinct_vectors : ¬(∀ q : Bool, psi1 q = psi2 q) := by
  intro h
  have h1 := h true
  revert h1
  decide

theorem equal_total :
    totalWeight enumBool psi1 = 2 ∧ totalWeight enumBool psi2 = 2 := by
  refine ⟨by decide, by decide⟩

#print axioms equal_weights
#print axioms distinct_vectors


theorem global_phase_blind {Q : Type} (v : Vec GaussInt Q) (q : Q) :
    phaseBlind (fun x => GaussInt.gmul GaussInt.gi (v x)) q =
      phaseBlind v q := by
  unfold phaseBlind
  rw [GaussInt.gconj_gi_mul (v q) (v q)]

#print axioms global_phase_blind

theorem phase_blind_presentation :
    (∀ q : Bool, phaseBlind psi1 q = phaseBlind psi2 q) ∧
      ¬(∀ q : Bool, psi1 q = psi2 q) ∧
      (∀ (v : Vec GaussInt Bool) (q : Bool),
        phaseBlind (fun x => GaussInt.gmul GaussInt.gi (v x)) q =
          phaseBlind v q) ∧
      totalWeight enumBool psi1 = totalWeight enumBool psi2 :=
  ⟨equal_weights, distinct_vectors,
    fun v q => global_phase_blind v q, by decide⟩

#print axioms phase_blind_presentation

end FableHilbertWalk20260819.H008

private def l5aProvenance : String :=
  "Origin: lean4/H008PhaseBlindPresentation.lean Claim: weight_nonneg AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
