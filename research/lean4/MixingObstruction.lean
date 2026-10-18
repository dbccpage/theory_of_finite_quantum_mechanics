
import QuotientFiber

namespace SuperpositionQuotientFiber

def mix (v : Vec GaussInt Bool) : Vec GaussInt Bool :=
  fun q =>
    if q then GaussInt.add (v false) (GaussInt.neg (v true))
    else GaussInt.add (v false) (v true)

def mixedReadout (v : Vec GaussInt Bool) : Bool → Int :=
  phaseBlind (mix v)

theorem mix_psi1 : mixedReadout psi1 = fun q => if q then 0 else 4 := by
  funext q; cases q <;> rfl

theorem mix_psi2 : mixedReadout psi2 = fun q => if q then 4 else 0 := by
  funext q; cases q <;> rfl

theorem mix_separates : mixedReadout psi1 ≠ mixedReadout psi2 := by
  intro h
  have h0 := congrFun h false
  revert h0
  decide

theorem no_descent_through_quotient :
    ¬ ∃ f : (Bool → Int) → (Bool → Int),
      ∀ v : Vec GaussInt Bool, mixedReadout v = f (phaseBlind v) := by
  intro ⟨f, hf⟩
  have h_same_weights : phaseBlind psi1 = phaseBlind psi2 := by
    funext q; exact psi1_psi2_in_same_fiber q
  have h1 : mixedReadout psi1 = f (phaseBlind psi1) := hf psi1
  have h2 : mixedReadout psi2 = f (phaseBlind psi2) := hf psi2
  rw [h_same_weights] at h1
  have h_contra : mixedReadout psi1 = mixedReadout psi2 := h1.trans h2.symm
  exact mix_separates h_contra

#print axioms no_descent_through_quotient

end SuperpositionQuotientFiber

private def l5aProvenance : String :=
  "Origin: lean4/MixingObstruction.lean Claim: mix_psi1 AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
