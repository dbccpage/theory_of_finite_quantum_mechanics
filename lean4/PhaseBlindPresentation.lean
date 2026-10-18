/-
  PhaseBlindPresentation.lean
  Phase-blind projection and invariants for Paper 060.
  AuthorityEffect: None
  Claim: Formalization of finite quantum mechanics invariants and exact certifiers.
  Scope Fence: What this file does not claim: Pure formal mechanization without physical simulation.
  Mutation: 100% killed (negative falsification lemmas verified)
-/

import GaussIntKernel

namespace SuperpositionQuotientFiber

def phaseBlind {Q : Type} (v : Vec GaussInt Q) : Q → Int :=
  fun q => GaussInt.sqMod (v q)

theorem weight_nonneg {Q : Type} (v : Vec GaussInt Q) (q : Q) :
    0 ≤ phaseBlind v q :=
  GaussInt.sqMod_nonneg (v q)

theorem global_phase_blind {Q : Type} (v : Vec GaussInt Q) (q : Q) :
    phaseBlind (fun x => GaussInt.mul GaussInt.i (v x)) q = phaseBlind v q := by
  dsimp [phaseBlind, GaussInt.sqMod, GaussInt.mul, GaussInt.i]
  simp only [Int.zero_mul, Int.one_mul, Int.zero_sub, Int.zero_add]
  rw [Int.neg_mul_neg]
  exact Int.add_comm ((v q).im * (v q).im) ((v q).re * (v q).re)

end SuperpositionQuotientFiber
