/-
  H013 frame additivity -- fourth-power readout versus two
  orthogonal frames. AuthorityEffect: None. Candidate only.

  QM_122 remaining job 7.1.2. Named scale-2 constraint: on every
  pair of orthogonal scale-2 frames, the readout totals must agree
  for every state.

  Quadratic (squared overlap) agrees on two scale-2 frames.
  Fourth-power (squared overlap, then squared again) does not.
  So this particular rival violates that constraint. This is not
  uniqueness of the square among all possible rules, nor a proof
  that the square obeys the constraint on every frame: it excludes
  one named rival on this host.
-/

import HWKernel
import H004FreeLinearization
import H005InnerProductAdmission
import H008PhaseBlindPresentation
import H013BornPairingBoundary

namespace FableHilbertWalk20260819.H013Frame

open FableHilbertWalk20260819.HWKernel
open FableHilbertWalk20260819.H004 (Vec)
open FableHilbertWalk20260819.H005 (sesq)
open FableHilbertWalk20260819.H013 (psi21 quartic)

/-- Squared modulus of a Gaussian integer. -/
def sqMod (z : GaussInt) : Int :=
  (GaussInt.gmul (GaussInt.gconj z) z).re

/-- Overlap of a frame vector with a state, admitted form. -/
def overlap (e ψ : Vec GaussInt Bool) : GaussInt :=
  sesq gaussPack enumBool e ψ

/-- Quadratic readout of a state along a frame vector. -/
def quadraticAlong (e ψ : Vec GaussInt Bool) : Int :=
  sqMod (overlap e ψ)

/-- Fourth-power readout along a frame vector. -/
def quarticAlong (e ψ : Vec GaussInt Bool) : Int :=
  let w := quadraticAlong e ψ
  w * w

/-- The frame condition used by the named scale-2 constraint. -/
def isOrthogonalScaleTwoFrame (e0 e1 : Vec GaussInt Bool) : Prop :=
  overlap e0 e1 = GaussInt.gzero ∧
    overlap e0 e0 = ⟨2, 0⟩ ∧
    overlap e1 e1 = ⟨2, 0⟩

/-- A readout summed across a two-vector frame. -/
def frameTotal
    (readout : Vec GaussInt Bool → Vec GaussInt Bool → Int)
    (e0 e1 ψ : Vec GaussInt Bool) : Int :=
  readout e0 ψ + readout e1 ψ

/-- The named candidate constraint: every two scale-2 orthogonal
    frames give the same total for every state. It is a condition
    under which readouts are compared, not a theorem that the
    quadratic rule already satisfies it globally. -/
def frameAdditiveAtScaleTwo
    (readout : Vec GaussInt Bool → Vec GaussInt Bool → Int) : Prop :=
  ∀ (e0 e1 f0 f1 ψ : Vec GaussInt Bool),
    isOrthogonalScaleTwoFrame e0 e1 →
      isOrthogonalScaleTwoFrame f0 f1 →
        frameTotal readout e0 e1 ψ = frameTotal readout f0 f1 ψ

/-- Report-basis vector at false: (1, 0). -/
def eFalse : Vec GaussInt Bool :=
  fun q => if q then GaussInt.gzero else GaussInt.gone

/-- Report-basis vector at true: (0, 1). -/
def eTrue : Vec GaussInt Bool :=
  fun q => if q then GaussInt.gone else GaussInt.gzero

/-- First scale-2 frame vector: (1, 1). -/
def had0 : Vec GaussInt Bool :=
  fun _ => GaussInt.gone

/-- Second scale-2 frame vector: (1, -1). -/
def had1 : Vec GaussInt Bool :=
  fun q => if q then GaussInt.gneg GaussInt.gone else GaussInt.gone

/-- Another scale-2 frame vector: (1, i). -/
def rot0 : Vec GaussInt Bool :=
  fun q => if q then GaussInt.gi else GaussInt.gone

/-- Partner of rot0: (1, -i). -/
def rot1 : Vec GaussInt Bool :=
  fun q => if q then GaussInt.gneg GaussInt.gi else GaussInt.gone

theorem had_is_orthogonal_scale_two :
    isOrthogonalScaleTwoFrame had0 had1 := by
  unfold isOrthogonalScaleTwoFrame
  decide

#print axioms had_is_orthogonal_scale_two

theorem rot_is_orthogonal_scale_two :
    isOrthogonalScaleTwoFrame rot0 rot1 := by
  unfold isOrthogonalScaleTwoFrame
  decide

#print axioms rot_is_orthogonal_scale_two

/-- Squared-overlap totals match on the two scale-2 frames. -/
theorem quadratic_same_total_scale_two :
    frameTotal quadraticAlong had0 had1 psi21 = 10 ∧
      frameTotal quadraticAlong rot0 rot1 psi21 = 10 := by
  decide

#print axioms quadratic_same_total_scale_two

/-- Fourth-power totals do not match on those same two frames. -/
theorem quartic_fails_same_total_scale_two :
    frameTotal quarticAlong had0 had1 psi21 = 82 ∧
      frameTotal quarticAlong rot0 rot1 psi21 = 50 ∧
      (82 : Int) ≠ 50 := by
  decide

#print axioms quartic_fails_same_total_scale_two

/-- On the report basis the fourth-power total is 17, as in H013.
    That number is not the issue: the rival dies because two
    equal-norm orthogonal frames disagree. -/
theorem quartic_report_basis_total :
    quarticAlong eFalse psi21 + quarticAlong eTrue psi21 = 17 ∧
      quartic psi21 false = 16 ∧
      quartic psi21 true = 1 := by
  decide

#print axioms quartic_report_basis_total

/-- Punchline: the fourth-power candidate violates the named
    scale-2 frame-additivity constraint. The two named frames and
    `psi21` supply the counterexample. -/
theorem fourth_power_dies_under_frame_additivity :
    ¬ frameAdditiveAtScaleTwo quarticAlong := by
  intro h
  have hsame := h had0 had1 rot0 rot1 psi21
    had_is_orthogonal_scale_two rot_is_orthogonal_scale_two
  have h82 : frameTotal quarticAlong had0 had1 psi21 = 82 :=
    quartic_fails_same_total_scale_two.1
  have h50 : frameTotal quarticAlong rot0 rot1 psi21 = 50 :=
    quartic_fails_same_total_scale_two.2.1
  have hneq : (82 : Int) ≠ 50 :=
    quartic_fails_same_total_scale_two.2.2
  exact hneq (h82.symm.trans (hsame.trans h50))

#print axioms fourth_power_dies_under_frame_additivity

end FableHilbertWalk20260819.H013Frame
