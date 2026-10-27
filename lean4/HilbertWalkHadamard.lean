




import HWKernel
import FreeLinearization
import HilbertWalkPhaseBlindPresentation
import InterferenceNonDescent

namespace HilbertWalk.Hadamard

open HilbertWalk.HWKernel
open HilbertWalk.FreeLinearization
open HilbertWalk.InterferenceNonDescent (mix)

theorem mix_mix_is_two (v : Vec GaussInt Bool) :
    ∀ q : Bool, mix (mix v) q = GaussInt.gadd (v q) (v q) := by
  intro q
  cases q <;> cases h0 : v false <;> cases h1 : v true <;> (
    simp [mix, GaussInt.gadd, GaussInt.gneg, h0, h1]
    constructor <;> omega
  )

#print axioms mix_mix_is_two

end HilbertWalk.Hadamard

private def l5aProvenance : String :=
  "Origin: lean4/HilbertWalkHadamard.lean Claim: mix_mix_is_two AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
