


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

def sqMod (z : GaussInt) : Int :=
  (GaussInt.gmul (GaussInt.gconj z) z).re

def overlap (e ψ : Vec GaussInt Bool) : GaussInt :=
  sesq gaussPack enumBool e ψ

def quadraticAlong (e ψ : Vec GaussInt Bool) : Int :=
  sqMod (overlap e ψ)

def quarticAlong (e ψ : Vec GaussInt Bool) : Int :=
  let w := quadraticAlong e ψ
  w * w

def isOrthogonalScaleTwoFrame (e0 e1 : Vec GaussInt Bool) : Prop :=
  overlap e0 e1 = GaussInt.gzero ∧
    overlap e0 e0 = ⟨2, 0⟩ ∧
    overlap e1 e1 = ⟨2, 0⟩

def frameTotal
    (readout : Vec GaussInt Bool → Vec GaussInt Bool → Int)
    (e0 e1 ψ : Vec GaussInt Bool) : Int :=
  readout e0 ψ + readout e1 ψ

def frameAdditiveAtScaleTwo
    (readout : Vec GaussInt Bool → Vec GaussInt Bool → Int) : Prop :=
  ∀ (e0 e1 f0 f1 ψ : Vec GaussInt Bool),
    isOrthogonalScaleTwoFrame e0 e1 →
      isOrthogonalScaleTwoFrame f0 f1 →
        frameTotal readout e0 e1 ψ = frameTotal readout f0 f1 ψ

def eFalse : Vec GaussInt Bool :=
  fun q => if q then GaussInt.gzero else GaussInt.gone

def eTrue : Vec GaussInt Bool :=
  fun q => if q then GaussInt.gone else GaussInt.gzero

def had0 : Vec GaussInt Bool :=
  fun _ => GaussInt.gone

def had1 : Vec GaussInt Bool :=
  fun q => if q then GaussInt.gneg GaussInt.gone else GaussInt.gone

def rot0 : Vec GaussInt Bool :=
  fun q => if q then GaussInt.gi else GaussInt.gone

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

theorem quadratic_same_total_scale_two :
    frameTotal quadraticAlong had0 had1 psi21 = 10 ∧
      frameTotal quadraticAlong rot0 rot1 psi21 = 10 := by
  decide

#print axioms quadratic_same_total_scale_two

theorem quartic_fails_same_total_scale_two :
    frameTotal quarticAlong had0 had1 psi21 = 82 ∧
      frameTotal quarticAlong rot0 rot1 psi21 = 50 ∧
      (82 : Int) ≠ 50 := by
  decide

#print axioms quartic_fails_same_total_scale_two

theorem quartic_report_basis_total :
    quarticAlong eFalse psi21 + quarticAlong eTrue psi21 = 17 ∧
      quartic psi21 false = 16 ∧
      quartic psi21 true = 1 := by
  decide

#print axioms quartic_report_basis_total

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

private def l5aProvenance : String :=
  "Origin: lean4/H013FrameAdditivity.lean Claim: had_is_orthogonal_scale_two AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
