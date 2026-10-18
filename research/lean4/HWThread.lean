








import HWKernel
import H000FinitePresentedCarrier
import H002ReportDynamics
import H003ReversibilityGate
import H006PermutationUnitary
import H008PhaseBlindPresentation

namespace FableHilbertWalk20260819.HWThread

open FableHilbertWalk20260819.HWKernel
open FableHilbertWalk20260819.H004 (Vec)
open FableHilbertWalk20260819.H002 (pushforward)
open FableHilbertWalk20260819.H003 (Reversible pushforward_reversible)
open FableHilbertWalk20260819.H006 (permU)
open FableHilbertWalk20260819.H008 (phaseBlind)

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
      pushforward FableHilbertWalk20260819.H000.boolFixture.enumQ τ
        (phaseBlind v) q :=
  phaseBlind_intertwines
    FableHilbertWalk20260819.H000.boolFixture.enumQ R v q

#print axioms thread_over_boolFixture

end FableHilbertWalk20260819.HWThread

private def l5aProvenance : String :=
  "Origin: lean4/HWThread.lean Claim: phaseBlind_intertwines AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
