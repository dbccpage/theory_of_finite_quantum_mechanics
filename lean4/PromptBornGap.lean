import H017Gleason
import H013QuarticRivalSeparation
import Mathlib.Tactic.NormNum

/- Finite contract insufficiency and a fixed three-dimensional quartic rival.
   No universal Gleason uniqueness theorem is imported as a proved conclusion.
   AuthorityEffect: None. -/
namespace QuantumMechanics.PromptBornGap
theorem two_label_dimension_refusal :
    ¬ FableHilbertWalk20260819.H017Gleason.GleasonDimAtLeastThree
      FableHilbertWalk20260819.HWKernel.enumBool :=
  FableHilbertWalk20260819.H017Gleason.two_label_host_not_gleason_dimension
theorem no_three_distinct_bool_labels :
    ¬ ∃ a b c : Bool, a ≠ b ∧ a ≠ c ∧ b ≠ c :=
  FableHilbertWalk20260819.H017Gleason.no_three_pairwise_distinct_reports
theorem actual_weak_source_disagreement :
    FableHilbertWalk20260819.H013Contract.bornRule
      FableHilbertWalk20260819.H013.psi21
      (FableHilbertWalk20260819.H013.indicator false) = 4 ∧
    FableHilbertWalk20260819.H013Contract.swappedRule
      FableHilbertWalk20260819.H013.psi21
      (FableHilbertWalk20260819.H013.indicator false) = 1 :=
  FableHilbertWalk20260819.H013Contract.disagree_on_false_indicator
theorem source_quartic_deficit :
    (FableHilbertWalk20260819.H013QuarticSeparation.quartReadout
      FableHilbertWalk20260819.H013QuarticSeparation.e1
      FableHilbertWalk20260819.H013QuarticSeparation.psi +
     FableHilbertWalk20260819.H013QuarticSeparation.quartReadout
      FableHilbertWalk20260819.H013QuarticSeparation.e2
      FableHilbertWalk20260819.H013QuarticSeparation.psi) -
    (FableHilbertWalk20260819.H013QuarticSeparation.quartReadout
      FableHilbertWalk20260819.H013QuarticSeparation.p1
      FableHilbertWalk20260819.H013QuarticSeparation.psi +
     FableHilbertWalk20260819.H013QuarticSeparation.quartReadout
      FableHilbertWalk20260819.H013QuarticSeparation.p2
      FableHilbertWalk20260819.H013QuarticSeparation.psi) = 180000 :=
  FableHilbertWalk20260819.H013QuarticSeparation.quartic_frame_deficit
theorem normalized_three_coordinate_counterexample :
    (9/25 : ℚ)+(16/25)+0=1 ∧
    (9/25 : ℚ)^2+(16/25)^2+0=337/625 ∧
    (1 : ℚ)-337/625=288/625 ∧ (288/625 : ℚ)>0 := by norm_num
end QuantumMechanics.PromptBornGap
#print axioms QuantumMechanics.PromptBornGap.two_label_dimension_refusal
#print axioms QuantumMechanics.PromptBornGap.no_three_distinct_bool_labels
#print axioms QuantumMechanics.PromptBornGap.actual_weak_source_disagreement
#print axioms QuantumMechanics.PromptBornGap.source_quartic_deficit
#print axioms QuantumMechanics.PromptBornGap.normalized_three_coordinate_counterexample
