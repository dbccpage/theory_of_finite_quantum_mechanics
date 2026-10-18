/-
  HWThread -- genuine cross-rung threading. AuthorityEffect: None.
  Candidate only. Not PROVEN. Kind: CONNECTIVE.

  Claim identifier: HW-THREAD
  Motivation (adversarial-review response, 2026-08-19): the capstone
  H017.finite_hilbert_boundary is a CONJUNCTION of separately-proved
  rung witnesses over a shared Bool/Int/GaussInt substrate; it does
  NOT thread a single carrier object through H000->H016. That is an
  honest limitation recorded in HILBERT_WALK.md ("What this is / is
  not") and FRONTIER.md (residue R0). This module supplies what the
  spine DOES connect, as a real theorem rather than a claim:

  Target proposition
    Over one shared report set Q and ONE reversible report map tau,
    the amplitude permutation-isometry U_tau (H006), the weight
    pushforward along tau (H002/H003), and the phase-blind
    presentation (H008) form a commuting square:

        phaseBlind (U_tau v) = pushforward_tau (phaseBlind v).

    The phase-blind readout INTERTWINES the amplitude-level isometry (H006)
    with the weight-level dynamics. This is a genuine equivariance
    (not a re-conjunction of parametric theorems): a single tau and
    a single v flow through both the H006 layer and the H002/H003
    layer and the two paths agree.

  Imports added at this rung
    None. Consumes H002 pushforward, H003 reversibility, H006 permU,
    H008 phaseBlind over one shared Q.

  Theorem or counterexample
    phaseBlind_intertwines: the commuting square, general over any
    DecidableEq report set with an enumeration.
    thread_over_boolFixture: instantiated at the H000 boolFixture's
    enumQ field; it does not consume boolFixture's carrier/presentation.

  Nonclaim boundary
    This threads the dynamics/isometry/phase layers over one tau and
    reuses H000's enumQ only. It does NOT thread the full spine through
    one carrier/presentation object; that remains open residue R0.

  AuthorityEffect: None
-/

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

/-- The commuting square: phase-blind readout intertwines the
    amplitude permutation-isometry with the weight pushforward,
    over one shared report set and one reversible report map. -/
theorem phaseBlind_intertwines {Q : Type} [DecidableEq Q] (EQ : Enum Q)
    {τ : Q → Q} (R : Reversible τ) (v : Vec GaussInt Q) (q : Q) :
    phaseBlind (permU gaussPack R v) q =
      pushforward EQ τ (phaseBlind v) q := by
  have hR : pushforward EQ τ (phaseBlind v) q = phaseBlind v (R.inv q) :=
    pushforward_reversible EQ τ R (phaseBlind v) q
  rw [hR]
  rfl

#print axioms phaseBlind_intertwines

/-- Instantiated with the enumQ field exported by H000's boolFixture;
    this reuses its report enumeration, not its carrier/presentation. -/
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
