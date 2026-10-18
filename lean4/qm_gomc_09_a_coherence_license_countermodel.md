import Mathlib.Data.Complex.Basic
import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Linarith

namespace QM.GOMC09A

structure AmplitudePresentation where
  amp1 : ℂ
  amp2 : ℂ
  born_1 : Complex.normSq amp1 = 1 / 2
  born_2 : Complex.normSq amp2 = 1 / 2

noncomputable def PresentationA : AmplitudePresentation where
  amp1 := ⟨1/2, 1/2⟩
  amp2 := ⟨1/2, 1/2⟩
  born_1 := by norm_num [Complex.normSq]
  born_2 := by norm_num [Complex.normSq]

noncomputable def PresentationB : AmplitudePresentation where
  amp1 := ⟨1/2, 1/2⟩
  amp2 := ⟨-(1/2), -(1/2)⟩
  born_1 := by norm_num [Complex.normSq]
  born_2 := by norm_num [Complex.normSq]

theorem amplitude_presentation_is_non_unique :
    PresentationA ≠ PresentationB := by
  intro h
  have h_amp2 : PresentationA.amp2 = PresentationB.amp2 := by
    rw [h]
  have h_re : PresentationA.amp2.re = PresentationB.amp2.re := congrArg Complex.re h_amp2
  revert h_re
  unfold PresentationA PresentationB
  intro h_eq
  linarith

end QM.GOMC09A
