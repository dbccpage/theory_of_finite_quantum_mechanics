








import HWKernel
import FinitePresentedCarrier
import ReportDynamics
import ReversibilityGate
import PermutationUnitary
import HilbertWalkPhaseBlindPresentation

namespace HilbertWalk.HWThread

open HilbertWalk.HWKernel
open HilbertWalk.FreeLinearization (Vec)
open HilbertWalk.ReportDynamics (pushforward)
open HilbertWalk.ReversibilityGate (Reversible pushforward_reversible)
open HilbertWalk.PermutationUnitary (permU)
open HilbertWalk.PhaseBlindPresentation (phaseBlind)

theorem phaseBlind_intertwines {Q : Type} [DecidableEq Q] (EQ : Enum Q)
    {τ : Q → Q} (R : Reversible τ) (v : Vec GaussInt Q) (q : Q) :
    phaseBlind (permU gaussPack R v) q =
      pushforward EQ τ (phaseBlind v) q := by
  have hR : pushforward EQ τ (phaseBlind v) q = phaseBlind v (R.inv q) :=
    pushforward_reversible EQ τ R (phaseBlind v) q
  rw [hR]
  rfl

#print axioms phaseBlind_intertwines

theorem thread_over_boolFixture
    {τ : Bool → Bool} (R : Reversible τ) (v : Vec GaussInt Bool)
    (q : Bool) :
    phaseBlind (permU gaussPack R v) q =
      pushforward HilbertWalk.FinitePresentedCarrier.boolFixture.enumQ τ
        (phaseBlind v) q :=
  phaseBlind_intertwines
    HilbertWalk.FinitePresentedCarrier.boolFixture.enumQ R v q

#print axioms thread_over_boolFixture

end HilbertWalk.HWThread

private def l5aProvenance : String :=
  "Origin: lean4/HWThread.lean Claim: phaseBlind_intertwines AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
