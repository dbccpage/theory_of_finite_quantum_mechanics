




import HWKernel
import H004FreeLinearization
import H008PhaseBlindPresentation
import H010InterferenceNonDescent

namespace FableHilbertWalk20260819.H010Hadamard

open FableHilbertWalk20260819.HWKernel
open FableHilbertWalk20260819.H004
open FableHilbertWalk20260819.H010 (mix)

theorem mix_mix_is_two (v : Vec GaussInt Bool) :
    ∀ q : Bool, mix (mix v) q = GaussInt.gadd (v q) (v q) := by
  intro q
  cases q <;> cases h0 : v false <;> cases h1 : v true <;> (
    simp [mix, GaussInt.gadd, GaussInt.gneg, h0, h1]
    constructor <;> omega
  )

#print axioms mix_mix_is_two

end FableHilbertWalk20260819.H010Hadamard

private def l5aProvenance : String :=
  "Origin: lean4/H010Hadamard.lean Claim: mix_mix_is_two AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
